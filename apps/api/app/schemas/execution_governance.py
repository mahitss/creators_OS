from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class BenefitCreate(BaseModel):
    name: str
    description: str
    owner: str
    benefitType: str
    baseline: float = 0.0
    target: float = 100.0
    unit: str = "USD"
    measurementMethod: str
    portfolioId: Optional[str] = None
    programId: Optional[str] = None
    initiativeId: Optional[str] = None
    outcomeId: Optional[str] = None

class BenefitRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    portfolioId: Optional[str]
    programId: Optional[str]
    initiativeId: Optional[str]
    outcomeId: Optional[str]
    name: str
    description: str
    owner: str
    status: str
    benefitType: str
    baseline: float
    target: float
    currentValue: float
    unit: str
    measurementMethod: str
    targetDate: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class BenefitEvidenceRead(BaseModel):
    id: str
    benefitId: str
    source: str
    reference: str
    observedAt: str
    confidence: float
    verificationStatus: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionMilestoneCreate(BaseModel):
    initiativeId: str
    name: str
    description: str
    dueDate: str

class ExecutionMilestoneRead(BaseModel):
    id: str
    initiativeId: str
    name: str
    description: str
    dueDate: str
    status: str
    completionEvidence: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ExecutionVarianceRead(BaseModel):
    id: str
    initiativeId: str
    varianceType: str
    baseline: str
    actual: str
    forecast: str
    delta: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionGateRead(BaseModel):
    id: str
    initiativeId: str
    gateType: str
    status: str
    waiverActor: Optional[str]
    waiverReason: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ExecutionChangeRequestRead(BaseModel):
    id: str
    initiativeId: str
    changeType: str
    requestedChange: str
    reason: str
    impactSummary: str
    status: str
    requester: str

    model_config = ConfigDict(from_attributes=True)

class ExecutionForecastRead(BaseModel):
    id: str
    initiativeId: str
    forecastCompletionDate: str
    forecastCost: float
    forecastBenefit: float
    lowerBound: float
    upperBound: float
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)

class ExecutionQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
