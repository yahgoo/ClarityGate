"""API routes for ClarityGate backend.

All routes derive scores, tiers, and verdicts fresh from the frozen evaluator.
No mission state is returned.  No score/tier/verdict is persisted.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, field_validator

from backend.database import connect
from backend.linter_adapter import (
    analyze_spec,
    apply_rewrite,
    get_analysis,
    remove_rewrite,
    reset_rewrites,
)

router = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class CreateSpecRequest(BaseModel):
    filename: str
    raw_text: str

    @field_validator("filename")
    @classmethod
    def filename_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("filename must not be empty")
        return v

    @field_validator("raw_text")
    @classmethod
    def raw_text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("raw_text must not be empty")
        return v


class ApplyRewriteRequest(BaseModel):
    line_number: int
    rewritten_text: str

    @field_validator("rewritten_text")
    @classmethod
    def rewritten_text_valid(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("rewritten_text must not be empty")
        return v


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_conn(request: Request):
    """Open a database connection from the app-level db_path."""
    return connect(request.app.state.db_path)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/specs", status_code=201)
def create_spec(body: CreateSpecRequest, request: Request):
    """Create a new spec and run the frozen linter analysis."""
    conn = _get_conn(request)
    try:
        result = analyze_spec(conn, body.filename, body.raw_text)
        return result
    finally:
        conn.close()


@router.get("/specs/{spec_id}")
def get_spec_analysis(spec_id: int, request: Request):
    """Return the current analysis for a spec using its rewrite overlays."""
    conn = _get_conn(request)
    try:
        result = get_analysis(conn, spec_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"spec_id {spec_id} not found")
        return result
    finally:
        conn.close()


@router.post("/specs/{spec_id}/rewrites")
def create_rewrite(spec_id: int, body: ApplyRewriteRequest, request: Request):
    """Apply a single-line rewrite overlay and re-analyze."""
    # Reject multi-line content at the route level (400)
    if "\n" in body.rewritten_text or "\r" in body.rewritten_text:
        raise HTTPException(
            status_code=400,
            detail="rewritten_text must be a single physical line (no \\n or \\r)",
        )

    conn = _get_conn(request)
    try:
        result = apply_rewrite(conn, spec_id, body.line_number, body.rewritten_text)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail=f"spec_id {spec_id} not found")
    except ValueError as exc:
        msg = str(exc)
        if "out of range" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=422, detail=msg)
    finally:
        conn.close()


@router.delete("/specs/{spec_id}/rewrites/{line_number}")
def delete_one_rewrite(spec_id: int, line_number: int, request: Request):
    """Delete one rewrite overlay and re-analyze."""
    conn = _get_conn(request)
    try:
        result = remove_rewrite(conn, spec_id, line_number)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail=f"spec_id {spec_id} not found")
    finally:
        conn.close()


@router.delete("/specs/{spec_id}/rewrites")
def delete_all_spec_rewrites(spec_id: int, request: Request):
    """Delete all rewrite overlays for a spec and re-analyze."""
    conn = _get_conn(request)
    try:
        result = reset_rewrites(conn, spec_id)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail=f"spec_id {spec_id} not found")
    finally:
        conn.close()
