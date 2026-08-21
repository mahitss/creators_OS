from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MissionTokenUsageSchema(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

class MissionCreate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    goal: Optional[str] = Field("", max_length=5000)
    description: str = Field("", max_length=10000)
    priority: str = Field("medium", pattern="^(?i)(low|medium|high|urgent|critical)$")
    agent_id: Optional[str] = Field(None, max_length=100)
    agentId: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def get_title(self) -> str:
        return self.name or self.title or "Untitled Mission"

    def get_agent_id(self) -> Optional[str]:
        return self.agentId or self.agent_id

class MissionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    goal: Optional[str] = Field(None, max_length=5000)
    description: Optional[str] = Field(None, max_length=10000)
    priority: Optional[str] = Field(None, pattern="^(?i)(low|medium|high|urgent|critical)$")
    status: Optional[str] = Field(None, pattern="^(?i)(draft|queued|planning|running|waiting|paused|completed|failed|cancelled|active|archived)$")
    agent_id: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class MissionActivityResponse(BaseModel):
    id: str
    mission_id: str
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: str

class PlanStepSchema(BaseModel):
    order: int
    title: str
    description: str
    step_type: Optional[str] = "analysis"
    expected_output_type: Optional[str] = "json"

class MissionPlanResponse(BaseModel):
    id: str
    mission_id: str
    version: int = 1
    goal: str
    summary: str
    steps: List[PlanStepSchema] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    usage_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
    updated_at: str

class MissionStepResponse(BaseModel):
    id: str
    mission_id: str
    workspace_id: Optional[str] = None
    plan_version_id: Optional[str] = None
    step_number: int = 1
    order: int = 1
    name: str = ""
    title: str = ""
    description: str = ""
    step_type: str = "analysis"
    status: str = "PENDING"
    input: Optional[Dict[str, Any]] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    failure_reason: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0})
    cost_usd: float = 0.0
    duration_ms: int = 0
    created_at: str
    updated_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

class MissionExecutionResponse(BaseModel):
    id: str
    mission_id: str
    status: str
    completed_steps_count: int = 0
    total_steps_count: int = 0
    created_at: str
    updated_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

class MissionStepsPayload(BaseModel):
    execution: Optional[MissionExecutionResponse] = None
    steps: List[MissionStepResponse] = Field(default_factory=list)

class MissionEventResponse(BaseModel):
    id: str
    mission_id: str
    workspace_id: str
    step_id: Optional[str] = None
    event_type: str
    timestamp: str
    payload: Dict[str, Any] = Field(default_factory=dict)

class MissionResponse(BaseModel):
    id: str
    workspace_id: str
    tenantId: Optional[str] = None
    tenant_id: Optional[str] = None
    title: str
    name: str = ""
    goal: str = ""
    description: str = ""
    status: str
    priority: str
    agent_id: Optional[str] = None
    agentId: Optional[str] = None
    model: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    plan: Optional[Dict[str, Any]] = None
    current_step: int = 0
    currentStep: int = 0
    progress: float = 0.0
    created_by: str
    createdBy: Optional[str] = None
    created_at: str
    createdAt: Optional[str] = None
    updated_at: str
    updatedAt: Optional[str] = None
    started_at: Optional[str] = None
    startedAt: Optional[str] = None
    completed_at: Optional[str] = None
    completedAt: Optional[str] = None
    failed_at: Optional[str] = None
    failedAt: Optional[str] = None
    cancelled_at: Optional[str] = None
    cancelledAt: Optional[str] = None
    error: Optional[Any] = None
    result: Optional[Any] = None
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0})
    tokenUsage: Optional[Dict[str, int]] = None
    cost: float = 0.0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    activities: List[MissionActivityResponse] = Field(default_factory=list)
    latest_plan: Optional[MissionPlanResponse] = None
    execution_status: Optional[str] = "idle"

class MissionListResponse(BaseModel):
    missions: List[MissionResponse]
    total: int
