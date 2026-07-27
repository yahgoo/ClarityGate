"""Linter adapter: wraps the frozen src.linter pipeline for the backend.

All linter behavior is imported from src.linter.* — never reimplemented.
Scores, tiers, and verdicts are derived fresh on every call by invoking the
frozen evaluator.  They are never persisted in the database.

Transaction ownership: public functions in this module own the transaction
boundary (commit on success, rollback on failure).  The database helper
functions they call never commit or roll back independently.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from src.linter.evaluator import evaluate
from src.linter.models import EvaluationResult, Finding, RequirementRecord
from src.linter.parser import parse_requirements
from src.linter.reporter import render_report
from src.linter.rule_engine import run_checks

from backend.database import (
    delete_all_rewrites,
    delete_rewrite,
    get_rewrites,
    get_spec,
    insert_spec,
    replace_findings,
    replace_requirements,
    upsert_rewrite,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _reconstruct_effective_text(raw_text: str, rewrites: list[sqlite3.Row]) -> str:
    """Apply single-line rewrite overlays to the raw text.

    Each overlay replaces the physical line at its 1-based line_number.
    No prefix reconstruction, fuzzy matching, or Markdown AST editing.
    """
    lines = raw_text.split("\n")
    for rw in rewrites:
        idx = rw["line_number"] - 1
        if 0 <= idx < len(lines):
            lines[idx] = rw["rewritten_text"]
    return "\n".join(lines)


def _run_pipeline(effective_text: str) -> tuple[list[RequirementRecord], list[Finding], EvaluationResult]:
    """Run the frozen parse → check → evaluate pipeline."""
    records = parse_requirements(effective_text)
    findings = run_checks(records)
    evaluation = evaluate(records, findings)
    return records, findings, evaluation


def _records_to_dicts(records: list[RequirementRecord]) -> list[dict[str, Any]]:
    """Convert RequirementRecord dataclasses to storage dicts."""
    return [
        {
            "line_number": r.line_number,
            "raw_text": r.raw_text,
            "statement": r.statement,
            "section": r.section,
            "uppercase_keywords": list(r.uppercase_keywords),
            "lowercase_keywords": list(r.lowercase_keywords),
        }
        for r in records
    ]


def _findings_to_dicts(findings: list[Finding]) -> list[dict[str, Any]]:
    """Convert Finding dataclasses to storage dicts."""
    return [
        {
            "line_number": f.line_number,
            "type": f.type,
            "severity": f.severity,
            "message": f.message,
            "suggested_rewrite": f.suggested_rewrite,
            "check_id": f.check_id,
            "category": f.category,
        }
        for f in findings
    ]


def _findings_to_response(findings: list[Finding]) -> list[dict[str, Any]]:
    """Convert Finding dataclasses to API response dicts."""
    return [
        {
            "line_number": f.line_number,
            "type": f.type,
            "severity": f.severity,
            "message": f.message,
            "suggested_rewrite": f.suggested_rewrite,
            "check_id": f.check_id,
            "category": f.category,
        }
        for f in findings
    ]


def _requirements_to_response(records: list[RequirementRecord]) -> list[dict[str, Any]]:
    """Convert RequirementRecord dataclasses to API response dicts."""
    return [
        {
            "line_number": r.line_number,
            "raw_text": r.raw_text,
            "statement": r.statement,
            "section": r.section,
            "uppercase_keywords": list(r.uppercase_keywords),
            "lowercase_keywords": list(r.lowercase_keywords),
        }
        for r in records
    ]


def _rewrites_to_response(rewrites: list[sqlite3.Row]) -> list[dict[str, Any]]:
    """Convert rewrite rows to API response dicts."""
    return [
        {
            "line_number": rw["line_number"],
            "rewritten_text": rw["rewritten_text"],
            "applied_at": rw["applied_at"],
        }
        for rw in rewrites
    ]


def _build_analysis_response(
    conn: sqlite3.Connection,
    spec_row: sqlite3.Row,
    records: list[RequirementRecord],
    findings: list[Finding],
    evaluation: EvaluationResult,
    effective_text: str,
) -> dict[str, Any]:
    """Build the full analysis response dict."""
    rewrites = get_rewrites(conn, spec_row["id"])
    report_md = render_report(spec_row["filename"], records, evaluation)
    return {
        "spec_id": spec_row["id"],
        "filename": spec_row["filename"],
        "raw_text": spec_row["raw_text"],
        "effective_markdown": effective_text,
        "created_at": spec_row["created_at"],
        "requirements": _requirements_to_response(records),
        "findings": _findings_to_response(findings),
        "rewrites": _rewrites_to_response(rewrites),
        "score": evaluation.score,
        "tier": evaluation.tier,
        "verdict": evaluation.verdict,
        "exit_code": evaluation.exit_code,
        "requirement_count": evaluation.requirement_count,
        "defects": evaluation.defects,
        "clarifications": evaluation.clarifications,
        "infos": evaluation.infos,
        "report_markdown": report_md,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def analyze_spec(conn: sqlite3.Connection, filename: str, raw_text: str) -> dict[str, Any]:
    """Insert a new spec, run the frozen linter, store results, return analysis.

    Owns the transaction: commits on success, rolls back on failure.
    """
    try:
        spec_id = insert_spec(conn, filename, raw_text)
        records, findings, evaluation = _run_pipeline(raw_text)
        replace_requirements(conn, spec_id, _records_to_dicts(records))
        replace_findings(conn, spec_id, _findings_to_dicts(findings))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    spec_row = get_spec(conn, spec_id)
    return _build_analysis_response(conn, spec_row, records, findings, evaluation, raw_text)


def get_analysis(conn: sqlite3.Connection, spec_id: int) -> dict[str, Any] | None:
    """Return the current analysis for a spec using its rewrite overlays.

    Does not mutate the database.  Returns None if spec_id is not found.
    """
    spec_row = get_spec(conn, spec_id)
    if spec_row is None:
        return None

    rewrites = get_rewrites(conn, spec_id)
    effective_text = _reconstruct_effective_text(spec_row["raw_text"], rewrites)
    records, findings, evaluation = _run_pipeline(effective_text)
    return _build_analysis_response(conn, spec_row, records, findings, evaluation, effective_text)


def apply_rewrite(
    conn: sqlite3.Connection,
    spec_id: int,
    line_number: int,
    rewritten_text: str,
) -> dict[str, Any]:
    """Apply a single-line rewrite overlay and re-analyze.

    Validates that line_number exists in the raw text and is a parsed
    requirement line.  Owns the transaction.

    Raises:
        KeyError: if spec_id not found.
        ValueError: if line_number is out of range or not a requirement line.
    """
    spec_row = get_spec(conn, spec_id)
    if spec_row is None:
        raise KeyError(f"spec_id {spec_id} not found")

    raw_lines = spec_row["raw_text"].split("\n")
    if line_number < 1 or line_number > len(raw_lines):
        raise ValueError(f"line_number {line_number} out of range (1-{len(raw_lines)})")

    # Verify line_number is a parsed requirement line
    rewrites = get_rewrites(conn, spec_id)
    effective_text = _reconstruct_effective_text(spec_row["raw_text"], rewrites)
    records = parse_requirements(effective_text)
    requirement_lines = {r.line_number for r in records}
    if line_number not in requirement_lines:
        raise ValueError(f"line_number {line_number} is not a parsed requirement line")

    try:
        upsert_rewrite(conn, spec_id, line_number, rewritten_text)
        # Re-analyze with the new overlay
        new_rewrites = get_rewrites(conn, spec_id)
        new_effective = _reconstruct_effective_text(spec_row["raw_text"], new_rewrites)
        records, findings, evaluation = _run_pipeline(new_effective)
        replace_requirements(conn, spec_id, _records_to_dicts(records))
        replace_findings(conn, spec_id, _findings_to_dicts(findings))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return _build_analysis_response(conn, spec_row, records, findings, evaluation, new_effective)


def remove_rewrite(
    conn: sqlite3.Connection,
    spec_id: int,
    line_number: int,
) -> dict[str, Any]:
    """Remove one rewrite overlay and re-analyze.

    Owns the transaction.

    Raises:
        KeyError: if spec_id not found.
    """
    spec_row = get_spec(conn, spec_id)
    if spec_row is None:
        raise KeyError(f"spec_id {spec_id} not found")

    try:
        delete_rewrite(conn, spec_id, line_number)
        rewrites = get_rewrites(conn, spec_id)
        effective_text = _reconstruct_effective_text(spec_row["raw_text"], rewrites)
        records, findings, evaluation = _run_pipeline(effective_text)
        replace_requirements(conn, spec_id, _records_to_dicts(records))
        replace_findings(conn, spec_id, _findings_to_dicts(findings))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return _build_analysis_response(conn, spec_row, records, findings, evaluation, effective_text)


def reset_rewrites(conn: sqlite3.Connection, spec_id: int) -> dict[str, Any]:
    """Delete all rewrite overlays for a spec and re-analyze.

    Owns the transaction.

    Raises:
        KeyError: if spec_id not found.
    """
    spec_row = get_spec(conn, spec_id)
    if spec_row is None:
        raise KeyError(f"spec_id {spec_id} not found")

    try:
        delete_all_rewrites(conn, spec_id)
        records, findings, evaluation = _run_pipeline(spec_row["raw_text"])
        replace_requirements(conn, spec_id, _records_to_dicts(records))
        replace_findings(conn, spec_id, _findings_to_dicts(findings))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return _build_analysis_response(conn, spec_row, records, findings, evaluation, spec_row["raw_text"])
