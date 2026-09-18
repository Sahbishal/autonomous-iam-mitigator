# Autonomous Cloud IAM Least-Privilege Mitigator


[![Pytest Status](https://img.shields.io/badge/pytest-8%20passed-emerald)](./backend/tests)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2-61DAFB)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC)](https://tailwindcss.com)

An autonomous AI security agent designed to reduce excessive, risky, and unused cloud IAM permissions while preserving 100% application and microservice functionality.

```
  [OBSERVE] ──► [ANALYZE] ──► [PLAN (v1)] ──► [ACT (Simulate)]
                                                     │
                                                     ▼

  [VERIFY] ◄── [ACT (Simulate v2)] ◄── [ADAPT] ◄── [EVALUATE Failure]
```


> ⚠️ **SAFETY & GUARDRAIL DISCLAIMER**:
> **SYNTHETIC CLOUD ENVIRONMENT — NO PRODUCTION ACCESS REQUIRED OR USED.**
> All operations execute inside an isolated Python simulation environment modeling synthetic users, roles, permissions, resources, microservice dependency graphs, and access logs.

---

## 1. Executive Summary & Problem Statement

### Why IAM Least Privilege Matters
Over 80% of cloud security incidents stem from overly broad or excessive IAM privileges (e.g. `iam:PassRole`, wildcard `*`, or unneeded `storage.delete` permissions). Security teams struggle to enforce the principle of least privilege because they fear revoking a permission will silently break a critical production service.

### Why Existing Approaches & Rule Engines Fail
Traditional static analyzers or fixed rule engines evaluate direct user access logs naively:
$$\text{If Direct Access Logs} = 0 \implies \text{Delete Permission}$$

This static logic fails catastrophically when permissions are required by **background microservices** or **indirect service-to-service calls** (e.g., an `ImageProcessingService` microservice reading storage on behalf of an application workflow).

### Why an Agentic Loop is Essential
Solving cloud IAM optimization under uncertainty requires an autonomous agent that can:
1. Formulate initial hypothesis plans based on access history.
2. Execute proposed changes in a policy simulator.
3. Observe simulation failure feedback when hidden service dependencies break.
4. Investigate root cause failures by inspecting dependency graphs.
5. Adapt its plan dynamically by preserving required service permissions while continuing to remove genuinely excessive risks.
6. Verify 100% service health before applying the policy.

---


## 2. Core Hackathon Demonstration Scenario (Scenario B)

The project includes a mandatory deterministic demonstration scenario with a hidden dependency:

### Baseline Developer Role Permissions
* `database.read` (Medium Risk) — 45 direct user calls
* `database.write` (Medium Risk) — 30 direct user calls
* `storage.write` (Medium Risk) — 22 direct user calls
* `storage.delete` (High Risk) — **0 direct user calls (UNUSED)**
* `iam.modify` (Critical Risk) — **0 direct user calls (UNUSED)**
* `storage.read` (Medium Risk) — **0 direct user calls (APPARENTLY UNUSED DIRECTLY)**

### The Hidden Dependency
`ImageProcessingService` microservice requires `storage.read` on `ObjectStorage` to generate image thumbnails during background developer batch workflows.

### Execution Trace

```
1. OBSERVE: Agent inspects Developer role permissions and establishes baseline risk score (0.0).
2. ANALYZE: Agent queries 90-day access logs. Flags storage.delete, iam.modify, and storage.read as candidates with 0 direct user activity.
3. PLAN: Agent proposes Policy v1 (removing storage.delete, iam.modify, storage.read).
4. ACT: Agent simulates Policy v1 against synthetic cloud workloads.
   ❌ SERVICE FAILURE: ImageProcessingService failed with AccessDeniedException on storage.read! Functionality drops to 60%.
5. EVALUATE: Agent inspects simulation failure evidence and queries the NetworkX Dependency Graph for storage.read.
   🔍 DISCOVERY: ImageProcessingService -> ObjectStorage -> storage.read.
6. ADAPT: Agent adapts its policy proposal. It restores/preserves storage.read, while keeping dangerous perms iam.modify & storage.delete removed (Policy v2).
7. ACT AGAIN: Agent re-simulates Policy v2.
   ✓ SUCCESS: 100% Functionality, 66.7% Security Risk Score.
8. VERIFY: Agent verifies all constraints and applies Policy v2 to the synthetic environment.
```

---

## 3. System Architecture

```
Frontend (React + Tailwind Dashboard)
       │
       ▼ (HTTP REST & SSE EventSource Stream)
FastAPI Backend (API & Agent Server)
       │
       ▼
Agent Orchestrator (Observe → Analyze → Plan → Act → Evaluate → Adapt → Verify)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
LLM Function Calling Adapter           Agent Memory & State Tracker
       │                                         │
       ▼                                         │
Controlled Tool Layer (12 Tools)                │
 (IAM, Access Logs, Dependency Graph,            │
  Policy Simulator, Mutation, Verification)      │
       │                                         │
       ▼                                         ▼
Synthetic Cloud Environment (Users, Roles, Resources, Services, Logs, NetworkX Graph)
```

---

## 4. Controlled Tool Layer (12 Tools)

The agent operates through 12 controlled tools with structured JSON contracts:

1. `get_iam_roles()`: Returns available roles in the synthetic environment.
2. `get_role_permissions(role_id)`: Returns active permissions for a role.
3. `get_access_history(role_id, days)`: Returns access logs and usage analytics over 30-90 days.
4. `get_permission_details(permission_id)`: Returns risk, resource, scope, and sensitivity metadata.
5. `get_service_dependencies(permission_id)`: Returns microservices and resources dependent on a permission.
6. `find_unused_permissions(role_id)`: Identifies permissions with zero direct user access logs.
7. `propose_policy_change(role_id, changes)`: Creates a proposed policy version for simulation.
8. `simulate_policy(policy_version)`: Runs synthetic cloud workloads against a proposed policy version.
9. `inspect_simulation_failure(simulation_id)`: Returns root cause traces for failed simulations.
10. `apply_policy(policy_version)`: Applies a verified policy version to a synthetic role.
11. `verify_policy(policy_version)`: Checks 100% functionality and risk reduction constraints.
12. `get_current_environment_state()`: Returns complete synthetic cloud environment topology.

---

## 5. Technology Stack

* **Backend**: Python 3.12, FastAPI, Pydantic v2, NetworkX, Uvicorn.
* **Frontend**: React 18, Vite, Tailwind CSS, Lucide React Icons, Recharts.
* **Testing**: pytest, pytest-asyncio, httpx.
* **Containerization**: Docker, docker-compose.

---

## 6. Quick Start & Local Execution

### Prerequisites
* Python 3.10+
* Node.js 18+

### Step 1: Clone & Setup Backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI Backend
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at `http://localhost:8000/docs`.

### Step 2: Setup & Start Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite Development Server
npm run dev
```
Dashboard will be available at `http://localhost:3000`.

### Running via Docker Compose
```bash
docker-compose up --build
```

---

## 7. Running Tests

Run the comprehensive pytest suite covering IAM environment, access log analytics, dependency graphs, policy simulator, tool registries, and full agent adaptation integration:

```bash
python -m pytest backend/tests/ -v
```

Expected Output:
```
backend/tests/test_agent_integration.py::test_full_agent_adaptation_integration_scenario_b PASSED
backend/tests/test_dependency_graph.py::test_dependency_graph_building PASSED
backend/tests/test_dependency_graph.py::test_permission_impact PASSED
backend/tests/test_iam_environment.py::test_cloud_environment_initialization PASSED
backend/tests/test_iam_environment.py::test_access_log_analytics PASSED
backend/tests/test_policy_simulator.py::test_policy_simulation_success PASSED
backend/tests/test_policy_simulator.py::test_policy_simulation_failure_on_hidden_dependency PASSED
backend/tests/test_tools.py::test_iam_tools_execution PASSED

======================== 8 passed in 0.77s ========================
```

---

## 8. Hackathon Deliverables & Documentation

* **Architecture Overview**: [`docs/architecture.md`](./docs/architecture.md)
* **Agent Workflow & Loop State Machine**: [`docs/agent-flow.md`](./docs/agent-flow.md)
* **Core Demo Scenario (Scenario B)**: [`docs/demo-scenario.md`](./docs/demo-scenario.md)
* **Presentation Outline (7-10 Slides)**: [`docs/presentation-outline.md`](./docs/presentation-outline.md)
* **Presenter 3-5 Min Demo Script**: [`docs/demo-script.md`](./docs/demo-script.md)

---

## 9. Evaluation Results Summary

| Metric | Baseline State | Agent Proposed (v1) | Final Verified Policy (v2) |
| :--- | :--- | :--- | :--- |
| **Active Permissions** | 6 | 3 | 4 |
| **Security Risk Score** | 0.0 / 100 | 100.0 / 100 | **66.7 / 100 (+66.7%)** |
| **Service Functionality** | 100% | 60% (FAILURE) | **100.0% (VERIFIED)** |
| **Failed Services** | None | ImageProcessingService | **0 (Zero Outages)** |
| **Risky Perms Removed** | None | `storage.delete`, `iam.modify`, `storage.read` | **`storage.delete`, `iam.modify`** |
| **Dependencies Preserved** | None | None | **`storage.read` (ImageProcessingService)** |

---

## 10. License

**Agentic AI Hackathon**. Released under the MIT License.
