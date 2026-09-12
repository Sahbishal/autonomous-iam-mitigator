from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SimulationResult(BaseModel):
    simulation_id: str
    policy_version: str
    success: bool
    security_score: float = Field(..., description="0 to 100 risk reduction score")
    functionality_score: float = Field(..., description="0 to 100 service health score")
    passed_tests: int = 0
    failed_tests: int = 0
    failed_services: List[str] = Field(default_factory=list)
    denied_actions: List[Dict[str, Any]] = Field(default_factory=list)
    affected_resources: List[str] = Field(default_factory=list)
    dependency_failures: List[Dict[str, Any]] = Field(default_factory=list)
    details: str = ""

class Evidence(BaseModel):
    permission_id: str
    decision: str = Field(..., description="removed, preserved, or retained")
    direct_usage_count: int = 0
    dependency_usage: bool = False
    dependent_services: List[str] = Field(default_factory=list)
    risk_level: str = "medium"
    explanation: str = ""

class AgentStepLog(BaseModel):
    step_number: int
    phase: str = Field(..., description="OBSERVE, ANALYZE, PLAN, ACT, EVALUATE, ADAPT, VERIFY")
    thought: str
    tool_called: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    observation: Optional[Any] = None
    timestamp: str = ""
    status: str = Field(default="info", description="success, failure, warning, info")

class AgentState(BaseModel):
    session_id: str
    scenario_id: str = "scenario_b"
    role_id: str = "Developer"
    goal: str = "Reduce excessive IAM permissions while preserving 100% service functionality"
    status: str = "idle"  # idle, running, completed, failed
    initial_permissions: List[str] = Field(default_factory=list)
    current_permissions: List[str] = Field(default_factory=list)
    candidate_removals: List[str] = Field(default_factory=list)
    preserved_permissions: List[str] = Field(default_factory=list)
    discovered_dependencies: List[Dict[str, Any]] = Field(default_factory=list)
    policy_history: List[Dict[str, Any]] = Field(default_factory=list)
    simulation_history: List[SimulationResult] = Field(default_factory=list)
    step_history: List[AgentStepLog] = Field(default_factory=list)
    evidence_list: List[Evidence] = Field(default_factory=list)
    initial_risk_score: float = 0.0
    current_risk_score: float = 0.0
    initial_functionality_score: float = 100.0
    current_functionality_score: float = 100.0
    iteration: int = 0
    verification_passed: bool = False
