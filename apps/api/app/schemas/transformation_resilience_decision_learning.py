from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceDecisionLearningDomainRead(BaseModel):
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

class TransformationResilienceDecisionExpectedOutcomeRead(BaseModel):
    id: str
    decisionId: str
    objective: str
    metric: str
    targetValue: float
    expectedTime: str
    confidence: float
    source: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionObservedOutcomeRead(BaseModel):
    id: str
    decisionId: str
    metric: str
    observedValue: float
    timestamp: str
    source: str
    confidence: float
    freshness: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionOutcomeComparisonRead(BaseModel):
    id: str
    decisionId: str
    expectedValue: float
    observedValue: float
    variancePct: float
    varianceType: str
    confidence: float
    materiality: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionAttributionRead(BaseModel):
    id: str
    decisionId: str
    attributionLevel: str
    rationale: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionExternalFactorRead(BaseModel):
    id: str
    decisionId: str
    factorType: str
    description: str
    impactLevel: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionFailureAnalysisRead(BaseModel):
    id: str
    decisionId: str
    failureType: str
    rootCauseSummary: str
    lessonsLearnedRef: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionSuccessPatternRead(BaseModel):
    id: str
    domainId: str
    patternTitle: str
    conditionsJson: Dict[str, Any]
    supportingCasesCount: int
    confidence: float
    limitations: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionFailurePatternRead(BaseModel):
    id: str
    domainId: str
    patternTitle: str
    frequency: int
    scopeJson: List[str]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionLessonRead(BaseModel):
    id: str
    domainId: str
    lessonType: str
    lesson: str
    evidenceJson: Dict[str, Any]
    confidence: str
    scopeJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionLessonConflictRead(BaseModel):
    id: str
    lessonAId: str
    lessonBId: str
    conflictDescription: str
    contextDifferencesJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionQualityAssessmentRead(BaseModel):
    id: str
    decisionId: str
    evidenceCompleteness: float
    assumptionQuality: float
    scenarioCoverage: float
    optionDiversity: float
    tradeoffCompleteness: float
    decisionTimeliness: float
    executionQuality: float
    verificationQuality: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionCalibrationRead(BaseModel):
    id: str
    decisionId: str
    predictionValue: float
    actualValue: float
    errorPct: float
    biasDirection: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionModelPerformanceRead(BaseModel):
    id: str
    modelVersion: str
    outcomeAccuracyPct: float
    evaluatedCasesCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionDelayAnalysisRead(BaseModel):
    id: str
    decisionId: str
    deadline: str
    actualDecisionTime: str
    delayDays: float
    consequenceSummary: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionLearningQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
