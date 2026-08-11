from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class OrganizationMemberRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    user_id: str = Field(..., alias="userId")
    role: str  # owner, admin, security_admin, billing_admin, member, viewer
    status: str
    created_at: datetime
    updated_at: datetime

class RoleUpdate(BaseModel):
    new_role: str = Field(..., alias="newRole")
    reason: Optional[str] = None

class AuditEventRead(BaseModel):
    id: str
    organization_id: str
    workspace_id: Optional[str] = None
    actor_id: str
    actor_type: str
    action: str
    resource_type: str
    resource_id: str
    result: str
    reason: Optional[str] = None
    ip_hash: Optional[str] = None
    user_agent_hash: Optional[str] = None
    metadata_info: Dict[str, Any]
    created_at: datetime

class RetentionPolicyCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    resource_type: str = Field(..., alias="resourceType")
    retention_days: int = Field(90, alias="retentionDays")
    legal_hold: bool = Field(False, alias="legalHold")

class RetentionPolicyRead(BaseModel):
    id: str
    organization_id: str
    resource_type: str
    retention_days: int
    legal_hold: bool
    status: str
    created_by: str
    updated_at: datetime

class LegalHoldCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    resource_type: str = Field(..., alias="resourceType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    reason: str

class LegalHoldRead(BaseModel):
    id: str
    organization_id: str
    resource_type: str
    resource_id: Optional[str] = None
    reason: str
    created_by: str
    created_at: datetime

class AccessReviewCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    title: str
    scope: str = "all_members"

class AccessReviewRead(BaseModel):
    id: str
    organization_id: str
    title: str
    scope: str
    status: str
    created_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None

class AccessReviewItemRead(BaseModel):
    id: str
    review_id: str
    resource: str
    principal_id: str
    permission: str
    scope: str
    last_used_at: Optional[datetime] = None
    risk_level: str
    decision: str  # retain, remove, modify, unknown
    reviewer_id: Optional[str] = None
    created_at: datetime

class ComplianceControlRead(BaseModel):
    id: str
    organization_id: str
    framework: str  # SOC_2, ISO_27001, GDPR
    control_id: str
    title: str
    description: str
    status: str  # not_assessed, in_progress, partially_supported, supported, not_applicable
    owner: str
    last_reviewed_at: datetime

class ComplianceEvidenceRead(BaseModel):
    id: str
    organization_id: str
    control_id: str
    evidence_type: str
    source: str
    source_reference: str
    collected_at: datetime
    status: str

class SecurityFindingRead(BaseModel):
    id: str
    organization_id: str
    severity: str
    category: str
    source: str
    resource: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

class PolicySimulationCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    policy_definition: Dict[str, Any] = Field(..., alias="policyDefinition")

class PolicySimulationRead(BaseModel):
    id: str
    organization_id: str
    policy_definition: Dict[str, Any]
    affected_workflows: List[Dict[str, Any]]
    affected_agents: List[Dict[str, Any]]
    simulated_by: str
    created_at: datetime
