from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceAssuranceDecisionIntelligenceDomainRead(BaseModel):
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

class TransformationResilienceAssuranceDecisionOutcomeRead(BaseModel):
    id: str
    decisionId: str
    conflictId: str
    planId: str
    recommendationId: str
    selectedOption: str
    executionStatus: str
    verificationStatus: str
    outcomeStatus: str
    observedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceExpectedActualComparisonRead(BaseModel):
    id: str
    decisionOutcomeId: str
    expectedRisk: float
    actualRisk: float
    expectedCoverage: float
    actualCoverage: float
    expectedEffort: str
    actualEffort: str
    expectedTimelineDays: int
    actualTimelineDays: int
    expectedCapacityPct: float
    actualCapacityPct: float
    expectedResidualRisk: float
    actualResidualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceOutcomeVarianceRead(BaseModel):
    id: str
    comparisonId: str
    dimension: str
    expectedVal: float
    actualVal: float
    delta: float
    confidence: float
    explanationStatus: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceOutcomeEvidenceRead(BaseModel):
    id: str
    decisionOutcomeId: str
    source: str
    evidenceType: str
    quality: float
    relationship: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceOutcomeCausalAnalysisRead(BaseModel):
    id: str
    decisionOutcomeId: str
    causalRelationship: str
    description: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRecommendationQualityRead(BaseModel):
    id: str
    recommendationId: str
    evidenceQuality: float
    scenarioQuality: float
    riskCalibration: float
    coverageAccuracy: float
    timelineAccuracy: float
    capacityAccuracy: float
    uncertaintyCalibration: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceDecisionQualityRead(BaseModel):
    id: str
    decisionId: str
    informationSufficiency: float
    optionCompleteness: float
    tradeoffVisibility: float
    uncertaintyVisibility: float
    governanceAlignment: float
    outcomeAlignment: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceDecisionQualityTrendRead(BaseModel):
    id: str
    domainId: str
    averageQuality: float
    trendDirection: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceResolutionPatternPerformanceRead(BaseModel):
    id: str
    patternId: str
    usageCount: int
    successCount: int
    failureCount: int
    riskReductionAvg: float
    coveragePreservationAvg: float
    deadlineRecoveryAvg: float
    capacityReliefAvg: float
    uncertaintyReductionAvg: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceContextSimilarityRead(BaseModel):
    id: str
    caseAId: str
    caseBId: str
    similarityScore: float
    matchingDimensionsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceHistoricalAnalogueRead(BaseModel):
    id: str
    currentCaseId: str
    historicalCaseId: str
    similaritiesDescription: str
    differencesDescription: str
    historicalOutcome: str
    relevanceScore: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRecommendationCalibrationRead(BaseModel):
    id: str
    domainId: str
    predictedConfidenceAvg: float
    observedAccuracyAvg: float
    calibrationError: float
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLearningSignalRead(BaseModel):
    id: str
    signalType: str
    source: str
    description: str
    priority: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLearningPriorityRead(BaseModel):
    id: str
    learningSignalId: str
    priorityScore: float
    decisionImpact: str
    recurrenceFrequency: int
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceKnowledgeUpdateProposalRead(BaseModel):
    id: str
    learningSignalId: str
    proposalType: str
    description: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRecommendationUpdateProposalRead(BaseModel):
    id: str
    learningSignalId: str
    currentBehavior: str
    observedWeakness: str
    proposedImprovement: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLearningVersionRead(BaseModel):
    id: str
    versionNumber: str
    parentVersion: str
    changesSummary: str
    reason: str
    approvalState: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRecommendationRegressionRead(BaseModel):
    id: str
    previousVersion: str
    newVersion: str
    affectedDimension: str
    severity: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRecommendationDriftRead(BaseModel):
    id: str
    driftType: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLessonRead(BaseModel):
    id: str
    lessonType: str
    title: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLessonQualityRead(BaseModel):
    id: str
    lessonId: str
    evidenceQuality: float
    recurrenceCount: int
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
