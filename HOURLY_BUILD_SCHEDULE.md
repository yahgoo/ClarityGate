# ClarityGate Option 2 — Hour-by-Hour Build Schedule
**Starting: Monday, July 27, 2026, 11:18 AM +08**
**Note: Blackout constraint overridden per explicit decision. Coding continues after 22:01 tonight and through the originally-planned blackout window (Jul 28-30).**

## Day 1 — Monday, Jul 27

| Time | Mode | Task | Deliverable |
|---|---|---|---|
| 11:18 AM - 12:00 PM | Qoder attended | Review this PLAN.md + ARCHITECTURE.md, confirm scope with Qoder, lock file tree | Shared understanding, no code yet |
| 12:00 PM - 1:00 PM | Qoder attended | Phase 1 start: scaffold `backend/` FastAPI skeleton, SQLite schema, models.py | `backend/app/main.py` boots, empty DB created |
| 1:00 PM - 2:00 PM | Qoder attended | Phase 1 continue: seed script (load ambiguous sample), model unit tests | Seed data loads, `pytest backend/tests/test_models.py` passes |
| 2:00 PM - 3:00 PM | Qoder attended | Phase 1 checkpoint: verify DB initializes from scratch cleanly, run core 36/36 to confirm untouched | Phase 1 acceptance criteria met |
| 3:00 PM - 4:00 PM | Qoder attended | Phase 2 start: `linter_adapter.py` — wrap src/linter/ calls | Adapter returns Finding/Score objects matching CLI output |
| 4:00 PM - 5:00 PM | Qoder attended | Phase 2: implement POST /api/specs, GET /api/specs/{id} | Routes tested via curl/pytest |
| 5:00 PM - 6:00 PM | Qoder attended | Phase 2: implement POST /api/specs/{id}/analyze | Analyze route persists findings + score correctly |
| 6:00 PM - 7:00 PM | Break / dinner | — | — |
| 7:00 PM - 8:00 PM | Qoder attended | Phase 2: implement rewrite/accept/report/impact routes | All 7 routes complete |
| 8:00 PM - 9:00 PM | Qoder attended | Phase 2 checkpoint: integration test — backend output matches CLI output exactly for both sample specs | Contract invariant test passes |
| 9:00 PM - 10:00 PM | Qoder attended | Write handover notes for overnight run; review Daytona/saturation review status if not yet done | Clear scheduled-task prompt drafted |
| 10:00 PM - 10:01 PM | — | Switch to Experts Mode, queue scheduled task | Task card confirmed, "Keep system awake" enabled |
| 10:01 PM onward | Qoder Experts Mode, unattended (Qwen3-Max-Preview, off-peak) | Phase 3: scaffold React frontend, build ImportStep, ReviewStep components wired to live backend | Components render with real API data |

## Day 2 — Tuesday, Jul 28 (was blackout, now coding day)

| Time | Mode | Task | Deliverable |
|---|---|---|---|
| Morning (review overnight output) | Qoder attended | Review Phase 3 overnight progress, fix any bugs, continue ResolveStep + ReadyStep | Full 4-step flow renders |
| Midday | Qoder attended | Wire ScorePanel + MissionsPanel to live score updates | Score updates in real time as findings are resolved |
| Afternoon | Qoder attended | Phase 3 checkpoint: full paste→analyze→resolve→ready loop works in browser with real data | Phase 3 acceptance criteria met |
| Evening | Qoder attended | Begin Phase 4: README updates, one-command start scripts for backend + frontend | `./start-backend.sh`, `./start-frontend.sh` work |
| After 10:01 PM | Qoder Experts Mode, unattended | Phase 4: Playwright E2E smoke test authoring, run twice against sample spec | E2E test passes twice |

## Day 3 — Wednesday, Jul 29

| Time | Mode | Task | Deliverable |
|---|---|---|---|
| Morning | Qoder attended | Review E2E test results, fix any flakiness, polish visual states (loading, error, success) | UI feels finished, not placeholder-y |
| Midday | Qoder attended | Cross-check: does UI-driven analysis match CLI output exactly? Re-run contract invariant test | No drift between UI and CLI results |
| Afternoon | Qoder attended | Narrow-viewport/responsive check, accessibility pass (labels, contrast) | Works on desktop + narrow viewport |
| Evening | Qoder attended | Prepare demo data/report output for video recording | Demo-ready dataset confirmed |
| After 10:01 PM | Qoder Experts Mode, unattended | Buffer/catch-up time for any Phase 3/4 issues; if ahead of schedule, begin demo video script draft | App fully stable, ready for rehearsal |

## Day 4 — Thursday, Jul 30

| Time | Mode | Task | Deliverable |
|---|---|---|---|
| Morning | Qoder attended | Full regression: core 36/36, backend pytest, E2E Playwright — all three suites green in one sitting | Full green build confirmed |
| Midday | Qoder attended | Rehearse demo using the REAL app (not just CLI) — paste weak spec live, resolve findings live, show score climb | Live demo rehearsed once successfully |
| Afternoon | Qoder attended | Decide: primary demo = live app walkthrough, CLI = backup if live demo has any risk | Demo strategy locked |
| Evening | Buffer | Catch up on WorkBuddy saturation review if not yet done (still an open item from Jul 26 night) | Saturation review complete |

## Day 5 onward — Jul 31 through Aug 4 (compressed submission target)

| Day | Focus |
|---|---|
| Jul 31 | Full rehearsal of both live-app demo and CLI backup, timed under 4 minutes |
| Aug 1 | Record final demo video (live app primary, CLI backup ready) |
| Aug 2 | Buffer/fix day if recording reveals issues |
| Aug 3 | Publish social post, finalize README/docs sync |
| Aug 4 | Final check, submit demo video + social post links via submission form |
| Aug 5 | Buffer day (official deadline, held in reserve) |

## Critical checkpoints — do not skip

1. **After Phase 1**: core 36/36 still passing — if not, STOP, do not proceed to Phase 2.
2. **After Phase 2**: contract invariant test (backend output == CLI output) — if this fails, the app is not trustworthy for a demo, fix before Phase 3.
3. **After Phase 3**: full paste→analyze→resolve→ready loop in browser twice, same score as CLI — if not, do not present the UI as primary demo.
4. **Before Aug 1 recording**: all three test suites green simultaneously (core unittest, backend pytest, frontend Playwright).

## Fallback preserved at every stage

At no point does this plan delete or disable the CLI or the static `demo-ui/index.html`. If the full-stack build stalls at any checkpoint above, you can fall back to the CLI + static shell demo immediately with zero lost time, since neither is touched by this build.
