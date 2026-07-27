# ClarityGate Full-Stack Expansion — Phase 0 Deliverable (Revised)

---

## A. Revised Boundary Amendment

**Required governance action**: The project owner must explicitly approve the amended text below. Once approved, the owner writes it into AGENTS.md manually or via a separate owner-approved commit. No agent may commit governance changes autonomously.

**Minimum change**: Replace the "Project scope" and "Permanent constraints" sections of AGENTS.md with:

```markdown
## Project scope
Project: ClarityGate

Implementation boundary: SIMPLIFIED_OPTION2_BUILD_PLAN.md (supersedes PLAN.md for new work).

Frozen core (read-only, never modify):
- src/linter/** (deterministic linter — 9 modules, 36/36 tests)
- tests/** (core test suite)
- SKILL.md
- specs/claritygate-mvp/**
- .kiro/specs/claritygate-mvp/**
- data/samples/**
- demo-ui/index.html

Permitted expansion directories (new code lives here):
- backend/            — FastAPI wrapper, SQLite schema, API routes
- tests_backend/      — backend integration tests (stdlib unittest + httpx test client)
- frontend/           — React + Vite + TypeScript application
- frontend/tests/     — Playwright smoke tests

## Permanent constraints
Do not let Qoder drift into:
- auth, Firebase, Firestore, SQLAlchemy, AI rewrite generation
- collaborative/concurrent editing
- modification of any frozen-core path
- persisted score history, undo history, per-finding acceptance state
- multi-line replacements, fuzzy line matching, Markdown AST editing, prefix reconstruction
- cloud deployment (Phase 5 is deferred and requires separate approval)
- pytest (use stdlib unittest for all Python tests)
- any endpoint that drops or recreates the database

Keep backend tests in stdlib `unittest`. Use httpx as test-only dependency for FastAPI TestClient.
Frontend tests use Playwright (single smoke flow only).
All linter logic must be imported from `src.linter.*` — never reimplemented.
Database must not store scores, tiers, verdicts, missions, or workflow state — derive them.
Missions are derived in the frontend only — never returned by the backend.
Every SQLite connection must set PRAGMA foreign_keys = ON.
DB_PATH must be injectable into create_app() — tests use TemporaryDirectory SQLite files; never touch development claritygate.db.
```

---

## B. Corrected API Contract

All endpoints return JSON. Scores/tiers/verdicts are derived by calling `evaluate()` on every response — never stored. Missions are **not** included in backend responses; the frontend derives them from the findings array.

### Endpoints

```
POST   /api/specs
  Body: { "filename": str, "raw_text": str }
  Action: INSERT spec → parse → run_checks → evaluate → INSERT requirements + findings
  Returns: {
    spec_id, filename, raw_text, created_at,
    requirements: [...],
    findings: [...],
    score, tier, verdict,
    requirement_count, defects, clarifications, infos
  }

GET    /api/specs/{spec_id}
  Returns: {
    spec_id, filename, raw_text, created_at,
    requirements: [...],
    findings: [...],
    rewrites: [...],
    score, tier, verdict,
    requirement_count, defects, clarifications, infos
  }

GET    /api/specs/{spec_id}/report
  Returns: { "markdown": str }
  Action: reconstruct effective Markdown → render_report()

PUT    /api/specs/{spec_id}/requirements/{line_number}
  Body: { "rewritten_text": str }
  Validation: reject if rewritten_text contains \n or \r (400 Bad Request)
  Action (single transaction):
    1. UPSERT rewrite row
    2. Reconstruct effective Markdown (raw_text lines + overlays)
    3. parse_requirements(effective_text)
    4. run_checks(records)
    5. evaluate(records, findings)
    6. DELETE + INSERT requirements and findings rows for this spec
    7. COMMIT (full rollback on any failure)
  Returns: {
    effective_markdown,
    requirements: [...],
    findings: [...],
    rewrites: [...],
    score, tier, verdict,
    requirement_count, defects, clarifications, infos
  }

DELETE /api/specs/{spec_id}/requirements/{line_number}/rewrite
  Action (single transaction): same as PUT but DELETE the overlay row first
  Returns: same shape as PUT

POST   /api/specs/{spec_id}/reset
  Action (single transaction):
    1. DELETE all rewrites for this spec_id
    2. Reconstruct effective Markdown (= raw_text, no overlays)
    3. Re-parse, re-check, re-evaluate
    4. Replace requirements + findings rows
    5. COMMIT
  Returns: same shape as GET
```

### Rewrite Semantics

- `rewritten_text` is one complete physical Markdown line including its list marker (e.g. `- WHEN an order...`).
- The backend does NOT reconstruct prefixes, parse Markdown structure, or perform fuzzy matching.
- Substitution is positional: line N of raw_text is replaced by the overlay text verbatim.

### What the Backend Does NOT Return

- `missions[]` — derived in frontend only
- persisted score history
- workflow step state

---

## C. Corrected Phase Gates

| Phase | Gate Condition | Evidence Required |
|---|---|---|
| **1 → 2** | Core 36/36 unchanged + POST ambiguous sample → exact 23 findings, 21 defects, 2 clarifications, score 0, verdict REFUSED + POST clean sample → 0 findings, score 100, verdict CERTIFIED + backend equivalence (result == direct linter call) | `python3 -m unittest discover -s tests -v` + `python3 -m unittest discover -s tests_backend -v` |
| **2 → 3** | TypeScript build exits 0 + dev server renders ambiguous sample with 23 findings visible in DOM + score displays 0/100 | `cd frontend && npm run build` + Playwright assertion |
| **3 one-rewrite** | PUT one prepared rewrite → **findings count decreases** (score may remain 0 due to evaluator clamping negative totals to zero — do NOT require score increase) | curl + assertion on findings count delta |
| **3 certification** | Apply **all six** prepared demo rewrites sequentially → validate complete effective Markdown directly with `parse_requirements → run_checks → evaluate` → findings == 0, score == 100, verdict == CERTIFIED | Automated validation script calling linter pipeline on reconstructed effective text |
| **3 → 4** | Both 3-one-rewrite and 3-certification gates pass + TypeScript build exits 0 | `cd frontend && npm run build` + validation scripts |
| **4 → done** | Playwright full flow succeeds twice from fresh temporary databases (import → review → resolve all → certified) + responsive at 375px and 1440px | `cd frontend && npx playwright test` (exits 0 × 2 with separate temp DBs) |

### Mission Derivation Rules (Frontend Only)

| Mission ID | Condition (computed from `findings[]` in response) |
|---|---|
| `eliminate_vague_language` | 0 findings where `category == "lexical"` |
| `add_measurable_thresholds` | 0 findings where `check_id == "AMB-VAGUE-ADJ"` |
| `add_failure_path` | 0 findings where `check_id == "COMP-HAPPY-PATH"` |
| `reach_quest_ready` | `score >= 90` AND `verdict == "CERTIFIED"` |

---

## D. Corrected Task/File List

### Canonical File Layout

```
backend/
  __init__.py
  config.py
  database.py
  schema.sql
  linter_adapter.py
  main.py
  routes.py

tests_backend/
  __init__.py
  test_database.py
  test_linter_adapter.py
  test_routes.py
  test_equivalence.py

frontend/
  package.json
  vite.config.ts
  tsconfig.json
  index.html
  playwright.config.ts
  src/
    main.tsx
    App.tsx
    vite-env.d.ts
    api/
      client.ts
      types.ts
    components/
      StepRail.tsx
      ScoreBar.tsx
      FindingsTable.tsx
      VerdictBadge.tsx
      StatsCards.tsx
      Missions.tsx
      RequirementEditor.tsx
    pages/
      ImportPage.tsx
      ReviewPage.tsx
      ResolvePage.tsx
      ReadyPage.tsx
    state/
      specStore.ts
    demo/
      preparedRewrites.ts
  tests/
    smoke.spec.ts
    certification.spec.ts

requirements-backend.txt
```

### Phase 1 — Backend Foundation

#### Task 1.1: SQLite Schema and Database Module
- **Files**: `backend/__init__.py`, `backend/database.py`, `backend/schema.sql`, `backend/config.py`
- **Test**: `python3 -m unittest tests_backend.test_database -v`
- **Dependencies**: None
- **Protected paths**: all frozen-core paths
- **Stop**: Tables created with `PRAGMA foreign_keys = ON`; CRUD helpers pass (insert_spec, get_spec, upsert_rewrite, delete_rewrite, get_rewrites, replace_requirements, replace_findings); all ops use transactions with rollback on failure; tests use TemporaryDirectory
- **Parallel**: Yes — with Task 1.2

#### Task 1.2: Backend Project Scaffold
- **Files**: `backend/main.py`, `requirements-backend.txt` (fastapi, uvicorn, httpx)
- **Test**: `python3 -c "from backend.main import create_app; app = create_app('/tmp/test.db'); print('OK')"`
- **Dependencies**: None
- **Protected paths**: all frozen-core paths
- **Stop**: `create_app(db_path)` accepts injectable DB_PATH, returns FastAPI instance; CORS allows localhost:5173; httpx listed as test-only dep
- **Parallel**: Yes — with Task 1.1

#### Task 1.3: Linter Adapter Layer
- **Files**: `backend/linter_adapter.py`, `tests_backend/__init__.py`, `tests_backend/test_linter_adapter.py`
- **Test**: `python3 -m unittest tests_backend.test_linter_adapter -v`
- **Dependencies**: Task 1.1
- **Protected paths**: all frozen-core paths; must NOT modify `src/linter/`
- **Stop**: `analyze_spec(db, raw_text, filename)` inserts and returns full state; `apply_rewrite(db, spec_id, line_number, text)` validates no `\n`/`\r`, performs single-transaction overlay+reconstruct+reparse+recheck+replace; `reset_rewrites(db, spec_id)` clears overlays and reanalyzes; equivalence: adapter result == direct linter call; tests use TemporaryDirectory
- **Parallel**: No (depends on 1.1)

#### Task 1.4: API Routes
- **Files**: `backend/routes.py`, `tests_backend/test_routes.py`
- **Test**: `python3 -m unittest tests_backend.test_routes -v`
- **Dependencies**: Task 1.2, Task 1.3
- **Protected paths**: all frozen-core paths
- **Stop**: 6 endpoints (POST /api/specs, GET /api/specs/{id}, GET /api/specs/{id}/report, PUT /api/specs/{id}/requirements/{line}, DELETE /api/specs/{id}/requirements/{line}/rewrite, POST /api/specs/{id}/reset); PUT rejects `\n`/`\r` with 400; no missions in responses; tests use httpx AsyncClient + TemporaryDirectory DB
- **Parallel**: No (depends on 1.2 + 1.3)

#### Task 1.5: Phase 1 Gate Validation
- **Files**: `tests_backend/test_equivalence.py`
- **Test**: `python3 -m unittest discover -s tests -v && python3 -m unittest discover -s tests_backend -v`
- **Dependencies**: Task 1.4
- **Protected paths**: all frozen-core paths
- **Stop**: Core 36/36 pass unchanged + POST ambiguous → 23 findings, 21 defects, 2 clarifications, score 0, REFUSED + POST clean → 0 findings, score 100, CERTIFIED + equivalence verified
- **Parallel**: No (final gate)

---

### Phase 2 — Gamified Frontend

#### Task 2.1: React Project Scaffold
- **Files**: `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/vite-env.d.ts`
- **Test**: `cd frontend && npm install && npm run build`
- **Dependencies**: Phase 1 gate (Task 1.5)
- **Protected paths**: all frozen-core paths
- **Stop**: `npm run build` exits 0
- **Parallel**: Yes — with Task 2.2

#### Task 2.2: API Client and Types
- **Files**: `frontend/src/api/client.ts`, `frontend/src/api/types.ts`
- **Test**: `cd frontend && npx tsc --noEmit`
- **Dependencies**: Phase 1 gate (Task 1.5)
- **Protected paths**: all frozen-core paths
- **Stop**: Types match API contract exactly (no missions in response types); compiles clean
- **Parallel**: Yes — with Task 2.1

#### Task 2.3: Core UI Components
- **Files**: `frontend/src/components/StepRail.tsx`, `ScoreBar.tsx`, `FindingsTable.tsx`, `VerdictBadge.tsx`, `StatsCards.tsx`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Task 2.1, Task 2.2
- **Protected paths**: all frozen-core paths
- **Stop**: Build succeeds; components accept typed props
- **Parallel**: No

#### Task 2.4: Import and Review Flow
- **Files**: `frontend/src/pages/ImportPage.tsx`, `frontend/src/pages/ReviewPage.tsx`, `frontend/src/state/specStore.ts`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Task 2.3
- **Protected paths**: all frozen-core paths
- **Stop**: Import calls POST /api/specs; Review displays findings from response
- **Parallel**: No

#### Task 2.5: Phase 2 Gate Validation
- **Files**: `frontend/playwright.config.ts`, `frontend/tests/smoke.spec.ts`
- **Test**: `cd frontend && npx playwright test`
- **Dependencies**: Task 2.4
- **Protected paths**: all frozen-core paths
- **Stop**: Playwright: import ambiguous sample → 23 findings in DOM → score 0/100
- **Parallel**: No

---

### Phase 3 — Requirement Rewrite and Re-lint

#### Task 3.1: Resolve Page UI
- **Files**: `frontend/src/pages/ResolvePage.tsx`, `frontend/src/components/RequirementEditor.tsx`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Phase 2 gate (Task 2.5)
- **Protected paths**: all frozen-core paths
- **Stop**: Renders findings grouped by requirement; RequirementEditor shows immutable raw text + editable single-line overlay field; plain text only
- **Parallel**: Yes — with Task 3.2

#### Task 3.2: Missions Component and Prepared Rewrites
- **Files**: `frontend/src/components/Missions.tsx`, `frontend/src/demo/preparedRewrites.ts`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Phase 2 gate (Task 2.5)
- **Protected paths**: all frozen-core paths
- **Stop**: Missions component derives 4 missions from findings[] using corrected rules (see Section C); preparedRewrites.ts contains 6 line-keyed replacements including Markdown list markers; build succeeds
- **Parallel**: Yes — with Task 3.1

#### Task 3.3: Apply-and-Reanalyze Integration
- **Files**: modify `frontend/src/pages/ResolvePage.tsx`, modify `frontend/src/state/specStore.ts`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Task 3.1, Task 3.2
- **Protected paths**: all frozen-core paths
- **Stop**: User edits one requirement → PUT fires → full frontend state replacement from response → findings count visible; no multi-line, no `\n`/`\r` in input
- **Parallel**: No

#### Task 3.4: Ready Page
- **Files**: `frontend/src/pages/ReadyPage.tsx`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Task 3.3
- **Protected paths**: all frozen-core paths
- **Stop**: When verdict == CERTIFIED and score >= 90, shows certification; export calls GET /api/specs/{id}/report
- **Parallel**: No

#### Task 3.5: Prepared Rewrites Validation
- **Files**: `frontend/tests/certification.spec.ts` (Playwright) OR `tests_backend/test_prepared_rewrites.py` (unittest calling linter directly)
- **Test**: `python3 -m unittest tests_backend.test_prepared_rewrites -v`
- **Dependencies**: Task 3.2 (needs preparedRewrites content finalized)
- **Protected paths**: all frozen-core paths
- **Stop**: Load ambiguous-requirements.md → apply all 6 prepared rewrites as line overlays → reconstruct effective Markdown → `parse_requirements → run_checks → evaluate` → assert exact expected findings count, score, tier, verdict. Do NOT assume the result — record the actual verified values as the frozen baseline.
- **Parallel**: Can run with Task 3.3/3.4 once 3.2 is done

#### Task 3.6: Phase 3 Gate Validation
- **Test**: `cd frontend && npx playwright test`
- **Dependencies**: Task 3.4, Task 3.5
- **Protected paths**: all frozen-core paths
- **Stop**: One-rewrite gate (findings decrease after single PUT) + full-certification gate (all 6 applied → expected final state) + build exits 0
- **Parallel**: No (final gate)

---

### Phase 4 — Integration and E2E

#### Task 4.1: Responsive Layout
- **Files**: CSS/Tailwind adjustments in `frontend/src/`
- **Test**: `cd frontend && npm run build`
- **Dependencies**: Phase 3 gate (Task 3.6)
- **Protected paths**: all frozen-core paths
- **Stop**: Layout renders at 375px and 1440px
- **Parallel**: Yes — with Task 4.2

#### Task 4.2: E2E Flow Test
- **Files**: update `frontend/tests/smoke.spec.ts` or add `frontend/tests/e2e-flow.spec.ts`
- **Test**: `cd frontend && npx playwright test`
- **Dependencies**: Phase 3 gate (Task 3.6)
- **Protected paths**: all frozen-core paths
- **Stop**: Full flow (import → review → resolve all 6 → certified) succeeds twice with fresh temp DBs; each run creates a new TemporaryDirectory SQLite; Playwright exits 0 both times
- **Parallel**: Yes — with Task 4.1

---

## E. Corrected Phase 1 Coding Prompt

```
Immediate task: ClarityGate Backend Foundation (Phase 1)

Context:
- Frozen linter in src/linter/ — DO NOT modify any file under src/linter/ or tests/.
- Import linter via:
    from src.linter.parser import parse_requirements
    from src.linter.rule_engine import run_checks
    from src.linter.evaluator import evaluate
    from src.linter.models import RequirementRecord, Finding, EvaluationResult
    from src.linter.reporter import render_report
- Database: SQLite via stdlib sqlite3. No SQLAlchemy. No pytest.
- Server: FastAPI + uvicorn. httpx for test client only.
- Every SQLite connection: PRAGMA foreign_keys = ON.
- DB_PATH injectable into create_app(db_path: str).
- All tests use tempfile.TemporaryDirectory for DB files. Never read/write claritygate.db.

Files to create:
- backend/__init__.py (empty)
- backend/config.py (DEFAULT_DB_PATH = "claritygate.db")
- backend/schema.sql (4 tables — see below)
- backend/database.py (init_db, get_connection context manager with foreign_keys ON,
  insert_spec, get_spec, upsert_rewrite, delete_rewrite, delete_all_rewrites,
  get_rewrites, replace_requirements, replace_findings — all transactional)
- backend/linter_adapter.py (analyze_spec, apply_rewrite, delete_rewrite_and_reanalyze,
  reset_rewrites — each performs single-transaction: overlay mutation + effective-text
  reconstruction + parse + check + evaluate + replace rows + commit; full rollback on failure)
- backend/main.py (create_app(db_path) factory, lifespan for init_db, CORS for localhost:5173)
- backend/routes.py (6 endpoints listed below)
- requirements-backend.txt (fastapi, uvicorn, httpx)
- tests_backend/__init__.py (empty)
- tests_backend/test_database.py (5 tests: insert, get, upsert rewrite, delete rewrite, foreign key enforcement)
- tests_backend/test_linter_adapter.py (4 tests: analyze ambiguous→23 findings, analyze clean→0 findings, apply rewrite→findings decrease, rewrite with newline rejected)
- tests_backend/test_routes.py (7 tests: one per endpoint + newline rejection 400)
- tests_backend/test_equivalence.py (2 tests: POST result matches direct linter call for both samples)

Schema (exact):
  CREATE TABLE specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    raw_text TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
  );
  CREATE TABLE requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spec_id INTEGER NOT NULL REFERENCES specs(id),
    line_number INTEGER NOT NULL,
    raw_text TEXT NOT NULL,
    statement TEXT NOT NULL,
    section TEXT,
    uppercase_keywords TEXT NOT NULL DEFAULT '[]',
    lowercase_keywords TEXT NOT NULL DEFAULT '[]',
    UNIQUE(spec_id, line_number)
  );
  CREATE TABLE findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spec_id INTEGER NOT NULL REFERENCES specs(id),
    line_number INTEGER NOT NULL,
    type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    suggested_rewrite TEXT NOT NULL,
    check_id TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT ''
  );
  CREATE TABLE rewrites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spec_id INTEGER NOT NULL REFERENCES specs(id),
    line_number INTEGER NOT NULL,
    rewritten_text TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(spec_id, line_number)
  );

Endpoints:
  POST   /api/specs                                    — create + analyze
  GET    /api/specs/{spec_id}                          — retrieve full state
  GET    /api/specs/{spec_id}/report                   — Markdown report
  PUT    /api/specs/{spec_id}/requirements/{line_number}  — apply rewrite + reanalyze
  DELETE /api/specs/{spec_id}/requirements/{line_number}/rewrite — remove overlay + reanalyze
  POST   /api/specs/{spec_id}/reset                    — delete all overlays + reanalyze

Constraints:
- Never store scores, tiers, verdicts, missions, or workflow state.
- Derive score/tier/verdict on every response by calling evaluate().
- Do NOT include missions[] in any response.
- specs.raw_text is immutable after INSERT.
- rewritten_text must be one physical line — reject \n or \r with HTTP 400.
- apply_rewrite must: read raw_text → split lines → substitute overlay at line_number → join → parse_requirements → run_checks → evaluate → replace DB rows. All in one transaction. Rollback on failure.
- All responses include: requirements[], findings[], score, tier, verdict, requirement_count, defects, clarifications, infos.
- PUT/DELETE-rewrite responses additionally include: effective_markdown, rewrites[].
- No DELETE /api/reset endpoint. No endpoint drops/recreates the database.

Test command:
  python3 -m unittest discover -s tests -v && python3 -m unittest discover -s tests_backend -v

Protected paths (do NOT modify):
  src/linter/**, tests/**, SKILL.md, specs/**, .kiro/specs/**, data/samples/**, demo-ui/index.html

Stop condition:
- Core 36/36 pass (unchanged, zero modifications to frozen paths).
- All tests_backend pass.
- POST data/samples/ambiguous-requirements.md → 23 findings, 21 defects, 2 clarifications, score 0, verdict REFUSED.
- POST data/samples/clean-ears-requirements.md → 0 findings, score 100, verdict CERTIFIED.
- Equivalence: backend result == direct linter call on same input for both samples.
- PUT with rewritten_text containing \n → 400 Bad Request.
- All tests use temporary databases, never claritygate.db.
```

---

## Stop

Deliverables A–E complete. No files modified. No code written. No dependencies installed. No servers started.

Awaiting explicit owner approval of the boundary amendment and implementation plan before any Phase 1 work begins.