# 1. Unified Status Snapshot

| Workstream | Status | Notes |
|---|---|---|
| ClarityGate core linter | Frozen | Complete, `36/36` tests passing, no scope drift, do not modify unless tests fail |
| ClarityGate demo/UI | Not started | Option 2 "Guided Gate" UI remains useful, but should be thin and demo-only if attempted |
| ClarityGate submission assets | In progress | README/docs/samples frozen; checklist, demo script, and social draft created; video/social/submission still pending; personal submission target is Aug 4, while the official hackathon deadline remains Aug 5 |
| Oxylabs scraping | Not started | Scope: deny-list expansion and scraping test cases for distillation pipeline |
| Daytona sandbox setup | Not started | Scope: run 5-coach Grill Mode prompts in parallel against test cases |
| Grill Mode 5-coach prompts | In progress / needs finalization | Need final prompt set before Daytona parallel runs |
| Distillation test cases | Not started | Need compact test cases for saturation review and coach-output comparison |

# 2. Time-Boxed Plan

## Today, Daytime (Qoder attended/interactive)

| Workstream | Objective | Exact deliverables | Tool | Success check |
|---|---|---|---|---|
| ClarityGate | Protect frozen core and prepare demo path | Finalize before/after demo spec pair, confirm demo script commands, update `PROGRESS.md` if Qoder changes anything | Qoder attended | `python3 -m unittest -v` stays `36/36`; ambiguous sample exits `2`; clean sample exits `0` |
| WorkBuddy | Prepare inputs for unattended work | Finalize 5 Grill Mode lens prompts; define 5-10 distillation test cases; draft Oxylabs scrape targets and deny-list fields | Qoder attended | Prompt set and test-case file are ready for batch execution |

## Today, After 22:01 (Qoder Experts Mode unattended)

| Workstream | Objective | Exact deliverables | Tool | Success check |
|---|---|---|---|---|
| ClarityGate | Optional thin demo wrapper only if you choose UI | Either no-code release audit, or a thin static Option 2 Guided Gate shell that displays existing sample/report outputs without changing core linter | Qoder Experts Mode unattended | Core tests still `36/36`; no core implementation files modified; UI, if built, is clearly separate and demo-only |
| WorkBuddy | Run heavier parallel batch work | Oxylabs scraping task for deny-list/test-case enrichment; Daytona sandbox task to run 5-coach prompts against selected distillation cases | Qoder Experts Mode unattended | Scraped outputs are saved; sandbox run logs exist; no manual clarification needed overnight |

## Remaining Days Before Seminar Blackout

| Workstream | Objective | Exact deliverables | Tool | Success check |
|---|---|---|---|---|
| ClarityGate | Convert stable build into submission material | Record or rehearse 2-3 minute demo; polish social post; keep implementation frozen | Qoder attended + Codex review | Demo can be recorded without new code; social draft has required tags |
| WorkBuddy | Review saturation and refine prompts | Compare 5-coach outputs, identify overlap/gaps, revise lens prompts once, finalize distilled findings | Qoder attended | Each coach lens contributes distinct value; test-case coverage is documented |

## Seminar Blackout (No Coding)

| Workstream | Objective | Exact deliverables | Tool | Success check |
|---|---|---|---|---|
| ClarityGate | Preserve state | No coding; only review notes if needed | None / light Codex planning | No repo changes |
| WorkBuddy | Preserve state | No coding; only read logs or jot review notes if time allows | None / light Codex planning | No repo changes |

## After Blackout Through Submission

| Workstream | Objective | Exact deliverables | Tool | Success check |
|---|---|---|---|---|
| Aug 3 submission rehearsal | Full rehearsal and final video attempt | 3x run-through of demo script, under 4 minutes each; record the final demo video the same day if rehearsal goes well. Compressed schedule — if rehearsal on Aug 3 reveals issues, Aug 4 becomes the fallback recording day, and Aug 5 remains available as final emergency buffer before the actual Aug 5 deadline. | Qoder only for bounded docs fixes | Three run-throughs are under 4 minutes; final demo video is recorded or fallback recording is explicitly activated for Aug 4 |
| Aug 4 personal submission target | Final check and submit | Final check; sync `specs/` and `.kiro` mirrors; publish social post; submit demo video link and social post URL via the submission form | Qoder only for bounded docs fixes | Personal submission is complete on Aug 4; final tests pass; official deadline remains Aug 5 |
| Aug 5 buffer / official deadline | Buffer day reserved for second hackathon project | Not part of the ClarityGate/WorkBuddy critical path; keep available only as final emergency buffer before the actual Aug 5 hackathon deadline | None unless emergency | Aug 5 is labeled as the actual unchanged hackathon deadline, not the personal target |
| WorkBuddy | Package distillation results | Final lens prompts, scrape/test-case summary, Daytona run summary | Qoder attended | Outputs are organized enough to reuse or present separately |

# 3. Single Progress Tracker Table

| Workstream | Status | Next action | Blockers | Done when |
|---|---|---|---|---|
| ClarityGate core linter | Frozen | Do not touch unless tests fail | None | `36/36` tests pass and CLI demo works |
| ClarityGate demo samples | Frozen | Ready for rehearsal/video | None | Ambiguous exits `2`, clean exits `0`; exit codes verified via Experts Mode practice run, 2026-07-26 |
| ClarityGate demo script | Done | Rehearse once aloud | Recording not done | Fits under 4 minutes for the Aug 3 full rehearsal |
| ClarityGate submission assets | In progress | Record video and publish social post | Missing video/social links | Submission form completed by the Aug 4 personal target; official deadline remains Aug 5 |
| ClarityGate UI/product shell | Optional / not started | Decide whether to build thin static shell | Risk of destabilizing schedule | Demo-only wrapper exists or is explicitly deferred |
| Oxylabs scraping | Done | Merge TC11-TC20 into saturation review | None | 4/4 queries succeeded; 31 organic results scraped; 30 new deny-list terms extracted; 10 new test cases generated; outputs saved under `output/` |
| Daytona sandbox setup | Done | Use saved results for review/submission evidence | None | Daytona batch completed: 50/50 evaluations succeeded, 0 duplicates, all coaches and test cases present; results saved at `output/daytona_grillmode_results.json` |
| Grill Mode 5-coach prompts | Done | Freeze prompt pack for Daytona/submission reuse | None | Five coach prompts validated through Daytona batch run |
| Distillation test cases | Done | Run full 20-TC saturation review, starting with verifying TC19's Coach 5 flag | None | TC01-TC20 are available for coach-output comparison; combined results saved at `output/daytona_grillmode_results_all20.json`; 100/100 evaluations completed with 0 unresolved errors |
| Unified tracking | Active | Keep updating `PROGRESS.md` for ClarityGate and separate WorkBuddy tracker if repo differs | Separate repos may fragment status | Latest status is visible before each Qoder run |

# 4. Qoder Prompt Queue

1. [WorkBuddy] Grill Mode 5-coach prompt finalization prompt
2. [WorkBuddy] Distillation test-case creation prompt
3. [WorkBuddy] Oxylabs scraper prompt
4. [WorkBuddy] Daytona sandbox parallel-run prompt
5. [ClarityGate] Before/after demo spec finalization prompt
6. [ClarityGate] Final no-code release audit prompt
7. [ClarityGate] Optional thin Option 2 UI shell prompt
8. [ClarityGate] Demo video rehearsal/package prompt
9. [WorkBuddy] Saturation review and prompt refinement prompt

# 5. Fastest Safe Path

If time gets tight, do not build the ClarityGate UI. Defer the Option 2 shell unless the core submission assets are already done.

Non-deferrable:
- ClarityGate final verification
- ClarityGate demo video
- ClarityGate social post
- ClarityGate submission form
- WorkBuddy 5-coach prompt finalization if WorkBuddy is still a required parallel deliverable

Safe to defer:
- ClarityGate UI/product shell
- Any backend/database/cloud work
- Advanced Oxylabs scraping beyond the minimum useful deny-list/test-case expansion
- Daytona reruns after the first usable saturation batch
- WorkBuddy polish if ClarityGate submission assets are not yet complete

Smallest strong ClarityGate path:
- CLI demo only, using ambiguous vs clean sample specs.
- Show `REFUSED 0/100` versus `CERTIFIED 100/100`.
- Explain Qoder built the linter through scoped Quest Mode batches.

Smallest useful WorkBuddy path:
- Final 5 coach prompts.
- 5 representative test cases.
- One Daytona parallel run.
- One saturation review summary.

# 6. Today's Next 3 Actions

1. Run Qoder attended on WorkBuddy prompt finalization: lock the 5 Grill Mode coach lenses and output format.

2. Run Qoder attended on WorkBuddy distillation test cases: create 5-10 compact cases for Daytona/Oxylabs use.

3. Rehearse the ClarityGate CLI demo once using the frozen samples and decide whether tonight's ClarityGate Qoder run is "release audit only" or "optional thin UI shell."
