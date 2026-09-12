import pytest
from backend.app.simulator.cloud_environment import SyntheticCloudEnvironment
from backend.app.simulator.access_logs import AccessLogEngine

def test_cloud_environment_initialization():
    env = SyntheticCloudEnvironment()
    roles = env.list_roles()
    assert len(roles) >= 4
    
    dev_role = env.get_role("Developer")
    assert dev_role is not None
    assert "storage.read" in dev_role.permissions
    assert "iam.modify" in dev_role.permissions
    assert "storage.delete" in dev_role.permissions

def test_access_log_analytics():
    log_engine = AccessLogEngine()
    analytics = log_engine.analyze_role_usage("Developer", days=90)
    
    # Verify database.read has direct calls
    assert analytics["database.read"]["direct_calls"] > 0
    
    # Verify storage.read has service calls from ImageProcessingService
    assert analytics["storage.read"]["service_calls"] > 0
    assert "ImageProcessingService" in analytics["storage.read"]["services"]
    
    # Verify storage.delete and iam.modify have zero calls
    assert "storage.delete" not in analytics or analytics["storage.delete"]["total_calls"] == 0
    assert "iam.modify" not in analytics or analytics["iam.modify"]["total_calls"] == 0
