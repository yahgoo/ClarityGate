# ClarityGate Demo Video — Full Workflow Reference

## Prerequisites

| Tool | Check |
|------|-------|
| ffmpeg / ffprobe | `which ffmpeg` |
| npx + HyperFrames | `npx hyperframes --version` (≥ 0.7.76) |
| Playwright + Chromium | `npx playwright install chromium` (one-time) |
| Node.js | v20+ |
| Backend server | `curl http://127.0.0.1:8000/docs` → 200 |
| Frontend server | `curl http://127.0.0.1:5173` → 200 |
| TTS (optional) | `.tts-venv` with `kokoro-onnx` + `soundfile` |

## Starting Servers

```bash
# Backend (from repo root)
python3 -m uvicorn backend.main:create_app --factory --host 127.0.0.1 --port 8000 &

# Frontend (from frontend/)
cd frontend && npm run dev -- --host 127.0.0.1 --port 5173 &
```

## Demo Input (exact)

```markdown
# Demo Requirements

The system should support login quickly.
The system shall handle user data.
If needed, the system may notify users.
THE System SHALL display the dashboard.
```

## Screenshot Capture

Use Playwright headless Chromium with explicit viewport:

```javascript
import { chromium } from 'playwright';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto('http://127.0.0.1:5173', { waitUntil: 'networkidle' });
// ... interact and screenshot
await page.screenshot({ path: 'scene-XX.png' });
```

**Hard gate**: every screenshot must be ≥ 1280×720. Preferred 1440×900.

**Do NOT use MCP browser-use screenshots** — they are limited to ~394×425 viewport.

### Required Scenes (8-scene full video)

| # | Filename | State |
|---|----------|-------|
| 1 | scene-01-empty-app.png | App loaded, empty |
| 2 | scene-02-demo-input.png | Demo text pasted |
| 3 | scene-03-refused-result.png | After Analyze: REFUSED 24/100 |
| 4 | scene-04-mission-board.png | Mission Board scrolled into view |
| 5 | scene-05-findings.png | Findings with check IDs + Apply fix |
| 6 | scene-06-after-apply-rewrite.png | After one Apply fix: score 44 |
| 7 | scene-07-accepted-rewrites.png | Accepted Rewrites section |
| 8 | scene-08-report-preview.png | Full Report Markdown expanded |

## HyperFrames Composition Structure

```html
<div data-composition-id="claritygate-demo-final"
     data-width="1920" data-height="1080"
     data-duration="90" data-start="0" data-no-timeline>

  <div class="clip" id="scene-01" data-start="0" data-duration="8">
    <div class="app-frame">
      <img src="assets/screenshots/scene-01-empty-app.png" />
    </div>
    <div class="lower-third">ClarityGate — Requirements Quality Gate</div>
  </div>
  <!-- ... repeat for scenes 2-8 ... -->

  <!-- Scene-aligned voiceover -->
  <audio data-start="1" data-duration="5" data-track-index="1"
         data-volume="1" src="assets/voice/scene-01.wav"></audio>
  <!-- ... one per scene ... -->

  <!-- Background music -->
  <audio data-start="0" data-duration="90" data-track-index="10"
         data-volume="0.10" src="assets/music/...mp3"></audio>
</div>
```

### Critical: Opacity Pitfall

**NEVER** set `.clip { opacity: 0 }` in CSS. HyperFrames controls clip visibility exclusively via `data-start`/`data-duration`. CSS opacity overrides this and produces blank frames.

Correct CSS:
```css
.clip { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
```

## SRT Naming Rule

MP4 and SRT must share the exact basename:
- `claritygate-demo-final.mp4`
- `claritygate-demo-final.srt`

This enables VLC to auto-load subtitles.

## Voiceover / SRT Sync Rule

- Generate **one WAV per scene** (not one compressed full-script track).
- Mount each `<audio>` at `data-start` = scene start + ~1s offset.
- SRT timestamps must be scene-aligned with the voiceover and remain visible long enough to read.
- Use Kokoro-82M `af_heart` voice at speed 0.95 for natural pacing.
- If TTS unavailable: produce silent video + SRT. Never use macOS `say`/Samantha.

### TTS Command

```bash
HYPERFRAMES_PYTHON="/path/to/.tts-venv/bin/python" \
  npx hyperframes tts --voice af_heart --speed 0.95 \
  -o assets/voice/scene-XX.wav /tmp/voX.txt
```

## Scene Timing (90s video)

| Scene | Start | Duration | VO start |
|-------|-------|----------|----------|
| 1 | 0 | 8 | 1 |
| 2 | 8 | 10 | 9 |
| 3 | 18 | 12 | 19 |
| 4 | 30 | 12 | 31 |
| 5 | 42 | 13 | 43 |
| 6 | 55 | 13 | 56 |
| 7 | 68 | 10 | 69 |
| 8 | 78 | 12 | 79 |

## Final Verification Commands

```bash
# Stream info
ffprobe -v error -show_entries format=duration,bit_rate \
  -show_entries stream=codec_type,codec_name,width,height \
  -of default=nw=1 claritygate-demo-final.mp4

# Contact sheet (1 frame per 10s, tiled 4×2)
ffmpeg -y -i claritygate-demo-final.mp4 \
  -vf "fps=1/10,scale=480:-1,tile=4x2" -frames:v 1 \
  final-contact-sheet.jpg

# Git safety
git diff --name-status HEAD -- backend frontend tests_backend \
  src/linter tests specs .kiro data demo-ui PLAN.md SKILL.md \
  requirements-backend.txt
# Expected: no output
```

## Failure Conditions (stop and report)

- Any screenshot below 1280×720
- Contact sheet shows blank/dark frames
- Contact sheet shows motion graphics instead of real app UI
- HyperFrames render fails
- Voiceover unavailable AND you're about to use robotic voice
- Product code paths show changes in git diff

## Final Report Checklist

- [ ] MP4 path + duration + resolution + bitrate
- [ ] SRT path + basename matches MP4
- [ ] Screenshot method + dimensions
- [ ] Source contact sheet path
- [ ] Final contact sheet path
- [ ] Voiceover method (scene-aligned / silent)
- [ ] Scene VO file durations
- [ ] "I visually verified the final contact sheet shows the real ClarityGate app UI."
- [ ] Confirmation no product code changed
