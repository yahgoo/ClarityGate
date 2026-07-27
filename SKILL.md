# SKILL — ClarityGate Requirements Engineering Linter

This file is an IDE-agnostic instruction set. It is usable by Qoder, Kiro, Cursor, and Qwen-based agents. Follow it literally when reviewing or authoring requirements.

## Purpose

ClarityGate is an automated quality gateway that catches "requirement bugs" before they propagate to design, implementation, and testing. By enforcing structured EARS syntax and flagging linguistic smells, it prevents **AI drift** — the tendency for coding agents to fill ambiguity with inconsistent assumptions. The agent using this skill acts as an **intent clarifier**: every requirement must be a testable constraint on observable behavior, not a vague thesis statement.

## When to Use

- At the start of every spec-driven workflow session.
- Mandatory review of `requirements.md` before generating `design.md` or `tasks.md`.
- Whenever a developer or PM modifies an existing requirement or adds a new user story.
- When moving from a prototype or "vibe" sketch to a production-ready specification.

## Review Checklist

1. **EARS Compliance**: Does every acceptance criterion follow one of the six canonical EARS patterns?
2. **Imperative Usage**: Is "SHALL" used for every mandatory requirement, with "should", "must", "may", and "will" rejected?
3. **Measurable Metrics**: Are all performance and success criteria quantifiable (e.g., "< 200ms", "99.9% uptime")?
4. **Error Path Coverage**: Does every nominal path have a corresponding "Unwanted Behavior" (IF-THEN) requirement?
5. **Ambiguity Scan**: Is the requirement free of lexical, referential, and syntactical ambiguity?

## Ambiguity Rules

Flag the following as defects:

- **Vague Verbs**: Prohibit verbs with no observable output — "handle", "provide", "support", "optimize", "manage".
- **Unquantified Adjectives**: Flag subjective terms — "fast", "scalable", "timely", "user-friendly", "appropriate".
- **Passive Voice**: Requirements MUST be active voice so the actor is explicit.
- **Pronoun Antecedents**: Flag "it", "this", "they" without a clear noun in the same statement.
- **Oblique Symbols**: Flag "/" used to combine synonyms (e.g., "symbol/sign") as referential ambiguity.
- **Escape Clauses**: Flag phrases permitting non-conformance — "as appropriate", "if necessary", "where possible".

## EARS Enforcement Rules

Every requirement SHALL conform to one of the six EARS patterns:

1. **Ubiquitous**: `THE System SHALL <behavior>`
2. **Event-Driven**: `WHEN <trigger> THE System SHALL <response>`
3. **State-Driven**: `WHILE <state> THE System SHALL <behavior>`
4. **Unwanted Behavior**: `IF <condition> THEN THE System SHALL <recovery action>`
5. **Optional Feature**: `WHERE <feature> is included THE System SHALL <behavior>`
6. **Complex**: `<precondition(s)> <trigger> THE System SHALL <response>`

Grammar rules:

- EARS keywords MUST be UPPERCASE.
- One "SHALL" per requirement to preserve singularity and traceability.
- A requirement with no EARS keyword is non-compliant and MUST be rewritten.

## Tacit Knowledge Checks

Use abductive reasoning to surface "dark matter" requirements:

- **Mismatched Silences**: Question assumptions the author omitted without intent.
- **Unrecognized Knowledge**: Flag where the author performs a task a specific way but omitted it as "obvious".
- **Domain Constraints**: Make implicit rules explicit (e.g., "Can an order be canceled before it is submitted?").
- **Silent Intent**: Note intent present in project transcripts but absent from the formal spec, and flag it for the author to confirm.

## Required Output Format

Findings SHALL be delivered as a **Clarification Queue** using simple two-option questions:

- **Ambiguity Question**: "The phrase 'remove the record' could mean hard-delete or soft-delete. Which did you mean? A) Keep as-is (Hard Delete); B) Change to Soft-Delete."
- **Conflict Question**: "Rule R1 and R2 fire in the same situation but demand incompatible outcomes. Which one takes priority?"
- **Surprising Scenario**: Present a concrete behavior the requirements accept or reject and ask whether it is intended.

## Escalation Rules

- **Inconsistency**: If two requirements are logically incompatible, block implementation and force arbitration.
- **AI Drift Risk**: If a requirement resists formalization (excessive ambiguity), abstain from design generation and request a rewrite.
- **Missing Error Paths**: If only happy-path criteria exist, prompt for "Unwanted Behavior" (IF-THEN) criteria before proceeding.

## Refusal Conditions

Refuse to proceed to the Design or Tasks phase if any of the following are present:

1. **Thesis-level requirements** — e.g., "The system shall be user-friendly".
2. **Implementation leakage** — e.g., "The system shall use an SQL database".
3. **Missing or lowercase EARS keywords**.
4. **Untestable statements** — requirements that cannot be mapped to observable inputs or outputs.
