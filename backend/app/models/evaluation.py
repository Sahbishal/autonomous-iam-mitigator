from typing import List, Dict, Any
from pydantic import BaseModel

class EvaluationReport(BaseModel):
    scenario_id: str
    role_id: str
    initial_permissions_count: int
    final_permissions_count: int
    permissions_removed: List[str]
    permissions_preserved: List[str]
    initial_risk_score: float
    final_risk_score: float
    security_improvement_pct: float
    initial_functionality_score: float
    final_functionality_score: float
    simulations_run: int
    simulation_failures_encountered: int
    replanning_iterations: int
    hidden_dependencies_identified: List[str]
    verification_passed: bool
    verdict: str  # SUCCESS, PARTIAL, FAILED
    summary: str
