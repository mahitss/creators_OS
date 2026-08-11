from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class DecisionSignalCreate(BaseModel):
    organization_id: str = Field("org_default_creator", alias="organizationId")
    workspace_id: str = Field("ws_default_creator", alias="workspaceId")
    type: str  # workflow_volume, workflow_failure_rate, agent_success_rate, agent_latency, model_latency, model_cost, provider_error_rate, queue_depth, incident_frequency, recovery_frequency, knowledge_freshness, retrieval_quality, security_findings, budget_usage, user_activity
    source: str
    value: float
    unit: Optional[str] = None
    window: str = "1h"
    quality: str = "fresh"

class DecisionSignalRead(BaseModel):
    id: str
    organization_id: str
    workspace_id: str
    type: str
    source: str
    value: float
    unit: Optional[str] = None
    timestamp: datetime
    window: str
    quality: str
    created_at: datetime

class SignalBaselineRead(BaseModel):
    id: str
    signal_type: str
    scope: str
    window: str
    baseline_value: float
    method: str
    calculated_at: datetime

class AnomalyEventRead(BaseModel):
    id: str
    signal_type: str
    baseline_value: float
    actual_value: float
    deviation: float
    severity: str
    detector: str
    detected_at: datetime

class ForecastRead(BaseModel):
    id: str
    signal_type: str
    horizon: str
    predicted_value: float
    predicted_range: Dict[str, float]
    method: str
    uncertainty: float
    generated_at: datetime
    expires_at: datetime

class ForecastEvaluationRead(BaseModel):
    id: str
    forecast_id: str
    signal_type: str
    predicted: float
    actual: float
    error: float
    mape: Optional[float] = None
    mae: float
    rmse: float
    evaluated_at: datetime

class RecommendationRead(BaseModel):
    id: str
    type: str
    reason: str
    evidence: List[Dict[str, Any]]
    expected_impact: str
    risk: str
    confidence: Optional[float] = None
    status: str
    created_at: datetime

class DecisionRecordRead(BaseModel):
    id: str
    organization_id: str
    workspace_id: str
    trigger: str
    evidence: List[Dict[str, Any]]
    recommendation_id: Optional[str] = None
    decision: str
    actor: str
    policy_version: int
    created_at: datetime

class DecisionScenarioCreate(BaseModel):
    name: str
    assumptions: Dict[str, Any] = Field(default_factory=dict)
    inputs: Dict[str, Any] = Field(default_factory=dict)

class DecisionScenarioRead(BaseModel):
    id: str
    name: str
    assumptions: Dict[str, Any]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    created_by: str
    created_at: datetime

class ScenarioResultRead(BaseModel):
    id: str
    scenario_id: str
    baseline: Dict[str, Any]
    scenario_output: Dict[str, Any]
    delta: Dict[str, Any]
    assumptions: Dict[str, Any]
    uncertainty: float
    run_at: datetime

class DecisionOutcomeRead(BaseModel):
    id: str
    decision_id: str
    expected_impact: str
    actual_impact: str
    error: float
    unintended_effects: List[Dict[str, Any]]
    recorded_at: datetime

class DecisionFeedbackCreate(BaseModel):
    recommendation_id: str = Field(..., alias="recommendationId")
    feedback: str  # useful, not_useful, incorrect, unsafe, missing_context
    actor: Optional[str] = Field("usr_executive_01", alias="actor")
