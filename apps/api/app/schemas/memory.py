from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class MemoryProvenanceRead(BaseModel):
    source_type: str = Field(..., alias="sourceType")
    source_id: Optional[str] = Field(None, alias="sourceId")
    created_by: str = Field(..., alias="createdBy")
    confidence: float = 1.0
    timestamp: Optional[str] = None

    class Config:
        populate_by_name = True


class MemoryCreate(BaseModel):
    type: str = Field(..., pattern="^(preference|fact|decision|goal|insight|lesson|relationship|context|episodic|semantic|procedural|working|EPISODIC|SEMANTIC|PROCEDURAL|WORKING)$")
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    importance: str = Field("medium", pattern="^(low|medium|high|critical)$")
    source_type: str = Field("manual", pattern="^(manual|mission|mission_plan|mission_execution|mission_result|user_action|ai_extraction|agent_run|agent_observation|tool_execution|MISSION_RESULT|EPISODIC|SEMANTIC|PROCEDURAL|WORKING)$")
    source_id: Optional[str] = None
    expires_at: Optional[str] = None
    metadata_dict: Dict[str, Any] = {}
    confidence: Optional[float] = 1.0
    provenance: Optional[Dict[str, Any]] = None


class MemoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    type: Optional[str] = Field(None, pattern="^(preference|fact|decision|goal|insight|lesson|relationship|context|episodic|semantic|procedural|working|EPISODIC|SEMANTIC|PROCEDURAL|WORKING)$")
    importance: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    is_archived: Optional[bool] = None
    metadata_dict: Optional[Dict[str, Any]] = None


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
    confidence: Optional[float] = 1.0
    provenance: Optional[Dict[str, Any]] = None


class MemoryListResponse(BaseModel):
    memories: List[MemoryResponse]
    total: int


class MemorySearchRequest(BaseModel):
    query: str
    type_filter: Optional[str] = None
    limit: Optional[int] = 5
    min_relevance: Optional[float] = 0.0


class MemorySearchResponse(BaseModel):
    memories: List[MemoryResponse]
    count: int
    query: str


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
    provenance: Optional[Dict[str, Any]] = None


class MemoryCandidateListResponse(BaseModel):
    candidates: List[MemoryCandidateResponse]
    total: int
