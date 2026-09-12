from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SensitivityLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    CRITICAL = "critical"

class Permission(BaseModel):
    id: str = Field(..., description="Unique permission ID e.g. storage.read")
    resource: str = Field(..., description="Target resource e.g. storage")
    action: str = Field(..., description="Action e.g. read")
    risk_level: RiskLevel = Field(..., description="Risk associated with this permission")
    sensitivity: SensitivityLevel = Field(default=SensitivityLevel.INTERNAL)
    scope: str = Field(default="resource", description="Scope e.g. resource, account, wildcard")
    description: str = Field(default="")

class Role(BaseModel):
    id: str = Field(..., description="Role ID e.g. Developer")
    name: str = Field(..., description="Human readable name")
    description: str = Field(default="")
    permissions: List[str] = Field(default_factory=list, description="List of permission IDs assigned to this role")

class User(BaseModel):
    id: str
    name: str
    role_ids: List[str] = Field(default_factory=list)

class CloudResource(BaseModel):
    id: str = Field(..., description="Resource ID e.g. ObjectStorage")
    name: str
    type: str = Field(..., description="Type e.g. storage, database, service")
    sensitivity: SensitivityLevel = Field(default=SensitivityLevel.INTERNAL)

class AccessLog(BaseModel):
    timestamp: str
    user: str
    role: str
    permission: str
    resource: str
    action: str
    status: str = Field(default="success", description="success or denied")
    service: str = Field(default="DirectUser", description="Calling service or DirectUser")
    source: str = Field(default="10.0.1.50")

class ServiceDependency(BaseModel):
    source_service: str = Field(..., description="Calling service e.g. ImageProcessingService")
    target_resource: str = Field(..., description="Target resource e.g. ObjectStorage")
    required_permission: str = Field(..., description="Required permission e.g. storage.read")
    criticality: str = Field(default="critical", description="critical or optional")
    description: str = Field(default="")

class PolicyVersion(BaseModel):
    version_id: str
    role_id: str
    permissions: List[str]
    created_at: str
    description: str = ""
