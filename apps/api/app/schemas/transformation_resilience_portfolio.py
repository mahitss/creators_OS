from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResiliencePortfolioRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    scope: str
    owner: str
    status: str
    version: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceExposureRead(BaseModel):
    id: str
    portfolioId: str
    transformationId: str
    exposureType: str
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationSharedDependencyRead(BaseModel):
    id: str
    portfolioId: str
    dependencyName: str
    affectedTransformationsJson: List[str]
    criticality: float
    failureImpactJson: Dict[str, Any]
    substitutionOptionsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationSharedCapacityExposureRead(BaseModel):
    id: str
    portfolioId: str
    capacityType: str
    affectedTransformationsJson: List[str]
    requiredCapacity: float
    availableCapacity: float
    contentionScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioCapacityConflictRead(BaseModel):
    id: str
    portfolioId: str
    conflictingInvestmentsJson: List[str]
    capacityResource: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioFailurePatternRead(BaseModel):
    id: str
    portfolioId: str
    patternName: str
    recurringFailureType: str
    affectedTransformationsCount: int
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioSystemicRiskRead(BaseModel):
    id: str
    portfolioId: str
    sourceDependency: str
    affectedScopeJson: List[str]
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioMultiFailureScenarioRead(BaseModel):
    id: str
    portfolioId: str
    scenarioTitle: str
    simultaneousFailuresJson: List[str]
    correlatedPropagationJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceInvestmentRead(BaseModel):
    id: str
    portfolioId: str
    investmentTitle: str
    cost: float
    protectedTransformationsJson: List[str]
    riskReductionPct: float
    priority: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInvestmentOverlapRead(BaseModel):
    id: str
    portfolioId: str
    overlappingInvestmentsJson: List[str]
    duplicatedCoverageDescription: str
    potentialSavings: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInvestmentGapRead(BaseModel):
    id: str
    portfolioId: str
    unprotectedSystemicExposure: str
    affectedTransformationsJson: List[str]
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResiliencePortfolioTradeoffRead(BaseModel):
    id: str
    portfolioId: str
    optionAJson: Dict[str, Any]
    optionBJson: Dict[str, Any]
    tradeoffComparisonJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInvestmentSequenceRead(BaseModel):
    id: str
    portfolioId: str
    sequenceOrder: int
    investmentId: str
    prerequisitesJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceOptionValueRead(BaseModel):
    id: str
    portfolioId: str
    optionName: str
    flexibilityScore: float
    preservedFuturePathsCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDiversificationPlanRead(BaseModel):
    id: str
    portfolioId: str
    concentrationTarget: str
    proposedDiversification: str
    recommendationOnly: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceRoadmapRead(BaseModel):
    id: str
    portfolioId: str
    roadmapTitle: str
    milestonesJson: List[str]
    totalBudget: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceReviewRead(BaseModel):
    id: str
    portfolioId: str
    reviewTrigger: str
    summaryFindingsJson: Dict[str, Any]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
