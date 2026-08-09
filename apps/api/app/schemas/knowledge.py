from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MemoryCandidateCreate(BaseModel):
    statement: str = Field(..., description="Statement to be stored as memory")
    type_name: str = Field("fact", description="Memory type: fact, preference, decision, requirement, project_context")
    scope: str = Field("workspace", description="Memory scope: personal, workspace, mission, agent")
    source_references: List[Dict[str, Any]] = Field(default_factory=list, description="Source references")
    confidence: float = Field(1.0, description="Confidence score 0.0 - 1.0")
    reason: str = Field("", description="User-safe reason for proposing memory candidate")
    mission_id: Optional[str] = Field(None, description="Optional Mission ID")

class MemoryCandidateResponse(BaseModel):
    id: str
    workspace_id: str
    scope: str
    owner_id: str
    mission_id: Optional[str] = None
    type: str
    statement: str
    source_references: List[Dict[str, Any]]
    confidence: float
    reason: Optional[str] = ""
    status: str
    created_at: str
    updated_at: str

class MemoryConflictResponse(BaseModel):
    id: str
    workspace_id: str
    memory_a_id: str
    memory_b_id: str
    reason: str
    status: str
    created_at: str
    resolved_at: Optional[str] = None

class ConflictResolutionPayload(BaseModel):
    choice: str = Field(..., description="Resolution choice: keep_a, keep_b, supersede")

class ProvenanceTraceResponse(BaseModel):
    memory_id: str
    statement: str
    scope: str
    owner_id: str
    confidence: float
    status: str
    source_references: List[Dict[str, Any]]
    created_at: str
    approved_by: Optional[str] = None
