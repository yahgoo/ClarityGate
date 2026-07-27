---
name: claritygate-demo-video
description: Create, repair, and verify ClarityGate demo videos using real full-viewport app screenshots, HyperFrames compositions, matching MP4/SRT subtitle files, and strict visual verification. Use when asked to make, fix, inspect, or document the ClarityGate demo video, especially when prior renders are cropped, blank, motion-only, or subtitle/voiceover sync is wrong.
---

# ClarityGate Demo Video

## Rules

1. **Always use real app screenshots** — never pure motion graphics as the primary visual.
2. **Screenshot method**: Playwright headless Chromium with explicit viewport (preferred 1440×900, minimum 1280×720). Do NOT use MCP browser screenshots if limited to 394×425.
3. **HyperFrames composition** lives under `output/demo-artifacts/`. Do NOT set `.clip { opacity: 0 }` — HyperFrames controls visibility via `data-start`/`data-duration`.
4. **MP4 and SRT must share the same basename** (e.g. `claritygate-demo-final.mp4` + `claritygate-demo-final.srt`) for VLC auto-loading.
5. **Voiceover**: If natural voice (Kokoro-82M `af_heart`) is available, generate scene-aligned audio files — one per scene, mounted at scene start. If unavailable, produce silent video with SRT. Never use macOS Samantha or robotic voices.
6. **SRT timing** must be scene-aligned with the voiceover and cover the spoken line long enough to read.
7. **Verification**: Extract frames at multiple timestamps, build a contact sheet, and visually confirm the real ClarityGate app UI is visible. Do NOT report success without this.
8. **Do not modify product code** (backend, frontend, src/linter, tests, specs, etc.).

## Quick Workflow

1. Confirm servers running (`curl` health checks on :8000 and :5173).
2. Capture screenshots with Playwright at 1440×900.
3. Verify all screenshots ≥ 1280×720.
4. Build HyperFrames composition HTML (scenes as `.clip` divs with `data-start`/`data-duration`).
5. Generate per-scene voiceover WAVs (if TTS available).
6. Create matching SRT.
7. `npx hyperframes check` → fix errors → `npx hyperframes render`.
8. Extract verification frames + contact sheet.
9. Visually inspect contact sheet — hard gate.
10. Report.

## Reference

See `references/claritygate-demo-video.md` for the full detailed workflow.
