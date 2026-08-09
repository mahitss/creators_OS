from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentControlOverviewResponse(BaseModel):
    active_agents: int
    waiting_approvals: int
    paused_agents: int
    failed_agents: int
    recovering_agents: int
    stuck_agents: int
    completed_today: int
    total_tokens: int
    total_estimated_cost: float
    eval_suite_status: str
    updated_at: str

class AgentRunSummaryResponse(BaseModel):
    id: str
    workspace_id: str
    mission_id: str
    status: str
    goal: str
    current_node: str
    current_tool: Optional[str] = None
    iteration_count: int
    max_iterations: int
    lease_worker_id: Optional[str] = None
    total_tokens: int
    estimated_cost: float
    created_at: str
    updated_at: str

class AgentDetailResponse(BaseModel):
    run: Dict[str, Any]
    steps: List[Dict[str, Any]]
    checkpoints: List[Dict[str, Any]]
    tool_executions: List[Dict[str, Any]]
    approvals: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    stuck_signals: List[Dict[str, Any]]

class OperatorActionPayload(BaseModel):
    action: str = Field(..., description="Action to perform: pause, resume, cancel, retry_safe_step")
    reason: Optional[str] = Field("", description="Operator audit reason for taking action")

class OperatorActionResponse(BaseModel):
    success: bool
    action: str
    agent_run_id: str
    new_status: str
    audit_log: Dict[str, Any]

class ToolOperationMetricResponse(BaseModel):
    tool_name: str
    calls: int
    success_rate: float
    avg_latency_ms: int
    failures: int

class ProviderHealthResponse(BaseModel):
    ai_providers: Dict[str, Any]
    google_calendar_api: Dict[str, Any]
    google_drive_api: Dict[str, Any]
    google_gmail_api: Dict[str, Any]
    database: Dict[str, Any]
    worker_queue: Dict[str, Any]
