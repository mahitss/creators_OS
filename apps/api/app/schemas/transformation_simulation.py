from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationDigitalTwinRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    scope: str
    version: str
    baselineSnapshotId: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationTwinBaselineRead(BaseModel):
    id: str
    twinId: str
    strategyStateJson: Dict[str, Any]
    operatingModelJson: Dict[str, Any]
    portfolioJson: Dict[str, Any]
    governanceJson: Dict[str, Any]
    capacityJson: Dict[str, Any]
    dependenciesJson: Dict[str, Any]
    risksJson: Dict[str, Any]
    benefitsJson: Dict[str, Any]
    kpisJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationTwinSnapshotRead(BaseModel):
    id: str
    twinId: str
    timestamp: str
    sourceVersionsJson: Dict[str, Any]
    includedSystemsJson: List[str]
    dataFreshnessMinutes: float

    model_config = ConfigDict(from_attributes=True)

class TransformationTwinStateRead(BaseModel):
    id: str
    twinId: str
    stateType: str
    stateDataJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationChangeSetRead(BaseModel):
    id: str
    twinId: str
    changesJson: List[Dict[str, Any]]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationRunRead(BaseModel):
    id: str
    twinId: str
    baselineStateId: str
    proposedStateId: str
    scenario: str
    modelVersion: str
    status: str
    startedAt: str
    completedAt: str
    hashFingerprint: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationModelRead(BaseModel):
    id: str
    modelType: str
    version: str
    assumptionsJson: Dict[str, Any]
    parametersJson: Dict[str, Any]
    evaluationStatus: str
    limitations: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationInputRead(BaseModel):
    id: str
    runId: str
    entity: str
    value: str
    source: str
    confidence: float
    assumption: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationOutputRead(BaseModel):
    id: str
    runId: str
    metric: str
    lowValue: float
    expectedValue: float
    highValue: float
    confidence: float
    timeHorizon: str
    scenario: str

    model_config = ConfigDict(from_attributes=True)

class TransformationMultiScenarioRunRead(BaseModel):
    id: str
    twinId: str
    changeSetId: str
    scenariosJson: List[Dict[str, Any]]
    robustnessScore: float
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationComparisonRead(BaseModel):
    id: str
    runId: str
    currentSummary: str
    proposedSummary: str
    alternativeSummary: str
    comparisonDimensionsJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationTradeoffRead(BaseModel):
    id: str
    runId: str
    benefitGained: str
    riskGained: str
    costImpact: float
    delayDays: float
    optionalityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationSensitivityAnalysisRead(BaseModel):
    id: str
    runId: str
    variableName: str
    lowValue: float
    expectedValue: float
    highValue: float
    impactScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSimulationReviewRead(BaseModel):
    id: str
    runId: str
    decisionImpact: str
    limitations: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWhatIfQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
