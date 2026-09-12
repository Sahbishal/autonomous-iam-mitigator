# Core Hackathon Demo Scenario — Scenario B

## Scenario Breakdown: Hidden Service Dependency Failure & Recovery

### Baseline Developer Role Permissions
* `database.read` (Medium Risk)
* `database.write` (Medium Risk)
* `storage.read` (Medium Risk)
* `storage.write` (Medium Risk)
* `storage.delete` (High Risk)
* `iam.modify` (Critical Risk)

### 90-Day Access Log Evidence
* `database.read`: 45 direct user calls (ACTIVE)
* `database.write`: 30 direct user calls (ACTIVE)
* `storage.write`: 22 direct user calls (ACTIVE)
* `storage.delete`: 0 direct user calls (UNUSED)
* `iam.modify`: 0 direct user calls (UNUSED)
* `storage.read`: 0 direct user calls (APPARENTLY UNUSED DIRECTLY)

### The Hidden Dependency
`ImageProcessingService` microservice requires `storage.read` on `ObjectStorage` to generate image thumbnails during background developer batch workflows.

### Demonstration Trace

```
1. Agent observes Developer role permissions.
2. Agent analyzes 90-day access logs -> Flags storage.delete, iam.modify, storage.read as candidates.
3. Agent proposes Policy v1 (removing storage.delete, iam.modify, storage.read).
4. Agent runs Policy Simulator -> ❌ SERVICE FAILURE: ImageProcessingService failed (AccessDeniedException on storage.read).
5. Agent inspects simulation failure -> Queries NetworkX dependency graph for storage.read.
6. Agent discovers ImageProcessingService -> ObjectStorage -> storage.read dependency.
7. Agent adapts policy -> Preserves storage.read, continues removing iam.modify and storage.delete (Policy v2).
8. Agent re-simulates -> ✓ SUCCESS: 100% Functionality, 66.7% Security Score.
9. Agent verifies & applies final least-privilege policy.
```
