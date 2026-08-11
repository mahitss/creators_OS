from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class OptimizationProblemCreate(BaseModel):
    name: str
    description: str
    objectiveType: str = "maximize_outcome"
    owner: str
    workspaceId: str = "ws_default"

class OptimizationProblemRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    objectiveType: str
    status: str
    owner: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class OptimizationOptionRead(BaseModel):
    id: str
    problemId: str
    variablesJson: Dict[str, Any]
    constraintsSatisfied: bool
    expectedOutcome: float
    expectedCost: float
    expectedRisk: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class PrescriptiveRecommendationRead(BaseModel):
    id: str
    problemId: str
    recommendedOptionId: str
    alternativesJson: List[Dict[str, Any]]
    objectiveSummary: str
    constraintsSummary: str
    evidence: str
    expectedImpact: str
    riskLevel: str
    confidencePct: float
    robustnessScore: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class OptimizationActionPlanRead(BaseModel):
    id: str
    recommendationId: str
    actionsJson: List[Dict[str, Any]]
    owner: str
    dependenciesJson: List[str]
    milestonesJson: List[str]
    rollbackPlan: str
    executionMode: str

    model_config = ConfigDict(from_attributes=True)

class RobustnessAnalysisRead(BaseModel):
    id: str
    optionId: str
    demandChange: str
    costChange: str
    capacityChange: str
    dependencyFailureImpact: str
    robustnessScore: float

    model_config = ConfigDict(from_attributes=True)

class SensitivityAnalysisRead(BaseModel):
    id: str
    optionId: str
    variableName: str
    impactDirection: str
    estimatedMagnitude: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class OptimizationTradeoffRead(BaseModel):
    id: str
    problemId: str
    optionAId: str
    optionBId: str
    comparisonJson: Dict[str, Any]
    paretoFrontierFlag: bool

    model_config = ConfigDict(from_attributes=True)

class OptimizationPerformanceRead(BaseModel):
    id: str
    recommendationId: str
    expectedOutcome: float
    actualOutcome: float
    expectedCost: float
    actualCost: float
    benefitAccuracy: float
    costAccuracy: float
    forecastError: float

    model_config = ConfigDict(from_attributes=True)

class PrescriptiveQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
