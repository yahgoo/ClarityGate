# ClarityGate — Design

This design is derived strictly from `specs/claritygate-mvp/requirements.md` and
`SKILL.md`. It stays within the MVP scope defined there: a lightweight,
command-line, dependency-free linter that scans a `requirements.md` file and emits
a Clarification Queue plus a Quality Report. No code-generation, design-authoring,
or enterprise-integration scope is introduced.

## Architecture Overview

ClarityGate is a single-pass, file-driven linter with a small, linear pipeline.
There is no server, no database, and no network calls (per NFR4: runs from the CLI
with no external service dependency).

```
            requirements.md (input)
                    │
                    ▼
        ┌───────────────────────┐
        │  1. Loader / Reader   │  read file as UTF-8 text
        └───────────────────────┘
                    │  raw text
                    ▼
        ┌───────────────────────┐
        │  2. Parser            │  split into requirement blocks;
        │                       │  extract EARS keyword + statement
        └───────────────────────┘
                    │  structured requirement records
                    ▼
        ┌───────────────────────┐
        │  3. Rule Engine       │  run each check (Ambiguity, EARS,
        │                       │  Tacit Knowledge) over each record
        └───────────────────────┘
                    │  findings
                    ▼
        ┌───────────────────────┐
        │  4. Evaluator         │  map findings → Refusal / Escalation
        │                       │  / Clarification Queue
        └───────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  5. Reporter          │  write Quality Report (Markdown) +
        │                       │  print summary to stdout  (AC6)
        └───────────────────────┘
                    │
                    ▼
          Quality Report + stdout summary (output)
```

The pipeline is synchronous and terminates after one scan. A progress indicator is
shown only when the file exceeds 20 requirements (AC4).

## Rule Engine Design

The Rule Engine is a registry of named **checks**. Each check implements a common
interface:

```
Check:
  id          : stable identifier (e.g., "AMB-PASSIVE")
  description : human-readable summary
  applies_to  : requirement record
  run(record) : returns 0+ Finding objects
```

`Finding` is the unit of output from every check:

```
Finding:
  check_id    : id of the rule that produced it
  severity    : "defect" | "clarification" | "info"
  line        : source line number in requirements.md
  category    : one of { lexical, referential, syntactical, completeness, tacit }
  message     : what is wrong / what to clarify
  suggestion  : concrete remediation or two-option question
```

Checks are implemented directly from the SKILL.md rules:

| Check ID        | SKILL.md Rule                 | Detection method                                  |
|-----------------|-------------------------------|---------------------------------------------------|
| AMB-VAGUE-VERB  | Vague Verbs                   | Token match against deny-list: handle, provide, support, optimize, manage |
| AMB-VAGUE-ADJ   | Unquantified Adjectives       | Token match against deny-list: fast, scalable, timely, user-friendly, appropriate |
| AMB-PASSIVE     | Passive Voice                 | Regex for `be <past-participle>` (e.g., `was/were/is/are + \w+ed`) at statement start |
| AMB-PRONOUN     | Pronoun Antecedents           | Flag "it"/"this"/"they" with no preceding noun in the same statement |
| AMB-OBLIQUE     | Oblique Symbols               | Regex for `/` joining two words: `\w+/\w+`        |
| AMB-ESCAPE      | Escape Clauses                | Phrase match: "as appropriate", "if necessary", "where possible" |
| EARS-KEYWORD    | EARS Enforcement (grammar)    | Require UPPERCASE WHEN/WHILE/WHERE/IF/THEN/SHALL; reject lowercase |
| EARS-SINGULAR   | One SHALL per requirement    | Count of "SHALL" > 1 ⇒ singularity violation (FR5) |
| EARS-PATTERN    | Six EARS patterns             | Match statement against the six templates (see below) |
| TACIT-SILENCE   | Mismatched Silences           | Heuristic: requirement asserts behavior with no stated trigger/condition |
| TACIT-UNREC     | Unrecognized Knowledge        | Heuristic: "obvious"/"simply"/"just" implying undocumented step |
| TACIT-DOMAIN    | Domain Constraints            | Prompt-only: ask explicit constraint questions |
| TACIT-SILENT    | Silent Intent                 | Optional: scan project transcripts if accessible (Open Question) |

Each deny-list / phrase-list is a plain data table in the source, so it is easy to
extend without changing check logic. All matching is case-insensitive for the
natural-language terms, but EARS keywords are matched case-sensitively UPPERCASE
(EARS-KEYWORD).

## Input/Output Contract

### Input
- A single file path argument: `requirements.md` (any path; default `./requirements.md`).
- File encoding: UTF-8 text.
- Expected structure: a Markdown document containing requirement statements. The
  parser recognizes a requirement as any line/item that contains an EARS keyword
  (`SHALL`) or is listed under a requirements-style heading. Non-requirement prose
  (Problem Statement, Goals) is read for context but not scored as acceptance criteria.

### Output
1. **Quality Report** — a Markdown file written to disk (NFR3: human-readable
   Markdown). Default path `./claritygate-report.md`, overridable via `--out`.
   Contents:
   - Scan metadata (file, requirement count, timestamp).
   - Per-finding table: `line | check_id | category | severity | message | suggestion`.
   - Clarification Queue section: every `clarification`-severity finding rendered as
     a two-option question (per SKILL.md Required Output Format).
   - Summary counts by category and severity.
2. **stdout summary** — printed when the scan completes (AC6): total requirements
   scanned, total findings, count of defects vs. clarifications, and a pass/refuse
   verdict (see Error/Escalation Handling).
3. **Exit code** — `0` if no Refusal Condition triggered; non-zero (`2`) if the
   tool refused to certify the spec (maps to Refusal Conditions).

Progress indicator (AC4) is written to stderr while scanning files >20 requirements
so it does not pollute the stdout summary or the report file.

## EARS Compliance Check Logic

A requirement record is parsed into `(keyword_prefix, statement)` where
`keyword_prefix` is the leading EARS construct.

**Step 1 — Keyword casing (EARS-KEYWORD, AC1).**
Scan for the six EARS keywords case-sensitively. If a keyword appears in lowercase
(e.g., `when`, `shall`), the file is rejected: the tool lists the required
UPPERCASE keywords and stops (AC1). This is a hard reject, not a clarification.

**Step 2 — Pattern match (EARS-PATTERN).**
Match the normalized statement against the six canonical templates:

1. Ubiquitous: `THE System SHALL <behavior>`
2. Event-Driven: `WHEN <trigger> THE System SHALL <response>`
3. State-Driven: `WHILE <state> THE System SHALL <behavior>`
4. Unwanted Behavior: `IF <condition> THEN THE System SHALL <recovery action>`
5. Optional Feature: `WHERE <feature> is included THE System SHALL <behavior>`
6. Complex: `<precondition(s)> <trigger> THE System SHALL <response>`

A statement that contains `SHALL` but matches none of the six templates is flagged
as a syntax defect (non-compliant pattern).

**Step 3 — Singularity (EARS-SINGULAR, FR5).**
Count occurrences of `SHALL` in the requirement. If `> 1`, flag a singularity
violation (one SHALL per requirement for traceability).

**Step 4 — Happy-path completeness (AC3).**
Group requirements by the feature they describe. If a feature has only nominal
(Event-Driven / State-Driven / Ubiquitous) criteria and zero Unwanted Behavior
(IF-THEN) criteria, emit an `IF … THEN` clarification prompt (AC3 / Escalation:
Missing Error Paths).

## Tacit Knowledge Detection Logic

Tacit checks are heuristic and conservative; they produce clarifications, never
hard rejects (except where they also trip a Refusal Condition).

- **Mismatched Silences (TACIT-SILENCE):** For each nominal requirement, check
  whether a trigger, precondition, or error path is implied but absent. If a
  requirement describes an outcome with no stated condition, flag "unstated
  assumption" and ask the author to confirm the missing condition.
- **Unrecognized Knowledge (TACIT-UNREC):** Flag phrases like "obviously",
  "simply", "just", "as usual" that signal an undocumented step the author assumes
  is known. Prompt the author to make the step explicit.
- **Domain Constraints (TACIT-DOMAIN):** Emit a fixed set of domain-probe
  questions (e.g., "Can an order be canceled before it is submitted?") relevant to
  the detected entities in the spec, to surface implicit business rules.
- **Silent Intent (TACIT-SILENT):** If project transcript access is available
  (Open Question — leave as opt-in flag `--scan-transcripts`), compare discussed
  intent against the formal spec and flag gaps. If access is unavailable, this
  check is a no-op and noted in the report as "skipped".

Abductive reasoning here is realized as pattern-based inference rules, not an LLM
call, to keep the MVP deterministic and dependency-free.

## Error / Escalation Handling

Findings flow into the Evaluator, which decides the disposition per SKILL.md.

**Refusal Conditions (hard stop → exit code 2, no Design/Tasks certification):**
1. Thesis-level requirement present (e.g., "The system shall be user-friendly") —
   detected by AMB-VAGUE-ADJ on a requirement whose only predicate is subjective.
2. Implementation leakage (e.g., "The system shall use an SQL database") — detected
   by a technology-keyword deny-list (sql, database, react, kafka, aws, …).
3. Missing or lowercase EARS keywords — from EARS-KEYWORD / EARS-PATTERN steps.
4. Untestable statement — a requirement with no mappable observable input/output
   (no measurable metric and no EARS trigger/response structure).

When any Refusal Condition fires, the tool prints the offending findings and the
verdict `REFUSED`, and does not emit a "certified" summary.

**Escalation Rules (clarification or block, not necessarily refuse):**
- **Inconsistency:** If two requirements are logically incompatible (e.g.,
  conflicting IF-THEN outcomes for the same trigger), emit a Conflict Question
  (SKILL.md Required Output Format) and mark implementation as blocked until
  arbitrated.
- **AI Drift Risk:** If a requirement produces excessive findings (threshold:
  ≥3 distinct defects) such that it resists formalization, abstain from certifying
  and request a rewrite of that requirement.
- **Missing Error Paths:** Handled in EARS Step 4 (AC3) — prompt for IF-THEN
  criteria before certifying.

**Non-fatal handling:**
- Lowercase EARS keywords → reject file (AC1), not silent fix.
- Unquantified adjectives / passive voice / oblique symbols / escape clauses →
  defects in the Clarification Queue with a suggested measurable replacement (AC2).

## Technology Choices

- **Language:** Python 3.11+. Chosen for readability, zero-build execution, and
  ubiquitous availability in Qoder/Kiro/Cursor workspaces. Meets NFR4 (CLI, no
  external service).
- **Parsing approach:** Line/token-based scanning with the standard library only —
  `re` for regex patterns, `argparse` for the CLI, no third-party parser. Markdown
  structure is intentionally treated as plain text with heading-aware splitting,
  avoiding a heavyweight Markdown AST dependency for the MVP.
- **Dependencies:** None required (stdlib only). This keeps install friction at
  zero and satisfies the hackathon MVP portability goal.
- **Entry point:** `src/linter/claritygate.py` with a `python -m linter.claritygate
  requirements.md` invocation, plus a thin `src/linter/__main__.py`.
- **Performance:** Single in-memory pass over the file; target ≤10s for ~20
  requirements (NFR2). No streaming or async needed at MVP scale.
- **Testing hook:** The deny-lists and EARS templates are plain data tables so they
  can be unit-tested against the labeled sample referenced in NFR1 (F-score ≥ 0.77
  on 50 held-out requirements) without altering check logic.

This design introduces no capability beyond `requirements.md` (FR1–FR6, NFR1–NFR4,
AC1–AC6) and `SKILL.md` (Ambiguity Rules, EARS Enforcement, Tacit Knowledge Checks,
Escalation Rules, Refusal Conditions).
