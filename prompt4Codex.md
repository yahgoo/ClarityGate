# Task

Convert the attached PLAN.md into a Qoder Experts Mode-ready prompt. Do not execute or implement anything yourself — your only job is to transform this planning document into a properly framed prompt that I will paste into Qoder later tonight (scheduled for 22:00 SGT execution).

# Why this matters

Qoder's Experts Mode requires prompts to explicitly state the end goal, repo context, tech constraints, quality requirements, and priorities, so its Lead Agent can decompose work across Full-Stack, QA, Reviewer, and Debug roles. Because this will run unattended overnight, the prompt must read like a complete handover note — I will not be present to clarify anything once it starts.

# Required Output Structure

Produce a single Markdown prompt using exactly this frame, populated with content from PLAN.md:

---
# Role & Objective
[State that Qoder is acting as an expert Python developer continuing an in-progress project called ClarityGate, and specify the exact scoped objective from PLAN.md's Summary section — the core linter engine only, no UI/backend/database.]

# Tech Stack
[Pull from PLAN.md: Python 3.11+, stdlib-only, unittest not pytest, src/linter/ layout with top-level linter/ shim package, no external dependencies.]

# Critical Rules & Constraints
[Convert PLAN.md's Assumptions and implementation constraints into numbered imperative rules, e.g.: work one module at a time, preserve read-only source-of-truth docs, do not touch .kiro/ mirrors, test reports must write to temp directories only, etc.]

# Project Structure
[Insert the exact file list from PLAN.md's Implementation Changes section: src/linter/ files, top-level linter/ shim files, tests/ files.]

# Rule Engine Decisions
[Insert PLAN.md's Rule Decisions section verbatim — the EARS casing rules, pattern validation logic, happy-path detection logic, pronoun/passive voice heuristics — since these are precise implementation decisions Qoder must follow exactly, not reinterpret.]

# Test Plan
[Insert PLAN.md's Test Plan section: the exact unittest commands to run after each module, the required fixture examples, and the final smoke test command.]

# Immediate Task
[State clearly: implement modules in this order — models.py, loader.py, parser.py, rule_engine.py, evaluator.py, reporter.py, claritygate.py, __main__.py, then the linter/ shim — running the corresponding test file after each module before proceeding to the next. Report back with a summary of what was built, test results, and any rule that was harder to implement than expected.]
---

# Formatting Requirements

- Keep all technical details from PLAN.md exact — do not simplify, paraphrase loosely, or drop any rule-engine decision.
- Do not add scope beyond what PLAN.md specifies (no database, no UI, no server).
- Output only the finished Qoder prompt in a single Markdown code block, ready for me to copy and paste directly into Qoder with no further editing.