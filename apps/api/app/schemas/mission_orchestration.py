from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class MissionObjectiveCreate(BaseModel):
    title: str
    goal: str
    priority: str = "medium"
    constraints: Dict[str, Any] = Field(default_factory=dict)
    success_criteria: List[str] = Field(default_factory=list, alias="successCriteria")
    deadline: Optional[str] = None
    budget_usd: Optional[float] = Field(10.0, alias="budgetUsd")

class MissionObjectiveRead(BaseModel):
    id: str
    mission_id: str = Field(..., alias="missionId")
    goal: str
    clarity: str # clear, ambiguous, underspecified, conflicting
    constraints: Dict[str, Any]
    success_criteria: List[str] = Field(..., alias="successCriteria")
    priority: str
    deadline: Optional[str] = None
    budget_usd: Optional[float] = Field(None, alias="budgetUsd")
    risk_level: str = Field(..., alias="riskLevel")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class MissionStepRead(BaseModel):
    id: str
    mission_id: str = Field(..., alias="missionId")
    plan_version: int = Field(..., alias="planVersion")
    step_index: int = Field(..., alias="stepIndex")
    step_type: str = Field(..., alias="stepType")
    title: str
    assigned_executor_id: Optional[str] = Field(None, alias="assignedExecutorId")
    assigned_executor_type: str = Field(..., alias="assignedExecutorType")
    required_capability_id: Optional[str] = Field(None, alias="requiredCapabilityId")
    status: str
    input_payload: Dict[str, Any] = Field(default_factory=dict, alias="inputPayload")
    output_payload: Dict[str, Any] = Field(default_factory=dict, alias="outputPayload")

    class Config:
        populate_by_name = True

class MissionPlanRead(BaseModel):
    id: str
    mission_id: str = Field(..., alias="missionId")
    version: int
    objective_summary: str = Field(..., alias="objectiveSummary")
    status: str
    max_replans: int = Field(..., alias="maxReplans")
    replan_count: int = Field(..., alias="replanCount")
    steps: List[MissionStepRead] = Field(default_factory=list)
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class MissionReplanRequest(BaseModel):
    trigger_reason: str = Field(..., alias="triggerReason")

class MissionValidateRequest(BaseModel):
    step_id: str = Field(..., alias="stepId")
    verifier_type: str = Field("action_gateway", alias="verifierType")

class MissionSimulateRequest(BaseModel):
    golden_test_cases: List[str] = Field(default_factory=list, alias="goldenTestCases")

class MissionCostRead(BaseModel):
    mission_id: str = Field(..., alias="missionId")
    estimated_cost_usd: float = Field(..., alias="estimatedCostUsd")
    actual_cost_usd: float = Field(..., alias="actualCostUsd")
    model_cost_usd: float = Field(..., alias="modelCostUsd")
    tool_cost_usd: float = Field(..., alias="toolCostUsd")
    remaining_budget_usd: float = Field(..., alias="remainingBudgetUsd")

    class Config:
        populate_by_name = True

class MissionRiskRead(BaseModel):
    mission_id: str = Field(..., alias="missionId")
    data_risk: str = Field(..., alias="dataRisk")
    action_risk: str = Field(..., alias="actionRisk")
    financial_risk: str = Field(..., alias="financialRisk")
    security_risk: str = Field(..., alias="securityRisk")
    execution_risk: str = Field(..., alias="executionRisk")
    active_warnings: List[str] = Field(default_factory=list, alias="activeWarnings")

    class Config:
        populate_by_name = True
