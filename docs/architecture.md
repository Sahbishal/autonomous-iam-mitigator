# System Architecture — Autonomous Cloud IAM Least-Privilege Mitigator

## System Topology & Data Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                        React Frontend Dashboard                        │
│   (Overview Metrics, Live Agent Timeline, Policy Matrix, Dep Graph)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST & SSE Stream
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          FastAPI Backend API                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Agent Orchestrator & Memory State                    │
│   (OBSERVE -> ANALYZE -> PLAN -> ACT -> EVALUATE -> ADAPT -> VERIFY)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Controlled Tool Calls
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          Tool Layer (12 Tools)                         │
│  (get_iam_roles, get_access_history, simulate_policy, verify, etc.)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Synthetic Cloud Environment                       │
│  ├── IAM Roles & Permissions                                           │
│  ├── 30-90 Days Synthetic Access Logs                                  │
│  ├── NetworkX Dependency Graph (Service -> Resource -> Permission)     │
│  └── Policy Simulator Workload Engine                                  │
└────────────────────────────────────────────────────────────────────────┘
```

## Architectural Design Principles

1. **Synthetic Isolation**: Complete isolation from real AWS/Azure/GCP production credentials. All security simulation runs against deterministic in-memory Python object models and graph structures.
2. **Tool-Gated Mutation**: The LLM / Agent Orchestrator does not directly mutate cloud database tables. All state changes occur via controlled, deterministic tool invocations (`propose_policy_change`, `apply_policy`).
3. **Dual Execution Mode**: Supports both live LLM function calling (Gemini / OpenAI API) and a stateful deterministic agentic loop out-of-the-box for offline hackathon judging reliability.
4. **Functionality Guarantee**: Incorporates a strict 100% service functionality constraint. Security risk reduction is never permitted to break required application microservices.
