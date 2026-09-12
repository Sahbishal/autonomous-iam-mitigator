import networkx as nx
from typing import List, Dict, Any, Optional
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment

class CloudDependencyGraph:
    """
    Graph representation using NetworkX modeling Cloud Services, Resources,
    Permissions, and Role-to-Service execution paths.
    """
    def __init__(self, env: SyntheticCloudEnvironment):
        self.env = env
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        """Constructs directed graph nodes and edges from environment data."""
        self.graph.clear()

        # Add Resource Nodes
        for res_id, res in self.env.resources.items():
            self.graph.add_node(res_id, type="resource", label=res.name, sensitivity=res.sensitivity.value)

        # Add Permission Nodes
        for perm_id, perm in self.env.permissions.items():
            self.graph.add_node(perm_id, type="permission", label=perm.id, risk=perm.risk_level.value)
            # Edge from Permission to Resource
            self.graph.add_edge(perm_id, perm.resource, relationship="protects")

        # Add Service Dependencies (Service -> Resource -> Permission)
        for dep in self.env.dependencies:
            service_id = dep.source_service
            if not self.graph.has_node(service_id):
                self.graph.add_node(service_id, type="service", label=service_id)

            # Edge from Service to Permission (Service depends on Permission)
            self.graph.add_edge(
                service_id,
                dep.required_permission,
                relationship="requires_permission",
                target_resource=dep.target_resource,
                criticality=dep.criticality,
                description=dep.description
            )
            # Edge from Service to Resource
            self.graph.add_edge(
                service_id,
                dep.target_resource,
                relationship="uses_resource"
            )

        # Add Role relationships to Services (e.g. Developer role relies on ImageProcessingService)
        self.graph.add_node("Developer", type="role", label="Developer")
        self.graph.add_edge("Developer", "ImageProcessingService", relationship="executes_workflow")

    def get_service_dependencies(self, permission_id: str) -> List[Dict[str, Any]]:
        """
        Returns all services and resources that depend on the given permission_id.
        """
        dependent_services = []
        if not self.graph.has_node(permission_id):
            return dependent_services

        # Search for nodes pointing to permission_id with relationship="requires_permission"
        for source_node, _, data in self.graph.in_edges(permission_id, data=True):
            if data.get("relationship") == "requires_permission":
                dependent_services.append({
                    "service": source_node,
                    "target_resource": data.get("target_resource"),
                    "required_permission": permission_id,
                    "criticality": data.get("criticality", "critical"),
                    "description": data.get("description", "")
                })

        return dependent_services

    def get_permission_impact(self, permission_id: str) -> Dict[str, Any]:
        """
        Evaluates the potential system impact if a permission is revoked.
        """
        deps = self.get_service_dependencies(permission_id)
        is_breaking = len(deps) > 0
        affected_services = [d["service"] for d in deps]

        return {
            "permission_id": permission_id,
            "has_dependencies": is_breaking,
            "affected_services": affected_services,
            "dependency_details": deps,
            "severity": "CRITICAL" if any(d["criticality"] == "critical" for d in deps) else ("LOW" if not is_breaking else "MEDIUM")
        }

    def get_full_graph_structure(self) -> Dict[str, Any]:
        """Returns node and edge structure formatted for UI network visualization."""
        nodes = []
        for n, data in self.graph.nodes(data=True):
            nodes.append({
                "id": n,
                "type": data.get("type", "unknown"),
                "label": data.get("label", n),
                "risk": data.get("risk"),
                "sensitivity": data.get("sensitivity")
            })

        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relationship": data.get("relationship", "relates_to"),
                "criticality": data.get("criticality")
            })

        return {"nodes": nodes, "edges": edges}
