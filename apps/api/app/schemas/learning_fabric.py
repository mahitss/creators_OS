from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentMemoryCreate(BaseModel):
    owner_type: str = Field("agent", alias="ownerType")
    owner_id: str = Field(..., alias="ownerId")
    memory_type: str = Field("semantic", alias="memoryType") # episodic, semantic, procedural, working, preference, execution
    scope: str = Field("workspace", alias="scope") # private, shared, workspace, organization
    title: str
    content: str
    importance: str = "medium"
    confidence: float = 0.85
    source_type: str = Field("user_input", alias="sourceType")
    source_id: str = Field("src_direct", alias="sourceId")

class AgentMemoryRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    owner_type: str = Field(..., alias="ownerType")
    owner_id: str = Field(..., alias="ownerId")
    memory_type: str = Field(..., alias="memoryType")
    scope: str
    title: str
    content: str
    status: str
    importance: str
    confidence: float
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    expires_at: Optional[str] = Field(None, alias="expiresAt")

    class Config:
        populate_by_name = True

class MemoryVersionRead(BaseModel):
    id: str
    memory_id: str = Field(..., alias="memoryId")
    version: int
    content_reference: Dict[str, Any] = Field(..., alias="contentReference")
    source: str
    status: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class MemoryProvenanceRead(BaseModel):
    id: str
    memory_id: str = Field(..., alias="memoryId")
    source_type: str = Field(..., alias="sourceType")
    source_id: str = Field(..., alias="sourceId")
    observed_at: str = Field(..., alias="observedAt")
    author: Optional[str] = None
    origin: Optional[str] = None

    class Config:
        populate_by_name = True

class MemoryCandidateRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    proposed_by_agent_id: str = Field(..., alias="proposedByAgentId")
    memory_type: str = Field(..., alias="memoryType")
    suggested_content: Dict[str, Any] = Field(..., alias="suggestedContent")
    evidence_reference: Dict[str, Any] = Field(..., alias="evidenceReference")
    status: str
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class MemoryConflictRead(BaseModel):
    id: str
    workspace_id: str = Field(..., alias="workspaceId")
    memory_id_a: str = Field(..., alias="memoryIdA")
    memory_id_b: str = Field(..., alias="memoryIdB")
    conflict_reason: str = Field(..., alias="conflictReason")
    status: str
    resolution_notes: Optional[str] = Field(None, alias="resolutionNotes")
    resolved_by: Optional[str] = Field(None, alias="resolvedBy")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True

class MemoryCorrectRequest(BaseModel):
    corrected_title: Optional[str] = Field(None, alias="correctedTitle")
    corrected_content: str = Field(..., alias="correctedContent")
    reason: str

class MemoryConflictResolveRequest(BaseModel):
    resolution: str # resolved_a, resolved_b, resolved_both
    notes: str
