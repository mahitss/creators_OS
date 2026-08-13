from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceOptimizationDomainRead(BaseModel):
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

class TransformationResilienceOptimizationObjectiveRead(BaseModel):
    id: str
    objectiveType: str
    description: str
    targetValue: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationObjectiveWeightRead(BaseModel):
    id: str
    objectiveId: str
    weight: float
    source: str
    effectiveFrom: str
    effectiveTo: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationConstraintRead(BaseModel):
    id: str
    constraintType: str
    limitValue: float
    currentValue: float
    remainingCapacity: float
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationProblemRead(BaseModel):
    id: str
    name: str
    objectivesJson: List[str]
    constraintsJson: List[str]
    candidateActionsJson: List[str]
    baselineStrategy: str
    horizonDays: int
    assumptionsJson: List[str]
    sourceSnapshotId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationCandidateRead(BaseModel):
    id: str
    candidateType: str
    title: str
    description: str
    reversibility: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationCandidateImpactRead(BaseModel):
    id: str
    candidateId: str
    riskReductionScore: float
    coverageScore: float
    recoveryScore: float
    capacityScore: float
    deadlineScore: float
    dependencyScore: float
    evidenceScore: float
    effortDays: int
    costUsd: float
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationScenarioRead(BaseModel):
    id: str
    scenarioType: str
    name: str
    snapshotId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRunRead(BaseModel):
    id: str
    problemId: str
    scenarioId: str
    algorithm: str
    version: str
    startTime: str
    endTime: Optional[str]
    status: str
    seed: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationParetoPointRead(BaseModel):
    id: str
    runId: str
    candidateSetJson: List[str]
    riskScore: float
    costUsd: float
    effortDays: int
    coverageScore: float
    recoveryScore: float
    capacityScore: float
    isNonDominated: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationParetoSetRead(BaseModel):
    id: str
    problemId: str
    nonDominatedPointsCount: int
    dominatedPointsCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationTradeoffRead(BaseModel):
    id: str
    optionA: str
    optionB: str
    tradeoffSummary: str
    costDifferenceUsd: float
    riskReductionDifference: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationResourceScenarioRead(BaseModel):
    id: str
    name: str
    resourceCategory: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationResourceRequirementRead(BaseModel):
    id: str
    candidateId: str
    resourceType: str
    required: float
    available: float
    shortfall: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationCapacityBufferRead(BaseModel):
    id: str
    baselineCapacity: float
    requiredCapacity: float
    buffer: float
    targetBuffer: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationInvestmentCaseRead(BaseModel):
    id: str
    candidateId: str
    expectedBenefit: str
    costUsd: float
    effortDays: int
    riskLevel: str
    timeHorizonMonths: int
    uncertaintyLevel: str
    label: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationInvestmentComparisonRead(BaseModel):
    id: str
    investmentAId: str
    investmentBId: str
    comparisonSummary: str
    residualRiskDifference: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationControlCandidateRead(BaseModel):
    id: str
    controlType: str
    target: str
    proposedEnhancement: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationControlImpactRead(BaseModel):
    id: str
    controlCandidateId: str
    failureReductionPct: float
    detectionImprovementPct: float
    responseImprovementPct: float
    recoveryImprovementPct: float
    effortDays: int

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRedundancyCandidateRead(BaseModel):
    id: str
    redundancyType: str
    targetComponent: str
    singlePointExposureReductionPct: float
    recoveryImprovementPct: float
    costUsd: float
    complexity: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationGapPriorityRead(BaseModel):
    id: str
    gapId: str
    impactScore: float
    urgencyScore: float
    uncertaintyScore: float
    dependencyConcentrationScore: float
    historicalFailureScore: float
    controlWeaknessScore: float
    rank: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRecommendationRead(BaseModel):
    id: str
    problemId: str
    baselineSummary: str
    candidateSummary: str
    scenarioProfile: str
    expectedImpactSummary: str
    tradeoffsSummary: str
    constraintsSummary: str
    uncertainty: float
    confidence: float
    assumptionsJson: List[str]
    label: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRecommendationSetRead(BaseModel):
    id: str
    problemId: str
    conservativeRecommendationId: str
    balancedRecommendationId: str
    aggressiveRecommendationId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationSensitivityRead(BaseModel):
    id: str
    problemId: str
    variedParameter: str
    variancePct: float
    recommendationChanged: bool
    sensitivitySummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRobustnessRead(BaseModel):
    id: str
    recommendationId: str
    stabilityScore: float
    uncertaintyRange: str
    failureConditionsSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationRegressionRead(BaseModel):
    id: str
    recommendationId: str
    previousRank: int
    currentRank: int
    status: str
    causeSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationDriftRead(BaseModel):
    id: str
    driftType: str
    magnitude: float
    summary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationOutcomeRead(BaseModel):
    id: str
    recommendationId: str
    expectedResilienceBenefit: str
    actualObservedBenefit: str
    expectedCostUsd: float
    actualCostUsd: float
    varianceSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationLessonRead(BaseModel):
    id: str
    lessonType: str
    summary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptimizationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
