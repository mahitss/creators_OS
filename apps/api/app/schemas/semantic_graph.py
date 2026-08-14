from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class SemanticEntityRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    entity_type: str = Field(..., alias="entityType")
    entity_id: str = Field(..., alias="entityId")
    display_name: str = Field(..., alias="displayName")
    status: str
    source: str
    provider: Optional[str] = None
    external_id: Optional[str] = Field(None, alias="externalId")
    resource_type: Optional[str] = Field(None, alias="resourceType")
    metadata_info: Dict[str, Any] = Field(..., alias="metadataInfo")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class SemanticRelationshipCreate(BaseModel):
    from_entity_id: str = Field(..., alias="fromEntityId")
    relationship_type: str = Field(..., alias="relationshipType")
    to_entity_id: str = Field(..., alias="toEntityId")
    source: Optional[str] = "native" # native, integration, derived, ai_suggested
    confidence: Optional[str] = "high" # high, medium, low
    evidence_references: List[Dict[str, Any]] = Field(default_factory=list, alias="evidenceReferences")

    model_config = ConfigDict(populate_by_name=True)

class SemanticRelationshipRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: Optional[str] = Field(None, alias="workspaceId")
    from_entity_id: str = Field(..., alias="fromEntityId")
    relationship_type: str = Field(..., alias="relationshipType")
    to_entity_id: str = Field(..., alias="toEntityId")
    source: str
    status: str
    confidence: str
    evidence_references: List[Dict[str, Any]] = Field(..., alias="evidenceReferences")
    valid_from: str = Field(..., alias="validFrom")
    valid_until: Optional[str] = Field(None, alias="validUntil")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class RelationshipConflictRead(BaseModel):
    id: str
    relationship_id: str = Field(..., alias="relationshipId")
    evidence_a: Dict[str, Any] = Field(..., alias="evidenceA")
    evidence_b: Dict[str, Any] = Field(..., alias="evidenceB")
    status: str
    resolution_notes: Optional[str] = Field(None, alias="resolutionNotes")
    created_at: str = Field(..., alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

class ContextPackCreate(BaseModel):
    scope: str
    root_entity_id: str = Field(..., alias="rootEntityId")
    max_depth: Optional[int] = Field(2, alias="maxDepth")
    max_nodes: Optional[int] = Field(50, alias="maxNodes")

    model_config = ConfigDict(populate_by_name=True)

class ContextPackRead(BaseModel):
    id: str
    organization_id: str = Field(..., alias="organizationId")
    workspace_id: str = Field(..., alias="workspaceId")
    entities: List[SemanticEntityRead]
    relationships: List[SemanticRelationshipRead]
    evidence: List[Dict[str, Any]]
    scope: str
    generated_at: str = Field(..., alias="generatedAt")
    expires_at: str = Field(..., alias="expiresAt")

    model_config = ConfigDict(populate_by_name=True)

class GraphImpactResponse(BaseModel):
    root_entity_id: str = Field(..., alias="rootEntityId")
    direct_dependencies: List[SemanticEntityRead] = Field(..., alias="directDependencies")
    indirect_dependencies: List[SemanticEntityRead] = Field(..., alias="indirectDependencies")
    affected_workflows: List[Dict[str, Any]] = Field(..., alias="affectedWorkflows")
    affected_agents: List[Dict[str, Any]] = Field(..., alias="affectedAgents")
    affected_integrations: List[Dict[str, Any]] = Field(..., alias="affectedIntegrations")
    total_impacted_count: int = Field(..., alias="totalImpactedCount")

    model_config = ConfigDict(populate_by_name=True)

class GraphHealthRead(BaseModel):
    entity_count: int = Field(..., alias="entityCount")
    relationship_count: int = Field(..., alias="relationshipCount")
    orphan_rate: float = Field(..., alias="orphanRate")
    invalid_relationship_rate: float = Field(..., alias="invalidRelationshipRate")
    sync_lag_seconds: float = Field(..., alias="syncLagSeconds")
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)
