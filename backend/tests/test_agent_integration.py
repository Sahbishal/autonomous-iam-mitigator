import pytest
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.access_logs import AccessLogEngine
from backend.app.simulator.dependency_graph import CloudDependencyGraph
from backend.app.simulator.policy_simulator import PolicySimulator
from backend.app.agent.loop import AgentOrchestrator

def test_full_agent_adaptation_integration_scenario_b():
    env = SyntheticCloudEnvironment()
    log_engine = AccessLogEngine()
    dep_graph = CloudDependencyGraph(env)
    simulator = PolicySimulator(env, dep_graph)
    orchestrator = AgentOrchestrator(env, log_engine, dep_graph, simulator)
    
    logs = []
    def callback(step):
        logs.append(step)

    res = orchestrator.run_agent_loop(
        session_id="test_session_b",
        scenario_id="scenario_b",
        role_id="Developer",
        callback=callback
    )
    
    # 1. State assertions
    state = res["state"]
    report = res["evaluation_report"]
    
    assert state["status"] == "completed"
    assert state["verification_passed"] is True
    assert report["verdict"] == "SUCCESS"
    
    # 2. Check permissions removed vs preserved
    assert "storage.delete" in report["permissions_removed"]
    assert "iam.modify" in report["permissions_removed"]
    assert "storage.read" in report["permissions_preserved"]
    assert "storage.read" in state["current_permissions"]
    
    # 3. Verify step log sequence: must contain simulation failure AND adaptation
    phases = [l["phase"] for l in state["step_history"]]
    assert "OBSERVE" in phases
    assert "ANALYZE" in phases
    assert "PLAN" in phases
    assert "ACT" in phases
    assert "EVALUATE" in phases
    assert "ADAPT" in phases
    assert "VERIFY" in phases
    
    # Verify simulation failure was detected and handled
    assert report["simulation_failures_encountered"] == 1
    assert report["replanning_iterations"] == 1
    assert report["final_functionality_score"] == 100.0
