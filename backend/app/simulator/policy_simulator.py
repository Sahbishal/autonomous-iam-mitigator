import uuid
from typing import List, Dict, Any, Tuple
from backend.app.models.iam import RiskLevel
from backend.app.models.agent_state import SimulationResult
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.dependency_graph import CloudDependencyGraph

class PolicySimulator:
    """
    Simulates proposed IAM policies against cloud service workloads and traffic.
    Calculates Security Risk Score and Functionality Score (0-100%).
    Detects denied actions, service outages, and hidden dependency failures.
    """
    def __init__(self, env: SyntheticCloudEnvironment, dep_graph: CloudDependencyGraph):
        self.env = env
        self.dep_graph = dep_graph

    def simulate_role_policy(self, role_id: str, proposed_permissions: List[str], version_id: str = "") -> SimulationResult:
        """
        Runs synthetic cloud traffic simulation for the given proposed policy.
        """
        if not version_id:
            version_id = f"policy_v_{uuid.uuid4().hex[:6]}"

        sim_id = f"sim_{uuid.uuid4().hex[:8]}"
        proposed_set = set(proposed_permissions)

        # 1. Evaluate Service Functionality
        # Check required permissions for active application workflows (e.g. Developer role workflows)
        failed_services = []
        denied_actions = []
        dependency_failures = []
        affected_resources = set()

        # Define test workloads to evaluate for the role
        # For Developer role:
        # Workload 1: Developer direct DB access -> database.read, database.write
        # Workload 2: Developer direct Storage upload -> storage.write
        # Workload 3: ImageProcessingService background worker -> storage.read, storage.write
        
        workloads = []
        if role_id == "Developer":
            workloads = [
                {"name": "Database Read Access", "service": "DirectUser", "required_perm": "database.read", "target_resource": "Database", "criticality": "critical"},
                {"name": "Database Write Access", "service": "DirectUser", "required_perm": "database.write", "target_resource": "Database", "criticality": "critical"},
                {"name": "Media Upload Access", "service": "DirectUser", "required_perm": "storage.write", "target_resource": "ObjectStorage", "criticality": "critical"},
                {"name": "Image Processing Pipeline Read", "service": "ImageProcessingService", "required_perm": "storage.read", "target_resource": "ObjectStorage", "criticality": "critical"},
                {"name": "Image Processing Pipeline Write", "service": "ImageProcessingService", "required_perm": "storage.write", "target_resource": "ObjectStorage", "criticality": "critical"},
            ]
        else:
            # Generic fallback workloads based on current dependencies
            for dep in self.env.dependencies:
                workloads.append({
                    "name": f"{dep.source_service} -> {dep.required_permission}",
                    "service": dep.source_service,
                    "required_perm": dep.required_permission,
                    "target_resource": dep.target_resource,
                    "criticality": dep.criticality
                })

        passed_tests = 0
        failed_tests = 0

        for test in workloads:
            required_p = test["required_perm"]
            if required_p in proposed_set:
                passed_tests += 1
            else:
                failed_tests += 1
                svc = test["service"]
                if svc not in failed_services:
                    failed_services.append(svc)
                
                affected_resources.add(test["target_resource"])

                denied_action = {
                    "workload": test["name"],
                    "service": svc,
                    "permission": required_p,
                    "resource": test["target_resource"],
                    "error": f"AccessDeniedException: {svc} is missing required permission '{required_p}' for resource '{test['target_resource']}'"
                }
                denied_actions.append(denied_action)

                # Check if this failure was due to an indirect service dependency
                if svc != "DirectUser":
                    dependency_failures.append({
                        "service": svc,
                        "permission": required_p,
                        "resource": test["target_resource"],
                        "reason": f"Service '{svc}' failed because permission '{required_p}' was removed from role '{role_id}'"
                    })

        total_tests = len(workloads)
        functionality_score = 100.0 if total_tests == 0 else round((passed_tests / total_tests) * 100.0, 1)
        success = (failed_tests == 0 and functionality_score == 100.0)

        # 2. Calculate Security Risk Score
        # Initial Developer baseline risk score (with all 6 permissions) = ~100
        # Removing unnecessary permissions improves the security score.
        security_score = self.calculate_security_score(role_id, proposed_permissions)

        details = ""
        if success:
            details = f"Simulation SUCCESSFUL: All {passed_tests} service workloads passed. Functionality 100%."
        else:
            details = f"Simulation FAILED: {failed_tests} workload failures detected. Failed services: {', '.join(failed_services)}."

        return SimulationResult(
            simulation_id=sim_id,
            policy_version=version_id,
            success=success,
            security_score=security_score,
            functionality_score=functionality_score,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            failed_services=failed_services,
            denied_actions=denied_actions,
            affected_resources=list(affected_resources),
            dependency_failures=dependency_failures,
            details=details
        )

    def calculate_security_score(self, role_id: str, active_permissions: List[str]) -> float:
        """
        Calculates Security Score (0 to 100).
        Higher score = fewer unnecessary & dangerous permissions retained.
        """
        # Baseline max risk total when all default permissions are assigned
        default_role = self.env.get_role(role_id)
        if not default_role:
            return 50.0

        all_perms = default_role.permissions
        
        # Risk weights per level
        weights = {
            RiskLevel.LOW: 5,
            RiskLevel.MEDIUM: 15,
            RiskLevel.HIGH: 35,
            RiskLevel.CRITICAL: 65
        }

        # Calculate max possible risk total
        max_possible_risk = 0
        for pid in all_perms:
            p = self.env.get_permission(pid)
            if p:
                max_possible_risk += weights.get(p.risk_level, 15)

        # Calculate current active risk total
        current_active_risk = 0
        for pid in active_permissions:
            p = self.env.get_permission(pid)
            if p:
                current_active_risk += weights.get(p.risk_level, 15)

        if max_possible_risk == 0:
            return 100.0

        # Score is inverted risk percentage: 100 - (current / max * 100)
        # 100 = 0 active risk, 0 = all max permissions retained
        # We normalize so least privilege policy gets ~90-100 score.
        raw_risk_pct = (current_active_risk / max_possible_risk) * 100.0
        security_score = round(100.0 - raw_risk_pct, 1)

        return max(0.0, min(100.0, security_score))

    def calculate_raw_risk_score(self, active_permissions: List[str]) -> float:
        """Calculates raw risk points (0 to 150+)."""
        weights = {
            RiskLevel.LOW: 5,
            RiskLevel.MEDIUM: 15,
            RiskLevel.HIGH: 35,
            RiskLevel.CRITICAL: 65
        }
        total_risk = 0.0
        for pid in active_permissions:
            p = self.env.get_permission(pid)
            if p:
                total_risk += weights.get(p.risk_level, 15)
        return total_risk
