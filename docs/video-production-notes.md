# ClarityGate Demo Video — Production Notes

## Summary

The final demo video (`output/demo-artifacts/claritygate-demo-final.mp4`) is a 90-second, 1920×1080 H.264+AAC render produced by HyperFrames v0.7.76 from real full-viewport ClarityGate app screenshots, with scene-aligned neural voiceover and matching SRT subtitles.

## Failed Approaches (chronological)

| Attempt | Problem |
|---------|---------|
| MCP browser-use `take_screenshot` | Viewport limited to 394×425 px — too small for video |
| macOS `screencapture -x` | Sandbox restriction: "could not create image from display" |
| Brave `--headless --screenshot` | Cancelled / unreliable in sandbox |
| Playwright (first try) | Browsers not installed; needed `npx playwright install chromium` |
| First HyperFrames render | **Blank frames** — caused by `.clip { opacity: 0 }` in CSS overriding HyperFrames visibility control |
| macOS `say` (Samantha voice) | Robotic, unacceptable for demo |
| Single compressed voiceover.wav (27s) | Voice finished at ~28s while video is 90s; SRT spans full duration — completely out of sync |

## Successful Pipeline

1. **Playwright headless Chromium** at 1440×900 viewport captures 8 real app screenshots.
2. **HyperFrames composition** (`output/demo-artifacts/hyperframes-full/index.html`) — 8 scenes, each a `.clip` div with `data-start`/`data-duration`, real screenshots as `<img>` inside a styled `.app-frame`.
3. **Kokoro-82M neural TTS** (`af_heart`, American female) generates 8 scene-aligned WAV files via `npx hyperframes tts`.
4. **Background music** at 10% volume under voiceover.
5. **SRT** with timestamps matching voiceover start per scene.
6. **Render**: `npx hyperframes render --quality high`.
7. **Verification**: extract frames at 10s intervals → tile into contact sheet → visually confirm real app UI.

## Key Lessons

- **Never set `.clip { opacity: 0 }`** — HyperFrames manages visibility via data attributes.
- **One voiceover WAV per scene**, not one full-script track. Mount at scene start + 1s.
- **SRT timestamps must match voiceover starts**, not scene boundaries.
- **MCP browser screenshots are too small** for video — always use Playwright with explicit viewport.
- **Always verify with a contact sheet** before reporting success.

## Artifact Locations

| Artifact | Path |
|----------|------|
| Final MP4 | `output/demo-artifacts/claritygate-demo-final.mp4` |
| Final SRT | `output/demo-artifacts/claritygate-demo-final.srt` |
| HyperFrames composition | `output/demo-artifacts/hyperframes-full/index.html` |
| Screenshots (1440×900) | `output/demo-artifacts/hyperframes-full/assets/screenshots/` |
| Scene voiceover WAVs | `output/demo-artifacts/hyperframes-full/assets/voice/` |
| Source contact sheet | `output/demo-artifacts/hyperframes-full/source-contact-sheet.jpg` |
| Final contact sheet | `output/demo-artifacts/hyperframes-full/final-contact-sheet.jpg` |
| Capture script | `output/demo-artifacts/hyperframes-full/capture-full.mjs` |
| 3-scene proof-of-concept | `output/demo-artifacts/hyperframes-test/` |

> **Note**: `output/` is gitignored. All video artifacts are local-only and not committed.

## Reusable Skill

A project-local Codex skill documenting this workflow lives at:

```
.agents/skills/claritygate-demo-video/
```

Invoke it when asked to create, repair, or verify the ClarityGate demo video.
