from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceDecisionKnowledgeDomainRead(BaseModel):
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

class TransformationResilienceDecisionKnowledgeObjectRead(BaseModel):
    id: str
    domainId: str
    type: str
    statement: str
    contextJson: Dict[str, Any]
    evidenceJson: Dict[str, Any]
    confidence: float
    applicabilityLevel: str
    limitations: str
    status: str
    version: int
    sourceDecisionId: Optional[str] = None
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeValidationRead(BaseModel):
    id: str
    knowledgeObjectId: str
    supportingCasesCount: int
    contradictingCasesCount: int
    evidenceQuality: float
    reproducibility: float
    contextConsistency: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeContextRead(BaseModel):
    id: str
    knowledgeObjectId: str
    transformationType: str
    dependencyProfile: str
    capacityProfile: str
    riskProfile: str
    recoveryProfile: str
    governanceContext: str
    timeHorizon: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeApplicabilityRead(BaseModel):
    id: str
    knowledgeObjectId: str
    targetDecisionContextId: str
    level: str
    applicabilityScore: float
    explanation: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeConflictRead(BaseModel):
    id: str
    knowledgeObjectAId: str
    knowledgeObjectBId: str
    conflictingClaims: str
    evidenceJson: Dict[str, Any]
    contextDifferences: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeInvalidationRead(BaseModel):
    id: str
    knowledgeObjectId: str
    trigger: str
    rationale: str
    contradictoryEvidenceJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeReviewRead(BaseModel):
    id: str
    knowledgeObjectId: str
    triggerReason: str
    status: str
    validFrom: str
    reviewAfter: str
    expiresAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeReuseRead(BaseModel):
    id: str
    knowledgeObjectId: str
    decisionId: str
    contextDescription: str
    recommendationInfluence: str
    result: str
    outcomeSummary: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgePackRead(BaseModel):
    id: str
    decisionId: str
    packVersion: str
    lessonsJson: List[Dict[str, Any]]
    precedentsJson: List[Dict[str, Any]]
    patternsJson: List[Dict[str, Any]]
    assumptionsJson: List[Dict[str, Any]]
    conflictsJson: List[Dict[str, Any]]
    limitationsJson: List[Dict[str, Any]]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeQualityRead(BaseModel):
    id: str
    knowledgeObjectId: str
    completeness: float
    provenance: float
    freshness: float
    consistency: float
    validationLevel: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeGapRead(BaseModel):
    id: str
    domainId: str
    gapTitle: str
    gapType: str
    priority: str
    recommendedActivity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionKnowledgeQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
