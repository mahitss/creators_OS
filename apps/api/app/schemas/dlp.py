from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class DataAssetRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    organization_id: str = Field(..., alias="organizationId")
    source_type: str = Field(..., alias="sourceType")
    source_id: str = Field(..., alias="sourceId")
    classification: str
    owner_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class SensitiveDataFindingRead(BaseModel):
    id: str
    asset_id: str
    workspace_id: str
    detector: str  # email, phone, credit_card, api_key, jwt_token, private_key, password
    classification: str
    action: str  # allow, redact, block, quarantine
    resource: str
    status: str
    created_at: datetime

class DLPPolicyCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    name: str
    classification: str
    source_scope: str = "all"
    destination_scope: str = "external"
    allowed_action: str = "redact"  # allow, redact, block, require_approval, quarantine
    approval_required: bool = False

class DLPPolicyRead(BaseModel):
    id: str
    organization_id: str
    name: str
    classification: str
    source_scope: str
    destination_scope: str
    allowed_action: str
    approval_required: bool
    enabled: bool
    version: int
    created_at: datetime

class DLPDecisionRead(BaseModel):
    id: str
    workspace_id: str
    action: str  # allow, redact, block, require_approval, quarantine
    reason_code: str
    classification: str
    detectors: List[str]
    policy_version: int
    redactions_count: int
    created_at: datetime

class DataLineageNodeRead(BaseModel):
    id: str
    resource_id: str
    type: str  # source, agent, model, output, destination
    classification: str
    timestamp: datetime

class DataLineageEdgeRead(BaseModel):
    id: str
    source_id: str
    destination_id: str
    transformation: str
    policy_decision_id: Optional[str] = None
    timestamp: datetime

class QuarantineRecordRead(BaseModel):
    id: str
    workspace_id: str
    resource_type: str
    resource_id: str
    reason: str
    quarantined_by: str
    status: str
    created_at: datetime

class PolicySimulationTestCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    content_sample: str = Field(..., alias="contentSample")
    destination: str = "external_model"
