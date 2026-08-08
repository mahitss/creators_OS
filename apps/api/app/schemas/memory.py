from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MemoryCreate(BaseModel):
    type: str = Field(..., pattern="^(preference|fact|decision|goal|insight|lesson|relationship|context)$")
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    importance: str = Field("medium", pattern="^(low|medium|high|critical)$")
    source_type: str = Field("manual", pattern="^(manual|mission|mission_plan|mission_execution|user_action|ai_extraction)$")
    source_id: Optional[str] = None
    expires_at: Optional[str] = None
    metadata_dict: Dict[str, Any] = {}

class MemoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    type: Optional[str] = Field(None, pattern="^(preference|fact|decision|goal|insight|lesson|relationship|context)$")
    importance: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    is_archived: Optional[bool] = None

class MemoryResponse(BaseModel):
    id: str
    workspace_id: str
    type: str
    title: str
    content: str
    source_type: str
    source_id: Optional[str] = None
    importance: str
    is_archived: bool
    created_at: str
    updated_at: str
    last_accessed_at: str
    expires_at: Optional[str] = None
    metadata_dict: Dict[str, Any] = {}

class MemoryListResponse(BaseModel):
    memories: List[MemoryResponse]
    total: int

class MemoryCandidateResponse(BaseModel):
    id: str
    workspace_id: str
    source_type: str
    source_id: Optional[str] = None
    type: str
    title: str
    content: str
    confidence: float
    status: str
    created_at: str

class MemoryCandidateListResponse(BaseModel):
    candidates: List[MemoryCandidateResponse]
    total: int
