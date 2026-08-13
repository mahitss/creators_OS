from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceKnowledgeAssuranceDomainRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    scope: str
    owner: str
    status: str
    version: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeHealthRead(BaseModel):
    id: str
    knowledgeObjectId: str
    freshnessScore: float
    provenanceScore: float
    validationStrength: float
    applicabilityScore: float
    reuseScore: float
    consistencyScore: float
    contextStability: float
    evidenceCoverage: float
    overallStatus: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeEvidenceAssuranceRead(BaseModel):
    id: str
    knowledgeObjectId: str
    source: str
    freshness: float
    quality: float
    reliability: float
    independenceType: str
    coverage: float
    conflictsCount: int

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeClaimRead(BaseModel):
    id: str
    knowledgeObjectId: str
    statement: str
    claimType: str
    confidence: float
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeClaimSupportRead(BaseModel):
    id: str
    claimId: str
    evidenceId: str
    supportStrength: float
    sourceIndependence: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeClaimConflictRead(BaseModel):
    id: str
    claimAId: str
    claimBId: str
    evidenceJson: Dict[str, Any]
    contextDescription: str
    severity: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeContextDriftRead(BaseModel):
    id: str
    knowledgeObjectId: str
    dimension: str
    driftDescription: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeReuseAssuranceRead(BaseModel):
    id: str
    knowledgeObjectId: str
    reuseCount: int
    successfulReuseCount: int
    failedReuseCount: int
    inconclusiveReuseCount: int
    contextSimilarityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeInfluenceRead(BaseModel):
    id: str
    knowledgeObjectId: str
    targetType: str
    targetId: str
    influenceLevel: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRiskRead(BaseModel):
    id: str
    knowledgeObjectId: str
    riskType: str
    severity: str
    affectedDecisionsJson: List[str]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReviewRead(BaseModel):
    id: str
    knowledgeObjectId: str
    trigger: str
    priority: str
    recommendedAction: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReviewPacketRead(BaseModel):
    id: str
    reviewId: str
    knowledgeObjectId: str
    claimsJson: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    conflictsJson: List[Dict[str, Any]]
    contextDriftJson: Dict[str, Any]
    reuseHistoryJson: List[Dict[str, Any]]
    influenceJson: Dict[str, Any]
    riskJson: Dict[str, Any]
    recommendedAction: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRevalidationRead(BaseModel):
    id: str
    knowledgeObjectId: str
    reviewQuestion: str
    newEvidenceJson: Dict[str, Any]
    newContext: str
    result: str
    reviewer: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeLineageRead(BaseModel):
    id: str
    knowledgeObjectId: str
    sourceDecisionId: str
    outcomeId: str
    lessonId: str
    patternId: str
    claimIdsJson: List[str]
    evidenceIdsJson: List[str]
    reuseIdsJson: List[str]
    reviewIdsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeEvidenceGapRead(BaseModel):
    id: str
    domainId: str
    gapTitle: str
    gapType: str
    priority: str
    recommendedActivity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeGovernanceStateRead(BaseModel):
    id: str
    knowledgeObjectId: str
    state: str
    authorizedBy: str
    rationale: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeGovernanceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
