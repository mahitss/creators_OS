from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationDecisionCaseRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    title: str
    description: str
    decisionType: str
    status: str
    priority: str
    owner: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionQuestionRead(BaseModel):
    id: str
    decisionCaseId: str
    questionText: str

    model_config = ConfigDict(from_attributes=True)

class TransformationEvidencePackRead(BaseModel):
    id: str
    decisionCaseId: str
    summaryJson: Dict[str, Any]
    qualityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationEvidenceItemRead(BaseModel):
    id: str
    evidencePackId: str
    type: str
    source: str
    valueJson: Dict[str, Any]
    timestamp: str
    freshness: str
    confidence: float
    provenance: str

    model_config = ConfigDict(from_attributes=True)

class TransformationEvidenceConflictRead(BaseModel):
    id: str
    decisionCaseId: str
    sourceA: str
    sourceB: str
    conflictingClaim: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionAssumptionRead(BaseModel):
    id: str
    decisionCaseId: str
    assumptionText: str
    source: str
    confidence: float
    status: str
    impact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionOptionRead(BaseModel):
    id: str
    decisionCaseId: str
    description: str
    expectedOutcome: str
    risksJson: List[Any]
    dependenciesJson: List[Any]
    cost: str
    capacity: str
    timing: str
    reversibility: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionTradeoffRead(BaseModel):
    id: str
    decisionCaseId: str
    optionId: str
    benefitGained: str
    costIncurred: str
    riskAccepted: str
    optionalityLost: str
    optionalityGained: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionRecommendationRead(BaseModel):
    id: str
    decisionCaseId: str
    recommendedOptionId: str
    rationaleSummary: str
    evidenceReferencesJson: List[Any]
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionPacketRead(BaseModel):
    id: str
    decisionCaseId: str
    versionTag: str
    packetJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionReadinessRead(BaseModel):
    id: str
    decisionCaseId: str
    status: str
    readinessDimensionsJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionLearningRead(BaseModel):
    id: str
    decisionCaseId: str
    predictionJson: Dict[str, Any]
    actualOutcomeJson: Dict[str, Any]
    lessonText: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionReassessmentRead(BaseModel):
    id: str
    decisionCaseId: str
    reassessmentReason: str
    changedEvidenceJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
