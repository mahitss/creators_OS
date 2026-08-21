"""Pydantic Schemas for Kinetiq Agent Runtime V1."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field("", max_length=2000)
    system_instructions: str = Field(..., min_length=1)
    capabilities: List[str] = Field(default_factory=list)
    allowed_tools: List[str] = Field(default_factory=list)
    allowed_models: List[str] = Field(default_factory=lambda: ["openrouter/free"])
    max_steps: Optional[int] = Field(20, ge=1, le=50)
    max_runtime_seconds: Optional[int] = Field(300, ge=10, le=3600)
    max_token_budget: Optional[int] = Field(100000, ge=1000, le=1000000)


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = None
    system_instructions: Optional[str] = None
    capabilities: Optional[List[str]] = None
    allowed_tools: Optional[List[str]] = None
    allowed_models: Optional[List[str]] = None
    max_steps: Optional[int] = Field(None, ge=1, le=50)
    max_runtime_seconds: Optional[int] = Field(None, ge=10, le=3600)
    max_token_budget: Optional[int] = Field(None, ge=1000, le=1000000)


class AgentVersionCreate(BaseModel):
    instructions: str = Field(..., min_length=1)
    capabilities: List[str] = Field(default_factory=list)
    tool_policy: Dict[str, Any] = Field(default_factory=dict)
    model_policy: Dict[str, Any] = Field(default_factory=dict)
    limits: Dict[str, Any] = Field(default_factory=dict)


class AgentVersionResponse(BaseModel):
    id: str
    agent_id: str
    workspace_id: str
    version: int
    instructions: str
    capabilities: List[str] = []
    tool_policy: Dict[str, Any] = {}
    model_policy: Dict[str, Any] = {}
    limits: Dict[str, Any] = {}
    created_at: str
    created_by: str


class AgentResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: str
    status: str
    system_instructions: str
    capabilities: List[str] = []
    allowed_tools: List[str] = []
    allowed_models: List[str] = []
    max_steps: int
    max_runtime_seconds: int
    max_token_budget: int
    created_by: str
    created_at: str
    updated_at: str
    current_version: int = 1
    latest_version_id: Optional[str] = None
    total_runs: int = 0


class AgentRunCreateRequest(BaseModel):
    agent_id: str
    agent_version_id: Optional[str] = None
    mission_id: Optional[str] = None
    goal: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AgentObservationResponse(BaseModel):
    id: str
    agent_run_id: str
    workspace_id: str
    step_number: int
    observation_type: str
    tool_name: Optional[str] = None
    status: str
    summary: str
    raw_data: Dict[str, Any] = {}
    timestamp: str


class AgentEventResponse(BaseModel):
    id: str
    agent_run_id: str
    workspace_id: str
    mission_id: Optional[str] = None
    event_type: str
    correlation_id: str
    timestamp: str
    payload: Dict[str, Any] = {}


class AgentRunDetailResponse(BaseModel):
    id: str
    agent_id: str
    agent_version_id: str
    mission_id: Optional[str] = None
    workspace_id: str
    status: str
    current_step: int
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    error_info: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None
    created_at: str
    observations: List[AgentObservationResponse] = []
    events: List[AgentEventResponse] = []
