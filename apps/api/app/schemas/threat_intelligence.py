from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ThreatSignalRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    sourceType: str
    sourceId: str
    signalType: str
    observedAt: str
    receivedAt: str
    confidence: str
    quality: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class WeakSignalRead(BaseModel):
    id: str
    signalId: str
    noveltyScore: float
    persistenceStatus: str
    signalVelocity: str
    confidence: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ThreatPatternRead(BaseModel):
    id: str
    patternType: str
    entitiesJson: List[Any]
    timeWindow: str
    strength: float
    confidence: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class EmergingThreatRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    affectedCapabilitiesJson: List[Any]
    probabilityRange: str
    timeHorizon: str
    severity: str
    confidence: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class EarlyWarningRead(BaseModel):
    id: str
    threatId: str
    triggerReason: str
    probability: str
    timeHorizon: str
    impactSummary: str
    confidence: str
    priority: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ThreatMitigationRead(BaseModel):
    id: str
    threatId: str
    actionName: str
    owner: str
    precondition: str
    authorizationStatus: str
    status: str
    expectedRiskReductionPct: float
    actualRiskReductionPct: float

    model_config = ConfigDict(from_attributes=True)

class ThreatBlindSpotRead(BaseModel):
    id: str
    domain: str
    missingSignalsJson: List[Any]
    impactSummary: str
    severity: str
    recommendation: str

    model_config = ConfigDict(from_attributes=True)

class ThreatQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
