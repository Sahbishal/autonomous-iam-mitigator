import pytest
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.dependency_graph import CloudDependencyGraph
from backend.app.simulator.policy_simulator import PolicySimulator

def test_policy_simulation_success():
    env = SyntheticCloudEnvironment()
    dep_graph = CloudDependencyGraph(env)
    simulator = PolicySimulator(env, dep_graph)
    
    # Valid least privilege policy: retains database.read, database.write, storage.write, storage.read
    proposed_perms = ["database.read", "database.write", "storage.read", "storage.write"]
    res = simulator.simulate_role_policy("Developer", proposed_perms, "v_valid")
    
    assert res.success is True
    assert res.functionality_score == 100.0
    assert len(res.failed_services) == 0
    assert res.security_score > 50.0

def test_policy_simulation_failure_on_hidden_dependency():
    env = SyntheticCloudEnvironment()
    dep_graph = CloudDependencyGraph(env)
    simulator = PolicySimulator(env, dep_graph)
    
    # Bad policy: removes storage.read
    proposed_perms = ["database.read", "database.write", "storage.write"]
    res = simulator.simulate_role_policy("Developer", proposed_perms, "v_invalid")
    
    assert res.success is False
    assert res.functionality_score < 100.0
    assert "ImageProcessingService" in res.failed_services
    assert len(res.denied_actions) > 0
    assert res.denied_actions[0]["permission"] == "storage.read"
