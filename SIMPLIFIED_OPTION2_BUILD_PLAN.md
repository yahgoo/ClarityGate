# ClarityGate Simplified Option 2 — Gamified Full-Stack Build Plan

**Prepared:** Monday, July 27, 2026  
**Target submission:** Wednesday, August 5, 2026  
**Status:** Proposed expansion accepted by the project owner, but implementation remains blocked until the active CLI-only project rules are formally reconciled.

## Objective

Turn the completed ClarityGate CLI into a gamified local application while preserving the existing deterministic linter as the frozen source of truth.

The intended demo flow is:

```text
Paste weak specification
    → Analyze
    → Review findings
    → Rewrite requirements
    → Re-run the frozen linter
    → Improve readiness score and missions
    → Reach Quest Ready
    → Export report
```

## Architecture

```text
React + Vite + TypeScript
            ↓ HTTP/JSON
         FastAPI
            ↓ direct imports
Frozen src/linter pipeline
            ↓
SQLite via Python sqlite3
```

### Technology choices

- Frontend: React, Vite, TypeScript, and project-owned CSS.
- Backend: Python 3.11 and FastAPI.
- Database: SQLite through Python's standard-library `sqlite3` module.
- Core engine: existing `src/linter/`, imported without modification.
- Backend tests: stdlib `unittest`.
- Frontend validation: TypeScript build, focused component tests, and one Playwright smoke flow.
- Deployment: local-first. Firebase Hosting plus Cloud Run is an optional final phase only.

## Protected baseline

The following must not be created, modified, deleted, renamed, moved, or reformatted during the expansion:

- `src/linter/**`
- existing `tests/**`
- `SKILL.md`
- `specs/claritygate-mvp/**`
- `.kiro/specs/claritygate-mvp/**`
- `data/samples/**`
- `demo-ui/index.html`

The existing CLI remains the deterministic source of truth and fallback.

### Required baseline behavior

- Core suite: 36/36 passing.
- Ambiguous sample: 6 requirements, 23 findings, 21 defects, 2 clarifications, 0/100, `REFUSED`.
- Clean sample: 3 requirements, 0 findings, 100/100, `CERTIFIED`.

## Database

Use four tables:

1. `specs`
2. `requirements`
3. `findings`
4. `rewrites`

Do not persist scores, missions, workflow steps, or finding-resolution state. Derive them from the current linter result.

## Accelerated rewrite model

Phase 3 uses requirement-level resolution rather than finding-level resolution.

### Rules

1. Group all findings for a physical requirement line.
2. Store one complete replacement requirement for that line.
3. Keep `specs.raw_text` immutable.
4. Store accepted replacements as overlays keyed by original line number.
5. Reconstruct effective Markdown by applying overlays to physical lines.
6. Run `parse_requirements`, `run_checks`, and `evaluate` against the effective Markdown.
7. Replace stale requirements and findings transactionally.
8. Return the entire refreshed state to the frontend.
9. Derive score and missions from the refreshed findings.

### Combined MVP endpoint

```text
PUT /api/specs/{spec_id}/requirements/{line_number}
```

Example request:

```json
{
  "rewritten_text": "WHEN an order is submitted, THE System SHALL display confirmation within 2 seconds."
}
```

The response returns:

- effective Markdown;
- parsed requirements;
- current findings;
- score;
- tier and verdict;
- derived mission progress.

### Explicit exclusions

Do not implement:

- multi-line replacements;
- fuzzy line matching;
- Markdown AST editing;
- collaborative or concurrent editing;
- undo history beyond resetting accepted overlays;
- per-finding acceptance;
- persisted score history;
- AI-generated rewrites;
- authentication;
- Firestore;
- Firebase Functions;
- SQLAlchemy.

Prepared demo rewrites may be provided for the six-line sample, but they must be labelled as prepared deterministic examples rather than AI-generated content.

## Gamification

Build only the elements that make the central flow easier to understand and more satisfying:

- Import → Review → Resolve → Ready progress rail.
- Animated readiness score.
- Finding-category badges.
- Findings grouped by requirement.
- Derived missions:
  - eliminate vague language;
  - add measurable thresholds;
  - add a failure path;
  - reach Quest Ready.
- Visible progress after each accepted requirement rewrite.
- Final Quest Ready certification state.
- Reset Demo action.
- Before/after specification comparison.
- Markdown report export.

## Phase gates

### Phase 0 — Boundary and contract

Deliverables:

- reconciled project boundary;
- protected-path list;
- database schema;
- frozen API contract;
- rewrite transaction;
- exact test commands.

Stop before implementation until the owner approves the final Qoder plan.

### Phase 1 — Backend foundation

Deliverables:

- FastAPI application;
- raw `sqlite3` initialization;
- four tables;
- create, retrieve, analyze, and report behavior;
- direct wrapper around the actual linter functions;
- equivalence tests.

Gate:

- core remains 36/36;
- both sample baselines remain exact;
- backend result equals direct linter result.

### Phase 2 — Gamified frontend

Deliverables:

- React application shell;
- four-step progress rail;
- Import and Review steps;
- real findings;
- animated score and missions;
- Resolve and Ready presentation components.

Gate:

- pasted ambiguous sample displays the real 23 findings and 0/100 score;
- TypeScript build succeeds;
- no invented API fields.

### Phase 3 — Requirement rewrite and re-lint

Deliverables:

- immutable raw specification;
- accepted line overlays;
- effective Markdown reconstruction;
- combined apply-and-reanalyze endpoint;
- refreshed frontend snapshot;
- reset behavior.

Gate:

```text
23 findings
    → apply one prepared replacement
    → effective Markdown changes
    → frozen linter reruns
    → findings decrease
    → score and missions update
```

### Phase 4 — Integration and E2E

Deliverables:

- predictable clean demo state;
- browser smoke test;
- responsive layout;
- accessibility pass;
- release candidate.

Gate:

- browser flow succeeds twice from clean temporary databases;
- all suites pass together;
- protected baseline remains unchanged;
- CLI fallback still works.

### Phase 5 — Optional deployment

Firebase Hosting plus Cloud Run may be considered only after the local release candidate passes every gate.

Deployment must not delay recording or submission. If cloud setup requires substantial repair, credentials work, billing work, or architectural changes, stop and use the local demo.

## Corrected hour-by-hour schedule

### Monday, July 27 — Boundary and backend foundation

| Time | Work |
|---|---|
| 14:30–15:00 | Record expansion decision and identify conflicts with the active CLI-only rules. |
| 15:00–16:00 | Freeze protected paths and four-table schema. |
| 16:00–17:00 | Freeze API contract. |
| 17:00–18:00 | Freeze rewrite transaction and verify core baselines. |
| 18:00–22:00 | Break and manually review the Qoder plan. |
| 22:01–23:00 | Scaffold backend and FastAPI application. |
| 23:00–00:00 | Implement SQLite initialization. |
| 00:00–01:00 | Implement the four tables. |
| 01:00–02:00 | Add database tests, run core regression, report evidence, and stop. |

### Tuesday, July 28 — Full build day

| Time | Work |
|---|---|
| 09:00–10:00 | Review backend foundation and rerun regression. |
| 10:00–11:00 | Implement the linter adapter. |
| 11:00–12:00 | Implement create, retrieve, and analyze behavior. |
| 12:00–13:00 | Lunch. |
| 13:00–14:00 | Complete report behavior and equivalence tests; freeze the API contract. |
| 14:00–15:00 | Scaffold React, Vite, and TypeScript. |
| 15:00–16:00 | Build application shell and Import step. |
| 16:00–17:00 | Build Review step, real finding groups, and score panel. |
| 17:00–18:00 | Connect paste → analyze → 23 real findings. |
| 22:01–23:00 | Build Resolve step grouped by requirement. |
| 23:00–00:00 | Add prepared editable demo rewrites. |
| 00:00–01:00 | Build Ready screen and run frontend validation. |

### Wednesday, July 29 — Coding only after 22:01

No project coding or Qoder execution before 22:01.

| Time | Work |
|---|---|
| 22:01–23:00 | Implement immutable rewrite overlays and effective-text reconstruction. |
| 23:00–00:00 | Implement combined apply-and-reanalyze behavior. |
| 00:00–01:00 | Connect Resolve step and replace frontend state from the response. |
| 01:00–02:00 | Run accelerated Phase 3 tests and complete the vertical slice twice. |

### Thursday, July 30 — Coding only after 22:01

No project coding or Qoder execution before 22:01.

| Time | Work |
|---|---|
| 22:01–23:00 | Add Reset Demo behavior and final score progression. |
| 23:00–00:00 | Add the browser E2E flow. |
| 00:00–01:00 | Run E2E twice from clean temporary databases. |
| 01:00–02:00 | Repair release blockers and create Release Candidate 1. |

### Friday, July 31 — Polish and QA

| Time | Work |
|---|---|
| 09:00–10:00 | Review Release Candidate 1 and run full regression. |
| 10:00–11:00 | Complete mission and progress behavior. |
| 11:00–12:00 | Accessibility and keyboard navigation. |
| 12:00–13:00 | Lunch. |
| 13:00–14:00 | Responsive and presentation-screen layout. |
| 14:00–15:00 | Polish animations, badges, and completion celebration. |
| 15:00–16:00 | Timed demo rehearsal. |
| 16:00–17:00 | Repair rehearsal blockers only. |
| 17:00–18:00 | Freeze Release Candidate 2. |
| 22:01–00:00 | Qoder Experts Mode final QA, code review, and UI validation. |
| 00:00–01:00 | Consolidate evidence and stop. |

### Saturday, August 1 — Final product decision

| Time | Work |
|---|---|
| 09:00–10:00 | Review final QA evidence. |
| 10:00–11:00 | Repair release blockers only. |
| 11:00–12:00 | Confirm startup and reset instructions. |
| 13:00–15:00 | Conduct two timed rehearsals. |
| 15:00–16:00 | Decide whether optional Firebase deployment is worthwhile. |
| 16:00–18:00 | Freeze the recording build. |

### Sunday, August 2 — Record and upload

| Time | Work |
|---|---|
| 09:00–10:00 | Final regression from clean state. |
| 10:00–11:00 | Rehearse. |
| 11:00–12:00 | Record take 1. |
| 12:00–13:00 | Review the recording. |
| 14:00–15:00 | Record the final take. |
| 15:00–17:00 | Edit, caption, and export. |
| 17:00–18:00 | Upload and verify logged-out access. |

### Monday, August 3 — Publish

| Time | Work |
|---|---|
| 09:00–10:00 | Finalize social copy and attachments. |
| 10:00–11:00 | Verify tags, hashtags, and links. |
| 11:00–12:00 | Publish. |
| 12:00–13:00 | Verify public access. |
| 14:00–17:00 | Respond to comments and share through relevant channels. |
| 17:00–18:00 | Prepare submission-form answers. |

### Tuesday, August 4 — Submit

| Time | Work |
|---|---|
| 09:00–10:00 | Final regression. |
| 10:00–11:00 | Confirm public video and social links. |
| 11:00–12:00 | Complete submission form. |
| 12:00–13:00 | Proofread. |
| 14:00–15:00 | Submit. |
| 15:00–16:00 | Save confirmation evidence. |
| 16:00–18:00 | Resolve administrative issues only. |

### Wednesday, August 5 — Emergency buffer

- 09:00–12:00: confirm receipt and links.
- 12:00–18:00: submission administration only.
- 18:00: internal absolute cutoff.
- No feature development.

## Qoder mode strategy

Qoder Quest modes are selected when a task is created. Use separate tasks rather than attempting to change the mode inside an existing task.

### Task A — Experts Mode, planning only

Purpose:

- inspect current state;
- reconcile the approved expansion with existing rules;
- validate the phase structure;
- produce exact file ownership;
- propose the final implementation plan;
- wait for approval.

No code changes are authorized.

### Tasks B–E — Agent Mode, bounded implementation

Use a new Agent Mode task for each narrow implementation batch:

1. backend database and application skeleton;
2. linter adapter and API;
3. React Import/Review interface;
4. accelerated rewrite and re-lint vertical slice.

Each task receives:

- immediate task;
- exact files;
- exact test commands;
- protected paths;
- one stop condition.

### Task F — Experts Mode, integration

After all implementation gates pass, create a new Experts Mode task for:

- cross-stack integration;
- QA;
- code review;
- browser validation;
- release-candidate evidence.

Experts Mode must not redesign the architecture or expand the feature set.

## Nightly Qoder operating rules

Every post-22:01 request must:

- cover one phase only;
- list exact writable paths;
- list exact test commands;
- repeat protected paths;
- prohibit dependency changes unless already approved;
- stop after reporting evidence.

Never queue cloud deployment, schema redesign, protected-core edits, or multiple phases as one unattended run.

## Fallback

If the rewrite vertical slice is not stable by July 30 at 00:00, simplify Resolve to prepared one-click replacements and preserve the functioning guided flow.

If browser E2E is not stable by July 31, record a manually verified local flow.

If the full-stack application becomes unstable, submit the verified CLI and static concept rather than missing the deadline.
