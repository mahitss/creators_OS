from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class StrategicPlanCreate(BaseModel):
    name: str
    description: str
    owner: str
    startDate: str
    endDate: str
    workspaceId: str = "ws_default"

class StrategicPlanRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    owner: str
    status: str
    startDate: str
    endDate: str
    version: int
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class StrategicObjectiveCreate(BaseModel):
    planId: str
    name: str
    description: str
    priority: str = "high"
    owner: str
    target: str
    currentState: str
    deadline: str

class StrategicObjectiveRead(BaseModel):
    id: str
    planId: str
    name: str
    description: str
    priority: str
    owner: str
    status: str
    target: str
    currentState: str
    deadline: str

    model_config = ConfigDict(from_attributes=True)

class StrategicInitiativeCreate(BaseModel):
    objectiveId: str
    name: str
    description: str
    owner: str
    priority: str = "high"
    expectedOutcome: str
    estimatedCost: float = 100000.0
    estimatedDuration: str = "6 months"

class StrategicInitiativeRead(BaseModel):
    id: str
    objectiveId: str
    name: str
    description: str
    owner: str
    status: str
    priority: str
    expectedOutcome: str
    estimatedCost: float
    estimatedDuration: str

    model_config = ConfigDict(from_attributes=True)

class StrategicAssumptionCreate(BaseModel):
    planId: str
    statement: str
    source: str
    confidence: str = "high"
    assumptionType: str

class StrategicAssumptionRead(BaseModel):
    id: str
    planId: str
    statement: str
    source: str
    confidence: str
    assumptionType: str
    validity: str
    createdAt: str
    verifiedAt: Optional[str] = None
    expiresAt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StrategicRecommendationRead(BaseModel):
    id: str
    planId: str
    recommendation: str
    evidenceJson: Dict[str, Any]
    alternativesJson: List[Dict[str, Any]]
    tradeoffsJson: Dict[str, Any]
    risksJson: List[str]
    assumptionsJson: List[str]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)

class StrategicReviewRead(BaseModel):
    id: str
    planId: str
    reviewCadence: str
    progressSummary: str
    assumptionsEvaluatedJson: List[str]
    risksEvaluatedJson: List[str]
    driftSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class StrategicDriftRead(BaseModel):
    id: str
    planId: str
    driftType: str
    signalSummary: str
    evidenceJson: Dict[str, Any]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class StrategicScenarioRead(BaseModel):
    id: str
    name: str
    scenarioType: str
    changedAssumptions: List[str]
    impactSummary: Dict[str, Any]
    confidencePct: float

class StrategyQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
