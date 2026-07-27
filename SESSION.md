# ClarityGate — Session Notes

Saved: 2026-07-27 05:10 +08

## Current Session Handoff

### What was accomplished this session

#### 1. Daytona sandbox infrastructure — FULLY OPERATIONAL
- `.env` configured with DAYTONA_API_KEY, LLM_API_KEY (Doubleword Kimi K2.6), LLM_API_URL, LLM_MODEL
- Daytona SDK v0.200.2 installed in `.venv-daytona/` (isolated from stdlib-only linter)
- API key verified: sandbox create → code_run → delete lifecycle works
- `.gitignore` covers `.env` and `.venv-daytona/`

#### 2. Grill Mode 5-coach batch — TC01-TC10 COMPLETE (50/50)
- `daytona_grillmode_batch.py` runs all 5 frozen coach prompts against test cases in a single Daytona sandbox
- Architecture: 1 sandbox, sequential LLM calls (justified: lightweight text-only workload)
- Kimi K2.6 reasoning model quirk: needs max_tokens=8192 (not 2048) or content field returns None
- All 50 evaluations clean, 0 errors after retries
- Results: `output/daytona_grillmode_results.json`

#### 3. Oxylabs scraping — COMPLETE
- Credentials: OXYLABS_USERNAME=kmsumu_3xAAD, password updated (in `.env`)
- 4 google_search queries executed via `scripts/oxylabs_scrape.py`
- 31 organic results scraped → `output/oxylabs_raw/`
- 30 new deny-list terms extracted → `output/oxylabs_deny_list.md`
- 10 new test cases (TC11-TC20) created → `output/oxylabs_test_cases.md`
- Run summary: `output/oxylabs_run_summary.md`

#### 4. TC11-TC20 Daytona batch — COMPLETE (50/50)
- `daytona_batch_tc11_20.py` with retry logic and 8192 max_tokens
- 2 transient connection resets retried successfully on fresh sandbox
- Results: `output/daytona_grillmode_results_tc11_20.json`

#### 5. Combined 20-TC results — MERGED
- `output/daytona_grillmode_results_all20.json` — 100 evaluations, 0 errors, 0 duplicates
- 5 coaches × 20 test cases = 100 unique (coach, TC) pairs confirmed
- TC19 (control) has 1 minor C5 false positive for saturation review

### Key files created this session
| File | Purpose |
|------|---------|
| `.env` | All credentials (Daytona, LLM, Oxylabs) |
| `daytona_test.py` | Connectivity test |
| `daytona_grillmode_batch.py` | Main batch runner (TC01-TC10) |
| `daytona_retry_failed.py` | Retry script for transient failures |
| `daytona_batch_tc11_20.py` | TC11-TC20 batch runner |
| `scripts/oxylabs_scrape.py` | Oxylabs google_search scraper |
| `data/samples/distillation-test-cases.json` | TC01-TC10 canonical JSON |
| `data/samples/distillation-test-cases-tc11-20.json` | TC11-TC20 canonical JSON |
| `output/daytona_grillmode_results_all20.json` | Combined 100 evaluations |
| `output/oxylabs_deny_list.md` | 30 new deny-list terms |
| `output/oxylabs_test_cases.md` | TC11-TC20 definitions |
| `output/oxylabs_run_summary.md` | Scraping run report |

### Important technical notes
- Kimi K2.6 is a reasoning model: response has `reasoning` field, `content` can be None if max_tokens too low
- Daytona sandbox `code_run` can throw ConnectionResetError — always wrap in retry
- Oxylabs password was changed mid-session from `dcRf!688` to `TN0cumEw+b4NOz_`
- `\\n` must be double-escaped in f-strings that generate code for sandbox execution

### Next recommended actions
1. Saturation review: compare coach outputs across TC01-TC20, identify overlap/gaps
2. TC19 C5 false positive: decide if Coach 5 prompt needs tightening
3. Optional: run deny-list terms through ClarityGate rule engine expansion (requires scope approval)
4. ClarityGate submission work: demo video, social post, submission form (core linter frozen)

### Constraints still in force
- ClarityGate core linter is FROZEN (36/36 tests, do not modify `src/linter/`)
- Do not modify `SKILL.md`, `specs/claritygate-mvp/`, `.kiro/specs/claritygate-mvp/`
- All credentials in `.env` only, never hardcoded
- No sandboxes left running; auto-delete intervals set as safety net

---

Saved: 2026-07-26 19:09 +08

## Previous Session Handoff

### Role / operating mode
- Codex is acting as Qoder mission controller, prompt strategist, and reviewer.
- Do not implement ClarityGate code directly unless explicitly asked for a tiny example snippet.
- Qoder is the coding tool. Cursor is no longer part of the active plan.

### ClarityGate status
- Core linter is frozen and complete.
- Latest recorded status: 36/36 tests passing.
- Accepted boundary remains `PLAN.md`: pure Python, standard library only, real implementation under `src/linter/`, five pipeline modules, no UI/backend/database/network in frozen core.
- Do not touch `SKILL.md`, source-of-truth specs, or `.kiro` mirrors.
- Remaining ClarityGate work is submission/demo work only: video, social post, submission form links, optional thin demo shell only if time allows.

### WorkBuddy / Grill Mode status
- Completed 10 test cases across 5 coaches: 50/50 original evaluations done.
- Coach 4 and Coach 5 were rewritten and retested successfully.
- Coach 2 was rewritten and retested successfully on TC03 and TC10.
- Remaining `needs-review` items are acceptable real-world strictness or intentional scope overlap, not blockers for Daytona.

### Final WorkBuddy files
- `grill-mode-final-prompt-pack.md` is the current Daytona-ready prompt pack.
- `requirements-grill-mode.zip` exists and contains `requirements-grill-mode/SKILL.md`.
- Important note: the zip was timestamped before the final Markdown validation-note correction, so if exact validation prose matters, prefer `grill-mode-final-prompt-pack.md` or rebuild the zip.

### Important correction made
- Updated `grill-mode-final-prompt-pack.md` validation note for Coach 4:
  - Correct: TC04 flagged `standard workflow`.
  - Correct: TC05, TC06, TC07, TC08, and TC10 returned empty flags after Coach 4 tightening.
  - Removed stale/mismatched note about `checkout is completed` and `Order confirmations`.

### Next recommended action
- Use `grill-mode-final-prompt-pack.md` for tonight's Daytona parallel run.
- If packaging matters, rebuild `requirements-grill-mode.zip` from the corrected prompt/skill source before distributing.

---

Saved: 2026-07-20

## What was accomplished

### 1. Cleaned requirements.md and SKILL.md (Task 1 & 2)
- Rewrote `requirements.md` with the required sections (Title, Problem Statement,
  Goals, Non-Goals, Target Users, User Stories, Functional Requirements,
  Non-Functional Requirements, Acceptance Criteria in EARS format, Open Questions).
- Rewrote `SKILL.md` as an IDE-agnostic instruction set (Qoder / Kiro / Cursor /
  Qwen) with the required sections (Purpose, When to Use, Review Checklist,
  Ambiguity Rules, EARS Enforcement Rules, Tacit Knowledge Checks, Required Output
  Format, Escalation Rules, Refusal Conditions).
- Removed all leftover citation/gutter artifacts from the original drafts.

### 2. File cleanup
- Deleted old lowercase `skill.md` (which on macOS case-insensitive FS was the same
  file as `SKILL.md` — recreated `SKILL.md` to avoid data loss).
- Removed `.DS_Store`.
- Created `.gitignore` (macOS + editor/OS/Python/Node artifacts).

### 3. Project structure (Task 3)
Created the full structure:
```
ClarityGate/
├── SKILL.md
├── README.md
├── .gitignore
├── src/linter/
├── specs/claritygate-mvp/
│   ├── requirements.md   (moved from root, content preserved)
│   ├── design.md
│   └── tasks.md
├── .kiro/specs/claritygate-mvp/
│   ├── requirements.md   (exact mirror)
│   ├── design.md         (exact mirror)
│   └── tasks.md
└── .cursor/rules/
    └── claritygate.mdc   (Cursor rule from SKILL.md, frontmatter globs + alwaysApply:false)
```

### 4. Wrote design.md
- `specs/claritygate-mvp/design.md` derived strictly from requirements.md + SKILL.md.
- Sections: Architecture Overview, Rule Engine Design, Input/Output Contract, EARS
  Compliance Check Logic, Tacit Knowledge Detection Logic, Error/Escalation
  Handling, Technology Choices.
- Mirrored byte-identically to `.kiro/specs/claritygate-mvp/design.md` (verified
  via diff, 239 lines each).

## Key invariants to preserve
- `specs/claritygate-mvp/requirements.md` and `.kiro/.../requirements.md` MUST stay
  byte-identical (verified identical).
- `specs/claritygate-mvp/design.md` and `.kiro/.../design.md` MUST stay
  byte-identical (verified identical).
- macOS case-insensitive FS: `skill.md` == `SKILL.md`. Never delete one expecting
  the other to survive. Keep a single canonical `SKILL.md`.

## Open / next steps
- `tasks.md` (both specs/ and .kiro/) are still empty placeholders. Qoder Quest
  Mode can generate from `specs/claritygate-mvp/design.md`, or agent can draft.
- `.kiro/.../tasks.md` must be mirrored from `specs/.../tasks.md` once written.
- Open Questions from requirements.md still unresolved (auto-rewrite vs queue;
  Complex EARS handling; transcript access feasibility).

## Verification commands used
- `diff -q specs/claritygate-mvp/requirements.md .kiro/specs/claritygate-mvp/requirements.md`
- `diff -q specs/claritygate-mvp/design.md .kiro/specs/claritygate-mvp/design.md`
