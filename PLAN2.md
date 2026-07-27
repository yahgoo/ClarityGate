# ClarityGate Option 2 — Full-Stack Build Plan
**Updated: Monday, July 27, 2026, 11:18 AM +08**
**Scope change: Building the real wired Option 2 app. Blackout constraint overridden per explicit user decision.**

## Objective

Convert ClarityGate from (a) a frozen CLI linter + (b) a static demo-only HTML
shell into (c) a real full-stack local app: React frontend + FastAPI backend +
SQLite persistence, wired live to the existing `src/linter/` engine.

## Non-negotiable constraints

1. **Do not modify or weaken** any existing rule-engine logic under `src/linter/`.
   The backend WRAPS the linter, it does not reimplement it.
2. **Do not touch** `SKILL.md`, `specs/claritygate-mvp/*`, or `.kiro` mirrors.
3. Core linter test suite must remain **36/36 passing** at every checkpoint.
4. New code lives in `backend/` and `frontend/` — clean separation from `src/linter/`.
5. Use stdlib/standard patterns where possible; keep dependencies minimal
   (FastAPI, SQLAlchemy or raw sqlite3, React + Vite + TypeScript + Tailwind).

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite + TypeScript + Tailwind CSS |
| Backend | Python 3.11, FastAPI |
| Database | SQLite (local file, no external DB server) |
| Core engine | Existing `src/linter/` modules (loader, parser, rule_engine, evaluator, reporter) — imported, not rewritten |
| Testing | pytest (backend), Vitest/Playwright (frontend), existing unittest suite (core, untouched) |

## Target file tree

```
ClarityGate/
  src/linter/              <- FROZEN, existing, do not modify
  backend/
    app/
      __init__.py
      main.py               <- FastAPI app entrypoint
      db.py                 <- SQLite connection/session
      models.py             <- SpecDocument, RequirementLine, Finding, Rewrite, ReadinessScore, Mission
      schemas.py             <- Pydantic request/response schemas
      routes/
        specs.py             <- POST /api/specs, GET /api/specs/{id}
        analyze.py            <- POST /api/specs/{id}/analyze
        findings.py           <- POST /api/findings/{id}/rewrite, /accept
        reports.py            <- GET /api/specs/{id}/report.md, /impact
      services/
        linter_adapter.py    <- Wraps src/linter/ calls, translates to DB models
        scoring.py            <- Readiness score computation
    tests/
      test_specs.py
      test_analyze.py
      test_findings.py
      test_reports.py
    pyproject.toml
    claritygate.db          <- SQLite file, gitignored
  frontend/
    src/
      main.tsx
      App.tsx
      components/
        ImportStep.tsx
        ReviewStep.tsx
        ResolveStep.tsx
        ReadyStep.tsx
        ScorePanel.tsx
        MissionsPanel.tsx
      api/
        client.ts            <- fetch wrapper for backend API
      types/
        index.ts
    tests/
      guided-gate.spec.ts    <- Playwright E2E
    package.json
    vite.config.ts
    tailwind.config.js
  demo-ui/                  <- KEEP as fallback static shell, do not delete
  data/samples/             <- FROZEN, existing demo specs
```

## API contract (backend)

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/specs` | Create a spec from pasted Markdown or uploaded file text |
| GET | `/api/specs/{id}` | Return raw text, parsed lines, findings, score, workflow state |
| POST | `/api/specs/{id}/analyze` | Run linter pipeline, persist findings |
| POST | `/api/findings/{id}/rewrite` | Save suggested or user-authored EARS rewrite |
| POST | `/api/findings/{id}/accept` | Mark rewrite accepted, recalculate score |
| GET | `/api/specs/{id}/report.md` | Return Markdown Quality Report |
| GET | `/api/specs/{id}/impact` | Return before/after demo comparison data |

## Core data models

- **SpecDocument**: id, title, raw_text, created_at, updated_at
- **RequirementLine**: id, spec_id, line_number, raw_text, ears_pattern, status
- **Finding**: id, spec_id, line_number, check_id, category, severity, message, suggestion, status
- **Rewrite**: id, finding_id, original_text, rewritten_text, accepted
- **ReadinessScore**: spec_id, score, tier, defect_count, clarification_count
- **Mission**: id, spec_id, title, description, status, completion_rule

## Frontend flow

- Left rail: Import → Review → Resolve → Ready (matches existing static shell visual design)
- Center pane: current step workspace, now wired to live API calls
- Right pane: readiness score, issue summary, missions
- Demo path: paste weak spec → analyze → resolve top findings → score improves → export clean spec/report

## Phases

| Phase | Deliverable | Acceptance criteria |
|---|---|---|
| 1. Backend skeleton + DB | FastAPI app boots, SQLite schema created, seed sample weak spec loads | DB initializes from scratch, unit tests cover model creation + score persistence |
| 2. Backend API + linter wiring | All 7 routes implemented, linter_adapter wraps src/linter/ without modifying it | API tests cover create/analyze/rewrite/accept/report; linter still detects all existing categories |
| 3. Frontend build | React app with 4-step flow, wired to live backend, replaces static demo-ui visually | User completes paste→analyze→resolve→ready in browser with REAL data, works on desktop + narrow viewport |
| 4. Integration + polish + E2E | Full app runs together, README updated, Playwright smoke test, demo data prepared | One-command backend start, one-command frontend start, tests pass, demo flow completes twice with sample spec |

## Definition of done

- `uvicorn backend.app.main:app` starts cleanly, `npm run dev` in `frontend/` starts cleanly
- Pasting the ambiguous sample spec through the UI produces the same 23 findings and 0/100 score as the CLI
- Resolving/accepting rewrites in the UI measurably increases the score, ending at or near 100/100 for the clean spec
- `python3 -m unittest -v` still shows 36/36 (core untouched)
- Backend pytest suite passes
- Playwright E2E smoke test passes (full guided-gate flow, twice)
- `demo-ui/index.html` (static fallback) remains untouched and functional as backup

## Risk notes

- This reverses the "safe path" recommendation from the original build plan, which
  explicitly deferred backend/database/UI work to protect the frozen, tested core
  before the Jul 28-30 blackout. Proceeding anyway means the blackout is being
  used as coding time instead of rest/seminar time — explicit user decision.
- Fallback preserved: if the full-stack build stalls or breaks anything, the
  frozen CLI + static demo-ui/index.html remains a complete, working submission
  path at all times. Nothing about this plan removes that safety net.
