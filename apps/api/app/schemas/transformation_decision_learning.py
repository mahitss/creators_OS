from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationDecisionLifecycleRead(BaseModel):
    id: str
    decisionCaseId: str
    currentStage: str
    startedAt: str
    completedAt: Optional[str] = None
    lastTransitionAt: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionStageTransitionRead(BaseModel):
    id: str
    lifecycleId: str
    fromStage: str
    toStage: str
    actor: str
    timestamp: str
    reason: str
    evidenceVersion: str
    decisionPacketVersion: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionBaselineRead(BaseModel):
    id: str
    decisionCaseId: str
    expectedBenefitsJson: Dict[str, Any]
    expectedRisksJson: Dict[str, Any]
    expectedTimingJson: Dict[str, Any]
    expectedCapacityJson: Dict[str, Any]
    expectedDependenciesJson: List[Any]
    expectedScenario: str
    expectedOutcome: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionExpectedOutcomeRead(BaseModel):
    id: str
    decisionCaseId: str
    metric: str
    target: str
    rangeStr: str
    timeHorizon: str
    confidence: float
    source: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionActualOutcomeRead(BaseModel):
    id: str
    decisionCaseId: str
    metric: str
    value: str
    timestamp: str
    source: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionVarianceRead(BaseModel):
    id: str
    decisionCaseId: str
    expected: str
    actual: str
    difference: str
    direction: str
    materiality: str
    varianceType: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionAssumptionOutcomeRead(BaseModel):
    id: str
    decisionCaseId: str
    assumption: str
    originalStatus: str
    actualState: str
    impact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecommendationOutcomeRead(BaseModel):
    id: str
    decisionCaseId: str
    recommendation: str
    decision: str
    result: str
    alignment: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionLessonRead(BaseModel):
    id: str
    lesson: str
    sourceDecision: str
    evidence: str
    confidence: str
    scope: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionPatternRead(BaseModel):
    id: str
    pattern: str
    sampleSize: int
    confidence: float
    limitations: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionLearningReviewRead(BaseModel):
    id: str
    lessonId: str
    status: str
    reviewer: str
    feedback: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionCounterfactualRead(BaseModel):
    id: str
    decisionCaseId: str
    actualPath: str
    alternativePath: str
    assumptions: str
    uncertainty: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionRegretAnalysisRead(BaseModel):
    id: str
    decisionCaseId: str
    missedBenefit: str
    avoidableRisk: str
    timingLoss: str
    optionalityLoss: str
    uncertainty: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionSuccessConditionRead(BaseModel):
    id: str
    decisionCaseId: str
    conditionText: str
    metricTarget: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionFailureAnalysisRead(BaseModel):
    id: str
    decisionCaseId: str
    decisionEffect: str
    executionEffect: str
    assumptionEffect: str
    externalEffect: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionQualityReviewRead(BaseModel):
    id: str
    decisionCaseId: str
    cadence: str
    evidenceQuality: float
    forecastAccuracy: float
    outcomeVariance: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationLearningQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
