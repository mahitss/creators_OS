from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class AIUsageEventRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    agentId: Optional[str] = None
    missionId: Optional[str] = None
    decisionId: Optional[str] = None
    workflowId: Optional[str] = None
    modelId: Optional[str] = None
    providerId: Optional[str] = None
    capabilityId: Optional[str] = None
    usageType: str
    unitsUsed: float
    tokensInput: int
    tokensOutput: int
    tokensCached: int
    tokensReasoning: int
    latencyMs: float
    timestamp: str

    model_config = ConfigDict(from_attributes=True)

class AIPriceCatalogRead(BaseModel):
    id: str
    provider: str
    model: str
    unit: str
    price: float
    currency: str
    effectiveFrom: str
    effectiveTo: Optional[str] = None
    source: str
    version: int

    model_config = ConfigDict(from_attributes=True)

class CostCalculationRead(BaseModel):
    id: str
    usageEventId: str
    priceVersionId: str
    units: float
    estimatedCost: float
    actualCost: Optional[float] = None
    currency: str
    costStatus: str = Field(..., description="estimated, reported, reconciled, unknown")
    organizationId: str
    workspaceId: str
    agentId: Optional[str] = None
    missionId: Optional[str] = None
    timestamp: str

    model_config = ConfigDict(from_attributes=True)

class AIBudgetCreate(BaseModel):
    scope: str = Field("organization", description="organization, workspace, team, agent, mission")
    period: str = Field("monthly", description="daily, weekly, monthly, custom")
    limitAmount: float
    currency: str = "USD"
    softThresholdPct: float = 75.0
    hardLimitAction: str = Field("require_approval", description="block, pause, require_approval, degrade")

class AIBudgetRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: Optional[str] = None
    teamId: Optional[str] = None
    agentId: Optional[str] = None
    missionId: Optional[str] = None
    scope: str
    period: str
    limitAmount: float
    currency: str
    spentAmount: float
    committedAmount: float
    forecastAmount: float
    remainingAmount: float
    softThresholdPct: float
    hardLimitAction: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class CostForecastRead(BaseModel):
    id: str
    organizationId: str
    scope: str
    currentPeriodExpected: float
    lowerBound: float
    upperBound: float
    confidencePct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class OptimizationRecommendationRead(BaseModel):
    id: str
    organizationId: str
    type: str = Field(..., description="model_switch, prompt_reduction, retrieval_reduction, retry_reduction, workflow_optimization, cache_usage, batching, scheduling")
    estimatedSavings: float
    qualityImpact: str
    latencyImpact: str
    riskLevel: str
    confidencePct: float
    evidenceJson: Dict[str, Any]
    approvalStatus: str

    model_config = ConfigDict(from_attributes=True)

class CostOptimizationExperimentCreate(BaseModel):
    recommendationId: str
    baselineConfigJson: Dict[str, Any] = {}
    optimizedConfigJson: Dict[str, Any] = {}

class CostOptimizationExperimentRead(BaseModel):
    id: str
    recommendationId: str
    baselineConfigJson: Dict[str, Any]
    optimizedConfigJson: Dict[str, Any]
    baselineCost: float
    optimizedCost: float
    baselineQuality: float
    optimizedQuality: float
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class AICapacitySnapshotRead(BaseModel):
    id: str
    concurrencyUsed: int
    concurrencyLimit: int
    queueDepth: int
    providerLimitsJson: Dict[str, Any]
    loadSheddingRecommended: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CostReconciliationRead(BaseModel):
    id: str
    organizationId: str
    period: str
    estimatedTotal: float
    providerReportedTotal: float
    varianceAmount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class CostAdjustmentCreate(BaseModel):
    costCalculationId: str
    originalAmount: float
    adjustedAmount: float
    reason: str
