from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.schemas.workflows import WorkflowDefinitionSchema

class WorkflowAIRequestCreate(BaseModel):
    workspace_id: str = Field(..., alias="workspaceId")
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    request_type: str = Field(..., description="create, modify, explain, debug, optimize, simulate, validate, summarize")
    request_text: str
    context: Dict[str, Any] = Field(default_factory=dict)

class WorkflowAIRequestRead(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    workflow_id: Optional[str] = None
    request_type: str
    request_text: str
    context: Dict[str, Any]
    status: str
    created_at: datetime

class WorkflowProposalRead(BaseModel):
    id: str
    workflow_id: Optional[str] = None
    request_id: str
    base_version_id: Optional[str] = None
    proposed_definition: Dict[str, Any]
    change_summary: Dict[str, Any]
    risk_summary: Dict[str, Any]
    capability_summary: Dict[str, Any]
    validation_result: Dict[str, Any]
    status: str
    created_at: datetime

class WorkflowExplainRequest(BaseModel):
    selected_node_id: Optional[str] = None
    explain_access: bool = False

class WorkflowExplainResponse(BaseModel):
    workflow_id: str
    version: int
    explanation: str
    trigger_summary: str
    step_sequence: List[str]
    branches: List[str]
    agent_roles: List[str]
    approval_gates: List[str]
    access_summary: Dict[str, Any]

class WorkflowDebugRequest(BaseModel):
    run_id: str

class WorkflowDebugResponse(BaseModel):
    run_id: str
    failure_category: str  # configuration, authorization, policy, tool, integration, agent, timeout, budget, approval, worker, unknown
    evidence_summary: str
    failed_node_id: Optional[str] = None
    suggested_remediation: str
    security_warning: Optional[str] = None

class WorkflowOptimizeRequest(BaseModel):
    goal: str = "balanced"  # cheaper, faster, safer, balanced

class WorkflowOptimizationResponse(BaseModel):
    proposal_id: str
    workflow_id: str
    reason: str
    current_metrics: Dict[str, Any]
    estimated_improvement: Dict[str, Any]
    proposed_definition: Dict[str, Any]
    capability_changes: Dict[str, Any]
    risk: str

class WorkflowSimulationRequest(BaseModel):
    scenarios: List[Dict[str, Any]] = Field(default_factory=list)

class WorkflowSimulationScenarioResponse(BaseModel):
    scenario_name: str
    node_path: List[str]
    conditions_evaluated: List[Dict[str, Any]]
    approvals_triggered: List[str]
    estimated_cost: float
    simulated_outcome: str
    potential_failures: List[str]

class WorkflowSimulationResponse(BaseModel):
    workflow_id: str
    version: int
    scenarios: List[WorkflowSimulationScenarioResponse]

class WorkflowReadinessResponse(BaseModel):
    workflow_id: str
    status: str  # PASS, WARN, FAIL
    gate_results: Dict[str, Any]
    evidence: List[str]
    risk_level: str

class WorkflowTestCaseCreate(BaseModel):
    name: str
    input: Dict[str, Any]
    expected_path: List[str] = Field(default_factory=list)
    expected_outcome: Dict[str, Any] = Field(default_factory=dict)

class WorkflowTestCaseRead(BaseModel):
    id: str
    workflow_version_id: str
    name: str
    input: Dict[str, Any]
    expected_path: List[str]
    expected_outcome: Dict[str, Any]
    created_by: str
    created_at: datetime

class WorkflowTestRunRead(BaseModel):
    id: str
    workflow_version_id: str
    test_case_id: Optional[str] = None
    status: str
    duration_ms: int
    node_path: List[str]
    failure_reason: Optional[str] = None
    created_at: datetime
