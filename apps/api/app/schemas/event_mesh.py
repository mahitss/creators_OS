from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class EventEnvelopePublishRequest(BaseModel):
    event_type: str = Field(..., alias="eventType")
    event_version: str = Field("1.0.0", alias="eventVersion")
    organization_id: str = Field("org_default_creator", alias="organizationId")
    workspace_id: Optional[str] = Field("ws_default_01", alias="workspaceId")
    source: str = Field(...)
    subject: str = Field(...)
    correlation_id: Optional[str] = Field(None, alias="correlationId")
    causation_id: Optional[str] = Field(None, alias="causationId")
    producer: str = Field(...)
    payload_reference: Dict[str, Any] = Field(default_factory=dict, alias="payloadReference")
    schema_version: str = Field("1.0.0", alias="schemaVersion")
    classification: str = Field("internal")
    metadata_info: Dict[str, Any] = Field(default_factory=dict, alias="metadataInfo")

    model_config = ConfigDict(populate_by_name=True)

class EventEnvelopeRead(BaseModel):
    id: str
    event_id: str = Field(..., alias="eventId")
    event_type: str = Field(..., alias="eventType")
    event_version: str = Field(..., alias="eventVersion")
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    source: str
    subject: str
    timestamp: str
    correlation_id: str = Field(..., alias="correlationId")
    causation_id: Optional[str] = Field(None, alias="causationId")
    producer: str
    payload_reference: Dict[str, Any] = Field(..., alias="payloadReference")
    schema_version: str = Field(..., alias="schemaVersion")
    classification: str
    metadata_info: Dict[str, Any] = Field(..., alias="metadataInfo")

    model_config = ConfigDict(populate_by_name=True)

class EventSchemaRead(BaseModel):
    id: str
    event_type: str = Field(..., alias="eventType")
    version: str
    schema_def: Dict[str, Any] = Field(..., alias="schemaJson")
    producer: str
    status: str
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class EventSubscriptionCreate(BaseModel):
    organization_id: str = Field("org_default_creator", alias="organizationId")
    workspace_id: Optional[str] = Field("ws_default_01", alias="workspaceId")
    event_type: str = Field(..., alias="eventType")
    consumer: str = Field(...)
    filter_config: Dict[str, Any] = Field(default_factory=dict, alias="filterConfig")
    enabled: bool = Field(True)

    model_config = ConfigDict(populate_by_name=True)

class EventSubscriptionRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    event_type: str = Field(..., alias="eventType")
    consumer: str
    filter_config: Dict[str, Any] = Field(..., alias="filterConfig")
    enabled: bool
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class EventDeliveryRead(BaseModel):
    id: str
    event_id: str = Field(..., alias="eventId")
    subscription_id: str = Field(..., alias="subscriptionId")
    status: str
    attempt_count: int = Field(..., alias="attemptCount")
    next_retry_at: Optional[str] = Field(None, alias="nextRetryAt")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    delivered_at: Optional[str] = Field(None, alias="deliveredAt")

    model_config = ConfigDict(populate_by_name=True)

class EventDeadLetterRead(BaseModel):
    id: str
    event_id: str = Field(..., alias="eventId")
    event_type: str = Field(..., alias="eventType")
    producer: str
    error: str
    attempt_count: int = Field(..., alias="attemptCount")
    payload_ref: Dict[str, Any] = Field(..., alias="payloadRef")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class EventReplayRequest(BaseModel):
    reason: str = Field(...)

class EventReplayRead(BaseModel):
    id: str
    event_id: str = Field(..., alias="eventId")
    authorized_by: str = Field(..., alias="authorizedBy")
    reason: str
    status: str
    replayed_at: str = Field(..., alias="replayedAt")

    model_config = ConfigDict(populate_by_name=True)

class EventHealthRead(BaseModel):
    throughput_eps: float = Field(..., alias="throughputEps")
    latency_p95: float = Field(..., alias="latencyP95")
    error_rate: float = Field(..., alias="errorRate")
    consumer_lag: int = Field(..., alias="consumerLag")
    dead_letter_count: int = Field(..., alias="deadLetterCount")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class EventCatalogRead(BaseModel):
    id: str
    event_type: str = Field(..., alias="eventType")
    version: str
    producer: str
    description: str
    classification: str
    retention_days: int = Field(..., alias="retentionDays")

    model_config = ConfigDict(populate_by_name=True)
