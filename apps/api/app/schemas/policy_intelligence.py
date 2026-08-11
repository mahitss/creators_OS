from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class PolicyCreate(BaseModel):
    name: str
    description: str = ""
    policy_type: str = Field("access", alias="policyType") # access, data, agent, tool, model, execution, approval, risk, compliance, retention, network, integration
    priority: int = 100
    hierarchy_level: str = Field("workspace", alias="hierarchyLevel") # organization, workspace, team, agent, mission, capability
    conditions: Dict[str, Any] = Field(default_factory=dict)
    actions: List[str] = Field(default_factory=list)

class PolicyVersionRead(BaseModel):
    id: str
    policy_id: str = Field(..., alias="policyId")
    version: int
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: List[str]
    priority: int
    status: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class PolicyRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    name: str
    description: str
    policy_type: str = Field(..., alias="policyType")
    status: str
    priority: int
    version: int
    hierarchy_level: str = Field(..., alias="hierarchyLevel")
    conditions: Dict[str, Any]
    actions: List[str]
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    class Config:
        populate_by_name = True

class PolicyEvaluateRequest(BaseModel):
    actor_id: str = Field(..., alias="actorId")
    action: str # read, write, delete, send, execute, approve, deploy, publish, export, share
    resource_id: str = Field(..., alias="resourceId")
    resource_type: str = Field(..., alias="resourceType") # document, email, calendar, database, API, tool, workflow, agent, skill, capability, model, knowledge_object
    context: Dict[str, Any] = Field(default_factory=dict)

class RiskAssessmentRead(BaseModel):
    id: str
    request_id: str = Field(..., alias="requestId")
    overall_risk_level: str = Field(..., alias="overallRiskLevel") # low, medium, high, critical
    data_risk: str = Field(..., alias="dataRisk")
    financial_risk: str = Field(..., alias="financialRisk")
    security_risk: str = Field(..., alias="securityRisk")
    privacy_risk: str = Field(..., alias="privacyRisk")
    operational_risk: str = Field(..., alias="operationalRisk")
    compliance_risk: str = Field(..., alias="complianceRisk")
    reputational_risk: str = Field(..., alias="reputationalRisk")
    score: float

    class Config:
        populate_by_name = True

class PolicyControlRead(BaseModel):
    id: str
    evaluation_id: str = Field(..., alias="evaluationId")
    control_type: str = Field(..., alias="controlType")
    parameters: Dict[str, Any]
    status: str

    class Config:
        populate_by_name = True

class PolicyEvaluateResponse(BaseModel):
    request_id: str = Field(..., alias="requestId")
    decision: str # allow, deny, approval_required, review_required, restricted, escalated, simulation_required, dry_run_required
    policy_references: List[str] = Field(default_factory=list, alias="policyReferences")
    controls: List[PolicyControlRead] = Field(default_factory=list)
    risk_assessment: Optional[RiskAssessmentRead] = Field(None, alias="riskAssessment")
    reason: str
    latency_ms: float = Field(..., alias="latencyMs")
    timestamp: str

    class Config:
        populate_by_name = True

class PolicyRequestRead(BaseModel):
    id: str
    request_id: str = Field(..., alias="requestId")
    actor_id: str = Field(..., alias="actorId")
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    action: str
    resource_id: str = Field(..., alias="resourceId")
    resource_type: str = Field(..., alias="resourceType")
    context: Dict[str, Any]
    timestamp: str

    class Config:
        populate_by_name = True

class PolicyConflictRead(BaseModel):
    id: str
    policy_a_id: str = Field(..., alias="policyAId")
    policy_b_id: str = Field(..., alias="policyBId")
    conflict_description: str = Field(..., alias="conflictDescription")
    precedence_applied: str = Field(..., alias="precedenceApplied")
    status: str

    class Config:
        populate_by_name = True

class PolicyGapRead(BaseModel):
    id: str
    action: str
    resource_type: str = Field(..., alias="resourceType")
    risk_level: str = Field(..., alias="riskLevel")
    frequency: int
    recommended_control: str = Field(..., alias="recommendedControl")
    status: str

    class Config:
        populate_by_name = True

class PolicySimulationCreate(BaseModel):
    test_type: str = Field("shadow", alias="testType") # historical, synthetic, shadow

class PolicySimulationRead(BaseModel):
    id: str
    candidate_policy_id: str = Field(..., alias="candidatePolicyId")
    test_type: str = Field(..., alias="testType")
    comparison_results: Dict[str, Any] = Field(..., alias="comparisonResults")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class PolicyOverrideCreate(BaseModel):
    reason: str
    scope: str = "single_request"
    duration_minutes: Optional[int] = Field(60, alias="durationMinutes")

class PolicyOverrideRead(BaseModel):
    id: str
    policy_id: str = Field(..., alias="policyId")
    actor_id: str = Field(..., alias="actorId")
    reason: str
    scope: str
    expires_at: Optional[str] = Field(None, alias="expiresAt")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class TemporaryAccessGrantCreate(BaseModel):
    actor_id: str = Field(..., alias="actorId")
    resource_type: str = Field(..., alias="resourceType")
    resource_id: str = Field(..., alias="resourceId")
    capability: str
    duration_minutes: int = Field(60, alias="durationMinutes")

class TemporaryAccessGrantRead(BaseModel):
    id: str
    actor_id: str = Field(..., alias="actorId")
    resource_type: str = Field(..., alias="resourceType")
    resource_id: str = Field(..., alias="resourceId")
    capability: str
    starts_at: str = Field(..., alias="startsAt")
    expires_at: str = Field(..., alias="expiresAt")
    granted_by: str = Field(..., alias="grantedBy")
    status: str

    class Config:
        populate_by_name = True

class BreakGlassGrantCreate(BaseModel):
    actor_id: str = Field(..., alias="actorId")
    reason: str
    duration_minutes: int = Field(30, alias="durationMinutes")

class BreakGlassGrantRead(BaseModel):
    id: str
    actor_id: str = Field(..., alias="actorId")
    reason: str
    authorized_by: str = Field(..., alias="authorizedBy")
    starts_at: str = Field(..., alias="startsAt")
    expires_at: str = Field(..., alias="expiresAt")
    audit_trail_id: str = Field(..., alias="auditTrailId")
    status: str

    class Config:
        populate_by_name = True
