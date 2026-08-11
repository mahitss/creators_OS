from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class PortfolioCreate(BaseModel):
    name: str
    description: str
    owner: str
    workspaceId: str = "ws_default"

class PortfolioRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    owner: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class ProgramCreate(BaseModel):
    portfolioId: str
    name: str
    description: str
    owner: str
    priority: str = "high"
    targetOutcome: str

class ProgramRead(BaseModel):
    id: str
    portfolioId: str
    name: str
    description: str
    owner: str
    status: str
    priority: str
    targetOutcome: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioResourceConflictRead(BaseModel):
    id: str
    portfolioId: str
    resourceType: str
    competingInitiativesJson: List[str]
    timeWindow: str
    capacityGapSummary: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioOverlapRead(BaseModel):
    id: str
    portfolioId: str
    initiativeIdsJson: List[str]
    overlapType: str
    similaritySummary: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioOutcomeVarianceRead(BaseModel):
    id: str
    portfolioId: str
    initiativeId: str
    varianceType: str
    expectedOutcome: str
    measuredOutcome: str
    deltaSummary: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioRecommendationRead(BaseModel):
    id: str
    portfolioId: str
    recommendation: str
    evidenceJson: Dict[str, Any]
    alternativesJson: List[Dict[str, Any]]
    tradeoffsJson: Dict[str, Any]
    reversibility: str
    approvalStatus: str
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)

class PortfolioReviewRead(BaseModel):
    id: str
    portfolioId: str
    reviewCadence: str
    progressSummary: str
    costVarianceSummary: str
    scheduleVarianceSummary: str
    riskExposureSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class PortfolioScenarioRead(BaseModel):
    id: str
    name: str
    scenarioType: str
    changedInvestment: Dict[str, Any]
    impactSummary: Dict[str, Any]
    confidencePct: float

class PortfolioQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
