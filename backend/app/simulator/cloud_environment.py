from typing import Dict, List, Optional
from backend.app.models.iam import (
    Permission, Role, User, CloudResource, ServiceDependency, RiskLevel, SensitivityLevel
)

class SyntheticCloudEnvironment:
    """
    In-memory synthetic cloud environment modeling users, roles, permissions,
    resources, services, and dependencies.
    """
    def __init__(self):
        self.permissions: Dict[str, Permission] = {}
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, CloudResource] = {}
        self.dependencies: List[ServiceDependency] = []
        self._seed_default_data()

    def _seed_default_data(self):
        # 1. Permissions
        perms_data = [
            # Database
            Permission(id="database.read", resource="Database", action="read", risk_level=RiskLevel.MEDIUM, sensitivity=SensitivityLevel.CONFIDENTIAL, description="Read records from primary database"),
            Permission(id="database.write", resource="Database", action="write", risk_level=RiskLevel.MEDIUM, sensitivity=SensitivityLevel.CONFIDENTIAL, description="Write/update records in primary database"),
            # Storage
            Permission(id="storage.read", resource="ObjectStorage", action="read", risk_level=RiskLevel.MEDIUM, sensitivity=SensitivityLevel.INTERNAL, description="Read objects from S3/Storage bucket"),
            Permission(id="storage.write", resource="ObjectStorage", action="write", risk_level=RiskLevel.MEDIUM, sensitivity=SensitivityLevel.INTERNAL, description="Upload objects to S3/Storage bucket"),
            Permission(id="storage.delete", resource="ObjectStorage", action="delete", risk_level=RiskLevel.HIGH, sensitivity=SensitivityLevel.INTERNAL, description="Delete objects from S3/Storage bucket"),
            # IAM
            Permission(id="iam.read", resource="IAM", action="read", risk_level=RiskLevel.LOW, sensitivity=SensitivityLevel.INTERNAL, description="View IAM roles and policies"),
            Permission(id="iam.modify", resource="IAM", action="modify", risk_level=RiskLevel.CRITICAL, sensitivity=SensitivityLevel.CRITICAL, scope="account", description="Modify IAM roles, policies, and privileges"),
            # Logs
            Permission(id="logs.read", resource="LoggingService", action="read", risk_level=RiskLevel.LOW, sensitivity=SensitivityLevel.INTERNAL, description="View system access logs"),
            Permission(id="logs.write", resource="LoggingService", action="write", risk_level=RiskLevel.LOW, sensitivity=SensitivityLevel.INTERNAL, description="Write log events"),
            # Payment
            Permission(id="payment.read", resource="PaymentService", action="read", risk_level=RiskLevel.HIGH, sensitivity=SensitivityLevel.CRITICAL, description="Read customer payment transactions"),
            Permission(id="payment.write", resource="PaymentService", action="write", risk_level=RiskLevel.CRITICAL, sensitivity=SensitivityLevel.CRITICAL, description="Execute payment transactions"),
        ]
        for p in perms_data:
            self.permissions[p.id] = p

        # 2. Cloud Resources
        resources_data = [
            CloudResource(id="Database", name="Production Database", type="database", sensitivity=SensitivityLevel.CONFIDENTIAL),
            CloudResource(id="ObjectStorage", name="Media & Assets Storage Bucket", type="storage", sensitivity=SensitivityLevel.INTERNAL),
            CloudResource(id="ImageProcessingService", name="Image Processing Microservice", type="service", sensitivity=SensitivityLevel.INTERNAL),
            CloudResource(id="PaymentService", name="Payment Gateway Service", type="service", sensitivity=SensitivityLevel.CRITICAL),
            CloudResource(id="LoggingService", name="Central Audit Logging Service", type="logs", sensitivity=SensitivityLevel.INTERNAL),
            CloudResource(id="AnalyticsService", name="Business Intelligence Service", type="service", sensitivity=SensitivityLevel.INTERNAL),
            CloudResource(id="IAM", name="Identity & Access Manager", type="iam", sensitivity=SensitivityLevel.CRITICAL),
        ]
        for r in resources_data:
            self.resources[r.id] = r

        # 3. Service Dependencies
        self.dependencies = [
            # Microservice -> Resource -> Required Permission
            ServiceDependency(
                source_service="ImageProcessingService",
                target_resource="ObjectStorage",
                required_permission="storage.read",
                criticality="critical",
                description="Image processing worker pipeline reads original images from ObjectStorage"
            ),
            ServiceDependency(
                source_service="ImageProcessingService",
                target_resource="ObjectStorage",
                required_permission="storage.write",
                criticality="critical",
                description="Image processing worker writes processed thumbnails back to ObjectStorage"
            ),
            ServiceDependency(
                source_service="PaymentService",
                target_resource="Database",
                required_permission="database.write",
                criticality="critical",
                description="Payment processor records completed billing ledger events into Database"
            ),
            ServiceDependency(
                source_service="AnalyticsService",
                target_resource="Database",
                required_permission="database.read",
                criticality="critical",
                description="Analytics pipeline queries user metrics from Database"
            ),
        ]

        # 4. Roles
        self.roles = {
            "Developer": Role(
                id="Developer",
                name="Application Developer",
                description="Standard role for software engineers building and maintaining core services",
                permissions=[
                    "database.read",
                    "database.write",
                    "storage.read",
                    "storage.write",
                    "storage.delete",
                    "iam.modify"
                ]
            ),
            "DataAnalyst": Role(
                id="DataAnalyst",
                name="Data Analyst",
                description="Role for querying business intelligence and generating reports",
                permissions=["database.read", "logs.read", "storage.read"]
            ),
            "DevOps": Role(
                id="DevOps",
                name="DevOps Infrastructure Engineer",
                description="Role for managing cloud deployment and logging pipelines",
                permissions=["database.read", "database.write", "storage.read", "storage.write", "logs.read", "logs.write", "iam.read"]
            ),
            "Admin": Role(
                id="Admin",
                name="Cloud System Administrator",
                description="Full administrative access role",
                permissions=["database.read", "database.write", "storage.read", "storage.write", "storage.delete", "iam.read", "iam.modify", "logs.read", "logs.write", "payment.read", "payment.write"]
            ),
        }

        # 5. Users
        self.users = {
            "Alice": User(id="Alice", name="Alice Chen (Senior Developer)", role_ids=["Developer"]),
            "Bob": User(id="Bob", name="Bob Smith (Data Analyst)", role_ids=["DataAnalyst"]),
            "Charlie": User(id="Charlie", name="Charlie Brown (DevOps Lead)", role_ids=["DevOps"]),
            "David": User(id="David", name="David Miller (System Admin)", role_ids=["Admin"]),
        }

    def get_role(self, role_id: str) -> Optional[Role]:
        return self.roles.get(role_id)

    def get_permission(self, permission_id: str) -> Optional[Permission]:
        return self.permissions.get(permission_id)

    def get_resource(self, resource_id: str) -> Optional[CloudResource]:
        return self.resources.get(resource_id)

    def list_roles(self) -> List[Role]:
        return list(self.roles.values())

    def reset(self):
        """Reset environment to default seed state."""
        self._seed_default_data()
