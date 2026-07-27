# ClarityGate — Social Post Draft

## LinkedIn Version

---

🚧 "The system should be fast."

That sentence just cost your AI coding agent 3 hours of rework.

I built **ClarityGate** — a requirements-quality linter that catches vague, ambiguous, and untestable requirements *before* an AI agent builds from them.

Here's the problem: in spec-driven workflows, vague requirements are bugs that compile fine. There's no linter for them. When a coding agent hits "should be user-friendly," it guesses. Every run produces different assumptions. That's AI drift.

ClarityGate gates the spec:

→ Scans your requirements.md with 15 deterministic checks
→ Flags vague verbs, weak imperatives, passive voice, escape clauses, missing error paths
→ Enforces EARS syntax (the same structured patterns used in aerospace/defense specs)
→ Produces a Clarification Queue with two-option questions
→ Returns a Quest Readiness Score: CERTIFIED or REFUSED

Demo:
• Bad spec → 23 findings, score 0/100, REFUSED
• Clean spec → 0 findings, score 100/100, CERTIFIED

The meta part? ClarityGate itself was built entirely in @QoderOfficial Quest Mode — spec-driven, test-first, pure Python stdlib. 36 tests. Zero dependencies. It practices what it preaches.

Bad spec in, bad AI build out. ClarityGate stops drift at the source.

#QoderHackathon #BuildWithQoder @QoderOfficial @AlibabaCloud

---

## X / Twitter Version (shorter)

---

"The system should be fast." ← this just broke your AI build.

I built ClarityGate: a linter that catches vague requirements BEFORE your coding agent builds from them.

15 checks. EARS syntax enforcement. Quest Readiness Score.

Bad spec → REFUSED (0/100)
Clean spec → CERTIFIED (100/100)

Built entirely in @QoderOfficial Quest Mode. Pure Python. Zero deps. 36 tests.

Bad spec in, bad AI build out. Gate the spec. Stop the drift.

#QoderHackathon #BuildWithQoder @QoderOfficial @AlibabaCloud

---

## Attachment Suggestions

1. **Terminal screenshot**: side-by-side of REFUSED vs CERTIFIED output
2. **Report screenshot**: the Markdown findings table with the Clarification Queue
3. **Short clip** (15s): running the ambiguous sample and showing the verdict

## Posting Tips

- Post between 8–10 AM local time for max LinkedIn reach.
- Reply to your own post with the demo video link once published.
- Engage with every comment in the first hour (algorithm boost).
- Cross-post to X with the shorter version + clip.
