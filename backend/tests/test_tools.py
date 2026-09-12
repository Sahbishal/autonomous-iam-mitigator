import pytest
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.access_logs import AccessLogEngine
from backend.app.simulator.dependency_graph import CloudDependencyGraph
from backend.app.simulator.policy_simulator import PolicySimulator
from backend.app.tools.base import ToolContext
from backend.app.tools.iam_tools import setup_iam_tools

def test_iam_tools_execution():
    env = SyntheticCloudEnvironment()
    log_engine = AccessLogEngine()
    dep_graph = CloudDependencyGraph(env)
    simulator = PolicySimulator(env, dep_graph)
    ctx = ToolContext(env, log_engine, dep_graph, simulator)
    registry = setup_iam_tools(ctx)
    
    # 1. get_iam_roles
    r1 = registry.execute("get_iam_roles", {})
    assert r1["status"] == "success"
    
    # 2. find_unused_permissions
    r2 = registry.execute("find_unused_permissions", {"role_id": "Developer"})
    assert r2["status"] == "success"
    candidates = [c["permission_id"] for c in r2["candidate_permissions"]]
    assert "storage.delete" in candidates
    assert "iam.modify" in candidates
    assert "storage.read" in candidates
    
    # 3. propose_policy_change
    r3 = registry.execute("propose_policy_change", {
        "role_id": "Developer",
        "changes": {"remove_permissions": ["storage.delete", "iam.modify"]}
    })
    assert r3["status"] == "success"
    v_id = r3["version_id"]
    
    # 4. simulate_policy
    r4 = registry.execute("simulate_policy", {"policy_version": v_id})
    assert r4["status"] == "success"
    assert r4["simulation"]["success"] is True
