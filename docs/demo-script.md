# ClarityGate — Demo Video Script

> For the full-stack (Option 2) recording flow, see [docs/fullstack-demo-runbook.md](fullstack-demo-runbook.md).

Target length: **2 minutes 30 seconds**

---

## COLD OPEN (0:00–0:15)

**[Screen recording: terminal with a vague requirements.md open]**

> "What happens when you hand *this* to an AI coding agent?"

**[Beat. Let the viewer read: "The system should be fast."]**

> "It guesses. It drifts. It builds the wrong thing. And you don't find out until code review."

---

## PROBLEM (0:15–0:35)

**[Slide or terminal: the words "AI DRIFT" appear]**

> "In spec-driven workflows, vague requirements are *bugs* — but they compile fine.
> There's no linter for them. Until now."

**[Terminal: `cd ClarityGate`]**

> "ClarityGate is a requirements-quality linter that catches ambiguity *before*
> your AI agent builds from it."

---

## DEMO: BAD SPEC (0:35–1:20)

**[Terminal: show `data/samples/ambiguous-requirements.md`]**

> "Here's a typical feature spec. 'Fast.' 'Should.' 'Obviously.' 'As appropriate.'
> Every line is a liability."

**[Type command:]**
```bash
python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/report.md
```

**[Terminal output appears:]**
```
Requirements scanned: 6
Findings: 23
Verdict: REFUSED
Quest Readiness Score: 0/100
```

> "Twenty-three findings. Six lines. The gate refuses to certify this spec.
> Exit code 2 — that's not a crash, that's a *verdict*."

**[Open /tmp/report.md in editor]**

> "The report gives you a findings table, line by line, check by check —
> and a Clarification Queue with two-option questions. No more 'what did you mean?'"

---

## DEMO: CLEAN SPEC (1:20–1:50)

**[Terminal: show `data/samples/clean-ears-requirements.md`]**

> "Same feature. Rewritten with EARS syntax. Measurable thresholds.
> An explicit error path."

**[Type command:]**
```bash
python3 -m linter.claritygate data/samples/clean-ears-requirements.md --out /tmp/clean.md
```

**[Terminal output:]**
```
Requirements scanned: 3
Findings: 0
Verdict: CERTIFIED
Quest Readiness Score: 100/100
```

> "Zero findings. Certified. Now *this* is safe to hand to Qoder Quest Mode."

---

## QODER ANGLE (1:50–2:15)

**[Screen: Qoder IDE with the project open]**

> "And the meta part? ClarityGate itself was built entirely in Qoder Quest Mode —
> spec-driven, test-first, zero external dependencies. Thirty-six tests, fifteen
> deterministic checks, pure Python stdlib. It practices what it preaches."

---

## CLOSE (2:15–2:30)

**[Terminal: the two verdicts side by side]**

> "Bad spec in, bad AI build out. ClarityGate is the gate that stops drift
> at the source. Built with Qoder. For the #QoderHackathon."

**[End card: GitHub link + #BuildWithQoder]**

---

## Production Notes

- Record terminal at 14pt font, dark theme, full screen.
- Use `asciinema` or OBS for terminal capture.
- Keep cuts tight — no dead air while commands run (< 1s each).
- Background music: optional, low-fi, fade under voiceover.
- Captions recommended for accessibility and silent scrolling.
