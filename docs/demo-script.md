# 3-5 Minute Hackathon Presenter Demo Script
## Autonomous Cloud IAM Least-Privilege Mitigator

### Minute 0:00 – 0:45: Introduction & Problem Context
* *"Good morning judges! We are presenting Problem Statement #10: Autonomous Cloud IAM Least-Privilege Mitigator."*
* *"In cloud security, over-privileged IAM roles are a massive vulnerability. However, security engineers are afraid to remove unused permissions because a hidden microservice dependency might break in production."*
* *"Static rule engines cannot solve this because they only see direct user access logs. Today, we show how an autonomous agentic loop solves this problem by observing, simulating, failing safely in simulation, investigating the root cause, and adapting its plan."*

---

### Minute 0:45 – 1:30: Overview of the Dashboard & Baseline
* *"Here is our React cybersecurity dashboard. Notice the top banner: **SYNTHETIC CLOUD ENVIRONMENT — NO PRODUCTION ACCESS**. Everything runs locally and safely."*
* *"Looking at our baseline **Developer Role**: it currently holds 6 permissions, including `iam.modify` (Critical risk) and `storage.delete` (High risk)."*
* *"Our baseline Security Risk Score is 0.0, and our Service Functionality is 100%."*

---

### Minute 1:30 – 3:30: Launching the Autonomous Agentic Loop (The Core Demo)
* *"I will now click **Run Demo Scenario (Scenario B)**."*
* *"Watch the live timeline on the left as the agent executes its loop:"*
  1. **OBSERVE**: *"The agent retrieves current Developer permissions."*
  2. **ANALYZE**: *"The agent checks 90-day access logs. It observes that `database.read`, `database.write`, and `storage.write` have frequent direct calls. But `storage.delete`, `iam.modify`, and `storage.read` have ZERO direct user calls."*
  3. **PLAN & ACT (Policy v1)**: *"The agent proposes Policy v1, removing all three candidates (`storage.delete`, `iam.modify`, `storage.read`). It simulates Policy v1 against synthetic cloud workloads."*
  4. **SIMULATION FAILURE DETECTED**: *"Look at the red alert in the timeline and console! Simulation FAILED! Functionality dropped to 60%. Microservice `ImageProcessingService` crashed with `AccessDeniedException` on `storage.read`."*
  5. **EVALUATE & INVESTIGATE**: *"Instead of giving up or deleting the test, the agent inspects the failure and queries our NetworkX Dependency Graph for `storage.read`. It discovers that `ImageProcessingService` microservice requires `storage.read` to generate image thumbnails!"*
  6. **ADAPT & RE-SIMULATE (Policy v2)**: *"The agent adapts its plan! It preserves `storage.read`, but keeps `iam.modify` and `storage.delete` removed! It simulates Policy v2."*
  7. **VERIFY & APPLY**: *"Simulation SUCCESSFUL! 100% service health restored, and Security Score improved to 66.7%! The agent verifies and applies the policy."*

---

### Minute 3:30 – 4:30: Evidence Matrix & Evaluation Report
* *"Looking at the Policy Matrix table, every decision is backed by evidence:"*
  - `iam.modify` -> **REMOVED** (Zero usage, critical risk).
  - `storage.delete` -> **REMOVED** (Zero usage, high risk).
  - `storage.read` -> **PRESERVED** (Zero direct calls, BUT critical dependency for ImageProcessingService).
* *"The Hackathon Evaluation Report summarizes: **+66.7% Security Improvement**, **100% Service Health Preserved**, **1 Simulation Failure Recovered**, **Verdict: SUCCESS**."*

---

### Minute 4:30 – 5:00: Q&A Wrap Up
* *"Our pytest integration suite passes 100% of test cases. Thank you, and we welcome your questions!"*
