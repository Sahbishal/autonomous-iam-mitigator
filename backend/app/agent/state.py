import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.app.models.agent_state import AgentState, AgentStepLog, SimulationResult, Evidence
from backend.app.models.evaluation import EvaluationReport

class AgentMemory:
    """
    Manages persistent memory and task state for the IAM Least-Privilege Mitigator agent.
    """
    def __init__(self, session_id: str, scenario_id: str = "scenario_b", role_id: str = "Developer"):
        self.state = AgentState(
            session_id=session_id,
            scenario_id=scenario_id,
            role_id=role_id
        )

    def log_step(self, phase: str, thought: str, tool_called: Optional[str] = None, tool_args: Optional[Dict[str, Any]] = None, observation: Optional[Any] = None, status: str = "info") -> AgentStepLog:
        step_number = len(self.state.step_history) + 1
        log_entry = AgentStepLog(
            step_number=step_number,
            phase=phase,
            thought=thought,
            tool_called=tool_called,
            tool_args=tool_args,
            observation=observation,
            timestamp=datetime.now().isoformat(),
            status=status
        )
        self.state.step_history.append(log_entry)
        return log_entry

    def record_simulation(self, result: SimulationResult):
        self.state.simulation_history.append(result)
        self.state.current_risk_score = result.security_score
        self.state.current_functionality_score = result.functionality_score

    def record_evidence(self, perm_id: str, decision: str, direct_calls: int, dep_usage: bool, services: List[str], risk_level: str, explanation: str):
        ev = Evidence(
            permission_id=perm_id,
            decision=decision,
            direct_usage_count=direct_calls,
            dependency_usage=dep_usage,
            dependent_services=services,
            risk_level=risk_level,
            explanation=explanation
        )
        self.state.evidence_list.append(ev)

    def get_summary(self) -> Dict[str, Any]:
        return self.state.dict()
