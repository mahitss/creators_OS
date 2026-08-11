from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentExecutionCreate(BaseModel):
    agent_id: str = Field(..., alias="agentId")
    mission_id: Optional[str] = Field(None, alias="missionId")
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    initial_variables: Dict[str, Any] = Field(default_factory=dict, alias="initialVariables")
    priority: str = "normal" # critical, high, normal, low

class AgentExecutionRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    agent_id: str = Field(..., alias="agentId")
    mission_id: Optional[str] = Field(None, alias="missionId")
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    status: str
    version: int
    current_step: Optional[str] = Field(None, alias="currentStep")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    class Config:
        populate_by_name = True

class AgentExecutionStateRead(BaseModel):
    id: str
    execution_id: str = Field(..., alias="executionId")
    version: int
    variables: Dict[str, Any]
    completed_steps: List[str] = Field(..., alias="completedSteps")
    pending_steps: List[str] = Field(..., alias="pendingSteps")
    active_steps: List[str] = Field(..., alias="activeSteps")
    blocked_steps: List[str] = Field(..., alias="blockedSteps")
    last_checkpoint_id: Optional[str] = Field(None, alias="lastCheckpointId")

    class Config:
        populate_by_name = True

class AgentExecutionStepRead(BaseModel):
    id: str
    execution_id: str = Field(..., alias="executionId")
    step_type: str = Field(..., alias="stepType")
    status: str
    attempt: int
    input_reference: Dict[str, Any] = Field(..., alias="inputReference")
    output_reference: Optional[Dict[str, Any]] = Field(None, alias="outputReference")
    started_at: Optional[str] = Field(None, alias="startedAt")
    completed_at: Optional[str] = Field(None, alias="completedAt")

    class Config:
        populate_by_name = True

class ExecutionCheckpointRead(BaseModel):
    id: str
    execution_id: str = Field(..., alias="executionId")
    execution_version: int = Field(..., alias="executionVersion")
    step_id: Optional[str] = Field(None, alias="stepId")
    state_reference: Dict[str, Any] = Field(..., alias="stateReference")
    reason: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class UnknownOutcomeResolveRequest(BaseModel):
    resolution: str # resolved_success, resolved_failure
    notes: str

class UnknownOutcomeRead(BaseModel):
    id: str
    execution_id: str = Field(..., alias="executionId")
    step_id: str = Field(..., alias="stepId")
    idempotency_key: str = Field(..., alias="idempotencyKey")
    action_type: str = Field(..., alias="actionType")
    status: str
    resolution_notes: Optional[str] = Field(None, alias="resolutionNotes")
    resolved_by: Optional[str] = Field(None, alias="resolvedBy")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class ExecutionTraceRead(BaseModel):
    execution: AgentExecutionRead
    state: AgentExecutionStateRead
    steps: List[AgentExecutionStepRead]
    checkpoints: List[ExecutionCheckpointRead]
    unknown_outcomes: List[UnknownOutcomeRead]

    class Config:
        populate_by_name = True

class ExecutionActionRequest(BaseModel):
    reason: Optional[str] = None
