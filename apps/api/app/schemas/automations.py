from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class SystemEventCreate(BaseModel):
    workspace_id: str
    source: str  # gmail, calendar, drive, mission, agent, approval, workspace, policy, integration, system
    event_type: str
    resource_type: str
    resource_id: str
    actor_id: Optional[str] = None
    occurred_at: Optional[datetime] = None
    dedupe_key: Optional[str] = None
    metadata_dict: Dict[str, Any] = Field(default_factory=dict)
    sensitivity: str = "internal"

class SystemEventRead(BaseModel):
    id: str
    workspace_id: str
    source: str
    event_type: str
    resource_type: str
    resource_id: str
    actor_id: Optional[str] = None
    occurred_at: datetime
    received_at: datetime
    dedupe_key: str
    metadata_dict: Dict[str, Any]
    sensitivity: str
    status: str
    created_at: datetime

class AgentTriggerCreate(BaseModel):
    workspace_id: str
    name: str
    description: Optional[str] = None
    event_type: str
    conditions: Dict[str, Any] = Field(default_factory=dict)
    action_type: str = "create_attention"  # create_attention, create_insight, create_mission, start_agent_run, request_approval, send_notification
    agent_definition_id: Optional[str] = None
    mission_id: Optional[str] = None
    scope: str = "workspace"  # personal, workspace, mission
    cooldown_seconds: int = 7200

class AgentTriggerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    action_type: Optional[str] = None
    agent_definition_id: Optional[str] = None
    mission_id: Optional[str] = None
    enabled: Optional[bool] = None
    status: Optional[str] = None
    scope: Optional[str] = None
    cooldown_seconds: Optional[int] = None

class AgentTriggerRead(BaseModel):
    id: str
    workspace_id: str
    created_by: str
    name: str
    description: Optional[str] = None
    event_type: str
    conditions: Dict[str, Any]
    action_type: str
    agent_definition_id: Optional[str] = None
    mission_id: Optional[str] = None
    enabled: bool
    status: str
    scope: str
    cooldown_seconds: int
    last_triggered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class SignalRead(BaseModel):
    id: str
    event_id: str
    workspace_id: str
    type: str
    importance: str
    confidence: float
    reason_code: str
    details: Dict[str, Any]
    created_at: datetime

class InsightRead(BaseModel):
    id: str
    workspace_id: str
    scope: str
    source_events: Dict[str, Any]
    title: str
    summary: str
    importance: str
    confidence: float
    source_references: Dict[str, Any]
    status: str
    created_at: datetime
    expires_at: Optional[datetime] = None

class AutomationExecutionRead(BaseModel):
    id: str
    trigger_id: str
    event_id: str
    workspace_id: str
    decision: str
    action_type: str
    status: str
    agent_run_id: Optional[str] = None
    insight_id: Optional[str] = None
    reason: str
    chain_id: Optional[str] = None
    chain_depth: int
    created_at: datetime

class DryRunTestRequest(BaseModel):
    event_type: str
    resource_type: str
    resource_id: str
    metadata_dict: Dict[str, Any] = Field(default_factory=dict)

class DryRunTestResponse(BaseModel):
    matched: bool
    trigger_id: str
    trigger_name: str
    policy_decision: str
    reason: str
    proposed_action: str
    requires_approval: bool
    cooldown_active: bool
    chain_depth: int
