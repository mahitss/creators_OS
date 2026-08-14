from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class KnowledgeProvenanceRead(BaseModel):
    id: str
    knowledge_object_id: str = Field(..., alias="knowledgeObjectId")
    source_type: str = Field(..., alias="sourceType")
    source_id: str = Field(..., alias="sourceId")
    external_id: Optional[str] = Field(None, alias="externalId")
    author: Optional[str] = None
    created_at: str = Field(..., alias="createdAt")
    observed_at: str = Field(..., alias="observedAt")
    ingested_at: str = Field(..., alias="ingestedAt")
    origin: str

    model_config = ConfigDict(populate_by_name=True)

class SourceAuthorityRead(BaseModel):
    id: str
    source_id: str = Field(..., alias="sourceId")
    source_type: str = Field(..., alias="sourceType")
    authority_level: str = Field(..., alias="authorityLevel")
    context_scope: str = Field(..., alias="contextScope")
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

class KnowledgeClaimRead(BaseModel):
    id: str
    subject: str
    predicate: str
    object_val: str = Field(..., alias="objectVal")
    source_references: List[Dict[str, Any]] = Field(..., alias="sourceReferences")
    status: str
    confidence: str
    observed_at: str = Field(..., alias="observedAt")

    model_config = ConfigDict(populate_by_name=True)

class KnowledgeConflictRead(BaseModel):
    id: str
    subject: str
    claim_a: Dict[str, Any] = Field(..., alias="claimA")
    claim_b: Dict[str, Any] = Field(..., alias="claimB")
    sources: List[Dict[str, Any]]
    status: str
    resolution_notes: Optional[str] = Field(None, alias="resolutionNotes")
    created_at: str = Field(..., alias="createdAt")
    resolved_at: Optional[str] = Field(None, alias="resolvedAt")

    model_config = ConfigDict(populate_by_name=True)

class TrustedContextRequest(BaseModel):
    query: str
    user_permissions: List[str] = Field(default_factory=list, alias="userPermissions")
    max_items: Optional[int] = Field(10, alias="maxItems")

class ContextItem(BaseModel):
    id: str
    content: str
    source: str
    authority: str
    freshness: str
    classification: str
    evidence_reference: Dict[str, Any] = Field(..., alias="evidenceReference")

    model_config = ConfigDict(populate_by_name=True)

class TrustedContextResponse(BaseModel):
    context_items: List[ContextItem] = Field(..., alias="contextItems")
    evidence: List[Dict[str, Any]]
    warnings: List[str]
    conflicts: List[KnowledgeConflictRead]
    freshness_summary: Dict[str, int] = Field(..., alias="freshnessSummary")

    model_config = ConfigDict(populate_by_name=True)

class CitationValidationResponse(BaseModel):
    is_valid: bool = Field(..., alias="isValid")
    cited_sources: List[Dict[str, Any]] = Field(..., alias="citedSources")
    missing_sources: List[str] = Field(..., alias="missingSources")
    status: str # grounded, partially_grounded, unsupported, citation_error

    model_config = ConfigDict(populate_by_name=True)

class AIOutputProvenanceRead(BaseModel):
    id: str
    output_id: str = Field(..., alias="outputId")
    model: str
    model_version: str = Field(..., alias="modelVersion")
    prompt_version: str = Field(..., alias="promptVersion")
    context_references: List[Dict[str, Any]] = Field(..., alias="contextReferences")
    generated_at: str = Field(..., alias="generatedAt")
    evaluation_status: str = Field(..., alias="evaluationStatus")

    model_config = ConfigDict(populate_by_name=True)

class KnowledgeFeedbackRequest(BaseModel):
    feedback_type: str = Field(..., alias="feedbackType")
    comments: Optional[str] = None

class KnowledgeVerificationRequest(BaseModel):
    decision: str # verified, rejected, deprecated
    reason: Optional[str] = None

class KnowledgeGovernanceOverview(BaseModel):
    total_objects: int = Field(..., alias="totalObjects")
    authoritative_sources_count: int = Field(..., alias="authoritativeSourcesCount")
    fresh_ratio: float = Field(..., alias="freshRatio")
    stale_count: int = Field(..., alias="staleCount")
    active_conflicts_count: int = Field(..., alias="activeConflictsCount")
    unverified_claims_count: int = Field(..., alias="unverifiedClaimsCount")
    grounding_accuracy: float = Field(..., alias="groundingAccuracy")
    last_updated: str = Field(..., alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)
