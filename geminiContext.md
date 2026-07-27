Here is a concise summary formatted specifically to copy-paste or save as a context file (`CONTEXT.md` / prompt) for **Codex**:

---

# Hackathon Context & Build Strategy

### 🎯 Project Overview & Constraints

* **Deadline:** August 2, 2026.
* **Commitments:** Full-day seminars on **July 29 & July 30, 2026**.
* **Primary Stack & Tools:**
* **Codex (Pro Plan / GPT-5.5):** Architecture planning, producing modular `SPEC.md` files, prompt engineering, and surgical refactoring.
* **Alibaba Qoder IDE:** Main autonomous coding engine using **Qwen3.8-Max-Preview**.
* **Credits Available:**
* Codex: Pro Plan with 100% weekly quota + SGD 130 credit safety net.
* Qoder: 2,000 credits available.





---

### 💰 Credit Optimization Strategy (Qoder)

* **Model Choice:** **Qwen3.8-Max-Preview** is the designated primary model.
* **Discount Windows (UTC+8 / SGT):**
* **Regular Hours (08:00–22:00 SGT):** 90% discount.
* **Off-Peak Hours (22:00–08:00 SGT):** **98% discount** (50x credit multiplier saving).


* **Execution Strategy:**
* **Daytime (08:00–22:00 SGT):** Use **Codex (GPT-5.5)** to write specs and **Qoder Agent Mode (Single Agent)** for light reviews.
* **Nighttime (22:00–08:00 SGT):** Use **Qoder Experts Mode (Multi-Agent Parallel)** for heavy batch generation and automated testing at 2% cost.



---

### ⏰ Workflow & Timeline Execution

| Date / Time Window | Phase | Primary Tool & Mode | Tasks |
| --- | --- | --- | --- |
| **July 26 – July 28** | **Planning & Specs** | Codex (`GPT-5.5`) | Finalize architecture, schema, API contracts, and modular `SPEC.md` files. |
| **July 28 @ 22:01 SGT** | **Phase 1 Overnight** | Qoder Scheduled Task (`Experts Mode` / `Qwen3.8-Max`) | Autonomous execution of Database & Backend APIs overnight. |
| **July 29 (Seminar 1)** | **Phase 2 Prep** | Codex (Day) $\rightarrow$ Scheduled Task (22:01) | Inspect Phase 1 PR in morning. Prepare `SPEC_FRONTEND.md`. Schedule overnight build. |
| **July 30 (Seminar 2)** | **Phase 3 Prep** | Codex (Day) $\rightarrow$ Scheduled Task (22:01) | Inspect UI build. Prepare `SPEC_POLISH.md` (integration, error states). Schedule overnight sweep. |
| **July 31 – Aug 1** | **Polish & Refactor** | Codex & Qoder Agent Mode | Surgical bug fixes, UI styling tweaks, edge-case testing, and README generation. |
| **Aug 2** | **Submission** | Feature Freeze | Final deployment checks, pitch deck, and submission. |

---

### ⚙️ Automation Rules for Codex

1. When asked for code plans, **Codex must output self-contained `SPEC.md` files** and **structured Qoder prompts** designed for hands-off execution.
2. Prompts generated for Qoder must explicitly instruct sub-agents (Lead, Full-Stack, QA) to operate iteratively, run build scripts, and self-debug without stopping for manual input.
3. Every scheduled overnight task prompt in Qoder must explicitly specify **Qwen3.8-Max-Preview** on all sub-agent roles.