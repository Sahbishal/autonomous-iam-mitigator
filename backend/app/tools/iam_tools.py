import uuid
from datetime import datetime
from typing import Dict, Any, List
from backend.app.tools.base import ToolContext, ToolRegistry
from backend.app.models.iam import PolicyVersion

def setup_iam_tools(context: ToolContext) -> ToolRegistry:
    registry = ToolRegistry(context)

    # Tool 1: get_iam_roles
    def get_iam_roles() -> Dict[str, Any]:
        roles = [role.dict() for role in context.env.list_roles()]
        return {"status": "success", "count": len(roles), "roles": roles}

    registry.register(
        name="get_iam_roles",
        description="Returns list of all available IAM roles in the synthetic environment.",
        parameters={"type": "object", "properties": {}},
        func=get_iam_roles
    )

    # Tool 2: get_role_permissions
    def get_role_permissions(role_id: str) -> Dict[str, Any]:
        role = context.env.get_role(role_id)
        if not role:
            return {"status": "error", "message": f"Role '{role_id}' not found"}
        
        perms_detail = []
        for pid in role.permissions:
            p = context.env.get_permission(pid)
            if p:
                perms_detail.append(p.dict())

        return {
            "status": "success",
            "role_id": role.id,
            "role_name": role.name,
            "permission_count": len(role.permissions),
            "permissions": role.permissions,
            "permission_details": perms_detail
        }

    registry.register(
        name="get_role_permissions",
        description="Returns current permissions assigned to a specific IAM role.",
        parameters={
            "type": "object",
            "properties": {
                "role_id": {"type": "string", "description": "The IAM role ID (e.g. Developer)"}
            },
            "required": ["role_id"]
        },
        func=get_role_permissions
    )

    # Tool 3: get_access_history
    def get_access_history(role_id: str, days: int = 90) -> Dict[str, Any]:
        stats = context.log_engine.analyze_role_usage(role_id, days)
        logs = [log.dict() for log in context.log_engine.get_logs_for_role(role_id, days)]
        return {
            "status": "success",
            "role_id": role_id,
            "lookback_days": days,
            "total_logs": len(logs),
            "usage_analytics": stats,
            "logs_sample": logs[:15]  # Sample first 15 for summary
        }

    registry.register(
        name="get_access_history",
        description="Returns access history and log analytics for a role over the past days.",
        parameters={
            "type": "object",
            "properties": {
                "role_id": {"type": "string", "description": "The IAM role ID"},
                "days": {"type": "integer", "description": "Number of lookback days (default: 90)"}
            },
            "required": ["role_id"]
        },
        func=get_access_history
    )

    # Tool 4: get_permission_details
    def get_permission_details(permission_id: str) -> Dict[str, Any]:
        perm = context.env.get_permission(permission_id)
        if not perm:
            return {"status": "error", "message": f"Permission '{permission_id}' not found"}

        impact = context.dep_graph.get_permission_impact(permission_id)
        return {
            "status": "success",
            "permission": perm.dict(),
            "dependency_impact": impact
        }

    registry.register(
        name="get_permission_details",
        description="Returns risk, resource, sensitivity, scope metadata, and dependency impact for a permission.",
        parameters={
            "type": "object",
            "properties": {
                "permission_id": {"type": "string", "description": "Permission ID (e.g. storage.read)"}
            },
            "required": ["permission_id"]
        },
        func=get_permission_details
    )

    # Tool 5: get_service_dependencies
    def get_service_dependencies(permission_id: str) -> Dict[str, Any]:
        impact = context.dep_graph.get_permission_impact(permission_id)
        deps = context.dep_graph.get_service_dependencies(permission_id)
        return {
            "status": "success",
            "permission_id": permission_id,
            "has_dependencies": len(deps) > 0,
            "dependent_services_count": len(deps),
            "dependent_services": deps,
            "impact_summary": impact
        }

    registry.register(
        name="get_service_dependencies",
        description="Returns microservices and resources that depend on a specific permission.",
        parameters={
            "type": "object",
            "properties": {
                "permission_id": {"type": "string", "description": "Permission ID"}
            },
            "required": ["permission_id"]
        },
        func=get_service_dependencies
    )

    # Tool 6: find_unused_permissions
    def find_unused_permissions(role_id: str) -> Dict[str, Any]:
        role = context.env.get_role(role_id)
        if not role:
            return {"status": "error", "message": f"Role '{role_id}' not found"}

        usage_stats = context.log_engine.analyze_role_usage(role_id, days=90)
        candidates = []

        for pid in role.permissions:
            perm_usage = usage_stats.get(pid, {"direct_calls": 0, "service_calls": 0, "total_calls": 0})
            direct_calls = perm_usage.get("direct_calls", 0)
            total_calls = perm_usage.get("total_calls", 0)

            # Check direct user usage vs total usage
            if direct_calls == 0:
                p_detail = context.env.get_permission(pid)
                candidates.append({
                    "permission_id": pid,
                    "direct_user_calls": direct_calls,
                    "service_calls": perm_usage.get("service_calls", 0),
                    "total_calls": total_calls,
                    "risk_level": p_detail.risk_level.value if p_detail else "medium",
                    "flag_reason": "Zero direct user activity observed in 90-day access log",
                    "note": "Agent must investigate dependency graph before deciding removal!"
                })

        return {
            "status": "success",
            "role_id": role_id,
            "candidate_count": len(candidates),
            "candidate_permissions": candidates
        }

    registry.register(
        name="find_unused_permissions",
        description="Returns candidate permissions with zero direct user access logs. Agent must investigate dependencies.",
        parameters={
            "type": "object",
            "properties": {
                "role_id": {"type": "string", "description": "The IAM role ID"}
            },
            "required": ["role_id"]
        },
        func=find_unused_permissions
    )

    # Tool 7: propose_policy_change
    def propose_policy_change(role_id: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        role = context.env.get_role(role_id)
        if not role:
            return {"status": "error", "message": f"Role '{role_id}' not found"}

        current_perms = set(role.permissions)
        
        # Apply mutations
        removals = set(changes.get("remove_permissions", []))
        additions = set(changes.get("add_permissions", []))
        override = changes.get("set_permissions", None)

        if override is not None:
            new_perms = set(override)
        else:
            new_perms = (current_perms - removals) | additions

        version_id = f"v_{len(context.proposed_policies) + 1}_{uuid.uuid4().hex[:4]}"
        policy_obj = PolicyVersion(
            version_id=version_id,
            role_id=role_id,
            permissions=sorted(list(new_perms)),
            created_at=datetime.now().isoformat(),
            description=changes.get("description", "Proposed policy mutation")
        )

        context.proposed_policies[version_id] = policy_obj.dict()

        return {
            "status": "success",
            "version_id": version_id,
            "role_id": role_id,
            "previous_permissions_count": len(role.permissions),
            "proposed_permissions_count": len(new_perms),
            "removed_permissions": sorted(list(removals)),
            "added_permissions": sorted(list(additions)),
            "proposed_permissions": sorted(list(new_perms))
        }

    registry.register(
        name="propose_policy_change",
        description="Creates a new proposed IAM policy version for simulation testing.",
        parameters={
            "type": "object",
            "properties": {
                "role_id": {"type": "string", "description": "The IAM role ID"},
                "changes": {
                    "type": "object",
                    "properties": {
                        "remove_permissions": {"type": "array", "items": {"type": "string"}},
                        "add_permissions": {"type": "array", "items": {"type": "string"}},
                        "set_permissions": {"type": "array", "items": {"type": "string"}},
                        "description": {"type": "string"}
                    }
                }
            },
            "required": ["role_id", "changes"]
        },
        func=propose_policy_change
    )

    # Tool 8: simulate_policy
    def simulate_policy(policy_version: str) -> Dict[str, Any]:
        policy_data = context.proposed_policies.get(policy_version)
        if not policy_data:
            return {"status": "error", "message": f"Policy version '{policy_version}' not found"}

        role_id = policy_data["role_id"]
        proposed_perms = policy_data["permissions"]

        result = context.simulator.simulate_role_policy(
            role_id=role_id,
            proposed_permissions=proposed_perms,
            version_id=policy_version
        )

        result_dict = result.dict()
        context.simulation_results[result.simulation_id] = result_dict

        return {
            "status": "success",
            "simulation": result_dict
        }

    registry.register(
        name="simulate_policy",
        description="Runs synthetic cloud workloads against a proposed policy version.",
        parameters={
            "type": "object",
            "properties": {
                "policy_version": {"type": "string", "description": "The policy version ID to simulate"}
            },
            "required": ["policy_version"]
        },
        func=simulate_policy
    )

    # Tool 9: inspect_simulation_failure
    def inspect_simulation_failure(simulation_id: str) -> Dict[str, Any]:
        sim_data = context.simulation_results.get(simulation_id)
        if not sim_data:
            return {"status": "error", "message": f"Simulation ID '{simulation_id}' not found"}

        if sim_data["success"]:
            return {"status": "info", "message": f"Simulation '{simulation_id}' had no failures."}

        return {
            "status": "success",
            "simulation_id": simulation_id,
            "policy_version": sim_data["policy_version"],
            "failed_services": sim_data["failed_services"],
            "denied_actions": sim_data["denied_actions"],
            "dependency_failures": sim_data["dependency_failures"],
            "affected_resources": sim_data["affected_resources"],
            "root_cause_analysis": [
                f"Service '{f['service']}' requires permission '{f['permission']}' to access '{f['resource']}'."
                for f in sim_data["dependency_failures"]
            ]
        }

    registry.register(
        name="inspect_simulation_failure",
        description="Inspects detailed root cause evidence for a failed policy simulation.",
        parameters={
            "type": "object",
            "properties": {
                "simulation_id": {"type": "string", "description": "The simulation ID"}
            },
            "required": ["simulation_id"]
        },
        func=inspect_simulation_failure
    )

    # Tool 10: apply_policy
    def apply_policy(policy_version: str) -> Dict[str, Any]:
        policy_data = context.proposed_policies.get(policy_version)
        if not policy_data:
            return {"status": "error", "message": f"Policy version '{policy_version}' not found"}

        role_id = policy_data["role_id"]
        role = context.env.get_role(role_id)
        if not role:
            return {"status": "error", "message": f"Role '{role_id}' not found"}

        role.permissions = policy_data["permissions"]

        return {
            "status": "success",
            "message": f"Applied policy '{policy_version}' to role '{role_id}' in synthetic environment.",
            "role_id": role_id,
            "active_permissions": role.permissions
        }

    registry.register(
        name="apply_policy",
        description="Applies a verified policy version to the synthetic cloud role.",
        parameters={
            "type": "object",
            "properties": {
                "policy_version": {"type": "string", "description": "The policy version ID"}
            },
            "required": ["policy_version"]
        },
        func=apply_policy
    )

    # Tool 11: verify_policy
    def verify_policy(policy_version: str) -> Dict[str, Any]:
        policy_data = context.proposed_policies.get(policy_version)
        if not policy_data:
            return {"status": "error", "message": f"Policy version '{policy_version}' not found"}

        role_id = policy_data["role_id"]
        proposed_perms = policy_data["permissions"]

        sim_res = context.simulator.simulate_role_policy(role_id, proposed_perms, version_id=policy_version)

        func_ok = (sim_res.functionality_score == 100.0)
        sec_improved = (sim_res.security_score > 30.0)

        verified = func_ok and sec_improved

        return {
            "status": "success",
            "policy_version": policy_version,
            "verified": verified,
            "functionality_score": sim_res.functionality_score,
            "security_score": sim_res.security_score,
            "constraints_satisfied": {
                "100_percent_functionality": func_ok,
                "security_improved": sec_improved,
                "zero_failed_services": len(sim_res.failed_services) == 0
            },
            "verdict": "POLICY_VERIFIED" if verified else "POLICY_REJECTED"
        }

    registry.register(
        name="verify_policy",
        description="Verifies that a policy satisfies 100% functionality and maximum security constraints.",
        parameters={
            "type": "object",
            "properties": {
                "policy_version": {"type": "string", "description": "Policy version ID to verify"}
            },
            "required": ["policy_version"]
        },
        func=verify_policy
    )

    # Tool 12: get_current_environment_state
    def get_current_environment_state() -> Dict[str, Any]:
        roles = [r.dict() for r in context.env.list_roles()]
        deps = [d.dict() for d in context.env.dependencies]
        return {
            "status": "success",
            "total_roles": len(roles),
            "roles": roles,
            "total_dependencies": len(deps),
            "dependencies": deps,
            "graph": context.dep_graph.get_full_graph_structure()
        }

    registry.register(
        name="get_current_environment_state",
        description="Returns complete current synthetic cloud environment state.",
        parameters={"type": "object", "properties": {}},
        func=get_current_environment_state
    )

    return registry
