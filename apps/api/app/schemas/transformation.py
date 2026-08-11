from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationProgramRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    strategicDriversJson: List[Any]
    scope: str
    horizon: str
    owner: str
    status: str
    version: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDriverRead(BaseModel):
    id: str
    programId: str
    driverType: str
    source: str
    evidenceJson: Dict[str, Any]
    confidence: str
    freshness: str

    model_config = ConfigDict(from_attributes=True)

class OperatingModelCurrentStateRead(BaseModel):
    id: str
    programId: str
    unitsJson: List[Any]
    capabilitiesJson: List[Any]
    processesJson: List[Any]
    decisionRightsJson: List[Any]
    dependenciesJson: List[Any]
    systemsJson: List[Any]
    capacityJson: Dict[str, Any]
    version: str

    model_config = ConfigDict(from_attributes=True)

class OperatingModelTargetStateRead(BaseModel):
    id: str
    programId: str
    structureDesc: str
    targetCapabilitiesJson: List[Any]
    targetProcessesJson: List[Any]
    targetDecisionRightsJson: List[Any]
    targetDependenciesJson: List[Any]
    technologyDesc: str
    capacityDesc: str
    version: str

    model_config = ConfigDict(from_attributes=True)

class OperatingModelDeltaRead(BaseModel):
    id: str
    programId: str
    currentStateId: str
    targetStateId: str
    gapSummary: str
    severity: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class FutureOperatingModelRead(BaseModel):
    id: str
    programId: str
    name: str
    description: str
    designPrinciplesJson: List[Any]
    constraintsJson: List[Any]
    assumptionsJson: List[Any]
    targetCapabilitiesJson: List[Any]
    targetProcessesJson: List[Any]
    targetDecisionRightsJson: List[Any]
    targetDependenciesJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class OperatingModelDesignOptionRead(BaseModel):
    id: str
    futureModelId: str
    optionType: str
    evidenceJson: Dict[str, Any]
    assumptionsJson: List[Any]
    expectedEffect: str
    risksJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class OperatingModelComparisonRead(BaseModel):
    id: str
    programId: str
    optionAId: str
    optionBId: str
    costTradeoff: float
    speedTradeoff: float
    controlTradeoff: float
    resilienceTradeoff: float
    complexityTradeoff: float
    classification: str

    model_config = ConfigDict(from_attributes=True)

class TransformationScenarioRead(BaseModel):
    id: str
    programId: str
    scenarioName: str
    scenarioType: str
    simulatedPerformance: float
    simulatedRisk: float
    simulatedResilience: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRoadmapRead(BaseModel):
    id: str
    programId: str
    name: str
    phasesJson: List[Any]
    workstreamsJson: List[Any]
    milestonesJson: List[Any]
    decisionGatesJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionGateRead(BaseModel):
    id: str
    roadmapId: str
    gateName: str
    requiredCriteriaJson: Dict[str, Any]
    evidenceJson: Dict[str, Any]
    gateOutcome: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPilotRead(BaseModel):
    id: str
    programId: str
    hypothesis: str
    expectedEffect: str
    measurementCriteria: str
    successThreshold: str
    durationDays: int
    outcomeStatus: str

    model_config = ConfigDict(from_attributes=True)

class TransformationChangeProposalRead(BaseModel):
    id: str
    programId: str
    proposalTitle: str
    description: str
    evidenceJson: Dict[str, Any]
    optionsJson: List[Any]
    expectedEffect: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
