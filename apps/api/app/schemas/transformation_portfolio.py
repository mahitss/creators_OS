from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationPortfolioRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    strategyId: str
    horizon: str
    status: str
    owner: str
    version: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationCandidateRead(BaseModel):
    id: str
    portfolioId: str
    transformationProgramId: str
    strategicValueJson: Dict[str, Any]
    urgency: str
    riskScore: float
    costEstimate: float
    capacityDemandJson: Dict[str, Any]
    optionalValue: float
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDependencyGraphRead(BaseModel):
    id: str
    portfolioId: str
    dependencyMatrixJson: Dict[str, Any]
    criticalPathJson: List[Any]
    parallelGroupsJson: List[Any]
    cyclesDetected: bool
    blockedCandidatesJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationSequenceRead(BaseModel):
    id: str
    portfolioId: str
    name: str
    sequenceType: str
    phasesJson: List[Any]
    orderJson: List[Any]
    parallelGroupsJson: List[Any]
    decisionGatesJson: List[Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSequenceComparisonRead(BaseModel):
    id: str
    portfolioId: str
    sequenceAId: str
    sequenceBId: str
    timeDiff: float
    costDiff: float
    riskDiff: float
    capacityDiff: float
    benefitDiff: float
    optionalityDiff: float
    robustnessScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioBottleneckRead(BaseModel):
    id: str
    portfolioId: str
    bottleneckType: str
    description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWaveRead(BaseModel):
    id: str
    portfolioId: str
    waveNumber: int
    waveType: str
    candidateIdsJson: List[Any]
    exitCriteriaJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioRebalanceRead(BaseModel):
    id: str
    portfolioId: str
    rebalanceReason: str
    proposedSequenceId: str
    evidenceJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
