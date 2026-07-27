# ClarityGate — Submission Checklist

Deadline: **August 5, 2026**

## Required Deliverables

- [ ] Working ClarityGate CLI linter (DONE — 36/36 tests passing)
- [ ] Clean README with how to run in Qoder (DONE — `README.md`)
- [ ] Demo video, 2–3 minutes (TODO — see `docs/demo-script.md`)
- [ ] Social post on LinkedIn or X (TODO — see `docs/social-post-draft.md`)
- [ ] Submission form entry with:
  - [ ] Social post link
  - [ ] Demo video link

## Demo Video Requirements

- [ ] 2–3 minutes long
- [ ] Shows the project in action
- [ ] Explains the problem it solves (AI drift from vague specs)
- [ ] Demonstrates key features (scan, findings table, clarification queue, verdict)
- [ ] Clear, short, compelling

## Social Post Requirements

- [ ] Mentions the project (ClarityGate)
- [ ] Describes what it does
- [ ] Shares experience using Qoder
- [ ] Tags `@QoderOfficial` and `@AlibabaCloud`
- [ ] Includes `#QoderHackathon` and `#BuildWithQoder`
- [ ] Screenshots or short clip attached (recommended)

## Pre-Submission Verification

```bash
# Confirm tests still pass
python3 -m unittest -v

# Confirm CLI works end-to-end
python3 -m linter.claritygate data/samples/ambiguous-requirements.md --out /tmp/verify.md

# Confirm clean spec certifies
python3 -m linter.claritygate data/samples/clean-ears-requirements.md --out /tmp/verify-clean.md
```

## Judging Criteria Awareness

| Criterion | Weight | Our strength |
|-----------|--------|--------------|
| Use of Qoder | 30% | Built entirely in Quest Mode; spec-driven workflow |
| Innovation & creativity | 25% | First requirements-quality linter targeting AI drift |
| Impact / reach / engagement | 20% | Social post + demo video |
| Technical execution | 15% | 36 tests, 15 deterministic checks, zero dependencies |
| Presentation & UGC | 10% | Demo script + social draft prepared |

## Story Arc

1. **Problem**: Vague requirements cause AI drift — coding agents fill gaps with inconsistent assumptions.
2. **Solution**: ClarityGate gates the spec before the agent builds.
3. **Proof**: Bad spec → 23 findings, REFUSED. Clean spec → 0 findings, CERTIFIED.
4. **Qoder angle**: Built entirely with Qoder Quest Mode in a spec-driven workflow — practicing what it preaches.
