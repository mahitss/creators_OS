from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class CapabilityCreate(BaseModel):
    owner_type: str = Field("workspace", alias="ownerType")
    owner_id: str = Field("ws_default_01", alias="ownerId")
    name: str
    display_name: str = Field(..., alias="displayName")
    description: str
    category: str = Field("productivity", alias="category")
    type: str = Field("skill", alias="type")
    input_schema: Dict[str, Any] = Field(default_factory=dict, alias="inputSchema")
    output_schema: Dict[str, Any] = Field(default_factory=dict, alias="outputSchema")
    requirements: List[str] = Field(default_factory=list, alias="requirements")
    dependencies: List[str] = Field(default_factory=list, alias="dependencies")

class CapabilityRead(BaseModel):
    id: str
    organization_id: Optional[str] = Field(None, alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    owner_type: str = Field(..., alias="ownerType")
    owner_id: str = Field(..., alias="ownerId")
    name: str
    display_name: str = Field(..., alias="displayName")
    description: str
    category: str
    type: str
    status: str
    current_version_id: Optional[str] = Field(None, alias="currentVersionId")
    access_status: str = Field("accessible", alias="accessStatus") # accessible, approval_required, not_invokable
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class CapabilityVersionRead(BaseModel):
    id: str
    capability_id: str = Field(..., alias="capabilityId")
    version: int
    definition_reference: Dict[str, Any] = Field(..., alias="definitionReference")
    input_schema: Dict[str, Any] = Field(..., alias="inputSchema")
    output_schema: Dict[str, Any] = Field(..., alias="outputSchema")
    requirements: List[str] = Field(..., alias="requirements")
    dependencies: List[str] = Field(..., alias="dependencies")
    status: str
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class CapabilityInstallationRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    capability_id: str = Field(..., alias="capabilityId")
    installed_by: str = Field(..., alias="installedBy")
    status: str
    installed_at: str = Field(..., alias="installedAt")

    model_config = ConfigDict(populate_by_name=True)

class CapabilityHealthRead(BaseModel):
    id: str
    capability_id: str = Field(..., alias="capabilityId")
    availability_rate: float = Field(..., alias="availabilityRate")
    latency_p95_ms: int = Field(..., alias="latencyP95Ms")
    error_rate: float = Field(..., alias="errorRate")
    security_state: str = Field(..., alias="securityState")
    status: str

    model_config = ConfigDict(populate_by_name=True)

class CapabilityRequestCreate(BaseModel):
    capability_id: str = Field(..., alias="capabilityId")
    reason: str

class CapabilityRequestRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    capability_id: str = Field(..., alias="capabilityId")
    requested_by: str = Field(..., alias="requestedBy")
    reason: str
    status: str
    reviewed_by: Optional[str] = Field(None, alias="reviewedBy")
    reviewed_at: Optional[str] = Field(None, alias="reviewedAt")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class CapabilityInvokeRequest(BaseModel):
    input_payload: Dict[str, Any] = Field(default_factory=dict, alias="inputPayload")
    calling_capability_ids: List[str] = Field(default_factory=list, alias="callingCapabilityIds")

class CapabilityInvokeResponse(BaseModel):
    capability_id: str = Field(..., alias="capabilityId")
    version_id: str = Field(..., alias="versionId")
    status: str
    routed_engine: str = Field(..., alias="routedEngine")
    output_payload: Dict[str, Any] = Field(..., alias="outputPayload")
    execution_id: str = Field(..., alias="executionId")
    duration_ms: int = Field(..., alias="durationMs")

class CapabilityPackageRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    name: str
    version: str
    contained_capability_ids: List[str] = Field(..., alias="containedCapabilityIds")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)
