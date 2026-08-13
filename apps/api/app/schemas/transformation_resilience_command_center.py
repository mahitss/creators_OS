from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceCommandCenterRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    scope: str
    owner: str
    status: str
    lastEvaluatedAt: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceExecutiveStateRead(BaseModel):
    id: str
    commandCenterId: str
    dimension: str
    state: str
    trend: str
    confidence: float
    freshness: float
    evidenceCount: int

    model_config = ConfigDict(from_attributes=True)

class TransformationResiliencePriorityItemRead(BaseModel):
    id: str
    commandCenterId: str
    itemType: str
    priority: str
    title: str
    impactScore: float
    urgencyScore: float
    confidence: float
    scope: str
    reversibility: str
    decisionDeadline: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSituationRead(BaseModel):
    id: str
    commandCenterId: str
    summary: str
    changesJson: List[str]
    affectedScopeJson: List[str]
    evidenceJson: Dict[str, Any]
    uncertaintyJson: Dict[str, Any]
    recommendedReview: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSituationSnapshotRead(BaseModel):
    id: str
    commandCenterId: str
    timestamp: str
    stateJson: Dict[str, Any]
    sourceVersionsJson: Dict[str, Any]
    freshness: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceExposureMapRead(BaseModel):
    id: str
    commandCenterId: str
    transformationId: str
    dimension: str
    severity: str
    confidence: float
    freshness: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceEvidenceSummaryRead(BaseModel):
    id: str
    commandCenterId: str
    sourceDiversityScore: float
    freshnessScore: float
    qualityScore: float
    hasConflicts: bool
    conflictsJson: List[Dict[str, Any]]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceUnappliedLessonRead(BaseModel):
    id: str
    commandCenterId: str
    lessonTitle: str
    affectedScopeJson: List[str]
    reasonNotApplied: str
    recommendedReview: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionPacketRead(BaseModel):
    id: str
    commandCenterId: str
    title: str
    evidenceJson: Dict[str, Any]
    scenarioResultsJson: Dict[str, Any]
    tradeoffsJson: Dict[str, Any]
    uncertaintyJson: Dict[str, Any]
    recommendation: str
    alternativesJson: List[str]
    requiredApproval: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCommandCenterQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
