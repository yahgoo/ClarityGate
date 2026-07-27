"""SQLite database helpers for ClarityGate backend.

All CRUD functions accept an existing sqlite3.Connection and never call
commit() or rollback().  Transaction boundaries are owned by the caller.

Return type convention: functions return sqlite3.Row objects (or lists of
them) so callers can access columns by name.  Use ``dict(row)`` to convert
to a plain dictionary when needed.
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Sequence

_SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def connect(db_path: str) -> sqlite3.Connection:
    """Open a connection with foreign keys enabled and Row factory set."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str) -> None:
    """Create the schema tables if they do not already exist.

    This function owns its own transaction and commits upon success.
    """
    conn = connect(db_path)
    try:
        schema_sql = _SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------


def insert_spec(connection: sqlite3.Connection, filename: str, raw_text: str) -> int:
    """Insert a new spec and return its integer id.

    Does not commit — caller owns the transaction.
    """
    cursor = connection.execute(
        "INSERT INTO specs (filename, raw_text) VALUES (?, ?)",
        (filename, raw_text),
    )
    return cursor.lastrowid  # type: ignore[return-value]


def get_spec(connection: sqlite3.Connection, spec_id: int) -> sqlite3.Row | None:
    """Return the spec row for *spec_id*, or None if not found."""
    cursor = connection.execute("SELECT * FROM specs WHERE id = ?", (spec_id,))
    return cursor.fetchone()


# ---------------------------------------------------------------------------
# Rewrites
# ---------------------------------------------------------------------------


def upsert_rewrite(
    connection: sqlite3.Connection,
    spec_id: int,
    line_number: int,
    rewritten_text: str,
) -> None:
    """Insert or replace a rewrite overlay for the given spec and line.

    Does not commit — caller owns the transaction.
    """
    connection.execute(
        """
        INSERT INTO rewrites (spec_id, line_number, rewritten_text)
        VALUES (?, ?, ?)
        ON CONFLICT(spec_id, line_number)
        DO UPDATE SET rewritten_text = excluded.rewritten_text,
                      applied_at = datetime('now')
        """,
        (spec_id, line_number, rewritten_text),
    )


def delete_rewrite(
    connection: sqlite3.Connection, spec_id: int, line_number: int
) -> None:
    """Delete a single rewrite overlay.

    Does not commit — caller owns the transaction.
    """
    connection.execute(
        "DELETE FROM rewrites WHERE spec_id = ? AND line_number = ?",
        (spec_id, line_number),
    )


def delete_all_rewrites(connection: sqlite3.Connection, spec_id: int) -> None:
    """Delete every rewrite overlay for *spec_id*.

    Does not commit — caller owns the transaction.
    """
    connection.execute("DELETE FROM rewrites WHERE spec_id = ?", (spec_id,))


def get_rewrites(connection: sqlite3.Connection, spec_id: int) -> list[sqlite3.Row]:
    """Return all rewrite overlays for *spec_id*, ordered by line number."""
    cursor = connection.execute(
        "SELECT * FROM rewrites WHERE spec_id = ? ORDER BY line_number",
        (spec_id,),
    )
    return cursor.fetchall()


# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------


def replace_requirements(
    connection: sqlite3.Connection,
    spec_id: int,
    records: Sequence[dict[str, Any]],
) -> None:
    """Delete and re-insert all requirement rows for *spec_id*.

    Each record dict must contain: line_number, raw_text, statement, section,
    uppercase_keywords (list), lowercase_keywords (list).

    Does not commit — caller owns the transaction.
    """
    connection.execute("DELETE FROM requirements WHERE spec_id = ?", (spec_id,))
    for rec in records:
        connection.execute(
            """
            INSERT INTO requirements
                (spec_id, line_number, raw_text, statement, section,
                 uppercase_keywords, lowercase_keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                spec_id,
                rec["line_number"],
                rec["raw_text"],
                rec["statement"],
                rec.get("section"),
                json.dumps(rec.get("uppercase_keywords", [])),
                json.dumps(rec.get("lowercase_keywords", [])),
            ),
        )


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


def replace_findings(
    connection: sqlite3.Connection,
    spec_id: int,
    findings: Sequence[dict[str, Any]],
) -> None:
    """Delete and re-insert all finding rows for *spec_id*.

    Each finding dict must contain: line_number, type, severity, message,
    suggested_rewrite.  Optional: check_id, category.

    Does not commit — caller owns the transaction.
    """
    connection.execute("DELETE FROM findings WHERE spec_id = ?", (spec_id,))
    for f in findings:
        connection.execute(
            """
            INSERT INTO findings
                (spec_id, line_number, type, severity, message,
                 suggested_rewrite, check_id, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                spec_id,
                f["line_number"],
                f["type"],
                f["severity"],
                f["message"],
                f["suggested_rewrite"],
                f.get("check_id", ""),
                f.get("category", ""),
            ),
        )
