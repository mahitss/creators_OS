from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceSensingDomainRead(BaseModel):
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

class TransformationResilienceObservationRead(BaseModel):
    id: str
    domainId: str
    source: str
    metric: str
    value: float
    timestamp: str
    confidence: float
    freshness: float
    scope: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceObservationQualityRead(BaseModel):
    id: str
    observationId: str
    completeness: float
    freshness: float
    consistency: float
    reliability: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSignalNormalizationRead(BaseModel):
    id: str
    domainId: str
    sourceMetric: str
    normalizedDimension: str
    normalizedScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDynamicBaselineRead(BaseModel):
    id: str
    domainId: str
    version: str
    effectivePeriod: str
    changeReason: str
    approvalContextJson: Dict[str, Any]
    baselineMetricsJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDriftRead(BaseModel):
    id: str
    domainId: str
    driftType: str
    metricName: str
    deviationPct: float
    severity: str
    detectedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStructuralChangeRead(BaseModel):
    id: str
    domainId: str
    changeType: str
    affectedScopeJson: List[str]
    materiality: str
    detectedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAlertEvaluationRead(BaseModel):
    id: str
    domainId: str
    conditionName: str
    persistenceCount: int
    corroborationScore: float
    actionable: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSensingWarningRead(BaseModel):
    id: str
    domainId: str
    condition: str
    severity: str
    confidence: float
    affectedScopeJson: List[str]
    recommendedReview: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSignalCorrelationRead(BaseModel):
    id: str
    domainId: str
    signalA: str
    signalB: str
    relationshipType: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceStateChangeRead(BaseModel):
    id: str
    domainId: str
    previousState: str
    newState: str
    evidenceJson: Dict[str, Any]
    confidence: float
    timestamp: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceTrendRead(BaseModel):
    id: str
    domainId: str
    dimension: str
    trendDirection: str
    window: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceForecastRead(BaseModel):
    id: str
    domainId: str
    targetMetric: str
    forecastValue: float
    uncertaintyJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssumptionRead(BaseModel):
    id: str
    domainId: str
    assumptionTitle: str
    sourceContext: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssumptionDriftRead(BaseModel):
    id: str
    assumptionId: str
    driftDescription: str
    severity: str
    affectedScenariosJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInvestmentReviewTriggerRead(BaseModel):
    id: str
    domainId: str
    affectedInvestmentId: str
    reason: str
    severity: str
    reviewDeadline: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPortfolioResilienceStateRead(BaseModel):
    id: str
    domainId: str
    robustness: float
    redundancy: float
    recoverability: float
    adaptability: float
    optionality: float
    observability: float
    governability: float
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceSensingQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
