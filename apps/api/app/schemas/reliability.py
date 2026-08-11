from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class HealthSignalCreate(BaseModel):
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    service: str
    resource_type: str = Field(..., alias="resourceType")
    resource_id: str = Field(..., alias="resourceId")
    severity: str = "warning"  # info, warning, high, critical
    signal_type: str = Field(..., alias="signalType")  # latency_degradation, error_rate_increase, queue_backlog, worker_failure, provider_failure, workflow_failure, agent_failure, integration_failure, budget_exhaustion
    observed_value: float = Field(..., alias="observedValue")
    baseline_value: Optional[float] = Field(None, alias="baselineValue")
    source: str = "telemetry"

class HealthSignalRead(BaseModel):
    id: str
    workspace_id: Optional[str] = None
    service: str
    resource_type: str
    resource_id: str
    severity: str
    signal_type: str
    observed_value: float
    baseline_value: Optional[float] = None
    source: str
    timestamp: datetime
    created_at: datetime

class IncidentDiagnosisRead(BaseModel):
    id: str
    incident_id: str
    summary: str
    observed: List[Dict[str, Any]]
    correlated: List[Dict[str, Any]]
    suspected: List[Dict[str, Any]]
    confidence: float
    created_at: datetime

class RecoveryStep(BaseModel):
    type: str  # retry_transient_job, restart_worker, pause_workflow, resume_workflow, requeue_dead_letter, switch_configured_fallback_model, clear_stale_lease
    target: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk: str = "low"
    reversible: bool = True
    timeout_sec: int = 30
    max_retries: int = 3
    verification: Dict[str, Any] = Field(default_factory=dict)

class RecoveryPlanCreate(BaseModel):
    incident_id: str = Field(..., alias="incidentId")
    steps: List[RecoveryStep]
    risk: str = "low"
    estimated_impact: Dict[str, Any] = Field(default_factory=dict, alias="estimatedImpact")

class RecoveryPlanRead(BaseModel):
    id: str
    incident_id: str
    steps: List[Dict[str, Any]]
    risk: str
    estimated_impact: Dict[str, Any]
    policy_requirements: List[str]
    status: str
    created_at: datetime

class RecoveryExecutionRead(BaseModel):
    id: str
    recovery_plan_id: str
    incident_id: str
    recovery_key: str
    step_index: int
    action_type: str
    target: str
    status: str
    verification_result: Dict[str, Any]
    duration_ms: int
    error_code: Optional[str] = None
    created_at: datetime

class CircuitBreakerRead(BaseModel):
    id: str
    service: str
    status: str  # closed, open, half_open
    failure_count: int
    last_failure_at: Optional[datetime] = None
    cooldown_seconds: int
    opened_at: Optional[datetime] = None
    half_opened_at: Optional[datetime] = None

class RunbookRead(BaseModel):
    id: str
    service: str
    name: str
    trigger_condition: Dict[str, Any]
    steps: List[Dict[str, Any]]
    verification: Dict[str, Any]
    rollback: Dict[str, Any]
    owner: str
    version: int
    status: str
    created_at: datetime

class ProblemRead(BaseModel):
    id: str
    workspace_id: Optional[str] = None
    service: str
    signature: str
    frequency: int
    incidents: List[str]
    status: str
    created_at: datetime
