# ClarityGate

A requirements-ambiguity linter for spec-driven development. ClarityGate catches
"requirement bugs" before they propagate to design, code, and tests — practicing
what it preaches by holding its own specs to a strict, testable standard.

## What it does

- **Enforces EARS syntax** — every acceptance criterion must conform to one of the
  six canonical EARS patterns (`WHEN … THE SYSTEM SHALL …`, etc.).
- **Detects linguistic smells** — vague adjectives, unquantified adverbs, passive
  voice, pronoun ambiguity, oblique symbols, and escape clauses.
- **Surfaces tacit knowledge** — flags missing error paths and unstated assumptions
  through abductive reasoning.
- **Produces a Clarification Queue** — two-option questions that turn ambiguity into
  a concrete decision for the spec author.

## Why

In AI-assisted workflows, vague requirements cause **AI drift**: a coding agent fills
the gap with its own inconsistent assumptions. ClarityGate is the quality gateway that
stops drift at the source.

## Current scope

The completed phase is a **core CLI linter only** — a five-stage pipeline (loader,
parser, rule engine, evaluator, reporter) that scans a `requirements.md` file and
emits a Markdown Quality Report plus a stdout summary. There is no UI, no backend
server, no database, and no network calls.

## Requirements

- Python 3.11+
- Standard library only (no `pip install` needed)

## Running tests

```bash
python3 -m unittest -v
```

Or run a single module:

```bash
python3 -m unittest tests.test_rule_engine -v
```

> If your environment provides `python` instead of `python3`, substitute accordingly.

## Running the CLI

```bash
python3 -m linter.claritygate <path-to-requirements.md> [--out <report-path>]
```

Example with a temporary output report:

```bash
python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/my-report.md
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0`  | Spec certified — no refusal-level findings |
| `2`  | Spec **REFUSED** — refusal-level findings detected (e.g., lowercase EARS keywords, missing EARS keywords, implementation leakage). This is a linter verdict, not a crash. |

### Demo samples

- `data/samples/ambiguous-requirements.md` — intentionally vague spec (triggers REFUSED)
- `data/samples/clean-ears-requirements.md` — well-formed EARS spec (triggers CERTIFIED)

## Project layout

```
ClarityGate/
├── SKILL.md                 # IDE-agnostic instruction set (Qoder / Kiro / Cursor / Qwen)
├── README.md
├── .gitignore
├── src/linter/              # Core linter implementation
│   ├── models.py            # Shared dataclasses
│   ├── loader.py            # UTF-8 file reader
│   ├── parser.py            # Markdown requirement extractor
│   ├── rule_engine.py       # 15 deterministic checks
│   ├── evaluator.py         # Scoring and verdict
│   ├── reporter.py          # Markdown report writer
│   └── claritygate.py       # CLI orchestration
├── linter/                  # Minimal shim for `python -m linter.claritygate`
├── tests/                   # stdlib unittest suite (36 tests)
├── data/samples/            # Demo input files
├── docs/                    # Demo handoff materials
├── specs/
│   └── claritygate-mvp/     # Canonical MVP spec (source of truth)
└── .kiro/specs/claritygate-mvp/   # Kiro mirror of the MVP spec
```

## Getting started

1. Read `SKILL.md` for the enforceable rules.
2. Run the demo: `python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/report.md`
3. Open `/tmp/report.md` to see the Clarification Queue and findings table.
4. Author or review specs under `specs/claritygate-mvp/`.
