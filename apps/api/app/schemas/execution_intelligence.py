from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ExecutionObjectiveRead(BaseModel):
    id: str
    strategyId: str
    name: str
    description: str
    targetOutcome: str
    priority: str
    owner: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class StrategicAlignmentAssessmentRead(BaseModel):
    id: str
    objectiveId: str
    portfolioId: Optional[str]
    initiativeId: Optional[str]
    missionId: Optional[str]
    alignmentStatus: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class ExecutionCoverageRead(BaseModel):
    id: str
    objectiveId: str
    portfolioCoveragePct: float
    initiativeCoveragePct: float
    missionCoveragePct: float
    executionCoveragePct: float
    benefitCoveragePct: float
    hasGap: bool

    model_config = ConfigDict(from_attributes=True)

class StrategicExecutionPathRead(BaseModel):
    id: str
    strategyId: str
    objectiveId: str
    initiativeId: str
    missionId: str
    actionId: Optional[str]
    deliverableId: Optional[str]
    outcomeId: Optional[str]
    benefitId: Optional[str]
    pathIntegrityStatus: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionDriftSignalRead(BaseModel):
    id: str
    strategyId: str
    objectiveId: str
    driftType: str
    severity: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class ExecutionDependencyBlockerRead(BaseModel):
    id: str
    blockedInitiativeId: str
    dependencyId: str
    owner: str
    durationDays: int
    impactSummary: str
    severity: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionRecommendationRead(BaseModel):
    id: str
    objectiveId: str
    initiativeId: str
    recommendationType: str
    reason: str
    evidenceJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
