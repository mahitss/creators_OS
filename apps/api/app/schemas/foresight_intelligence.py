from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ForesightProgramRead(BaseModel):
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

class FutureDriverRead(BaseModel):
    id: str
    programId: str
    type: str
    driverName: str
    strength: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class StrategicTrendRead(BaseModel):
    id: str
    programId: str
    trendName: str
    direction: str
    velocity: str
    persistence: str
    confidence: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class StrategicAssumptionRead(BaseModel):
    id: str
    programId: str
    statement: str
    source: str
    confidence: str
    validUntil: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class FutureScenarioRead(BaseModel):
    id: str
    programId: str
    name: str
    description: str
    horizon: str
    scenarioType: str
    plausibility: str
    assumptionsJson: List[Any]
    driversJson: List[Any]
    uncertaintiesJson: List[Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class ScenarioIndicatorRead(BaseModel):
    id: str
    scenarioId: str
    indicatorName: str
    baselineVal: float
    thresholdVal: float
    currentVal: float
    direction: str
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class StrategicOptionRead(BaseModel):
    id: str
    scenarioId: str
    optionName: str
    optionType: str
    reversibility: str
    robustnessScore: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class StrategicBetRead(BaseModel):
    id: str
    programId: str
    thesis: str
    investmentAmount: float
    expectedOutcomesJson: List[Any]
    scenariosJson: List[Any]
    evidence: str
    reviewDate: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ForesightQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
