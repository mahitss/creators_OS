from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class UsageRecordCreate(BaseModel):
    workspace_id: str = Field(..., alias="workspaceId")
    trace_id: str = Field(..., alias="traceId")
    span_id: str = Field(..., alias="spanId")
    parent_span_id: Optional[str] = Field(None, alias="parentSpanId")
    user_id: Optional[str] = Field(None, alias="userId")
    mission_id: Optional[str] = Field(None, alias="missionId")
    agent_run_id: Optional[str] = Field(None, alias="agentRunId")
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    workflow_run_id: Optional[str] = Field(None, alias="workflowRunId")
    node_id: Optional[str] = Field(None, alias="nodeId")
    provider: str
    model: str
    resource_type: str = "model"  # model, tool, embedding, retrieval
    input_units: int = 0
    output_units: int = 0
    cached_units: int = 0
    reasoning_units: int = 0
    duration_ms: int = 0
    error_code: Optional[str] = None

class UsageRecordRead(BaseModel):
    id: str
    workspace_id: str
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    user_id: Optional[str] = None
    mission_id: Optional[str] = None
    agent_run_id: Optional[str] = None
    workflow_id: Optional[str] = None
    workflow_run_id: Optional[str] = None
    node_id: Optional[str] = None
    provider: str
    model: str
    resource_type: str
    input_units: int
    output_units: int
    cached_units: int
    reasoning_units: int
    cost: float
    currency: str
    pricing_version: int
    status: str
    duration_ms: int
    error_code: Optional[str] = None
    timestamp: datetime

class BudgetCreate(BaseModel):
    workspace_id: str = Field(..., alias="workspaceId")
    scope_type: str = "workspace"  # workspace, user, mission, workflow, agent
    scope_id: str
    period: str = "monthly"  # daily, monthly, total
    limit_amount: float
    currency: str = "USD"
    warning_threshold_pct: float = 90.0

class BudgetRead(BaseModel):
    id: str
    workspace_id: str
    scope_type: str
    scope_id: str
    period: str
    limit_amount: float
    used_amount: float
    reserved_amount: float
    currency: str
    warning_threshold_pct: float
    status: str
    created_at: datetime
    updated_at: datetime

class UsageAnomalyRead(BaseModel):
    id: str
    workspace_id: str
    type: str  # cost_spike, latency_spike, failure_spike, token_spike, retry_spike
    severity: str
    resource_type: str
    resource_id: str
    observed_value: float
    baseline_value: float
    confidence: float
    status: str
    explanation: str
    created_at: datetime

class OperationalIncidentRead(BaseModel):
    id: str
    workspace_id: Optional[str] = None
    service: str
    severity: str
    status: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    summary: str
    source_references: Dict[str, Any]

class FinOpsOverviewResponse(BaseModel):
    workspace_id: str
    today_cost: float
    last_7d_cost: float
    last_30d_cost: float
    mtd_cost: float
    budget_limit: float
    budget_used: float
    budget_remaining: float
    active_incidents_count: int
    active_anomalies_count: int
    currency: str = "USD"

class FinOpsForecastResponse(BaseModel):
    workspace_id: str
    current_run_rate_daily: float
    projected_end_of_month_cost: float
    historical_baseline_daily: float
    confidence: float
    forecast_status: str

class ModelHealthSnapshot(BaseModel):
    provider: str
    model: str
    status: str  # healthy, degraded, unavailable, unknown
    latency_p50_ms: int
    latency_p95_ms: int
    success_rate: float
    total_calls_24h: int
    estimated_cost_24h: float
