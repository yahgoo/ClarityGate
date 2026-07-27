<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# ClarityGate — AI Product Handoff Package

This package assembles everything currently defined in the project's spec assets into a structured handoff document. It also flags where information is missing and states explicit assumptions rather than inventing unnecessary complexity, per the constraints of this exercise.

***

## 1. Executive Summary

**Problem statement**: Bad requirements are expensive when discovered late — rework tied to poor specs (not implementation bugs) can account for up to half of total development costs, and in AI-assisted workflows, vague requirements cause "AI drift," where coding agents fill gaps with inconsistent assumptions.[^1]

**Target users**: Business Analysts / Requirements Engineers (primary), Product Managers (secondary), Developers/Engineering Leads (indirect beneficiaries).[^2][^1]

**Value proposition**: ClarityGate is an upstream quality gate that scores, teaches, and gamifies the rewriting of ambiguous requirements into strict EARS syntax before they're handed to an AI coding agent (Qoder), directly improving the reliability of AI-generated output.[^2]

**Why this product should exist**: No lightweight, hackathon-scoped tool currently sits between "vibe coding" prototypes and formal AI build execution to catch requirement-level defects before they become code-level defects.[^1]

**Success metrics (assumption — not explicitly defined in source docs)**: (a) Quest Readiness Score improvement per session, (b) reduction in flagged ambiguity count per document, (c) qualitative delta between "before" and "after" Quest Mode build outputs.

**Elevator pitch**: ClarityGate is a gamified spec-quality cockpit that catches vague, untestable requirements before Qoder builds from them — turning "the system should be fast" into "WHEN an order is placed, THE SYSTEM SHALL confirm within 2 seconds," so the same AI agent produces dramatically better software from a cleaner spec.[^2]

***

## 2. Product Vision

- **Long-term vision**: Become the default requirements-quality layer for any spec-driven AI development workflow, portable across Qoder, Kiro, and Cursor.[^2]
- **MVP vision**: A local-first Python linter wrapped in a lightweight, gamified web UI, demoable within a hackathon timeframe.[^2]
- **Future roadmap (assumption, not sourced)**: Multi-user team spaces, integration with issue trackers, direct chat-transcript ingestion for "silent intent" detection  (currently listed as an Open Question, not committed).[^1]
- **Guiding principles**: Local-first, no unnecessary infrastructure, Qoder-centric narrative, professional (not childish) gamification, teach-don't-just-flag philosophy.[^3][^2]

***

## 3. User Personas

| Persona | Goals | Frustrations | Technical Ability | Accessibility Notes | Primary Use Cases |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Business Analyst / Requirements Engineer (primary) | Turn vague meeting notes into actionable, testable requirements [^2] | Sees refinement as tedious "police work" rather than craft; time pressure | Low-to-moderate technical; domain-expert, not necessarily a coder | Needs clear text contrast, no jargon-heavy error messages | Paste draft spec, run analyzer, rewrite via EARS Coach |
| Product Manager (secondary) | Ensure specs are measurable, scoped, testable before engineering handoff [^2] | Reducing AI guesswork; proving spec quality to stakeholders | Moderate; comfortable with docs, not code | Same as above | Reviewing Quest Readiness Score, Impact View for stakeholder proof |
| Developer / Engineering Lead (indirect) | Fewer ambiguous tickets, better AI-generated code [^2] | Rework caused by unclear upstream specs | High | N/A (not a direct UI user) | Consumes cleaned spec output, not an active UI persona |


***

## 4. Jobs To Be Done

- When I receive vague meeting notes, I want to quickly identify which lines are ambiguous, so that I can rewrite them before handoff.
- When I write acceptance criteria, I want to verify EARS compliance, so that requirements are testable.[^1]
- When my document only covers happy-path scenarios, I want to be prompted for error paths, so that AI agents don't implement biased "happy path only" logic.[^1]
- When I finish cleaning a spec, I want to see proof that it improves AI build output, so that I can justify the time spent refining it.[^2]

***

## 5. User Stories

| Story | Priority | Complexity | MVP/Future |
| :-- | :-- | :-- | :-- |
| As a developer, I want to scan requirements.md for vague terms like "fast" so I can replace them with measurable metrics [^1] | High | Medium | MVP |
| As a PM, I want to verify EARS "WHEN...SHALL..." structure compliance [^1] | High | Medium | MVP |
| As a quality engineer, I want the tool to flag missing "Unwanted Behavior" (IF-THEN) paths [^1] | High | Medium | MVP |
| As a spec author, I want two-option clarification questions for ambiguous phrases [^1][^3] | Medium | High | Future (MVP: flag only, no interactive Q\&A loop — see assumption below) |
| As a developer, I want tacit-knowledge gaps flagged (unstated assumptions) [^1] | Medium | High | Future (stretch for MVP) |
| As a BA, I want a Quest Readiness Score so I know if my spec is safe to hand to Qoder [^2] | High | Low | MVP |
| As a BA, I want gamified missions to make cleanup feel like progress [^2] | Medium | Medium | MVP (simplified) |
| As a PM, I want a before/after Impact View comparing weak vs. strong AI builds [^2] | High | Medium | MVP |

**Assumption**: The interactive two-option "Clarification Queue" (US4 in requirements.md) is scoped as Future for MVP, since building an interactive Q\&A loop is higher complexity than the hackathon timeline supports; MVP will only flag and suggest, not conduct a full dialogue.[^1]

***

## 6. User Journey

**Discovery** → User learns about ClarityGate via hackathon demo/social post, opens the repo in Qoder.

**Onboarding** → User pastes a sample or their own draft requirements.md into Spec Inbox. No account creation assumed for MVP (local-first, single-user tool).[^2]

**Core workflow** → Paste → Analyze (Analyzer flags issues) → Rewrite (EARS Coach) → Score (Quest Readiness Score) → Missions (optional gamified nudges) → Impact View (before/after Quest Mode comparison).

**Completion** → User reaches a Quest Readiness Score they're satisfied with and exports/hands off the cleaned spec to Qoder Quest Mode.

**Retention** → Refinement Streak tracking (from gamification design) encourages return visits for ongoing spec work.

**Decision points**: Continue rewriting vs. accept current score and proceed; accept suggested rewrite vs. write manually.

**Alternate paths**: User skips EARS Coach and goes straight from Analyzer to exporting (lower score, discouraged but not blocked — no punishment mechanics per design constraints).

**Failure paths**: Malformed/empty file upload; requirements file with only thesis-level statements (tool should refuse to proceed to Design phase per skill.md refusal conditions).[^3]

***

## 7. Information Architecture

```
ClarityGate Web App
├── Spec Inbox (entry screen)
├── Analyzer (findings list, grouped by type/severity)
├── EARS Coach (per-line rewrite workspace)
├── Quest Readiness Score (score + tier display)
├── Missions (task list, streak indicator)
└── Impact View (before/after comparison, delta summary)
```

- **Navigation model (assumption)**: Linear/sequential primary flow with persistent top or side navigation allowing jump-back to any screen — not a strict wizard, since BAs may revisit Analyzer after partial rewrites.
- **Settings**: Not defined in source docs — **assumption**: no settings screen needed for MVP (local-first, single config file if any).
- **Deep links**: Not required for MVP (single local session, no multi-user routing).

***

## 8. Screen Inventory

| Screen | Purpose | Inputs | Outputs | Buttons | Empty State | Loading State | Error State | Accessibility | Analytics Events (assumption) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Spec Inbox | Ingest draft spec [^2] | Pasted text or .md upload | Stored draft ready for analysis | "Analyze" | "No drafts yet — paste or upload to begin" | N/A | "File must be UTF-8 .md" [^1] | Label all inputs, keyboard-accessible upload | `spec_submitted` |
| Analyzer | Run checks, highlight issues [^2] | Draft spec from Inbox | List of findings by type/severity | "Send to EARS Coach", "Re-scan" | "No issues found — spec may already be clean" | Progress indicator (required for larger files) [^1] | "Scan failed — invalid file encoding" | Color is not sole severity indicator (icon + text) | `analysis_completed`, `finding_flagged` |
| EARS Coach | Teach EARS rewrite per line [^2] | Flagged line + user rewrite | Validated EARS-compliant line | "Accept rewrite", "Skip", "Rewrite again" | N/A (always has content if findings exist) | Brief validation spinner | "Rewrite still fails EARS grammar" | Clear actor/trigger/response labeling in plain language [^2] | `rewrite_submitted`, `rewrite_accepted` |
| Quest Readiness Score | Show overall spec quality [^2] | Aggregated finding/rewrite data | Score 0–100, tier label | "View Missions", "Proceed to Impact View" | Score defaults to baseline on first scan | N/A | N/A | Score shown as number + text label, not color alone | `score_viewed` |
| Missions | Gamified nudges [^2] | Current findings/score state | List of suggested tasks | "Mark complete" (auto-detected via rewrite state — assumption) | "No missions — spec is in great shape" | N/A | N/A | N/A | `mission_completed` |
| Impact View | Before/after Quest Mode comparison [^2] | Weak build output + strong build output | Delta summary, annotated comparison | "Export summary" (assumption) | "Run Quest Mode to see comparison" | "Generating comparison..." | "Quest Mode build failed — retry" | Text-based delta summary, not visual-only | `impact_view_generated` |


***

## 9. Functional Requirements

**Assumption**: Categories requested (Authentication, Profile, Search, Sharing, Notifications, Administration, Integrations) largely **do not apply** to this MVP, since ClarityGate is a local-first, single-user tool with no backend, network dependency, or multi-user model. Only Content and Settings-adjacent categories are relevant.[^2]


| Category | Feature | Inputs | Outputs | Business Rules | Validation | Dependencies |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Content (Parsing) | Parse requirements.md for EARS keywords | UTF-8 .md file | Structured token list | Keywords WHEN, WHILE, WHERE, IF, THEN, SHALL must be UPPERCASE [^1] | Reject non-UTF-8 files | Loader stage [^2] |
| Content (Linting) | Flag vague verbs, adjectives, passive voice, escape clauses, pronoun antecedents, oblique symbols [^3] | Parsed requirement lines | List of Findings (type, severity, line) | One SHALL per requirement (singularity) [^3] | N/A | Rule Engine stage [^2] |
| Content (Coaching) | Suggest EARS rewrite | Flagged line | Rewritten EARS-compliant line | Must match one of 6 canonical EARS patterns [^3] | Rewrite re-validated against grammar rules | Evaluator stage [^2] |
| Content (Reporting) | Generate Quality Report | All findings | Markdown report + stdout summary + exit code [^1] | N/A | N/A | Reporter stage [^2] |
| Content (Scoring) | Compute Quest Readiness Score | Finding count/severity | 0–100 score | Scoring formula **not defined in source docs — assumption**: weighted deduction per finding severity | N/A | Evaluator stage |
| Settings (Auth) | N/A | — | — | **Assumption**: No authentication for MVP (local tool, single user) | — | — |


***

## 10. Non-Functional Requirements

| Category | Requirement |
| :-- | :-- |
| Performance | Scan of ~20 requirements completes within 10 seconds [^1] |
| Scalability | Not a stated concern for MVP — local-first, single-document scope [^2] |
| Accessibility | Quality Report output in human-readable Markdown [^1]; **assumption**: WCAG 2.1 AA for web UI components not explicitly specified, recommended as best practice |
| Privacy | No network dependency, no data leaves local machine [^2] |
| Security | No auth/backend attack surface by design (local-first) [^2] |
| Offline behavior | Fully offline-capable — no server or database [^2] |
| Localization | Not addressed in source docs — **assumption**: English-only for MVP |
| Responsiveness | Not specified — **assumption**: Desktop-first, since target users work at a desk during spec review sessions |
| Browser support | Not specified — **assumption**: Modern Chromium/Firefox/Safari, no legacy browser support required |
| Device support | Not specified — **assumption**: Desktop/laptop only for MVP, no mobile requirement |
| Reliability | Accuracy target: F-score ≥ 77% in detecting ambiguous words [^1] |


***

## 11. UX Guidelines

- **Navigation**: Linear core loop (paste → analyze → rewrite → score → compare) should remain visually obvious; avoid burying screens in nested menus.[^2]
- **Visual hierarchy**: Findings severity (High/Med/Low) must be distinguishable without relying on color alone (accessibility).
- **Feedback patterns**: Real-time progress indicator during scans of larger files; immediate validation feedback on EARS rewrites.[^1]
- **Error handling**: Clear, non-technical error messages (e.g., "This file isn't UTF-8 text" rather than a stack trace).[^1]
- **Empty states**: Should feel encouraging, not punitive (e.g., "No issues found" rather than a blank silence).
- **Micro-interactions**: Subtle, professional — no confetti or cartoon mascots per explicit constraint.[^2]
- **Motion guidelines**: Minimal; used only to reinforce state changes (e.g., score updating), never decorative.
- **Accessibility rules**: Keyboard-navigable forms, sufficient contrast, screen-reader labels on all inputs/buttons.
- **Touch targets / Dark mode**: Not addressed in source docs — **assumption**: not required for MVP given desktop-first, professional-tool context.

***

## 12. Design System

**Assumption**: No design system currently exists — this is the first attempt at defining one, since prior exploration confirmed only text specs exist, no visual mockups.[^2]


| Element | Recommendation (assumption, pending Product Design review) |
| :-- | :-- |
| Typography | Clean sans-serif (e.g., Inter, IBM Plex Sans) — professional, enterprise-tool feel |
| Colors | Muted, low-saturation palette (navy/slate primary, single accent color); avoid bright "gamey" palettes per constraint [^2] |
| Spacing | 8px base grid |
| Grid | 12-column responsive grid, desktop-first |
| Icons | Simple line icons, no illustrative/cartoon icon sets |
| Buttons | Rectangular, minimal rounding, clear primary/secondary hierarchy |
| Cards | Used for Findings and Missions lists |
| Forms | Single-column, clear labels above inputs |
| Dialogs | Used sparingly — e.g., rewrite confirmation |
| Charts | Score ring/gauge for Quest Readiness Score; simple bar/delta chart for Impact View |
| Animation | Subtle fade/slide only; no bounce or playful easing |


***

## 13. Data Model

**Assumption**: No database is planned for MVP (local-first, file-based). Entities below represent in-memory/session objects, not persisted database tables, unless local session persistence is added later.[^2]


| Entity | Attributes | Relationships | Constraints | Lifecycle |
| :-- | :-- | :-- | :-- | :-- |
| SpecDocument | id, raw_text, upload_timestamp | Has many Findings | Must be valid UTF-8 [^1] | Created on upload, discarded/exported at session end |
| Finding | id, spec_document_id, line_number, type, severity, suggested_rewrite | Belongs to SpecDocument; may link to Rewrite | Type in {vague_verb, vague_adjective, passive_voice, escape_clause, pronoun_antecedent, oblique_symbol, ears_violation} [^3] | Created during Analyzer scan; resolved when rewrite accepted |
| Rewrite | id, finding_id, original_line, rewritten_line, ears_pattern, accepted (bool) | Belongs to Finding | Must match one of 6 EARS patterns [^3] | Created in EARS Coach, finalized on accept |
| ReadinessScore | spec_document_id, score (0-100), tier | Belongs to SpecDocument | Score range 0–100 [^2] | Recalculated after each accepted rewrite |
| Mission | id, description, completion_condition | Related to Finding/ReadinessScore state | N/A | Generated dynamically based on current findings |
| ImpactComparison | spec_document_id, weak_build_output, strong_build_output, delta_summary | Belongs to SpecDocument | Requires two Quest Mode runs (before/after) [^2] | Created after both Quest Mode builds complete |


***

## 14. API Specification

**Assumption**: MVP is local-first with no server/network dependency, so this section describes a local **module interface** rather than a networked REST API, since no backend was specified in source docs.[^2]


| Function | Purpose | Request | Response | Auth | Validation | Errors |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `load_spec(path)` | Load and validate a requirements.md file [^1] | File path/text | Parsed SpecDocument object | N/A (local) | UTF-8 encoding check | `InvalidEncodingError` |
| `run_analysis(spec_document)` | Execute Rule Engine checks [^2] | SpecDocument | List of Findings | N/A | N/A | `ScanTimeoutError` if >10s on 20-req file [^1] |
| `generate_rewrite(finding)` | Suggest EARS-compliant rewrite | Finding | Rewrite suggestion | N/A | Rewrite validated against EARS grammar [^3] | `RewriteValidationError` |
| `compute_score(spec_document)` | Calculate Quest Readiness Score | SpecDocument + Findings | Score (0-100) + tier | N/A | N/A | N/A |
| `generate_report(spec_document)` | Output Markdown Quality Report [^1] | SpecDocument | Markdown file + stdout summary + exit code | N/A | N/A | N/A |

If a web UI wrapper requires HTTP endpoints (e.g., local Flask/FastAPI server for the browser UI), these functions should be exposed as thin local REST wrappers — exact framework choice deferred to Section 21.

***

## 15. State Management

| State | Behavior |
| :-- | :-- |
| Loading | Progress indicator during scans of larger files only [^1] |
| Success | Findings/score/rewrite displayed immediately, no page reload |
| Failure | Inline error messages (invalid file, failed rewrite validation) |
| Caching | **Assumption**: In-memory session cache only; no persistence across app restarts for MVP |
| Offline | Fully offline by design — no network calls required [^2] |
| Synchronization | N/A — single local session, no multi-device sync |
| Optimistic updates | Rewrite acceptance can update score display optimistically before full re-validation completes, then reconcile |


***

## 16. Edge Cases

| Case | Handling |
| :-- | :-- |
| Network failures | N/A for core linter (offline); relevant only if Quest Mode API calls fail — retry or show clear error |
| Timeouts | Scan exceeding 10s on standard file size should surface a warning, not silently hang [^1] |
| Invalid input | Non-UTF-8 or empty file rejected with clear message [^1] |
| Duplicate actions | Re-running analysis on unchanged spec should be idempotent (no duplicate findings) |
| Permissions | N/A (no auth/multi-user model in MVP) |
| Expired sessions | N/A (no session/auth system in MVP) |
| Large datasets | Files well beyond ~20 requirements should still show progress indicator and not silently fail [^1] |
| No data | Empty Spec Inbox shows encouraging empty state, not a broken screen |
| Slow devices | Not addressed in source docs — **assumption**: acceptable given lightweight stdlib-only Python engine [^2] |
| Thesis-level/untestable requirements | Tool SHALL refuse to proceed to Design phase and request rewrite [^3] |
| Only happy-path requirements present | Tool SHALL prompt for "Unwanted Behavior" (IF-THEN) criteria [^1] |


***

## 17. Risks

| Category | Risk |
| :-- | :-- |
| Technical | Ambiguity-detection accuracy (77% F-score target) may not generalize across varied writing styles [^1] |
| Business | Hackathon judging rewards "impact/reach," which depends on marketing execution, not just product quality [file:456 from prior context] |
| Legal | None identified — local-first tool, no data collection |
| Privacy | Low risk given no network dependency [^2] |
| Security | Low risk given no auth/backend surface [^2] |
| Operational | Single point of failure in demo: if the "before/after" Quest Mode run fails, the core demo narrative breaks |
| User adoption | BAs may perceive gamification as gimmicky if not executed with restraint — explicit constraint against childish mechanics [^2] |
| Unknown assumptions | Scoring formula, mission-completion logic, and export format are undefined in source docs (see Section 26) |


***

## 18. MVP Definition

**Must Have**

- Loader/Parser/Rule Engine/Evaluator/Reporter pipeline[^2]
- Spec Inbox, Analyzer, EARS Coach, Quest Readiness Score, Impact View screens
- Core ambiguity rules (vague verbs/adjectives, passive voice, escape clauses, EARS grammar/singularity)[^3]
- Before/after Quest Mode demo capability[^2]

**Should Have**

- Missions/gamification layer (simplified)
- Markdown Quality Report export[^1]

**Could Have**

- Tacit knowledge / "dark matter" detection (abductive reasoning)[^3][^1]
- Interactive two-option Clarification Queue[^3]
- Refinement Streak tracking

**Won't Have (for MVP)**

- Multi-user accounts/authentication
- Chat-transcript ingestion for "silent intent"  (explicitly listed as an Open Question, feasibility uncertain for hackathon scope)[^1]
- Enterprise RM tool integration (e.g., IBM DOORS)  — explicit Non-Goal[^1]

**Why**: The hackathon scope demands a working, demoable core loop over broad feature coverage; abductive reasoning and interactive dialogue systems are high-complexity, high-uncertainty features better deferred past MVP.[^3][^1]

***

## 19. Acceptance Criteria

| Feature | Given | When | Then | Measurable Success |
| :-- | :-- | :-- | :-- | :-- |
| EARS keyword validation | A requirements.md with lowercase keywords | User runs a scan | System rejects file and lists required uppercase keywords [^1] | 100% of lowercase keyword instances flagged |
| Vague adjective detection | A requirement contains "user-friendly" | Scan runs | Line flagged as "unverifiable" with suggested measurable threshold [^1] | ≥77% F-score on ambiguous word detection [^1] |
| Happy-path-only detection | A feature description has only nominal scenarios | Scan runs | System prompts for IF-THEN "Unwanted Behavior" criteria [^1] | 100% of happy-path-only docs trigger prompt |
| Scan performance | A ~20-requirement file | Scan runs | Completes within 10 seconds [^1] | Measured scan duration ≤10s |
| Oblique symbol detection | A line uses "symbol/sign" | Scan runs | Line flagged for referential ambiguity [^1] | 100% of oblique-symbol lines flagged |


***

## 20. Testing Strategy

- **Unit tests**: Each Rule Engine check (vague verb, passive voice, EARS grammar, etc.) tested against known positive/negative examples.
- **Integration tests**: Full Loader → Parser → Rule Engine → Evaluator → Reporter pipeline against sample requirements.md files.
- **UI tests**: Six-screen flow (Spec Inbox → Impact View) tested for navigation integrity and state persistence within a session.
- **Accessibility tests**: Keyboard navigation and screen-reader labeling checks on all interactive elements.
- **Performance tests**: Verify 10-second scan target on ~20-requirement files.[^1]
- **Manual QA checklist**: Run the full before/after Quest Mode demo end-to-end at least twice before any public demo, given it's the single highest-stakes deliverable.

***

## 21. Technical Architecture

| Layer | Recommendation | Justification |
| :-- | :-- | :-- |
| Core engine | Python 3.11+, stdlib-only [^2] | Already decided in design.md; keeps engine dependency-free and portable [^2] |
| Frontend | Lightweight HTML/CSS/JS or a minimal framework (assumption: vanilla or lightweight framework, not a heavy SPA stack) | Matches "lightweight, easy to run" constraint [^2] |
| Backend | Thin local server wrapper only if the web UI needs to call the Python engine (assumption: Flask/FastAPI, minimal) | No server was originally planned for the CLI [^2]; a minimal local server is the smallest addition needed to bridge UI and engine |
| Database | None — file-based, in-memory session state [^2] | Explicit non-goal: no database [^2] |
| Authentication | None | Local-first, single-user tool |
| Hosting | Local execution only (run via Qoder) [^2] | Demo positioning is Qoder-run, not cloud-hosted [^2] |
| Storage | Local filesystem (.md files) | Matches input/output contract [^1] |
| Messaging | N/A | No async/queue needs for MVP |
| Monitoring/Logging | Stdout summary + exit codes [^1] | Already specified in design.md |
| CI/CD | **Assumption**: Not required for hackathon MVP; manual run/demo sufficient |  |


***

## 22. AI Agent Implementation Plan

| Phase | Goal | Deliverables | Dependencies | Complexity | Suggested Agent |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1. Repository setup | Confirm/preserve existing structure | Verified `src/linter/`, `specs/`, `.kiro/`, `.cursor/` mirrors intact [^2] | None | Low | Qoder Quest Mode |
| 2. Core linter engine | Implement 5-stage pipeline | Loader, Parser, Rule Engine, Evaluator, Reporter modules [^2] | Phase 1 | Medium | Qoder Quest Mode |
| 3. Web UI scaffold | Build six screens | Spec Inbox, Analyzer, EARS Coach, Score, Missions, Impact View [^2] | Phase 2 (engine must exist to wire to UI) | Medium-High | Qoder Quest Mode / Codex |
| 4. Gamification layer | Add scoring tiers, missions, streak | Quest Readiness tiers, Mission logic, basic streak tracking | Phase 3 | Medium | Codex |
| 5. Demo integration | Wire before/after Quest Mode comparison | Impact View functional end-to-end [^2] | Phases 2-4 | Medium | Qoder Quest Mode |
| 6. Testing \& polish | Run test suite, fix bugs, finalize demo | Passing tests, rehearsed demo flow | Phase 5 | Low-Medium | Codex |


***

## 23. AI Coding Instructions (AGENTS.md)

```markdown
# AGENTS.md — ClarityGate

## Project Goals
- Preserve existing repo structure and source-of-truth files: SKILL.md, specs/claritygate-mvp/requirements.md, specs/claritygate-mvp/design.md.
- Do not restart from scratch. Do not reduce scope back to "just a CLI linter."
- Keep Qoder positioned as the primary build/orchestration engine, not a competitor.

## Coding Standards
- Python 3.11+, stdlib-only for the linter engine (no external dependencies).
- Follow EARS grammar rules literally when generating or validating requirement text: keywords UPPERCASE, one SHALL per requirement.

## Folder Conventions
- src/linter/ — core engine only.
- specs/claritygate-mvp/ — canonical spec files.
- .kiro/specs/claritygate-mvp/ — byte-identical mirror of specs/.
- .cursor/rules/claritygate.mdc — Cursor-compatible rule adapter.
- Do not scatter duplicate requirement files in other locations.

## Naming Conventions
- Modules named by pipeline stage: loader.py, parser.py, rule_engine.py, evaluator.py, reporter.py.

## Testing Expectations
- Unit test each Rule Engine check independently.
- Integration test the full pipeline against sample requirements.md fixtures.

## Commit Message Format
- Assumption: conventional commits (feat:, fix:, docs:, test:) — not specified in source docs.

## Definition of Done
- Feature passes unit + integration tests.
- Mirrors (.kiro/, .cursor/) stay in sync with specs/ when specs change.
- No implementation-language leakage into requirements.md (e.g., no "shall use SQL").

## Preferred Libraries
- None beyond Python stdlib for the core engine [file:435].

## Commands
- Build: (assumption) `python -m linter.claritygate <path-to-requirements.md>` [file:430]
- Test: (assumption) `pytest`
- Lint: (assumption) not yet defined — recommend flake8/ruff for MVP

## Known Constraints
- No backend, no database, no network dependency for the core engine [file:435].
- Web UI must remain lightweight and easy to run locally.
```


***

## 24. Product Design Review Checklist

- [ ] Is the six-screen flow intuitive without onboarding instructions?
- [ ] Is navigation simple enough for a time-pressured BA to use without training?
- [ ] Are empty states encouraging rather than discouraging?
- [ ] Are accessibility requirements (contrast, keyboard nav, screen reader labels) met?
- [ ] Are there unnecessary screens that could be merged (e.g., Missions into Score)?
- [ ] Can the paste → analyze → rewrite → score loop be simplified further?
- [ ] Is the gamification restrained enough to feel professional, not childish?[^2]
- [ ] Is the before/after Impact View comparison clear and convincing without narration?
- [ ] Are severity levels distinguishable without relying solely on color?

***

## 25. Codex Handoff Checklist

- [ ] Repository structure confirmed intact (`src/`, `specs/`, `.kiro/`, `.cursor/`)[^2]
- [ ] Architecture documented (5-stage pipeline: Loader → Parser → Rule Engine → Evaluator → Reporter)[^2]
- [ ] Components identified (six UI screens + core engine modules)
- [ ] APIs documented (local module interface, Section 14)
- [ ] Database — N/A, explicitly out of scope[^2]
- [ ] Acceptance criteria complete (Section 19, sourced from requirements.md)[^1]
- [ ] Edge cases covered (Section 16)
- [ ] Test plan included (Section 20)
- [ ] Remaining questions listed (Section 26)

***

## 26. Open Questions

- Should ClarityGate automatically rewrite the file or only provide suggestions in a separate queue?[^1]
- How should the tool handle "Complex" EARS patterns exceeding two keywords?[^1]
- Is project chat transcript access feasible for finding "silent intent" in a hackathon setting?[^1]
- What is the exact Quest Readiness Score formula (weighting per finding severity)? **Not defined in any source document — pure assumption used in Section 9.**
- Is a local server (Flask/FastAPI) required to bridge the Python engine to a browser UI, or will the UI be a separate static mockup for demo purposes only? **Not decided.**
- Should Missions have explicit "completion" tracking (checkbox) or auto-detect completion from rewrite/score state? **Assumed auto-detect, unconfirmed.**
- Is multi-session persistence (saving a spec across app restarts) needed, or is single-session-only acceptable for MVP? **Assumed single-session only.**
- What export format is expected for the cleaned spec (Markdown file, clipboard copy, direct Quest Mode handoff)? **Not specified.**

***

## Executive Handoff Summary (for another AI agent)

ClarityGate is a local-first, Python stdlib-only requirements-quality linter wrapped in a lightweight six-screen web UI (Spec Inbox, Analyzer, EARS Coach, Quest Readiness Score, Missions, Impact View), built for the Alibaba Cloud x Qoder Hackathon. It detects ambiguous/vague/untestable requirements using rules already defined in SKILL.md (vague verbs, vague adjectives, passive voice, escape clauses, pronoun antecedents, oblique symbols, EARS grammar/singularity violations) and teaches users to rewrite them into EARS format (WHEN/WHILE/WHERE/IF...THE SYSTEM SHALL...). The engine follows a 5-stage pipeline: Loader → Parser → Rule Engine → Evaluator → Reporter, with no backend, database, or network dependency. The MVP must preserve the existing repo structure exactly (`src/linter/`, `specs/claritygate-mvp/`, `.kiro/` mirror, `.cursor/rules/`) and must not be reduced back to a plain CLI tool — the differentiator is the gamified UI and the before/after Qoder Quest Mode demo proving that a cleaned spec produces measurably better AI-generated code. Critical unresolved items before implementation: the exact Quest Readiness Score formula, whether a local server is needed for the UI-to-engine bridge, and the scope of the interactive Clarification Queue (deferred to post-MVP). All assumptions made in this document are explicitly marked and should be confirmed with stakeholders before Codex/Qoder begins Phase 2 of the implementation plan.

<div align="center">⁂</div>

[^1]: requirements.md

[^2]: ClarityGate-v1.md

[^3]: skill.md

