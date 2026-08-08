from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentRunCreate(BaseModel):
    goal: str
    max_iterations: Optional[int] = 20

class AgentRunResponse(BaseModel):
    id: str
    workspace_id: str
    mission_id: str
    status: str
    goal: str
    iteration_count: int
    max_iterations: int
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

class AgentStepResponse(BaseModel):
    id: str
    agent_run_id: str
    sequence: int
    type: str
    status: str
    tool_name: Optional[str] = None
    input: Dict[str, Any] = {}
    result: Dict[str, Any] = {}
    error_code: Optional[str] = None
    created_at: str

class AgentApprovalResponse(BaseModel):
    id: str
    agent_run_id: str
    workspace_id: str
    action: str
    tool_name: str
    description: str
    risk_level: str
    status: str
    input_hash: Optional[str] = None
