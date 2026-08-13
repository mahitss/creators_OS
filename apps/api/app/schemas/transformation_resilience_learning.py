from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceLearningDomainRead(BaseModel):
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

class TransformationResilienceLearningObservationRead(BaseModel):
    id: str
    observationType: str
    source: str
    timestamp: str
    objectId: str
    valueJson: Dict[str, Any]
    confidence: float
    evidenceJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningExpectationRead(BaseModel):
    id: str
    sourceSystem: str
    predictionType: str
    expectedValueJson: Dict[str, Any]
    expectedWindow: str
    confidence: float
    modelVersion: str
    assumptionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningActualOutcomeRead(BaseModel):
    id: str
    expectationId: str
    observedValueJson: Dict[str, Any]
    observedWindow: str
    evidenceJson: Dict[str, Any]
    confidence: float
    source: str
    validationStatus: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningOutcomeComparisonRead(BaseModel):
    id: str
    expectationId: str
    actualOutcomeId: str
    varianceScore: float
    direction: str
    magnitude: float
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningPredictionErrorRead(BaseModel):
    id: str
    comparisonId: str
    errorType: str
    description: str
    severityDelta: float
    timingDeltaHours: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningWarningCalibrationRead(BaseModel):
    id: str
    warningId: str
    predictedSeverity: float
    actualSeverity: float
    predictedTimingWindow: str
    actualTimingWindow: str
    leadTimeHours: float
    isFalsePositive: bool
    isFalseNegative: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningWarningQualityRead(BaseModel):
    id: str
    precisionPct: float
    recallPct: float
    avgLeadTimeHours: float
    falsePositiveRate: float
    falseNegativeRate: float
    confidenceCalibrationScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningInterventionOutcomeRead(BaseModel):
    id: str
    interventionId: str
    expectedEffect: str
    actualEffect: str
    sideEffectsJson: List[str]
    recoveryImpactScore: float
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningInterventionEffectivenessRead(BaseModel):
    id: str
    interventionId: str
    riskReductionScore: float
    timeReductionScore: float
    coverageImprovementScore: float
    recoveryImprovementScore: float
    sideEffectSeverity: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningDecisionOutcomeProjectionRead(BaseModel):
    id: str
    decisionId: str
    decisionExpectation: str
    actualOutcome: str
    decisionAssumptionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningRecoveryOutcomeRead(BaseModel):
    id: str
    expectedRecoveryHours: float
    actualRecoveryHours: float
    recoveryCoveragePct: float
    residualExposureScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningSimulationErrorRead(BaseModel):
    id: str
    simulationId: str
    simulatedResult: str
    observedResult: str
    varianceScore: float
    modelVersion: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningTwinValidationRead(BaseModel):
    id: str
    twinPrediction: str
    realState: str
    divergenceScore: float
    source: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningOptimizationOutcomeRead(BaseModel):
    id: str
    recommendationId: str
    expectedBenefit: str
    actualBenefit: str
    expectedCostUsd: float
    actualCostUsd: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningControlOutcomeRead(BaseModel):
    id: str
    controlId: str
    expectedBehavior: str
    observedBehavior: str
    failureMode: str
    effectivenessPct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningAssumptionRead(BaseModel):
    id: str
    assumptionText: str
    source: str
    confidence: float
    validationStatus: str
    lastValidatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningAssumptionFailureRead(BaseModel):
    id: str
    assumptionId: str
    expected: str
    actual: str
    impactDescription: str
    downstreamEffectsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningLessonRead(BaseModel):
    id: str
    lessonType: str
    title: str
    summary: str
    confidence: float
    evidenceCount: int
    validationCount: int
    recurrenceCount: int
    stabilityScore: float
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningPatternRead(BaseModel):
    id: str
    patternType: str
    description: str
    status: str
    occurrences: int
    firstSeen: str
    lastSeen: str
    affectedDomainsJson: List[str]
    affectedTransformationsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningCalibrationProposalRead(BaseModel):
    id: str
    targetType: str
    title: str
    description: str
    proposedChangeJson: Dict[str, Any]
    evidenceJson: Dict[str, Any]
    expectedBenefit: str
    governanceRequirement: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningCalibrationChangeRead(BaseModel):
    id: str
    proposalId: str
    beforeStateJson: Dict[str, Any]
    afterStateJson: Dict[str, Any]
    reason: str
    evidenceSummary: str
    expectedEffect: str
    previousVersion: str
    calibrationVersion: str
    appliedBy: str
    appliedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningModelPerformanceRead(BaseModel):
    id: str
    modelName: str
    modelVersion: str
    domain: str
    sampleCount: int
    errorRate: float
    confidenceScore: float
    calibrationScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningModelRegressionRead(BaseModel):
    id: str
    modelName: str
    previousVersion: str
    currentVersion: str
    regressionType: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningModelDriftRead(BaseModel):
    id: str
    modelName: str
    driftType: str
    magnitude: float
    summary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningExperimentRead(BaseModel):
    id: str
    name: str
    baselineCalibration: str
    candidateCalibration: str
    status: str
    resultSummary: str
    variancePct: float
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLearningQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
