# Qoder Experts Mode Execution Strategy for ClarityGate

## Scope and safety boundary

This answer is **planning and workflow strategy only**. It does **not** assume that `PLAN2.md` has been approved. It also does **not** authorize full-stack implementation.

For ClarityGate, the controlling facts are:

- The deterministic CLI linter is complete and frozen.
- `src/linter/**` and the existing test/sample/spec paths are protected.
- `PLAN.md` is still the accepted implementation boundary.
- `PLAN2.md` is only a proposed full-stack expansion.
- There is currently no `.git` directory, so Git-based rollback and branch protection are unavailable unless you create them.
- The existing CLI must remain the fallback and the source of deterministic truth.

Because you asked for exact official Qoder documentation citations for every product-behavior claim, I must be explicit:

> I cannot verify official Qoder documentation pages from this session, and I will not invent Qoder settings, labels, or documentation URLs.  
> Therefore, every Qoder product-behavior statement below is marked:  
> **UNVERIFIED — confirm in the installed Qoder version.**  
> Recommended practice is separated from product-behavior claims.

If you want a citation-backed version, the safest path is to open the official Qoder documentation for your exact Qoder version and verify each item in the UI before execution.

---

# 1. Plan approval mechanics

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Does Experts Mode always pause after generating its plan?

**Do not assume it always pauses.**

For a protected project like ClarityGate, you should assume that execution may begin automatically unless you have confirmed that a plan-approval gate is enabled in your Qoder version.

Recommended practice:

- Require a planning-only response first.
- Explicitly forbid file modification, dependency installation, test execution that writes artifacts, server startup, and expert delegation for implementation.
- Require the Lead Agent to stop and wait for a named approval phrase.

### What exact control or interface action approves the plan?

I cannot give an exact control label without risking invention.

You should look for a control in your Qoder UI with meaning equivalent to:

- Approve plan
- Continue
- Run
- Execute
- Accept proposed changes
- Authorize agent actions

The exact label must be confirmed in your installed Qoder version.

Recommended practice:

Even if Qoder has a graphical approve button, also use explicit textual approval wording in the conversation, such as:

> `PLAN APPROVED FOR PHASE 0 ONLY.`

This creates an unambiguous conversational gate.

### Can execution begin automatically?

**Possibly.**

Treat automatic execution as possible until you verify otherwise.

Recommended practice:

Assume execution can begin automatically if:

- auto-run is enabled,
- command approval is disabled,
- plan approval is not required,
- the agent has workspace write permission,
- the prompt does not explicitly forbid execution.

For ClarityGate, that is too risky unless the protected paths are externally protected.

### What exact setting disables auto-execution?

I cannot provide an exact setting name without risking invention.

Look for settings with meanings like:

- require approval before execution,
- disable auto-run,
- confirm before file edits,
- approve terminal commands,
- planning-only mode,
- agent autonomy level,
- workspace permission mode.

The exact setting name must be confirmed in your Qoder version.

Recommended practice:

Before any ClarityGate expansion work, verify and enable every available setting that means:

1. Show a plan before execution.
2. Require approval before file writes.
3. Require approval before terminal commands.
4. Require approval before dependency installation.
5. Require approval before starting servers or browsers.

### If the setting varies by Qoder Desktop, IDE plugin, or CLI, explain each relevant workflow separately

All of the following are **UNVERIFIED — confirm in the installed Qoder version**.

#### Qoder Desktop

Likely has graphical settings and a chat/task panel. You should look for plan approval, auto-run, command approval, and workspace permission controls in the application settings or task view.

#### IDE plugin

Likely has settings inside the IDE preferences or plugin sidebar. You should look for agent execution controls, file-edit approval, and terminal-command approval.

#### CLI

Likely uses flags, environment variables, or config files. You should look for options that control autonomy, approval, sandboxing, allowed paths, and command execution.

Do not rely on any of these until verified.

### Can I require “show the final plan and wait for explicit approval” reliably?

Only if both of these are true:

1. Qoder has an enforced approval setting, and
2. the agent actually obeys the conversational stop instruction.

Without verification, treat this as **not reliably enforced**.

Recommended practice:

Use three layers:

1. UI setting: require approval before execution, if available.
2. Prompt instruction: planning-only, no writes, wait for approval.
3. External protection: Git baseline, SHA-256 manifest, read-only file permissions, or sandboxing.

For ClarityGate, the external protection layer is the most important.

---

# 2. Expert scheduling

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Are Researcher, Full-Stack Engineer, QA, Code Reviewer, UI Operator, and Debug Engineer guaranteed to run?

Do not assume that every named expert is guaranteed to run.

In multi-agent systems, expert selection is often dynamic. The Lead Agent may choose which experts to invoke based on the task, context, cost, or internal planning logic.

Recommended practice:

Explicitly request required experts, but do not rely on that request as a hard guarantee.

For ClarityGate, the useful roles are:

- Researcher: inspect the frozen core API and produce integration notes.
- Backend Engineer: implement only under `backend/**`.
- Frontend Engineer: implement only under `frontend/**`.
- QA: run tests and produce gate reports.
- Code Reviewer: read-only review.
- UI Operator: browser validation only.
- Debug Engineer: invoked only when a gate fails.

### Can the user explicitly require or exclude a built-in expert?

Possibly, but this is **UNVERIFIED**.

Recommended practice:

State required and excluded experts in the prompt.

Example instruction:

> Required experts for this phase: Researcher, Backend Engineer, QA, Code Reviewer.  
> Do not invoke UI Operator in this phase.  
> Do not allow Debug Engineer to modify protected paths.

But again, treat this as a prompt-level instruction unless Qoder provides verified expert-selection controls.

### Can responsibilities be assigned to particular experts in the main prompt?

Yes, as a prompt instruction.

However, whether the Lead Agent honors the assignment exactly is **UNVERIFIED**.

Recommended practice:

Provide an explicit role table:

| Role | Allowed responsibility | Allowed writable paths |
|---|---|---|
| Researcher | Read core, summarize API | none |
| Backend Engineer | Backend wrapper only | `backend/**` |
| Frontend Engineer | Frontend only | `frontend/**` |
| QA | Test execution and reports | test/report paths only |
| Code Reviewer | Read-only review | none |
| UI Operator | Browser validation | browser evidence/report paths only |

### Can the Lead Agent ignore or reinterpret those assignments?

Yes, it may be able to.

Treat the Lead Agent as capable of reinterpreting instructions unless Qoder has verified hard constraints.

Recommended practice:

Put the most important constraints in multiple places:

1. Main prompt.
2. Project rules or instructions, if Qoder supports them.
3. Phase-specific approval messages.
4. External verification, such as hash manifests and manual diff review.

### How can I inspect which expert performed each task?

Look for a Qoder activity view, timeline, agent trace, expert log, or diff attribution panel. The exact feature name is **UNVERIFIED**.

Recommended practice:

Require the Lead Agent to produce an attribution report after every phase:

> For each task, list the expert name, the action taken, the files touched, the commands run, and the result.

Do not rely on this report alone. Also inspect file changes externally.

---

# 3. Parallelism and dependency gates

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Does “parallel execution” mean every expert starts at once?

Do not assume that.

In most agent systems, parallelism means independent subtasks may run concurrently, not that every expert starts at once.

Recommended practice:

Define independence explicitly.

For ClarityGate, these can be parallel only after the contract is frozen:

- Backend implementation.
- Frontend implementation against a mocked frozen contract.
- QA test scaffolding.

These must not be parallel:

- Inspecting the core API.
- Freezing the backend contract.
- Implementing backend behavior.
- Running backend/core equivalence tests.
- Integrating the frontend against the real backend.

### Can the Lead Agent enforce this dependency order?

Desired order:

A. Inspect actual core API.  
B. Freeze backend data/API contract.  
C. Implement backend.  
D. Pass backend/core equivalence tests.  
E. Implement frontend.  
F. Pass browser E2E.

Whether the Lead Agent can technically enforce this is **UNVERIFIED**.

Recommended practice:

Do not rely on the Lead Agent alone. Use human approval gates between A/B, B/C, C/D, D/E, and E/F.

### Can a failed gate prevent dependent tasks from starting?

Possibly, if Qoder has gate enforcement. But this is **UNVERIFIED**.

Recommended practice:

Treat gates as human-approved checkpoints unless verified otherwise.

A gate should require:

1. A written gate report.
2. Test output evidence.
3. Protected-path hash verification.
4. Your explicit approval message before the next phase.

### What prompt structure produces real parallelism without letting frontend race ahead?

Use a contract-first, gate-based prompt structure.

Recommended pattern:

> Phase 1: Read-only research. Produce a core API survey.  
> Phase 2: Freeze the backend contract. Do not implement.  
> Phase 3: Implement backend only. Frontend integration is forbidden.  
> Phase 4: Run backend/core equivalence tests. If any fail, stop.  
> Phase 5: Implement frontend only against the frozen contract.  
> Phase 6: Run integration and browser E2E only after backend gate passes.

Add this explicit rule:

> Frontend work may begin against a mock of the frozen contract only after the contract is approved. Frontend work must not assume any backend behavior that is not written in the frozen contract. Frontend integration with the real backend is forbidden until the backend equivalence gate passes.

---

# 4. File ownership and collision handling

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### When multiple experts share a workspace, can they edit the same file concurrently?

Possibly.

Do not assume Qoder prevents concurrent edits.

Recommended practice:

Design the plan so that only one expert may write to a given path in a given phase.

For ClarityGate:

- Backend Engineer writes only under `backend/**`.
- Frontend Engineer writes only under `frontend/**`.
- QA writes only under approved test/report paths.
- Researcher and Code Reviewer write nothing.
- UI Operator writes only validation evidence or reports, if needed.

### How does Qoder resolve conflicting edits?

This is **UNVERIFIED**.

Do not rely on automatic conflict resolution.

Recommended practice:

Avoid conflicts by construction:

1. One writer per directory.
2. One writer per file.
3. Phase gates between writers.
4. External diff review after each phase.

### Can tasks be given exclusive path ownership?

You can request it in the prompt.

Whether Qoder enforces it is **UNVERIFIED**.

Recommended ownership model:

| Expert | Intended access |
|---|---|
| Researcher | read-only |
| Backend Engineer | write `backend/**` only |
| Frontend Engineer | write `frontend/**` only |
| QA | write only new test/report paths; run commands |
| Code Reviewer | read-only |
| UI Operator | browser validation only; no source writes |

### Is path ownership an enforced capability or only a prompt instruction?

Assume it is only a prompt instruction until verified.

For ClarityGate, that means path ownership is not sufficient protection for `src/linter/**`.

Recommended practice:

Use external protection:

- Git baseline.
- SHA-256 manifest.
- read-only file permissions.
- sandbox or container with protected paths mounted read-only.
- manual diff review after every phase.

---

# 5. Protection of `src/linter/`

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Can Qoder enforce a deny-write rule for `src/linter/**`?

Do not assume it can.

Treat any deny-write capability as **UNVERIFIED**.

Recommended practice:

Assume that any agent with workspace write access can modify `src/linter/**` unless the operating system, sandbox, or version-control process prevents it.

### Can built-in experts be made read-only?

Possibly, but **UNVERIFIED**.

Recommended practice:

Define read-only roles in the prompt, but do not rely on that alone.

Read-only roles:

- Researcher.
- Code Reviewer.
- UI Operator, except possibly for evidence/report artifacts.

### Can the Code Reviewer technically block or halt changes?

Possibly, but **UNVERIFIED**.

Recommended practice:

Treat Code Reviewer output as advisory unless Qoder has a verified blocking gate.

Require Code Reviewer to produce a clear verdict:

- `PASS`
- `FAIL`
- `BLOCKED`
- `PROTECTED PATH VIOLATION`

But the actual halt should be enforced by you or by an external gate.

### Can a QA or reviewer failure stop the Lead Agent from proceeding?

Possibly, if Qoder supports enforced gates. But this is **UNVERIFIED**.

Recommended practice:

Require the Lead Agent to stop on any QA or reviewer failure, but also verify externally.

### If Qoder lacks path-level enforcement, what is the strongest supported alternative?

The strongest practical alternative is layered external protection:

1. Create a Git baseline commit before any expansion work.
2. Tag the baseline.
3. Generate a SHA-256 manifest of all protected files.
4. Make protected files read-only at the filesystem level, if appropriate.
5. Run Qoder inside a sandbox or container where protected paths are mounted read-only.
6. After every phase, compare the new SHA-256 manifest to the baseline.
7. Do not approve the next phase if any protected hash changed.

This is recommended practice, not a confirmed Qoder feature.

---

# 6. Operating without Git

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Does Experts Mode require a Git repository for safe rollback or review?

Do not assume that Experts Mode requires Git.

However, safe rollback, branch isolation, and commit-based review are much weaker without Git.

Recommended practice:

Do not begin full-stack expansion without first creating a Git baseline.

### Which Qoder review, commit, worktree, or rollback features are unavailable without `.git`?

Any feature that depends on Git commits, branches, tags, worktrees, or Git diffs will be unavailable unless Qoder has its own non-Git snapshot system.

Whether Qoder has a non-Git snapshot or checkpoint system is **UNVERIFIED**.

Without `.git`, you should assume these are unavailable:

- Git commit history.
- Git branch isolation.
- Git worktrees.
- Git tag-based rollback.
- Git diff against a known baseline.
- Git stash.
- Git revert/reset.

Qoder may still show file diffs, but that is **UNVERIFIED**.

### Should I initialize Git and make a baseline commit before execution?

Yes.

Recommended practice:

Initialize Git before approving or executing any full-stack expansion.

This is useful even if `PLAN2.md` is never approved, because it preserves the verified CLI baseline.

### Safest exact preparation sequence

This is an operational sequence, not implementation code.

Before initializing Git:

1. Confirm that the current directory is the real project root.
2. Review all files for secrets, tokens, credentials, local database files, environment files, private keys, and proprietary data.
3. Review generated artifacts, caches, virtual environments, and dependency directories.
4. Decide what should be ignored by Git, such as:
   - Python caches,
   - virtual environments,
   - Node dependencies,
   - build output,
   - environment files,
   - local SQLite databases,
   - generated reports, if you do not want them committed.
5. Confirm that protected sample files and frozen specs are present and unmodified.
6. Confirm that the existing 36 unittest tests pass.
7. Confirm that the two sample baselines still produce the expected results:
   - ambiguous sample: 6 requirements, 23 findings, 21 defects, 2 clarifications, 0/100, REFUSED;
   - clean sample: 3 requirements, 0 findings, 100/100, CERTIFIED.

Then create the Git baseline:

1. Initialize a Git repository at the project root.
2. Add all intended baseline files.
3. Create a baseline commit with a message such as:
   - `ClarityGate deterministic CLI baseline`
4. Create a tag such as:
   - `claritygate-cli-baseline`
5. Create a protected-file manifest file, for example:
   - `manifests/protected-baseline.sha256`
6. Commit the manifest.
7. Optionally create a separate branch for proposed full-stack work, but only after `PLAN2.md` is approved.

Do not create the full-stack branch as an implicit approval. The branch is not approval.

### If Git is not used, can Qoder create and compare a SHA-256 manifest?

It may be possible to instruct Qoder to create and compare a manifest, but this is **UNVERIFIED**.

Recommended practice:

Do not rely on Qoder alone to police protected files.

Use a manifest process that you can inspect yourself.

The manifest should contain, for each protected file:

- relative path,
- SHA-256 digest.

Protected manifest targets should include at least:

- `src/linter/**`
- existing tests under `tests/**`
- `SKILL.md`
- `specs/claritygate-mvp/**`
- `.kiro/specs/claritygate-mvp/**`
- `data/samples/**`
- `demo-ui/index.html`

Before each phase:

1. Verify the manifest matches the working tree.
2. If any protected file differs, stop.

After each phase:

1. Regenerate the manifest.
2. Compare it to the baseline.
3. If any protected path changed, treat it as a stop condition.

---

# 7. Expert customization

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Where are “Additional Prompt,” model selection, Skills, and MCP settings configured?

I cannot give exact setting locations without risking invention.

Look in places such as:

- Qoder settings,
- project settings,
- expert configuration panel,
- agent mode settings,
- skills configuration,
- MCP server configuration,
- workspace rules,
- conversation-level instruction fields.

The exact location and scope must be confirmed in your installed Qoder version.

### Are these settings per project, per conversation, or global?

This is **UNVERIFIED**.

Recommended practice:

Assume that critical constraints must be repeated in:

1. The main prompt.
2. The project-level instructions, if available.
3. Each phase approval message.

Do not assume that an instruction given once will be permanently visible to every expert.

### Can I configure permanent instructions such as: “Never modify src/linter/**; report and halt if another expert does”?

You can and should write that instruction.

Whether it is permanent, inherited, and enforced is **UNVERIFIED**.

Recommended instruction text:

> Never create, modify, delete, move, rename, or overwrite any file under `src/linter/**`, existing `tests/**`, `SKILL.md`, `specs/claritygate-mvp/**`, `.kiro/specs/claritygate-mvp/**`, `data/samples/**`, or `demo-ui/index.html`.  
> If any requested task appears to require modifying those paths, stop immediately and report a protected-path violation.

### What limits apply to additional prompts?

Possible limits include:

- token length,
- priority relative to system instructions,
- conflict with other rules,
- context compression,
- expert-specific visibility,
- model-specific instruction following.

All of these are **UNVERIFIED**.

Recommended practice:

Keep critical rules short, repeated, and unambiguous.

### Does the Lead Agent inherit or see expert-specific additional prompts?

This is **UNVERIFIED**.

Recommended practice:

Assume the Lead Agent may not see every expert-specific instruction.

Therefore, put the most important constraints in the main prompt and in the phase approval message, not only in expert-specific settings.

---

# 8. Backend and frontend runtime

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Can Experts Mode install Python and npm dependencies?

Possibly, if terminal execution and dependency installation are permitted.

This is **UNVERIFIED**.

Recommended practice:

Require explicit approval before any dependency installation.

For ClarityGate, dependency installation should not happen until `PLAN2.md` is approved and the backend/frontend phase is explicitly authorized.

### How are dependency-install approvals handled?

Likely through terminal-command approval or agent-action approval, if available.

This is **UNVERIFIED**.

Recommended practice:

Require the agent to show:

- the exact package manager,
- the exact packages,
- the reason for each package,
- the target directory,
- the expected lockfile changes,

and then wait for approval.

### Can it keep FastAPI and Vite development servers running simultaneously?

Possibly, if Qoder supports background processes or multiple terminals.

This is **UNVERIFIED**.

Recommended practice:

Do not assume long-running servers are managed safely.

Specify:

- backend port,
- frontend port,
- health endpoints,
- startup timeout,
- shutdown procedure,
- process cleanup,
- log location.

For hackathon safety, use non-default ports to reduce collision risk, for example:

- backend: `8010`
- frontend: `5180`
- E2E backend: `8011`
- E2E frontend: `5181`

The exact ports should be decided during implementation planning.

### Can UI Operator access localhost services started by another expert?

Possibly, if the UI Operator and the servers share the same network namespace.

This is **UNVERIFIED**.

Recommended practice:

Verify this before relying on browser E2E.

If Qoder runs agents in separate containers, `localhost` may not mean the same machine. You may need a service name or explicit host configuration. Confirm this in the installed environment.

### Can UI Operator run Playwright or use its own browser validation?

Possibly, but **UNVERIFIED**.

Requirements to verify:

- Playwright is installed.
- Browser binaries are installed.
- The UI Operator can reach the frontend URL.
- The UI Operator can capture screenshots or traces.
- The browser process is cleaned up.

Recommended practice:

If Playwright is not verified, use a fallback validation path:

- manual browser check,
- static frontend preview,
- API-level validation,
- CLI fallback demo.

### How should ports, startup readiness, server cleanup, and test isolation be specified?

Specify them explicitly in the plan.

Recommended rules:

1. Use fixed ports for each environment.
2. Do not use production ports.
3. Backend must expose a health or readiness endpoint.
4. Frontend must wait until backend is ready before integration tests.
5. Each E2E run should use a separate temporary SQLite database.
6. Tests must not mutate the deterministic core or sample data.
7. Servers must be shut down after the phase.
8. Logs must be written to a generated artifacts directory, not protected paths.
9. No test may depend on a server left running from a previous phase.

---

# 9. Test gating

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### Can QA run and report these suites independently?

Suites:

a. existing stdlib unittest core suite  
b. new backend tests  
c. frontend unit tests  
d. Playwright E2E  

Possibly, if the required runtimes and tools are installed and command execution is allowed.

This is **UNVERIFIED**.

Recommended practice:

Require QA to report each suite separately.

QA gate report should include:

- suite name,
- command run,
- pass/fail count,
- failures,
- duration,
- whether protected paths changed,
- whether baseline CLI outputs changed.

### Can I require the existing 36-test suite after every phase?

Yes, as a project rule and gate requirement.

Whether Qoder enforces it automatically is **UNVERIFIED**.

Recommended practice:

Make the 36-test suite a mandatory phase gate.

No phase should be considered complete unless:

- the existing core suite is 36/36,
- the protected-file manifest is unchanged,
- the ambiguous sample baseline remains exact,
- the clean sample baseline remains exact.

### Can the Lead Agent be instructed to stop immediately under these conditions?

Yes, you can instruct it.

Whether the stop is technically enforced is **UNVERIFIED**.

Stop conditions:

1. Any protected-file hash changes.
2. The core suite is not 36/36.
3. Ambiguous sample output is not exactly:
   - 6 requirements,
   - 23 findings,
   - 21 defects,
   - 2 clarifications,
   - 0/100,
   - REFUSED.
4. Clean sample output is not exactly:
   - 3 requirements,
   - 0 findings,
   - 100/100,
   - CERTIFIED.

### Is this stop behavior enforced or merely prompt-following?

Assume it is merely prompt-following unless verified.

Recommended practice:

Use external verification:

- run the core suite yourself after each phase,
- compare SHA-256 manifests yourself,
- review diffs yourself,
- do not issue the next approval phrase until verification passes.

---

# 10. Credit, context, and request strategy

## Documented Qoder behavior

No exact official Qoder documentation page is cited here.

All product-behavior answers in this section are:

> **UNVERIFIED — confirm in the installed Qoder version.**

## Answers

### How are Experts Mode credits calculated?

This is **UNVERIFIED**.

Possible factors may include:

- model used,
- number of experts,
- number of tool calls,
- number of terminal commands,
- input tokens,
- output tokens,
- retrieved file context,
- duration,
- browser or MCP usage.

Do not rely on any specific formula without official confirmation.

### Is one large request cheaper than four gated requests?

Not necessarily.

A single large request may reduce repeated context loading, but it may also increase risk of:

- context overflow,
- confused dependencies,
- unnecessary expert invocations,
- rework,
- unsafe file changes,
- expensive debugging.

For ClarityGate, safety and determinism matter more than minimizing the number of invocations.

Recommended practice:

Use phased requests.

### Does official documentation support the claim that fewer invocations reduce total credit use?

I cannot confirm this without exact official documentation.

Treat any such claim as **UNVERIFIED**.

### Does each expert receive the complete initial prompt and project context?

This is **UNVERIFIED**.

Do not assume every expert sees the full original prompt.

Recommended practice:

Create small, durable artifacts that experts can read:

- `PROJECT_STATE.md`
- `PROTECTED_PATHS.md`
- `BACKEND_CONTRACT.md`
- `TEST_GATE_REPORT.md`
- `PHASE_APPROVALS.md`

These artifacts should be outside protected paths and should contain the minimum facts needed to avoid drift.

### How are discoveries shared between experts?

Possibly through the Lead Agent, shared workspace files, task results, or internal memory.

This is **UNVERIFIED**.

Recommended practice:

Force discoveries into written files.

For example:

- Researcher writes `CORE_API_SURVEY.md`.
- Backend Engineer writes `BACKEND_CONTRACT.md`.
- QA writes `TEST_GATE_REPORT.md`.
- Code Reviewer writes `REVIEW_REPORT.md`.
- UI Operator writes `UI_VALIDATION_REPORT.md`.

Do not rely on implicit memory.

### How does context compression affect a long full-stack run?

Context compression may drop or summarize important details.

This is **UNVERIFIED**, but it is a common risk in long agent runs.

Recommended practice:

Keep critical facts short and repeat them:

- frozen core,
- protected paths,
- 36-test baseline,
- ambiguous sample baseline,
- clean sample baseline,
- no modification to `src/linter/**`,
- `PLAN2.md` not approved until explicitly approved.

### Is the documented “~67% quality improvement” a schedule or cost claim?

I cannot verify that claim.

Treat it as **UNVERIFIED**.

Recommended interpretation:

If such a number exists in Qoder material, treat it as an internal quality benchmark unless the official documentation explicitly says it is a cost, speed, or schedule claim.

Do not use it to justify a risky one-shot full-stack build.

---

# 11. Recommended execution shape

## Options compared

### Option A: One large Experts Mode request for the entire full-stack build

Assessment:

- High risk.
- Hard to control dependencies.
- High chance of context drift.
- Harder to protect the frozen core.
- Harder to debug failures.
- Poor fit for a project without Git.
- Dangerous under hackathon time pressure.

Verdict:

Not recommended.

---

### Option B: Four separate gated Experts Mode requests

Assessment:

- Better control.
- Clearer gates.
- Easier fallback.
- Easier to verify protected paths.
- May use more credits or require more coordination.
- Still depends on Qoder’s actual gating behavior.

Verdict:

Reasonable, but possibly heavier than needed for a hackathon.

---

### Option C: One planning/audit request followed by smaller Agent Mode implementation

Assessment:

- Good control.
- Lower complexity per step.
- Easier to inspect diffs.
- Good for frozen core.
- Requires more human coordination.
- Good fallback behavior.

Verdict:

Strong option.

---

### Option D: Hybrid where Experts Mode handles integration/review but Agent Mode handles narrow implementation batches

Assessment:

- Best balance of control and speed.
- Uses Experts Mode for high-level planning, architecture, review, and integration validation.
- Uses Agent Mode for small, bounded implementation tasks.
- Reduces risk of a large autonomous full-stack run.
- Preserves CLI fallback.
- Fits hackathon constraints better.

Verdict:

Recommended.

---

## Recommended approach for ClarityGate

Use a **hybrid, phase-gated approach**.

Recommended shape:

### Phase 0: Planning and boundary approval

Use Experts Mode or Agent Mode in planning-only mode.

Goal:

- Confirm whether `PLAN2.md` should be approved.
- Identify exact Qoder controls.
- Produce a protected-path manifest plan.
- Produce a dependency and runtime plan.
- Do not modify code.

Gate:

- Project owner explicitly approves or rejects the full-stack expansion boundary.

---

### Phase 1: Read-only core API survey and contract proposal

Use Experts Mode or Agent Mode with read-only intent.

Goal:

- Inspect the real core models and pipeline.
- Document how the backend must wrap the deterministic linter.
- Propose backend API and data contract.
- Propose equivalence tests.
- Do not implement backend or frontend.

Gate:

- Contract is reviewed and frozen by owner.

---

### Phase 2: Backend implementation

Use narrow Agent Mode tasks.

Goal:

- Implement only under `backend/**`.
- Wrap the existing linter.
- Do not modify `src/linter/**`.
- Add backend tests.
- Prove backend output equivalence with CLI baselines.

Gate:

- Core suite remains 36/36.
- Protected hashes unchanged.
- Backend equivalence tests pass.
- Ambiguous and clean sample baselines remain exact.

---

### Phase 3: Frontend implementation against frozen contract

Use narrow Agent Mode tasks.

Goal:

- Implement only under `frontend/**`.
- Use the frozen contract.
- Initially use mocks if helpful.
- Do not change backend contract without approval.

Gate:

- Frontend builds.
- Frontend unit tests pass, if any.
- Protected hashes unchanged.
- Core suite remains 36/36.

---

### Phase 4: Integration, UI validation, and review

Use Experts Mode for integration review, QA, UI validation, and code review.

Goal:

- Connect frontend to backend.
- Run E2E if Playwright is available.
- Validate the live demo path.
- Validate CLI fallback still works.
- Produce final review report.

Gate:

- E2E passes or manual browser validation passes.
- CLI fallback passes.
- Protected hashes unchanged.
- Core suite remains 36/36.
- Code Reviewer reports no protected-path violation.

---

## Why this is best for ClarityGate

This approach fits your constraints:

### Frozen deterministic core

The core is protected by explicit gates and external verification.

### Lack of Git

The plan recommends creating a Git baseline before expansion.

### Cross-stack dependencies

The contract-first sequence prevents frontend from racing ahead.

### Limited hackathon time

Narrow Agent Mode tasks are easier to complete and verify than one giant autonomous request.

### Need for a reliable live demo

The CLI remains the fallback at every phase.

### Ability to fall back to the existing CLI

If the full-stack layer fails, the deterministic CLI still works and can be demonstrated.

---

# 12. Required final deliverables

## A. Recommended preflight checklist

Complete all of these before any full-stack execution.

### 1. Boundary approval

- Confirm whether `PLAN.md` remains the only approved boundary.
- Confirm whether `PLAN2.md` is approved, rejected, or deferred.
- If approved, record the exact approved scope.
- If not approved, stop after planning.

### 2. Git baseline

- Review the working tree for secrets and unwanted artifacts.
- Create a `.gitignore` for generated and local-only files.
- Initialize Git.
- Create a baseline commit.
- Tag the baseline.
- Commit a protected-file SHA-256 manifest.

### 3. Protected-path verification

Confirm these paths exist and are unchanged:

- `src/linter/**`
- existing `tests/**`
- `SKILL.md`
- `specs/claritygate-mvp/**`
- `.kiro/specs/claritygate-mvp/**`
- `data/samples/**`
- `demo-ui/index.html`

### 4. Baseline test verification

Confirm:

- existing stdlib unittest suite passes 36/36.

### 5. Baseline behavior verification

Confirm:

- `data/samples/ambiguous-requirements.md` produces:
  - 6 requirements,
  - 23 findings,
  - 21 defects,
  - 2 clarifications,
  - 0/100,
  - REFUSED.
- `data/samples/clean-ears-requirements.md` produces:
  - 3 requirements,
  - 0 findings,
  - 100/100,
  - CERTIFIED.

### 6. Qoder control verification

Manually verify in the installed Qoder version:

- plan approval required,
- auto-execution disabled,
- command approval enabled,
- file-edit approval enabled,
- dependency-install approval enabled,
- expert activity logs visible,
- diff review visible,
- workspace permission scope understood,
- sandbox or path restrictions, if any, understood.

### 7. Runtime verification

If full-stack work is approved, verify:

- Python version,
- Node version,
- npm or equivalent package manager,
- ability to install backend dependencies,
- ability to install frontend dependencies,
- ability to run FastAPI,
- ability to run Vite,
- ability to access localhost,
- ability to run Playwright, if E2E is required.

### 8. Fallback verification

Confirm that the CLI demo still works without backend or frontend.

The fallback command shape is:

```text
python3 -m linter.claritygate <requirements.md> --out <report.md>
```

Do not change this command shape during expansion.

---

## B. Recommended expert-role configuration

This is a recommended configuration, not a confirmed Qoder capability.

| Role | Purpose | Access | Writable paths | Gate authority |
|---|---|---|---|---|
| Lead Agent | Coordinate phases, enforce gates, produce reports | Should not directly modify protected paths | Planning/report paths only, if approved | Must stop on gate failure |
| Researcher | Inspect core API and produce integration notes | Read-only | None | None |
| Backend Engineer | Wrap deterministic linter with FastAPI | Write only backend | `backend/**` | None |
| Frontend Engineer | Build UI against frozen contract | Write only frontend | `frontend/**` | None |
| QA | Run tests and produce gate reports | Run approved commands | Test/report paths only | Reports pass/fail |
| Code Reviewer | Read-only review and protected-path audit | Read-only | None | Advisory fail/block |
| UI Operator | Browser validation | Browser only | Evidence/report paths only, if approved | Reports UI pass/fail |
| Debug Engineer | Diagnose failures | Minimal write, no protected paths | Non-protected debug/report paths only | None |

Recommended rule:

> The Lead Agent must not approve a phase transition if QA, Code Reviewer, or protected-path manifest verification reports failure.

---

## C. Dependency-aware phase structure

### Phase 0: Planning-only

Inputs:

- Current verified implementation state.
- Protected paths.
- Existing baselines.
- `PLAN.md`.
- Proposed `PLAN2.md`.

Work:

- Produce a full-stack expansion plan.
- Identify risks.
- Identify Qoder controls to verify.
- Produce a gate structure.
- Do not modify files.

Exit gate:

- Owner explicitly approves or rejects `PLAN2.md`.

---

### Phase 1: Core API survey and contract freeze

Inputs:

- Frozen core source.
- Existing models:
  - `RequirementRecord`
  - `Finding`
  - `EvaluationResult`
  - `ReportResult`
- Existing pipeline:
  - loader,
  - parser,
  - rule engine,
  - evaluator,
  - reporter.

Work:

- Read-only inspection.
- Document how backend must call the core.
- Propose backend request/response contract.
- Propose persistence model, if SQLite is approved.
- Propose equivalence tests.

Exit gate:

- Owner approves frozen backend contract.

---

### Phase 2: Backend implementation

Inputs:

- Frozen backend contract.
- Approved backend scope.
- Approved dependency list.

Work:

- Implement under `backend/**`.
- Import and wrap the core linter.
- Do not modify `src/linter/**`.
- Add backend tests.
- Add equivalence tests against sample baselines.

Exit gate:

- Core suite remains 36/36.
- Protected manifest unchanged.
- Backend equivalence tests pass.
- Ambiguous baseline remains exact.
- Clean baseline remains exact.

---

### Phase 3: Frontend implementation

Inputs:

- Frozen backend contract.
- Backend gate passed.
- Approved frontend scope.

Work:

- Implement under `frontend/**`.
- Use frozen contract.
- Use mocks if useful.
- Do not modify backend or core.

Exit gate:

- Frontend builds.
- Frontend unit tests pass, if any.
- Protected manifest unchanged.
- Core suite remains 36/36.

---

### Phase 4: Integration and E2E

Inputs:

- Backend gate passed.
- Frontend gate passed.
- Runtime environment verified.

Work:

- Connect frontend to backend.
- Run E2E if Playwright is available.
- Validate report export.
- Validate fallback CLI.

Exit gate:

- Integration tests pass.
- Browser validation passes or manual validation passes.
- Protected manifest unchanged.
- Core suite remains 36/36.
- Servers cleaned up.

---

### Phase 5: Review and demo packaging

Inputs:

- All previous gate reports.

Work:

- Code Reviewer audit.
- Protected-path audit.
- Demo script.
- Fallback script.
- Final known-issues list.

Exit gate:

- Owner accepts demo readiness.

---

## D. Exact first planning-only prompt to paste into Qoder Experts Mode

Use this only for planning. It does not approve `PLAN2.md`.

```text
You are in PLANNING-ONLY mode for the ClarityGate project.

Do not create, modify, delete, move, rename, install, build, start, stop, or execute anything that changes project state.

Do not modify any file.
Do not install dependencies.
Do not start servers.
Do not run browsers.
Do not execute tests unless I explicitly approve a read-only verification command.
Do not delegate implementation work.
Do not treat PLAN2.md as approved.

PROJECT STATE

ClarityGate currently has a complete, working deterministic CLI linter.

Implementation:
- Pure Python, standard library only.
- Real implementation is under src/linter/.
- Pipeline:
  1. loader.load_requirements(path)
  2. parser.parse_requirements(text)
  3. rule_engine.run_checks(records)
  4. evaluator.evaluate(records, findings)
  5. reporter.write_report(input_path, records, evaluation, out_path)
- CLI entry point:
  python3 -m linter.claritygate <requirements.md> --out <report.md>
- A top-level linter/ shim forwards to src/linter/.
- No backend, database, network calls, or live frontend currently exist.
- demo-ui/index.html is an existing static visual shell only.

Existing core models:
- RequirementRecord
- Finding
- EvaluationResult
- ReportResult

Important actual fields:
- Finding: line_number, type, severity, message, suggested_rewrite, check_id, category
- EvaluationResult: score, tier, verdict, exit_code, findings, requirement_count, defects, clarifications, infos

Verified baselines:
- 36 stdlib unittest tests pass.
- data/samples/ambiguous-requirements.md:
  6 requirements, 23 findings, 21 defects, 2 clarifications,
  0/100, REFUSED.
- data/samples/clean-ears-requirements.md:
  3 requirements, 0 findings, 100/100, CERTIFIED.

Protected and frozen paths:
- src/linter/**
- existing tests/**
- SKILL.md
- specs/claritygate-mvp/**
- .kiro/specs/claritygate-mvp/**
- data/samples/**
- demo-ui/index.html

Repository limitation:
- The working directory currently has no .git directory.
- Therefore git diff, git rollback, worktrees, commits, and branch-based protection are not currently available.

PLANNING STATUS

PLAN.md remains the currently accepted implementation boundary. It permits only the pure-Python CLI and expressly excludes UI, backend, database, and network work.

PLAN2.md is a proposed, not-yet-approved full-stack expansion:
- Backend: Python 3.11 + FastAPI
- Persistence: SQLite
- Frontend: React + Vite + TypeScript + Tailwind
- Core linter imported and wrapped, never modified
- Backend and frontend code isolated under backend/ and frontend/
- Existing CLI and static demo retained as fallback
- Proposed flow:
  paste Markdown → analyze → review findings → accept rewrites →
  rerun deterministic linter → improved score → export report

TASK

Produce a planning and Qoder-workflow research report only.

Do not implement anything.

Your report must include:

1. A phase-gated execution strategy for moving from the current CLI to the proposed full-stack system, conditional on explicit owner approval of PLAN2.md.

2. A protected-path protection plan for:
   - src/linter/**
   - existing tests/**
   - SKILL.md
   - specs/claritygate-mvp/**
   - .kiro/specs/claritygate-mvp/**
   - data/samples/**
   - demo-ui/index.html

3. A Git baseline preparation plan, including what must be reviewed before initializing Git.

4. A SHA-256 manifest plan for verifying protected files before and after each phase.

5. A dependency-aware phase order:
   A. inspect actual core API
   B. freeze backend data/API contract
   C. implement backend
   D. pass backend/core equivalence tests
   E. implement frontend
   F. pass browser E2E

6. A recommended expert-role assignment table, including:
   - Researcher
   - Backend Engineer
   - Frontend Engineer
   - QA
   - Code Reviewer
   - UI Operator
   - Debug Engineer

7. Explicit stop conditions, including:
   - any protected-file hash changes;
   - the core suite is not 36/36;
   - ambiguous output is not exactly 23 findings and 0/100;
   - clean output is not exactly 0 findings and 100/100;
   - any expert writes outside its assigned paths;
   - any dependency install occurs without approval;
   - any server or browser starts without approval.

8. A list of Qoder product-behavior claims that must be manually verified in the installed Qoder version before execution.

For every Qoder product-behavior claim, cite the exact official Qoder documentation page. If you cannot cite exact official documentation, mark the claim:

UNVERIFIED — confirm in the installed Qoder version.

Do not invent Qoder settings, labels, or documentation pages.

Finish by asking me for one of these explicit decisions:

- APPROVE PLAN2 FULL-STACK EXPANSION
- REJECT PLAN2 FULL-STACK EXPANSION
- DEFER PLAN2 PENDING QODER UI VERIFICATION
```

---

## E. Explicit plan-approval wording

Use explicit, phase-limited approval messages.

### Planning-only approval

If you only approve planning:

```text
APPROVE PHASE 0 ONLY: planning and Qoder-workflow research.
Do not modify files.
Do not install dependencies.
Do not start servers.
Do not run browsers.
Do not execute implementation work.
```

### Read-only research approval

```text
APPROVE PHASE 1 ONLY: read-only core API survey and contract proposal.
You may read protected files.
You may not modify any file.
You may not install dependencies.
You may not start servers.
You may not run browsers.
```

### Backend implementation approval

```text
APPROVE PHASE 2 ONLY: backend implementation under backend/**.
Do not modify src/linter/**, existing tests/**, SKILL.md, specs/claritygate-mvp/**, .kiro/specs/claritygate-mvp/**, data/samples/**, or demo-ui/index.html.
Stop immediately if the core suite is not 36/36 or if any protected-file hash changes.
```

### Frontend implementation approval

```text
APPROVE PHASE 3 ONLY: frontend implementation under frontend/**.
Use the frozen backend contract only.
Do not modify backend/**, src/linter/**, existing tests/**, SKILL.md, specs/claritygate-mvp/**, .kiro/specs/claritygate-mvp/**, data/samples/**, or demo-ui/index.html.
Stop immediately if the core suite is not 36/36 or if any protected-file hash changes.
```

### Integration/E2E approval

```text
APPROVE PHASE 4 ONLY: integration and browser validation.
Do not modify protected paths.
Use temporary test databases only.
Clean up all servers and browser processes.
Stop immediately if the core suite is not 36/36 or if any protected-file hash changes.
```

### Full-stop wording

If anything goes wrong:

```text
STOP ALL WORK IMMEDIATELY.
Do not modify any further files.
Do not run any further commands.
Produce a violation report listing:
- phase,
- expert,
- action,
- files touched,
- commands run,
- failed gate,
- observed mismatch.
Wait for my explicit instruction.
```

---

## F. Explicit stop conditions

The following should stop all work immediately.

### Protected-path stop conditions

Stop if any of these change:

- `src/linter/**`
- existing `tests/**`
- `SKILL.md`
- `specs/claritygate-mvp/**`
- `.kiro/specs/claritygate-mvp/**`
- `data/samples/**`
- `demo-ui/index.html`

Stop if:

- a file is modified,
- a file is deleted,
- a file is renamed,
- a file is moved,
- a file permission change affects usability,
- a SHA-256 manifest mismatch occurs.

### Core test stop conditions

Stop if:

- the existing stdlib unittest suite is not 36/36.

### Baseline behavior stop conditions

Stop if the ambiguous sample does not produce exactly:

- 6 requirements,
- 23 findings,
- 21 defects,
- 2 clarifications,
- 0/100,
- REFUSED.

Stop if the clean sample does not produce exactly:

- 3 requirements,
- 0 findings,
- 100/100,
- CERTIFIED.

### Contract stop conditions

Stop if:

- the backend contract changes after freeze without explicit approval,
- the frontend assumes an endpoint not in the frozen contract,
- the backend changes response shapes without approval,
- persistence changes affect deterministic output.

### Runtime stop conditions

Stop if:

- dependency installation occurs without approval,
- a server starts without approval,
- a browser starts without approval,
- a required port is already in use,
- a server fails readiness checks,
- server cleanup fails,
- a test uses a non-temporary database.

### Expert-role stop conditions

Stop if:

- an expert writes outside its assigned paths,
- a read-only expert attempts to modify files,
- the Lead Agent cannot identify which expert performed an action,
- QA cannot produce an independent suite report,
- Code Reviewer reports a protected-path violation.

---

## G. Claims and controls that must be manually verified in the Qoder UI

Before any code execution, verify each of the following in your installed Qoder version.

### Plan approval controls

Verify:

- Whether Experts Mode pauses after planning.
- Whether a plan must be approved before execution.
- The exact approval control.
- Whether execution can begin automatically.
- Whether auto-execution can be disabled.

### Command execution controls

Verify:

- Whether terminal commands require approval.
- Whether dependency installation requires approval.
- Whether server startup requires approval.
- Whether browser launch requires approval.

### Expert visibility controls

Verify:

- Which experts exist.
- Whether experts are dynamically selected.
- Whether required experts can be forced.
- Whether unwanted experts can be excluded.
- Whether expert attribution is visible per action.

### File protection controls

Verify:

- Whether path-level write restrictions exist.
- Whether protected paths can be made read-only.
- Whether experts can be restricted by path.
- Whether file edits are reviewed before application.
- Whether conflicting edits are detected.

### Review and rollback controls

Verify:

- Whether Qoder requires Git.
- Whether Qoder has non-Git snapshots.
- Whether rollback is possible without Git.
- Whether diff review is available without Git.
- Whether commits, branches, tags, or worktrees depend on Git.

### Runtime and UI controls

Verify:

- Whether Qoder can install Python dependencies.
- Whether Qoder can install npm dependencies.
- Whether Qoder can run FastAPI and Vite simultaneously.
- Whether UI Operator can access localhost services.
- Whether UI Operator can run Playwright.
- Whether browser processes are cleaned up.

### Context and credit controls

Verify:

- How credits are calculated.
- Whether expert count affects cost.
- Whether each expert receives the full prompt.
- Whether context is compressed.
- Whether long runs lose critical constraints.
- Whether any “quality improvement” claim is cost, schedule, or internal benchmark.

### Instruction scope controls

Verify:

- Where expert-specific additional prompts are configured.
- Whether settings are global, project-level, or conversation-level.
- Whether the Lead Agent sees expert-specific instructions.
- Whether permanent project rules exist.
- Whether protected-path instructions are inherited by all experts.

---

# Final recommendation

For ClarityGate, do **not** use one large autonomous Experts Mode request to build the full stack.

Use this instead:

1. Keep `PLAN.md` as the active boundary until you explicitly approve `PLAN2.md`.
2. Create a Git baseline and protected-file SHA-256 manifest before any expansion work.
3. Use a planning-only Experts Mode request first.
4. Freeze the backend contract before any implementation.
5. Use narrow Agent Mode tasks for backend and frontend implementation.
6. Use Experts Mode for integration review, QA gating, UI validation, and final audit.
7. Treat every Qoder enforcement claim as **UNVERIFIED — confirm in the installed Qoder version** until you have checked the actual UI.
8. Keep the deterministic CLI as the primary fallback and the source of truth at all times.