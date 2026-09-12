from typing import Dict, Any, Callable, List
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.access_logs import AccessLogEngine
from backend.app.simulator.dependency_graph import CloudDependencyGraph
from backend.app.simulator.policy_simulator import PolicySimulator

class ToolContext:
    """Shared context for executing tools against synthetic environment state."""
    def __init__(self, env: SyntheticCloudEnvironment, log_engine: AccessLogEngine, dep_graph: CloudDependencyGraph, simulator: PolicySimulator):
        self.env = env
        self.log_engine = log_engine
        self.dep_graph = dep_graph
        self.simulator = simulator
        self.proposed_policies: Dict[str, Dict[str, Any]] = {}
        self.simulation_results: Dict[str, Any] = {}

class ToolRegistry:
    """Registry for agent callable tools."""
    def __init__(self, context: ToolContext):
        self.context = context
        self.tools: Dict[str, Callable[..., Dict[str, Any]]] = {}
        self.definitions: List[Dict[str, Any]] = []

    def register(self, name: str, description: str, parameters: Dict[str, Any], func: Callable[..., Dict[str, Any]]):
        self.tools[name] = func
        self.definitions.append({
            "name": name,
            "description": description,
            "parameters": parameters
        })

    def execute(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        try:
            return self.tools[tool_name](**args)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
