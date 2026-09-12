import pytest
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.dependency_graph import CloudDependencyGraph

def test_dependency_graph_building():
    env = SyntheticCloudEnvironment()
    dep_graph = CloudDependencyGraph(env)
    
    deps = dep_graph.get_service_dependencies("storage.read")
    assert len(deps) > 0
    assert deps[0]["service"] == "ImageProcessingService"
    assert deps[0]["target_resource"] == "ObjectStorage"
    assert deps[0]["criticality"] == "critical"

def test_permission_impact():
    env = SyntheticCloudEnvironment()
    dep_graph = CloudDependencyGraph(env)
    
    impact = dep_graph.get_permission_impact("storage.read")
    assert impact["has_dependencies"] is True
    assert "ImageProcessingService" in impact["affected_services"]
    
    impact_unused = dep_graph.get_permission_impact("storage.delete")
    assert impact_unused["has_dependencies"] is False
