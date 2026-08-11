from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class IntegrationRead(BaseModel):
    id: str
    organization_id: str
    name: str
    provider: str
    category: str
    description: str
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

class IntegrationConnectionRead(BaseModel):
    id: str
    integration_id: str
    organization_id: str
    workspace_id: str
    owner_id: str
    auth_type: str
    status: str
    scopes: List[str]
    metadata_info: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class IntegrationCapabilityRead(BaseModel):
    id: str
    integration_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    risk_level: str
    required_scopes: List[str]
    enabled: bool

class ActionExecuteRequest(BaseModel):
    capability_id: str = Field(..., alias="capabilityId")
    connection_id: str = Field(..., alias="connectionId")
    input_data: Dict[str, Any] = Field(default_dict={}, alias="inputData")
    idempotency_key: Optional[str] = Field(None, alias="idempotencyKey")
    simulate_only: bool = Field(False, alias="simulateOnly")

class ActionResultRead(BaseModel):
    id: str
    action_id: str
    status: str
    provider_status: int
    resource_reference: Dict[str, Any]
    safe_metadata: Dict[str, Any]
    error_code: Optional[str] = None
    recorded_at: datetime

class IntegrationActionRead(BaseModel):
    id: str
    capability_id: str
    connection_id: str
    actor: str
    input_data: Dict[str, Any]
    status: str
    result_reference: Dict[str, Any]
    idempotency_key: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class WebhookIngestRequest(BaseModel):
    event_id: str = Field(..., alias="eventId")
    event_type: str = Field(..., alias="eventType")
    payload: Dict[str, Any]
    signature: str
    timestamp: str

class IntegrationHealthRead(BaseModel):
    id: str
    connection_id: str
    status: str
    latency_ms: float
    error_rate: float
    circuit_breaker_state: str
    last_successful_call: Optional[datetime] = None
    last_error: Optional[str] = None
