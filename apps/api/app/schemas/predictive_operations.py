from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ForecastCreate(BaseModel):
    entityType: str = "kpi"
    entityId: str
    metricId: Optional[str] = None
    horizon: str = "medium_term"
    method: str = "ensemble_timeseries"
    workspaceId: str = "ws_default"

class ForecastRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    entityType: str
    entityId: str
    metricId: Optional[str]
    horizon: str
    method: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class ForecastPointRead(BaseModel):
    id: str
    forecastId: str
    timestamp: str
    value: float
    lowerBound: float
    upperBound: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class PredictiveAlertRead(BaseModel):
    id: str
    forecastId: str
    alertType: str
    predictedWindow: str
    confidence: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class PredictiveRiskRead(BaseModel):
    id: str
    forecastId: str
    riskId: str
    affectedEntityId: str
    probabilityRange: str
    impact: str
    evidence: str

    model_config = ConfigDict(from_attributes=True)

class PredictiveRecommendationRead(BaseModel):
    id: str
    signalId: str
    optionsJson: List[Dict[str, Any]]
    expectedEffect: str
    riskLevel: str
    confidencePct: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class CapacityForecastRead(BaseModel):
    id: str
    capacityType: str
    demandValue: float
    capacityValue: float
    gap: float
    horizon: str

    model_config = ConfigDict(from_attributes=True)

class ForecastScenarioRead(BaseModel):
    id: str
    forecastId: str
    scenarioName: str
    scenarioParamsJson: Dict[str, Any]
    outputDistributionJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class ForecastAccuracyRead(BaseModel):
    id: str
    forecastId: str
    actualValue: float
    absoluteError: float
    percentageError: float
    intervalCoverage: float
    calibration: float

    model_config = ConfigDict(from_attributes=True)

class PredictiveQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
