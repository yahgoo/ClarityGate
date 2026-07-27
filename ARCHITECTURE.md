# ClarityGate Option 2 — Architecture
**Updated: Monday, July 27, 2026, 11:18 AM +08**

## Architecture Overview

ClarityGate Option 2 is a local-first, three-layer full-stack application:

```
┌─────────────────────────────────────────────┐
│  Frontend (React + Vite + TS + Tailwind)     │
│  Guided Gate UI: Import → Review → Resolve → Ready  │
└──────────────────┬────────────────────────────┘
                    │ HTTP/JSON (fetch)
┌──────────────────▼────────────────────────────┐
│  Backend (FastAPI, Python 3.11)                │
│  Routes → Services → linter_adapter            │
└──────────────────┬────────────────────────────┘
                    │ imports (no subprocess)
┌──────────────────▼────────────────────────────┐
│  Core Engine (src/linter/) — FROZEN, unchanged │
│  loader → parser → rule_engine → evaluator → reporter │
└──────────────────┬────────────────────────────┘
                    │ persists via
┌──────────────────▼────────────────────────────┐
│  SQLite (claritygate.db)                       │
└─────────────────────────────────────────────────┘
```

## Rule Engine Design (unchanged, referenced only)

The backend never reimplements linter logic. `linter_adapter.py` imports the
existing `src/linter/` pipeline functions directly:

```python
from src.linter.loader import load_spec
from src.linter.parser import parse_requirements
from src.linter.rule_engine import run_checks
from src.linter.evaluator import evaluate
from src.linter.reporter import generate_report
```

The adapter's only job is translation: take DB-stored spec text in, call the
existing pipeline, take `Finding`/`EvaluationResult` objects out, and persist
them as backend DB rows. No rule logic, scoring logic, or EARS pattern logic
is duplicated or modified.

## Input/Output Contract

**Input to backend:** raw Markdown text (pasted or uploaded), stored as
`SpecDocument.raw_text`.

**Output from analyze step:** list of `Finding` rows (mirrors existing
`Finding` dataclass from `src/linter/models.py` — same fields: line_number,
check_id, category, severity, message, suggestion), plus a `ReadinessScore`
row (mirrors `EvaluationResult` — score, tier, defect_count, exit-code-equivalent
verdict).

**Contract invariant:** for any given spec text, the score/verdict/finding-count
produced by the backend MUST exactly match what the CLI (`python -m linter.claritygate`)
produces for the same text. This is enforced by an integration test that runs
both paths against `data/samples/ambiguous-requirements.md` and
`data/samples/clean-ears-requirements.md` and asserts identical results.

## EARS Compliance Check Logic

Unchanged — delegated entirely to `src/linter/rule_engine.py`. The frontend's
Review step displays whatever checks the rule engine already implements:
vague verbs/adjectives, non-mandatory imperatives, -ly adverbs, passive voice,
pronoun ambiguity, oblique symbols, escape clauses, EARS casing/pattern/
singularity, missing EARS keyword, tacit knowledge phrasing, implementation
leakage, happy-path-only detection.

## Tacit Knowledge Detection Logic

Unchanged — delegated to existing rule engine. No new heuristics are added
in this phase; this app is a UI/persistence wrapper, not a rule-engine expansion.

## Error/Escalation Handling

| Scenario | Backend behavior | Frontend behavior |
|---|---|---|
| Invalid/empty spec text | 422 response with clear message | Show inline error in Import step, block progression |
| Linter raises LoadError | 500 with error detail logged | Show "Analysis failed" state, allow retry |
| Finding not found (bad ID) | 404 | Show "not found" toast, refresh finding list |
| DB write failure | 500, transaction rolled back | Show retry button, do not lose user's typed rewrite text |
| Concurrent analyze calls on same spec | Last-write-wins, log a warning | Disable Analyze button while a request is in flight |

## Technology Choices

- **FastAPI** over Flask/Django: async support, automatic OpenAPI docs, fast
  to scaffold, pairs well with Pydantic validation for the Finding/Rewrite schemas.
- **SQLite** over Postgres: zero-setup, local-first, matches hackathon demo
  constraints (no external DB server to configure or fail during a live demo).
- **React + Vite + TS + Tailwind**: matches the existing static `demo-ui/index.html`
  visual design language, so the wired app can reuse the same dark theme,
  step indicator, and card layout — minimizing visual rework, only adding
  real data wiring and interactivity.
- **No ORM initially (raw sqlite3 or lightweight SQLAlchemy Core)**: keeps
  the schema simple and inspectable for a hackathon timeline; can upgrade to
  full SQLAlchemy ORM later if time allows, not required for MVP.

## What stays exactly as-is

- `src/linter/` — all 5 pipeline modules, all rule logic, all 36 tests
- `data/samples/ambiguous-requirements.md`, `clean-ears-requirements.md`
- `demo-ui/index.html` — kept as a static fallback, unmodified
- `SKILL.md`, `specs/claritygate-mvp/*`, `.kiro/*` mirrors
