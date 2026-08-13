from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceDigitalTwinDomainRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    scope: str
    sourceVersion: str
    stateVersion: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinStateRead(BaseModel):
    id: str
    domainId: str
    timestamp: str
    sourceEventId: str
    sourceVersion: str
    stateHash: str
    freshness: float
    completeness: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinSnapshotRead(BaseModel):
    id: str
    version: str
    parentVersion: str
    transformationsCount: int
    plansCount: int
    dependenciesCount: int
    risksCount: int
    knowledgeCount: int
    evidenceCount: int
    warningsCount: int
    conflictsCount: int
    interventionsCount: int
    decisionsCount: int
    resourcesCount: int
    deadlinesCount: int
    stateHash: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinSynchronizationRead(BaseModel):
    id: str
    lastSourceEventId: str
    lastProcessedEventId: str
    lagSeconds: float
    errorsCount: int
    rebuildStatus: str
    synchronizationMode: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinStateDiffRead(BaseModel):
    id: str
    previousSnapshotVersion: str
    currentSnapshotVersion: str
    changedObjectsJson: List[str]
    addedObjectsJson: List[str]
    removedObjectsJson: List[str]
    changedRelationshipsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinNodeRead(BaseModel):
    id: str
    nodeType: str
    nodeId: str
    domain: str
    severity: str
    state: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinRelationshipRead(BaseModel):
    id: str
    sourceNodeId: str
    targetNodeId: str
    relationship: str
    confidence: float
    validFrom: str
    validTo: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinRealityComparisonRead(BaseModel):
    id: str
    productionStateSummary: str
    twinStateSummary: str
    differenceDescription: str
    freshness: float
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinScenarioForkRead(BaseModel):
    id: str
    baseSnapshotId: str
    scenarioId: str
    owner: str
    createdAt: str
    expiresAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinScenarioStateRead(BaseModel):
    id: str
    scenarioForkId: str
    hypotheticalStateJson: Dict[str, Any]
    isolationLevel: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinCounterfactualChangeRead(BaseModel):
    id: str
    changeType: str
    targetObjectId: str
    parametersJson: Dict[str, Any]
    description: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinCounterfactualScenarioRead(BaseModel):
    id: str
    baselineSnapshotId: str
    changesJson: List[str]
    assumptionsJson: List[str]
    horizonDays: int
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinScenarioOutcomeRead(BaseModel):
    id: str
    scenarioId: str
    riskScore: float
    coverageScore: float
    capacityScore: float
    deadlineImpactDays: int
    dependencyExposureScore: float
    residualRiskScore: float
    recoveryTimeDays: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinCounterfactualComparisonRead(BaseModel):
    id: str
    baselineId: str
    scenarioId: str
    differenceSummary: str
    uncertainty: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinStressScenarioRead(BaseModel):
    id: str
    stressType: str
    severity: str
    affectedDomainsJson: List[str]
    recoveryImpact: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinExternalShockScenarioRead(BaseModel):
    id: str
    shockName: str
    affectedDomainsJson: List[str]
    severity: str
    durationDays: int
    recoveryAssumptionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinRecoveryScenarioRead(BaseModel):
    id: str
    recoveryMode: str
    timeToStabilizationDays: int
    riskReductionPct: float
    coverageRecoveryPct: float
    capacityRecoveryPct: float
    residualExposure: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinExperimentRead(BaseModel):
    id: str
    title: str
    hypothesis: str
    scope: str
    assumptionsJson: List[str]
    expectedResult: str
    status: str
    authorizationRef: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinExperimentResultRead(BaseModel):
    id: str
    experimentId: str
    hypothesis: str
    observedResult: str
    expectedResult: str
    variance: str
    confidence: float
    limitationsJson: List[str]
    snapshotVersion: str
    scenarioVersion: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinValidationRead(BaseModel):
    id: str
    accuracyPct: float
    coveragePct: float
    divergencePct: float
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinModelErrorRead(BaseModel):
    id: str
    errorType: str
    description: str
    predictedValue: str
    observedValue: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinDriftRead(BaseModel):
    id: str
    driftType: str
    description: str
    driftMagnitude: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinScenarioLibraryRead(BaseModel):
    id: str
    name: str
    category: str
    scenarioRef: str
    approvedForReuse: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDigitalTwinQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
