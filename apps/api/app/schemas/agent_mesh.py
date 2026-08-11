from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class AgentCapabilityCreate(BaseModel):
    agent_id: str = Field(..., alias="agentId")
    type: str  # research, analysis, retrieval, coding, planning, writing, data_processing, validation, communication, scheduling
    name: str
    description: Optional[str] = ""
    input_schema: Dict[str, Any] = Field(default_factory=dict, alias="inputSchema")
    output_schema: Dict[str, Any] = Field(default_factory=dict, alias="outputSchema")
    risk_level: str = Field("low", alias="riskLevel")

class AgentCapabilityRead(BaseModel):
    id: str
    agent_id: str
    type: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    risk_level: str
    enabled: bool
    created_at: datetime

class AgentRegistryRead(BaseModel):
    id: str
    workspace_id: str
    organization_id: str
    agent_name: str
    specialization: str
    capabilities: List[str]
    status: str
    availability: bool
    max_delegation_depth: int
    max_concurrent_tasks: int
    budget_limit: float
    data_classification_ceiling: str
    risk_level: str
    created_at: datetime

class DelegationRequestCreate(BaseModel):
    parent_agent_id: str = Field(..., alias="parentAgentId")
    child_agent_id: str = Field(..., alias="childAgentId")
    mission_id: str = Field(..., alias="missionId")
    task_id: str = Field(..., alias="taskId")
    scope: str = "read_only"
    input_references: List[Dict[str, Any]] = Field(default_factory=list, alias="inputReferences")
    required_output: str = Field(..., alias="requiredOutput")
    risk_level: str = Field("low", alias="riskLevel")

class DelegationRequestRead(BaseModel):
    id: str
    parent_agent_id: str
    child_agent_id: str
    mission_id: str
    task_id: str
    scope: str
    input_references: List[Dict[str, Any]]
    required_output: str
    risk_level: str
    status: str
    created_at: datetime

class AgentArtifactRead(BaseModel):
    id: str
    mission_id: str
    task_id: str
    agent_id: str
    type: str
    schema_version: str
    reference_url: Optional[str] = None
    content_json: Dict[str, Any]
    classification: str
    validation_status: str
    version: int
    created_at: datetime

class AgentDisagreementRead(BaseModel):
    id: str
    mission_id: str
    task_id: str
    agents: List[str]
    positions: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    resolution: str
    status: str
    created_at: datetime

class AgentReviewTaskRead(BaseModel):
    id: str
    mission_id: str
    task_id: str
    artifact_id: str
    reason: str
    risk_level: str
    status: str
    assigned_to: Optional[str] = None
    created_at: datetime

class ReviewActionRequest(BaseModel):
    action: str  # approve, reject, request_revision, cancel
    feedback: Optional[str] = ""
    assigned_to: Optional[str] = Field("usr_executive_01", alias="assignedTo")
