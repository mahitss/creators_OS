from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class KnowledgeSourceCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    type: str  # drive, gmail, calendar, document, memory, workflow, agent, mission, manual
    name: str
    configuration: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeSourceRead(BaseModel):
    id: str
    organization_id: str
    workspace_id: str
    type: str
    name: str
    status: str  # connected, syncing, healthy, degraded, paused, error, disconnected
    configuration: Dict[str, Any]
    created_by: str
    created_at: datetime
    updated_at: datetime

class KnowledgeCollectionCreate(BaseModel):
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    name: str
    description: Optional[str] = ""
    classification: str = "internal"

class KnowledgeCollectionRead(BaseModel):
    id: str
    organization_id: str
    workspace_id: str
    name: str
    description: str
    owner_id: str
    classification: str
    status: str
    created_at: datetime
    updated_at: datetime

class KnowledgeDocumentRead(BaseModel):
    id: str
    source_id: str
    external_id: str
    workspace_id: str
    organization_id: str
    title: str
    mime_type: str
    source_url: Optional[str] = None
    classification: str
    owner_id: Optional[str] = None
    version: int
    content_hash: str
    source_updated_at: datetime
    indexed_at: datetime
    status: str
    created_at: datetime
    updated_at: datetime

class KnowledgeQueryRequest(BaseModel):
    query: str
    organization_id: str = Field("org_default_creator", alias="organizationId")
    workspace_id: str = Field("ws_default_creator", alias="workspaceId")
    classification_ceiling: str = Field("restricted", alias="classificationCeiling")
    source_filters: List[str] = Field(default_factory=list, alias="sourceFilters")
    collection_ids: List[str] = Field(default_factory=list, alias="collectionIds")
    limit: int = 10

class KnowledgeCitation(BaseModel):
    document_id: str
    source_name: str
    title: str
    section: Optional[str] = None
    source_url: Optional[str] = None
    classification: str
    snippet: str

class KnowledgeAskResponse(BaseModel):
    query: str
    answer: str
    evidence_status: str  # strong_evidence, partial_evidence, insufficient_evidence
    citations: List[KnowledgeCitation]
    sources_consulted_count: int
    authorized_chunks_count: int
    policy_decisions: Dict[str, Any]
    created_at: datetime

class KnowledgeEntityRead(BaseModel):
    id: str
    type: str
    name: str
    canonical_key: str
    workspace_id: str
    organization_id: str
    created_at: datetime

class KnowledgeRelationshipRead(BaseModel):
    id: str
    source_entity_id: str
    relationship: str
    target_entity_id: str
    source_reference: str
    confidence: float
    created_at: datetime
