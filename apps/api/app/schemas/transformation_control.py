from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationControlTowerRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    portfolioId: str
    status: str
    owner: str
    lastEvaluatedAt: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationLiveStateRead(BaseModel):
    id: str
    controlTowerId: str
    plannedStateJson: Dict[str, Any]
    actualStateJson: Dict[str, Any]
    forecastStateJson: Dict[str, Any]
    lastChange: str
    lastEvaluation: str

    model_config = ConfigDict(from_attributes=True)

class TransformationControlSignalRead(BaseModel):
    id: str
    controlTowerId: str
    signalType: str
    severity: str
    status: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationSituationRead(BaseModel):
    id: str
    controlTowerId: str
    signalsJson: List[Any]
    affectedTransformationsJson: List[Any]
    affectedWavesJson: List[Any]
    affectedObjectivesJson: List[Any]
    evidenceJson: Dict[str, Any]
    confidence: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRootCauseAssessmentRead(BaseModel):
    id: str
    situationId: str
    category: str
    evidenceLabel: str
    description: str
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWaveReadinessRead(BaseModel):
    id: str
    waveId: str
    capabilityReadiness: float
    technologyReadiness: float
    processReadiness: float
    capacityReadiness: float
    dependencyReadiness: float
    riskReadiness: float
    adoptionReadiness: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationChangeRequestRead(BaseModel):
    id: str
    controlTowerId: str
    requestType: str
    proposedChangeDesc: str
    impactAnalysisJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationIncidentRead(BaseModel):
    id: str
    controlTowerId: str
    title: str
    severity: str
    impactSummary: str
    responseRecommendation: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationEscalationRead(BaseModel):
    id: str
    controlTowerId: str
    triggerReason: str
    urgency: str
    decisionOwnerUnitId: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWeeklyReviewRead(BaseModel):
    id: str
    controlTowerId: str
    portfolioSummary: str
    wavesSummary: str
    signalsSummary: str
    risksSummary: str
    benefitsSummary: str
    decisionsSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationControlQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
