# ClarityGate — Requirements Engineering Linter

## Problem Statement

Poorly written requirements are expensive to fix when discovered late in the development lifecycle. A large share of software defects originate in ambiguous or incomplete specifications rather than in implementation bugs, and rework attributable to unclear requirements can account for a substantial portion of total development cost.

In AI-assisted, spec-driven workflows this problem compounds. When a requirement is vague, a coding agent fills the gap with its own assumptions, producing inconsistent behavior across runs — a failure mode known as **AI drift**. There is a need for an automated quality gateway that catches requirement defects before they are turned into design, code, or tests.

## Goals

- **Enforce syntax**: Validate that every acceptance criterion conforms to one of the six canonical EARS patterns.
- **Detect smells**: Flag linguistic smells such as vague adjectives, unquantified adverbs, and passive voice.
- **Measure clarity**: Flag requirements that are too abstract to be testable.
- **Surface tacit knowledge**: Identify missing error paths and unstated assumptions through abductive reasoning.
- **MVP scope**: Provide a lightweight, hackathon-ready tool that scans a `requirements.md` file and reports findings.

## Non-Goals

- Generating code, design documents (`design.md`), or task breakdowns (`tasks.md`).
- Integrating with enterprise requirements-management tooling (e.g., IBM DOORS).
- Replacing human review; the tool produces a clarification queue for the author, not an authoritative verdict.

## Target Users

- **Software Engineers** who hand unambiguous specs to coding agents.
- **Product Managers** who want requirements to be testable and complete before handoff.
- **AI Agents** participating in spec-driven workflows that need an unambiguous source of truth to avoid rework.

## User Stories

- **US1 (Linguistic Scan)**: As a developer, I want to scan my `requirements.md` for vague terms like "fast" or "scalable" so that I can replace them with quantifiable metrics.
- **US2 (EARS Validation)**: As a PM, I want to verify that every acceptance criterion uses a valid EARS structure so that requirements are testable.
- **US3 (Completeness Check)**: As a quality engineer, I want the tool to flag missing "Unwanted Behavior" (IF-THEN) criteria so that happy-path bias is avoided.
- **US4 (Ambiguity Resolution)**: As a spec author, I want the tool to present two-option questions for ambiguous phrases (e.g., "remove" vs. "soft-delete") so that my intent is clarified.
- **US5 (Tacit Gap Detection)**: As a developer, I want to flag requirements that rely on unstated domain knowledge so that hidden assumptions are made explicit.

## Functional Requirements

- **FR1**: The system SHALL parse a `requirements.md` file and detect EARS keywords (WHEN, WHILE, WHERE, IF, THEN, SHALL).
- **FR2**: The system SHALL flag non-mandatory imperatives ("should", "must", "may", "will") used in place of "SHALL".
- **FR3**: The system SHALL flag linguistic smells, including unquantified adjectives and adverbs ending in "-ly".
- **FR4**: The system SHALL detect passive-voice constructions in requirement statements.
- **FR5**: The system SHALL flag singularity violations where one requirement contains more than one "SHALL".
- **FR6**: The system SHALL produce a Quality Report summarizing detected ambiguities and completeness gaps.

## Non-Functional Requirements

- **NFR1 (Accuracy)**: The system SHALL achieve an F-score of at least 0.77 in detecting ambiguous words on a held-out sample of 50 labeled requirements.
- **NFR2 (Performance)**: The system SHALL complete a scan of a standard feature spec (approximately 20 requirements) within 10 seconds on a laptop-class machine.
- **NFR3 (Accessibility)**: The Quality Report SHALL be emitted in human-readable Markdown.
- **NFR4 (Portability)**: The tool SHALL run from the command line with no external service dependency, so it works in Qoder, Kiro, and Cursor workspaces.

## Acceptance Criteria

- **AC1**: WHEN the user runs a scan on a file containing lowercase EARS keywords, THE SYSTEM SHALL reject the file and list the required UPPERCASE keywords.
- **AC2**: WHEN a requirement uses a vague adjective (e.g., "user-friendly"), THE SYSTEM SHALL flag the line as "unverifiable" and suggest a measurable replacement.
- **AC3**: IF a feature description contains only happy-path scenarios, THEN THE SYSTEM SHALL prompt the user to add "Unwanted Behavior" (IF-THEN) criteria.
- **AC4**: WHEN a scan is in progress on a file exceeding 20 requirements, THE SYSTEM SHALL display a progress indicator.
- **AC5**: WHERE an oblique symbol ("/") combines synonyms (e.g., "symbol/sign"), THE SYSTEM SHALL flag the line for referential ambiguity.
- **AC6**: WHEN the scan completes, THE SYSTEM SHALL write a Quality Report to a file and print a summary to stdout.

## Open Questions

- Should ClarityGate rewrite the file automatically, or only propose changes in a separate clarification queue?
- How should the tool handle "Complex" EARS patterns that combine more than two keywords?
- Is read access to project chat transcripts feasible for detecting silent intent within a hackathon time budget?
