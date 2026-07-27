# ClarityGate Full-Stack Demo Runbook

Recording guide for the Simplified Option 2 full-stack demo (local-only).

---

## Prerequisites

- Branch: `option2-fullstack`
- Backend dependencies installed (`fastapi`, `uvicorn`, `httpx`)
- Frontend npm dependencies installed (`cd frontend && npm install`)
- Local ports **8000** and **5173** available
- Note: `.venv-daytona` may not have uvicorn; system Python (`/opt/homebrew/bin/python3`) worked during validation

---

## Startup Commands

**Backend** (from repo root):

```bash
python3 -m uvicorn backend.main:create_app --factory --host 127.0.0.1 --port 8000
```

**Frontend** (from `frontend/`):

```bash
npm run dev -- --host 127.0.0.1 --port 5173
```

---

## Health Checks

```bash
curl -i http://127.0.0.1:8000/docs   # expect HTTP 200
curl -i http://127.0.0.1:5173        # expect HTTP 200
```

---

## Demo Input

Paste exactly this into the textarea:

```markdown
# Demo Requirements

The system should support login quickly.
The system shall handle user data.
If needed, the system may notify users.
THE System SHALL display the dashboard.
```

---

## Recording Flow

1. Open `http://127.0.0.1:5173`
2. Show the Import panel (filename defaults to `requirements.md`)
3. Paste the demo input
4. Click **Analyze**
5. Point out the **REFUSED** verdict and score (24/100)
6. Point out the stats row: 4 requirements, 9 defects, 1 clarification, 0 info
7. Point out the **Mission Board** — 1/5 complete, Quest-ready criteria visible
8. Scroll through findings — note line numbers, check IDs (AMB-VAGUE-VERB, EARS-IMPERATIVE, etc.)
9. Click **Apply fix** on one finding with a suggested rewrite
10. Show score/findings update (24 → 44, findings 10 → 8)
11. Show the **Accepted Rewrites** section
12. Click **Remove** on the accepted rewrite — score reverts
13. Apply a fix again, then click **Reset all** — rewrites cleared
14. Expand **Parsed Requirements** — shows 4 requirements with line numbers
15. Expand **Full Report (Markdown)** — shows complete linter report

---

## Suggested Voiceover Beats

Keep it concise and natural:

- "ClarityGate is a deterministic requirements-quality linter — no AI scoring, no hallucinated feedback."
- "The core pipeline is frozen and tested; the backend wraps it without modification."
- "The rewrite loop lets you accept suggested fixes and watch the score update live."
- "Missions are derived entirely in the frontend from the analysis response — nothing persisted server-side."
- "Built for Qoder handoff readiness: paste a spec, clear defects, reach Quest-ready."

---

## Known Expected Values (Phase 5 Validation)

| Metric | Value |
|--------|-------|
| Verdict | REFUSED |
| Score | 24/100 |
| Requirements | 4 |
| Defects | 9 |
| Clarifications | 1 |
| Info | 0 |
| Findings | 10 |
| After one apply fix | Score 44, findings 8, defects 6 |

Exact values change only if the demo input changes.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `127.0.0.1 refused to connect` | Start both servers (see Startup Commands) |
| Backend fails in `.venv-daytona` | Use system `python3` (Homebrew) |
| Port 8000/5173 occupied | `lsof -iTCP:8000 -sTCP:LISTEN` to identify; do not kill unrelated processes |
| `claritygate.db` in project root | Gitignored runtime artifact — safe to ignore |
| `node_modules`/`dist` visible | Gitignored — not committed |

---

## Final Pre-Recording Checklist

```bash
python3 -m unittest discover -s tests -v          # 36/36
python3 -m unittest discover -s tests_backend -v  # 53/53
cd frontend && npm run build                      # success
git status --short                                # no tracked changes
```

Then do a quick browser smoke test of the full flow above before hitting record.
