# ClarityGate Demo Video — Recording & Overlay Plan

**Target length:** 90–150 seconds
**Format:** Browser screen recording + lower-third text overlays + optional voiceover
**Route:** Brag-style launch clip (current repo, just shipped, local-only demo)

---

## Video Objective

Show ClarityGate turning ambiguous requirements into Qoder-ready requirements through a deterministic linter, live rewrite loop, and frontend-derived Mission Board.

Key messages:
- Deterministic scoring — no AI hallucination
- Frozen core pipeline, full-stack API wrapper
- One-click rewrite acceptance with live score updates
- Mission Board tracks progress toward Quest-ready

---

## Demo Input (exact)

```markdown
# Demo Requirements

The system should support login quickly.
The system shall handle user data.
If needed, the system may notify users.
THE System SHALL display the dashboard.
```

---

## Expected Values (Phase 5 validated)

| Metric | Initial | After one fix |
|--------|---------|---------------|
| Verdict | REFUSED | REFUSED |
| Score | 24/100 | 44/100 |
| Requirements | 4 | 4 |
| Defects | 9 | 6 |
| Clarifications | 1 | 1 |
| Findings | 10 | 8 |

Values depend on using the exact demo input above.

---

## Scene-by-Scene Shotlist

### Scene 1 — Title Card (0:00–0:06)

| Element | Detail |
|---------|--------|
| Screen | App header visible at `http://127.0.0.1:5173` |
| Action | Hold on empty state |
| Voiceover | "ClarityGate — a requirements quality gate for AI-driven development." |
| Overlay | `ClarityGate — Requirements Quality Gate` |
| Focus | Full window, header centered |

### Scene 2 — Problem (0:06–0:16)

| Element | Detail |
|---------|--------|
| Screen | Import panel, textarea empty |
| Action | Cursor hovers over textarea |
| Voiceover | "Vague specs cause AI build drift. There's no compiler error for ambiguity." |
| Overlay | `Ambiguous specs → AI drift` |
| Focus | Left panel, crop to import area |

### Scene 3 — Import (0:16–0:28)

| Element | Detail |
|---------|--------|
| Screen | Textarea being filled |
| Action | Paste demo input (pre-copied) |
| Voiceover | "Paste a requirements spec. ClarityGate scans every line deterministically." |
| Overlay | `Paste → Scan → Score` |
| Focus | Left panel textarea, show all 4 requirement lines |

### Scene 4 — Analyze (0:28–0:36)

| Element | Detail |
|---------|--------|
| Screen | Click Analyze button |
| Action | Button click, brief loading state |
| Voiceover | "Fifteen rule checks run. No AI. No network. Pure Python." |
| Overlay | `Deterministic scan — 15 checks` |
| Focus | Analyze button → results panel appearing |

### Scene 5 — Result (0:36–0:48)

| Element | Detail |
|---------|--------|
| Screen | Score card + stats row |
| Action | Hold on REFUSED verdict, score 24 |
| Voiceover | "Score 24 out of 100. Verdict: REFUSED. Nine defects, one clarification." |
| Overlay | `REFUSED — 24/100 — 9 defects` |
| Focus | Crop to score card + stats row (right panel top) |

### Scene 6 — Findings (0:48–1:02)

| Element | Detail |
|---------|--------|
| Screen | Findings list |
| Action | Slow scroll through findings |
| Voiceover | "Each finding maps to a line, a check ID, and a suggested rewrite." |
| Overlay | `Line-level findings with check IDs` |
| Focus | Findings section, show 2–3 findings with badges visible |

### Scene 7 — Rewrite (1:02–1:14)

| Element | Detail |
|---------|--------|
| Screen | One finding with "Apply fix" button |
| Action | Click "Apply fix" |
| Voiceover | "Accept a suggested fix. One click. The score recalculates instantly." |
| Overlay | `Apply fix → live re-score` |
| Focus | Crop to the finding + Apply button |

### Scene 8 — Live Update (1:14–1:24)

| Element | Detail |
|---------|--------|
| Screen | Score card updates, Accepted Rewrites appears |
| Action | Hold on updated score 44, Accepted Rewrites section |
| Voiceover | "Score jumps from 24 to 44. Findings drop from ten to eight." |
| Overlay | `24 → 44 — findings 10 → 8` |
| Focus | Score card + Accepted Rewrites section |

### Scene 9 — Mission Board (1:24–1:36)

| Element | Detail |
|---------|--------|
| Screen | Mission Board panel |
| Action | Scroll to Mission Board, show 2/5 progress |
| Voiceover | "The Mission Board tracks your path to Quest-ready. All derived in the frontend." |
| Overlay | `Mission Board — progress to Quest-ready` |
| Focus | Mission Board with progress meter and mission list |

### Scene 10 — Report (1:36–1:44)

| Element | Detail |
|---------|--------|
| Screen | Full Report (Markdown) expanded |
| Action | Click to expand report preview |
| Voiceover | "Full Markdown report — ready for review or version control." |
| Overlay | `Full report — Markdown export` |
| Focus | Report preview area, scroll slightly |

### Scene 11 — Close (1:44–1:54)

| Element | Detail |
|---------|--------|
| Screen | Full app view or fade to solid background |
| Action | Hold / fade out |
| Voiceover | "ClarityGate. Stop drift at the source. Built with Qoder." |
| Overlay | `ClarityGate — Qoder-ready requirements` |
| Focus | Full window or end card |

---

## Text Overlay Style Rules

- Position: lower-third, left-aligned
- Font: system sans-serif, 16–20px equivalent
- Background: semi-transparent dark pill (rgba(0,0,0,0.7))
- Color: white text
- Duration: visible for scene length, fade in/out 0.3s
- Max words: 9 per overlay
- No exclamation marks, no emoji
- Do not claim: cloud deployment, Firebase, AI rewriting, persisted missions, contest win

---

## Recording Checklist

- [ ] Start backend: `python3 -m uvicorn backend.main:create_app --factory --host 127.0.0.1 --port 8000`
- [ ] Start frontend: `cd frontend && npm run dev -- --host 127.0.0.1 --port 5173`
- [ ] Verify: `curl -i http://127.0.0.1:8000/docs` → HTTP 200
- [ ] Verify: `curl -i http://127.0.0.1:5173` → HTTP 200
- [ ] Set browser window to 1440×900 (or 1920×1080 for full HD)
- [ ] Set browser zoom to 100%
- [ ] Clear textarea and reset filename to `requirements.md`
- [ ] Copy demo input to clipboard
- [ ] Start screen recording (OBS / QuickTime / ScreenFlow)
- [ ] Follow shotlist scenes 1–11
- [ ] Stop recording
- [ ] Save raw: `output/demo-artifacts/claritygate-demo-raw.mov`
- [ ] Add text overlays in editor per scene table
- [ ] Record voiceover (optional, per scene scripts above)
- [ ] Export final: `output/demo-artifacts/claritygate-demo-final.mp4`

---

## File Naming

| Artifact | Path |
|----------|------|
| Raw recording | `output/demo-artifacts/claritygate-demo-raw.mov` |
| Final edited | `output/demo-artifacts/claritygate-demo-final.mp4` |
| This plan | `docs/video-recording-overlay-plan.md` |

---

## Voiceover Direction

Use an American female voiceover: clear, confident, and demo-focused, with a practical founder-style delivery. Keep the pace brisk but understandable. The voiceover should explain what the viewer is seeing while the text overlays highlight only the key proof points.

| Attribute | Direction |
|-----------|----------|
| Voice | American female |
| Tone | Confident, clear, founder-demo style |
| Pace | Medium-fast, suited to 90–150s demo |
| Delivery | Polished but natural, not salesy |
| Emotion | Calm urgency, practical confidence |

Captions and text overlays should support the voiceover, not duplicate every spoken line. Overlays carry the proof points (scores, verdicts, counts); the voice carries the narrative.

---

## Notes

- Local-only demo. No cloud, no deployment, no auth.
- Missions are frontend-derived, not persisted in backend.
- Rewrites use suggested_rewrite exactly as returned by the frozen linter.
- If recording exceeds 150s, trim Scene 10 (Report) or Scene 2 (Problem).
- Background music optional: low-fi, fade under voiceover, no lyrics.
