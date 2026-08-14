from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class OperationalHealthRead(BaseModel):
    scope: str
    scope_id: str = Field(..., alias="scopeId")
    status: str
    signals: Dict[str, Any]
    source: str
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)

class ServiceTopologyNode(BaseModel):
    id: str
    name: str
    category: str
    status: str
    dependencies: List[str]
    latency_ms: float = Field(..., alias="latencyMs")
    error_rate: float = Field(..., alias="errorRate")
    throughput_qps: float = Field(..., alias="throughputQps")

    model_config = ConfigDict(populate_by_name=True)

class ControlActionRequest(BaseModel):
    action_type: str = Field(..., alias="actionType")
    target_resource: str = Field(..., alias="targetResource")
    reason: str
    risk_level: Optional[str] = Field("medium", alias="riskLevel")
    idempotency_key: Optional[str] = Field(None, alias="idempotencyKey")
    metadata_info: Dict[str, Any] = Field(default_factory=dict, alias="metadataInfo")

    model_config = ConfigDict(populate_by_name=True)

class ControlActionRead(BaseModel):
    id: str
    action_type: str = Field(..., alias="actionType")
    target_resource: str = Field(..., alias="targetResource")
    requested_by: str = Field(..., alias="requestedBy")
    reason: str
    risk_level: str = Field(..., alias="riskLevel")
    status: str
    idempotency_key: Optional[str] = Field(None, alias="idempotencyKey")
    metadata_info: Dict[str, Any] = Field(..., alias="metadataInfo")
    created_at: str = Field(..., alias="createdAt")
    completed_at: Optional[str] = Field(None, alias="completedAt")

    model_config = ConfigDict(populate_by_name=True)

class ControlActionApprovalRequest(BaseModel):
    decision: str # approved, rejected
    comments: Optional[str] = None

class ControlActionApprovalRead(BaseModel):
    id: str
    action_id: str = Field(..., alias="actionId")
    approver_id: str = Field(..., alias="approverId")
    decision: str
    comments: Optional[str] = None
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class OperationsOverviewRead(BaseModel):
    system_status: str = Field(..., alias="systemStatus")
    active_incidents_count: int = Field(..., alias="activeIncidentsCount")
    workflow_health: str = Field(..., alias="workflowHealth")
    agent_health: str = Field(..., alias="agentHealth")
    integration_health: str = Field(..., alias="integrationHealth")
    security_health: str = Field(..., alias="securityHealth")
    cost_health: str = Field(..., alias="costHealth")
    event_health: str = Field(..., alias="eventHealth")
    contributing_signals: List[Dict[str, Any]] = Field(..., alias="contributingSignals")
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)

class AIOperationsQueryRequest(BaseModel):
    prompt: str

class AIOperationsQueryResponse(BaseModel):
    query: str
    answer: str
    evidence_signals: List[Dict[str, Any]] = Field(..., alias="evidenceSignals")
    proposed_actions: List[Dict[str, Any]] = Field(..., alias="proposedActions")
    confidence: float
