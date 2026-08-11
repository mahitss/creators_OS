from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class AdaptiveStrategyRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    strategicIntent: str
    horizon: str
    status: str
    owner: str
    version: int
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class StrategicThesisRead(BaseModel):
    id: str
    strategyId: str
    belief: str
    evidenceJson: Dict[str, Any]
    assumptionsJson: List[Any]
    expectedOutcome: str
    confidence: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class StrategyIndicatorRead(BaseModel):
    id: str
    strategyId: str
    metric: str
    baseline: float
    target: float
    current: float
    direction: str
    threshold: float
    source: str
    freshness: str
    type: str

    model_config = ConfigDict(from_attributes=True)

class StrategyDriftSignalRead(BaseModel):
    id: str
    strategyId: str
    driftType: str
    severity: str
    evidenceJson: Dict[str, Any]
    affectedStrategy: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioReconfigurationRead(BaseModel):
    id: str
    strategyId: str
    reconfigurationType: str
    currentStateJson: Dict[str, Any]
    proposedStateJson: Dict[str, Any]
    reason: str
    evidenceJson: Dict[str, Any]
    expectedEffect: str
    risksJson: List[Any]
    affectedInitiativesJson: List[Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class StrategicExperimentRead(BaseModel):
    id: str
    strategyId: str
    hypothesis: str
    testDesign: str
    durationDays: int
    cost: float
    successCriteria: str
    decisionThreshold: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class AdaptiveStrategyQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
