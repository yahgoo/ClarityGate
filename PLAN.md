# ClarityGate Core Linter Engine Plan

## Summary

Implement the scoped first phase only: a pure Python, stdlib-only CLI linter under `src/linter/` with the five documented pipeline modules: loader, parser, rule engine, evaluator, reporter. No UI, backend server, database, network calls, or spec edits.

One implementation detail needs to be locked in for the requested command: because the repo uses a `src/linter/` layout and has no package config, add a minimal top-level `linter/` shim package that forwards to `src/linter/` so `python -m linter.claritygate <path>` works from the repo root without requiring `PYTHONPATH=src`. The real implementation remains in `src/linter/`.

## Implementation Changes

- Add core package files in `src/linter/`: `__init__.py`, `models.py`, `loader.py`, `parser.py`, `rule_engine.py`, `evaluator.py`, `reporter.py`, `claritygate.py`, and `__main__.py`.
- Add top-level command shim: `linter/__init__.py`, `linter/claritygate.py`, and `linter/__main__.py`, delegating to `src.linter.claritygate`.
- Use dataclasses for `RequirementRecord`, `Finding`, `EvaluationResult`, and `ReportResult`.
- Loader reads UTF-8 only and raises a clear `LoadError` for missing, unreadable, or non-UTF-8 files.
- Parser extracts requirement-like Markdown lines, tracks original line numbers, detects EARS keywords, lowercase EARS keyword usage, and requirement sections.
- Rule engine implements these checks with deterministic regex/token rules: vague verbs, vague adjectives, non-mandatory imperatives, adverbs ending in `-ly`, passive voice, pronoun ambiguity, oblique symbols, escape clauses, EARS casing, EARS pattern, EARS singularity, missing EARS keyword, tacit “obvious/just/simply/as usual” wording, implementation leakage, and happy-path-only detection.
- Evaluator computes Quest Readiness Score from findings, assigns tiers, and returns exit code `2` when refusal conditions fire.
- Reporter writes `claritygate-report.md` by default, supports `--out`, prints stdout summary, writes progress to stderr only when requirement count exceeds 20, and keeps the report human-readable Markdown.
- CLI supports `python -m linter.claritygate <path-to-requirements.md>` and optional `--out <report-path>`.

## Rule Decisions

- EARS lowercase rejection flags any lowercase `when`, `while`, `where`, `if`, `then`, or `shall` used as requirement keywords, and the report lists required uppercase forms: `WHEN`, `WHILE`, `WHERE`, `IF`, `THEN`, `SHALL`.
- EARS pattern validation accepts punctuation after clauses, including comma variants like `WHEN <trigger>, THE System SHALL <response>`.
- Complex EARS is MVP-light: accept any line that contains at least one leading uppercase condition keyword before `THE System SHALL`, while still enforcing one `SHALL`.
- Happy-path-only detection is document-level: if at least one nominal requirement exists and no valid `IF ... THEN THE System SHALL ...` requirement exists, add a clarification finding prompting for an Unwanted Behavior criterion.
- Pronoun detection is heuristic: flag `it`, `this`, or `they` when no clear noun-like token appears before the pronoun in the same statement.
- Passive voice is heuristic: flag forms like `is processed`, `are handled`, `was created`, `were sent`, `be updated`, and similar `be + past participle` constructions.

## Test Plan

- Use stdlib `unittest`, not `pytest`, to preserve the no-external-dependency rule.
- Add tests under `tests/`: `test_loader.py`, `test_parser.py`, `test_rule_engine.py`, `test_evaluator.py`, `test_reporter.py`, and `test_integration_cli.py`.
- For every rule-engine check, include at least one positive example that must flag and one negative example that must not flag.
- Add the required ambiguous sample fixture and verify each sample line triggers at least one finding.
- Add acceptance tests for lowercase EARS rejection, `user-friendly` measurable suggestion, happy-path-only prompt, oblique symbol detection, report generation, and the canonical command.
- Run after each module during implementation: `python -m unittest tests.test_loader`, then parser, rule engine, evaluator, reporter, and finally `python -m unittest`.
- Final smoke command: `python -m linter.claritygate specs/claritygate-mvp/requirements.md`.

## Assumptions

- Existing source-of-truth docs remain read-only: `SKILL.md`, `specs/claritygate-mvp/requirements.md`, and `specs/claritygate-mvp/design.md`.
- `.kiro/specs/claritygate-mvp/` mirrors are not changed in this phase.
- The top-level `linter/` shim is acceptable because it is the smallest way to satisfy the exact requested CLI command while keeping implementation in `src/linter/`.
- Report output file creation is allowed as normal CLI behavior, but tests should write reports only into temporary directories.
