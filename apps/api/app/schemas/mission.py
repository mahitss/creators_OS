from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MissionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field("", max_length=5000)
    priority: str = Field("medium", pattern="^(low|medium|high|urgent)$")

class MissionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    status: Optional[str] = Field(None, pattern="^(draft|active|completed|archived)$")

class MissionActivityResponse(BaseModel):
    id: str
    mission_id: str
    action: str
    details: Dict[str, Any] = {}
    created_at: str

class PlanStepSchema(BaseModel):
    order: int
    title: str
    description: str

class MissionPlanResponse(BaseModel):
    id: str
    mission_id: str
    version: int
    goal: str
    summary: str
    steps: List[PlanStepSchema] = []
    deliverables: List[str] = []
    open_questions: List[str] = []
    recommendations: List[str] = []
    usage_metadata: Dict[str, Any] = {}
    created_at: str
    updated_at: str

class MissionResponse(BaseModel):
    id: str
    workspace_id: str
    title: str
    description: str
    status: str
    priority: str
    created_by: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
    activities: List[MissionActivityResponse] = []
    latest_plan: Optional[MissionPlanResponse] = None

class MissionListResponse(BaseModel):
    missions: List[MissionResponse]
    total: int
