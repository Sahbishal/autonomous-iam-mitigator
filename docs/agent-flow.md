# Agent Workflow & Decision State Machine

## The Agentic Loop

```
  [START]
     │
     ▼
 ┌───────────────┐
 │ 1. OBSERVE    │ ──► Inspect IAM role baseline permissions & initial risk score
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ 2. ANALYZE    │ ──► Retrieve 90-day access logs & identify candidate unused perms
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ 3. PLAN       │ ──► Formulate candidate removal proposal (Policy v1)
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ 4. ACT        │ ──► Execute Policy Simulator against synthetic service traffic
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐        SIMULATION FAILED? (Hidden Dependency Detected)
 │ 5. EVALUATE   │ ────────────────────────────────────────────────────────┐
 └───────┬───────┘                                                         │
         │ SIMULATION PASSED (100% Functionality)                          ▼
         │                                                         ┌───────────────┐
         │                                                         │ 6. ADAPT      │
         │                                                         │    & REPLAN   │
         │                                                         └───────┬───────┘
         │                                                                 │ Restore dependency perm
         │                                                                 ▼
         │                                                         ┌───────────────┐
         │                                                         │ Re-simulate   │
         │                                                         └───────┬───────┘
         │                                                                 │
         ▼                                                                 │
 ┌───────────────┐                                                         │
 │ 7. VERIFY     │ ◄───────────────────────────────────────────────────────┘
 └───────┬───────┘
         │ Check 100% service health & apply policy
         ▼
       [END]
```

## Detailed Step Mechanics

1. **OBSERVE**: Invokes `get_role_permissions("Developer")` to map active baseline permissions.
2. **ANALYZE**: Invokes `get_access_history("Developer", 90)` and `find_unused_permissions("Developer")`.
3. **PLAN**: Generates Policy v1 removing `storage.delete`, `iam.modify`, and `storage.read` (which has 0 direct user access).
4. **ACT**: Calls `simulate_policy("v1")`. Simulator detects `ImageProcessingService` failure due to missing `storage.read`.
5. **EVALUATE**: Calls `inspect_simulation_failure()` and `get_service_dependencies("storage.read")`. Graph reveals `ImageProcessingService -> ObjectStorage -> storage.read`.
6. **ADAPT**: Agent reasoning engine revises proposal. It preserves `storage.read` while keeping dangerous perms `iam.modify` and `storage.delete` removed (Policy v2).
7. **RE-SIMULATE**: Calls `simulate_policy("v2")`. Returns 100% functionality score and +66.7% security score.
8. **VERIFY**: Calls `verify_policy("v2")` and `apply_policy("v2")`.
