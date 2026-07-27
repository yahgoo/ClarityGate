# ClarityGate — 2-Minute Demo Flow

## Story

"Bad spec in, bad AI build out." ClarityGate catches requirement defects *before*
an AI coding agent builds from them — preventing AI drift at the source.

## Setup (before the demo)

```bash
cd ClarityGate
```

No install step. Python 3.11+ with stdlib only.

## Demo Sequence

### 1. Show the bad spec (10 seconds)

Open `data/samples/ambiguous-requirements.md`. Point out:

- "fast" — unquantified adjective
- "should" — weak imperative, not SHALL
- "obviously" — tacit knowledge assumption
- "as appropriate" — escape clause permitting non-conformance
- "symbol/sign" — oblique symbol creating referential ambiguity
- No IF-THEN error-path coverage

### 2. Run the linter (15 seconds)

```bash
python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/demo-ambiguous-report.md
```

**What to point out in stdout:**

- `Requirements scanned: 6` — it parsed the Markdown
- `Findings: 23` — every line has multiple issues
- `Verdict: REFUSED` — the spec is blocked from AI handoff
- `Quest Readiness Score: 0/100` — not ready for a coding agent
- Exit code is `2` — this is a *verdict*, not a crash

### 3. Open the report (20 seconds)

```bash
open /tmp/demo-ambiguous-report.md   # macOS
# or: cat /tmp/demo-ambiguous-report.md
```

**What to point out in the Markdown report:**

- **Findings table** — line-by-line, check-by-check with specific messages
- **Clarification Queue** — two-option questions the author must answer
- **Suggested rewrites** — measurable replacements (e.g., "within 2 seconds for 95% of requests")

### 4. Show the clean spec (10 seconds)

Open `data/samples/clean-ears-requirements.md`. Point out:

- Proper EARS keywords: `WHEN`, `WHILE`, `IF … THEN`, `THE System SHALL`
- Measurable thresholds: "within 2 seconds", "30 minutes", "within 1 minute"
- One IF-THEN Unwanted Behavior criterion (error-path coverage)

### 5. Run the linter on the clean spec (10 seconds)

```bash
python3 -m linter.claritygate data/samples/clean-ears-requirements.md --out /tmp/demo-clean-report.md
```

**What to point out:**

- `Findings: 0`
- `Quest Readiness Score: 100/100 (Quest Ready)`
- `Verdict: CERTIFIED`
- Exit code `0` — safe to hand to an AI coding agent

### 6. Close the loop (15 seconds)

Say: "The same AI agent that would have built from the vague spec now gets an
unambiguous source of truth. No drift. No rework. The gate caught 23 defects
before they became 23 bugs."

## What NOT to demo yet

- No UI (CLI only)
- No backend server
- No database
- No cloud deployment
- No automatic rewriting of specs (report only)

## Quick-reference commands

```bash
# Full test suite (36 tests)
python3 -m unittest -v

# Ambiguous spec → REFUSED
python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/demo-ambiguous-report.md

# Clean spec → CERTIFIED
python3 -m linter.claritygate data/samples/clean-ears-requirements.md --out /tmp/demo-clean-report.md

# Scan the project's own spec (meta!)
python3 -m linter.claritygate specs/claritygate-mvp/requirements.md --out /tmp/demo-self-report.md
```
