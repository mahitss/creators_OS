from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class KPICreate(BaseModel):
    name: str
    description: str
    definition: str
    owner: str
    category: str = "operational"
    unit: str = "USD"
    direction: str = "higher_is_better"
    workspaceId: str = "ws_default"

class KPIRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    definition: str
    owner: str
    status: str
    category: str
    unit: str
    direction: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class KPITargetCreate(BaseModel):
    kpiId: str
    targetValue: float
    effectiveFrom: str
    effectiveTo: str
    owner: str

class KPITargetRead(BaseModel):
    id: str
    kpiId: str
    targetValue: float
    effectiveFrom: str
    effectiveTo: str
    owner: str
    version: int

    model_config = ConfigDict(from_attributes=True)

class KPIMeasurementCreate(BaseModel):
    kpiId: str
    value: float
    periodStart: str
    periodEnd: str
    source: str
    quality: str = "verified"

class KPIMeasurementRead(BaseModel):
    id: str
    kpiId: str
    value: float
    timestamp: str
    periodStart: str
    periodEnd: str
    source: str
    quality: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class KPIVarianceRead(BaseModel):
    id: str
    kpiId: str
    actual: float
    target: float
    baseline: float
    delta: float
    percentageDelta: float
    severity: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class KPIAlertRead(BaseModel):
    id: str
    kpiId: str
    alertType: str
    title: str
    description: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class KPIDriverRead(BaseModel):
    id: str
    kpiId: str
    driverName: str
    driverType: str
    associationType: str
    confidencePct: float
    evidenceSummary: str

    model_config = ConfigDict(from_attributes=True)

class KPIForecastRead(BaseModel):
    id: str
    kpiId: str
    forecastValue: float
    lowerBound: float
    upperBound: float
    confidencePct: float
    generatedAt: str

    model_config = ConfigDict(from_attributes=True)

class KPIScorecardRead(BaseModel):
    id: str
    organizationId: str
    name: str
    scorecardType: str
    kpiIdsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class KPIQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
