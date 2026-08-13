from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceStressTestingDomainRead(BaseModel):
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

class TransformationResilienceStressTestingHypothesisRead(BaseModel):
    id: str
    hypothesis: str
    assumptionsJson: List[str]
    expectedOutcome: str
    confidence: float
    owner: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingCampaignRead(BaseModel):
    id: str
    name: str
    objective: str
    scope: str
    hypothesesJson: List[str]
    scenarioSetJson: List[str]
    schedule: str
    governanceRef: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingFailureInjectionRead(BaseModel):
    id: str
    injectionType: str
    targetId: str
    domain: str
    severity: str
    duration: str
    environment: str
    sandboxId: str
    sourceSnapshotId: str
    authorizationRef: str
    rollbackPlan: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingCompoundFailureRead(BaseModel):
    id: str
    failureAId: str
    failureBId: str
    failureCId: Optional[str]
    interaction: str
    combinedImpact: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingScenarioRead(BaseModel):
    id: str
    baselineSnapshotId: str
    injectionsJson: List[str]
    assumptionsJson: List[str]
    horizonDays: int
    expectedOutcome: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingRunRead(BaseModel):
    id: str
    scenarioId: str
    snapshotId: str
    simulationVersion: str
    seed: int
    startTime: str
    endTime: Optional[str]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingDetectionResultRead(BaseModel):
    id: str
    runId: str
    detected: bool
    detectionTimeSeconds: float
    detectionSource: str
    confidence: float
    falseNegative: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingWarningValidationRead(BaseModel):
    id: str
    expectedWarning: str
    actualWarning: str
    severity: str
    timingLeadTimeDays: int
    accuracyPct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingInterventionValidationRead(BaseModel):
    id: str
    interventionRecommended: bool
    interventionAuthorized: bool
    interventionExecuted: bool
    effectivenessPct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingRecoveryResultRead(BaseModel):
    id: str
    recoveryStartTime: str
    stabilizationDays: int
    coverageRestorationPct: float
    riskReductionPct: float
    residualExposure: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingResultRead(BaseModel):
    id: str
    runId: str
    detectionPassed: bool
    warningPassed: bool
    interventionPassed: bool
    recoveryPassed: bool
    residualExposure: float
    hypothesisResult: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingAssuranceGapRead(BaseModel):
    id: str
    gapType: str
    description: str
    severity: str
    evidenceJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingControlRead(BaseModel):
    id: str
    name: str
    controlType: str
    target: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingControlResultRead(BaseModel):
    id: str
    controlId: str
    expectedBehavior: str
    observedBehavior: str
    variance: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingControlFailureRead(BaseModel):
    id: str
    controlId: str
    failureReason: str
    impact: str
    recommendedImprovement: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingScorecardRead(BaseModel):
    id: str
    detectionScore: float
    responseScore: float
    recoveryScore: float
    evidenceScore: float
    dependencyResilienceScore: float
    governanceScore: float
    coverageScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingTrendRead(BaseModel):
    id: str
    direction: str
    summary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingRegressionRead(BaseModel):
    id: str
    testId: str
    previousResult: str
    currentResult: str
    status: str
    likelyCause: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingCoverageRead(BaseModel):
    id: str
    transformationsPct: float
    plansPct: float
    dependenciesPct: float
    risksPct: float
    knowledgePct: float
    decisionsPct: float
    interventionsPct: float
    recoveryPathsPct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingCoverageGapRead(BaseModel):
    id: str
    targetArea: str
    gapReason: str
    severity: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingScenarioMutationRead(BaseModel):
    id: str
    mutationType: str
    targetScenarioId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingAdversarialScenarioRead(BaseModel):
    id: str
    title: str
    adversarialPattern: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingRecoveryPlaybookTestRead(BaseModel):
    id: str
    playbookName: str
    readinessStatus: str
    missingDependenciesJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingGovernanceTestRead(BaseModel):
    id: str
    testedBoundary: str
    compliancePassed: bool
    findingsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingRemediationRecommendationRead(BaseModel):
    id: str
    gapId: str
    recommendedImprovement: str
    expectedBenefit: str
    effort: str
    risk: str
    confidence: float
    label: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStressTestingQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
