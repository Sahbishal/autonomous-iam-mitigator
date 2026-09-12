# Tech Zephyr 4.0 Hackathon Pitch Deck
## Autonomous Cloud IAM Least-Privilege Mitigator (Problem Statement #10)

### Slide 1: Title & Team
* **Project Name**: Autonomous Cloud IAM Least-Privilege Mitigator
* **Event**: Tech Zephyr 4.0 — Agentic AI Hackathon
* **Problem Statement**: #10 — Cloud Security & Autonomous Privilege Reduction
* **Tagline**: Self-healing IAM optimization through simulation feedback and service dependency discovery.

---

### Slide 2: The Problem
* **Over-Privileged Cloud Credentials**: Over 80% of cloud security breaches involve overly broad IAM roles (e.g. `iam:PassRole`, wildcard `*`, `storage.delete`).
* **Why Rule Engines Fail**: Static analyzers assume `0 direct user logs = safe to delete`. They strip permissions that background microservices secretly rely on, causing catastrophic production outages.
* **The Dilemma**: Security teams fear breaking production services, so over-privileged roles remain active for years.

---

### Slide 3: Our Solution — The Autonomous IAM Agent
* An intelligent security agent that **simulates, learns, and adapts**.
* Runs an explicit **OBSERVE → ANALYZE → PLAN → ACT → EVALUATE → ADAPT → VERIFY** loop.
* Combines **Access History Log Analytics**, **NetworkX Service Dependency Graphs**, and a **Cloud Policy Simulator**.

---

### Slide 4: System Architecture
* **Frontend**: React + Tailwind + Live Agent Loop Streaming (SSE) + Recharts.
* **Backend**: FastAPI + Pydantic + SQLite + NetworkX.
* **Simulator**: Synthetic Cloud Environment modeling Users, Roles, Resources, Microservices, and Traffic.
* **Tool Layer**: 12 deterministic tools for inspection, mutation, simulation, and verification.

---

### Slide 5: The Core Breakthrough — Failure & Recovery Loop
* **Hidden Dependency Scenario**:
  - `storage.read` has **0 direct user access logs**.
  - Static analyzers would naively delete it.
  - Our agent initially proposes deletion → **Simulation Fails** on `ImageProcessingService`.
  - Agent **investigates the failure**, discovers the microservice dependency, **adapts its plan**, preserves `storage.read`, and keeps `iam.modify` & `storage.delete` removed!

---

### Slide 6: Policy Optimization Scoring
* **Functionality Score**: Strict 100% required constraint. Zero service outages allowed.
* **Security Risk Score**: Inverted risk calculation based on permission risk levels (`critical`, `high`, `medium`, `low`) and active attack surface.
* **Result**: Maximize security score improvement while preserving 100% functionality.

---

### Slide 7: Demonstration & Evaluation Results
* **Baseline Risk**: Developer Role with 6 permissions (Risk Score ~0.0).
* **Final Least-Privilege State**: 4 active permissions, 2 high-risk permissions removed, 1 hidden dependency preserved.
* **Security Score Improvement**: **+66.7%**.
* **Service Outages**: **0** (100% service health preserved).

---

### Slide 8: Technical Innovation & Robustness
* **No Real Cloud Credentials Needed**: Fully synthetic, safe local simulation engine.
* **Dual Execution Mode**: Works out-of-the-box in deterministic stateful mode or with live LLM tool calling (Gemini / OpenAI API).
* **Automated Test Suite**: 100% passing pytest integration tests.

---

### Slide 9: Conclusion & Future Roadmap
* Autonomous IAM optimization shifts security from reactive firefighting to self-correcting continuous enforcement.
* **Future Expansion**: AWS IAM Policy Simulator integration, Azure RBAC mapping, Terraform infrastructure-as-code PR generation.
