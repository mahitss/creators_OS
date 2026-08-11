from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationForesightDomainRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    horizon: str
    scope: str
    owner: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationFutureDriverRead(BaseModel):
    id: str
    domainId: str
    driverType: str
    name: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationDriverTrendRead(BaseModel):
    id: str
    driverId: str
    direction: str
    velocity: float
    acceleration: float
    uncertaintyScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationWeakSignalRead(BaseModel):
    id: str
    domainId: str
    signalText: str
    evidenceJson: Dict[str, Any]
    possibleMeaning: str
    alternativeInterpretationsJson: List[Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationEmergingPatternRead(BaseModel):
    id: str
    domainId: str
    patternName: str
    signalsJson: List[Any]
    frequency: int
    confidence: float
    timeWindow: str

    model_config = ConfigDict(from_attributes=True)

class TransformationFutureStateRead(BaseModel):
    id: str
    domainId: str
    stateType: str
    variablesJson: Dict[str, Any]
    description: str

    model_config = ConfigDict(from_attributes=True)

class TransformationScenarioImpactRead(BaseModel):
    id: str
    scenarioId: str
    transformationIdsJson: List[Any]
    impactRangeJson: Dict[str, Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationSecondOrderEffectRead(BaseModel):
    id: str
    scenarioImpactId: str
    propagationPathJson: List[Any]
    description: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationVulnerabilityProfileRead(BaseModel):
    id: str
    transformationId: str
    vulnerabilityDimensionsJson: Dict[str, Any]
    overallScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationOpportunityProfileRead(BaseModel):
    id: str
    transformationId: str
    opportunityType: str
    potentialBenefit: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationNoRegretActionRead(BaseModel):
    id: str
    domainId: str
    actionDesc: str
    multiscenarioUtility: float
    reversibility: str
    downsideRisk: str

    model_config = ConfigDict(from_attributes=True)

class TransformationForesightTriggerRead(BaseModel):
    id: str
    thresholdId: str
    status: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationForecastVersionRead(BaseModel):
    id: str
    domainId: str
    versionTag: str
    predictionJson: Dict[str, Any]
    confidence: float
    modelVersion: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationForesightReviewRead(BaseModel):
    id: str
    domainId: str
    reviewCadence: str
    summaryJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
