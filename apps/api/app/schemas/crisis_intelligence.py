from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class CrisisCreate(BaseModel):
    name: str
    description: str
    severity: str = "SEV1"
    declaredBy: str
    commanderId: str
    workspaceId: str = "ws_default"

class CrisisRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    status: str
    severity: str
    declaredBy: str
    declaredAt: str
    commanderId: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class CrisisSignalRead(BaseModel):
    id: str
    crisisId: str
    signalType: str
    confidence: str
    source: str
    observedAt: str
    receivedAt: str
    sourceVersion: str

    model_config = ConfigDict(from_attributes=True)

class CrisisImpactAssessmentRead(BaseModel):
    id: str
    crisisId: str
    impactStatus: str
    evidence: str

    model_config = ConfigDict(from_attributes=True)

class CrisisCommandRead(BaseModel):
    id: str
    crisisId: str
    incidentCommander: str
    operationsLead: str
    technicalLead: str
    securityLead: str
    communicationsLead: str
    businessLead: str
    recoveryLead: str

    model_config = ConfigDict(from_attributes=True)

class CrisisResponseOptionRead(BaseModel):
    id: str
    crisisId: str
    name: str
    expectedImpact: str
    costEstimate: float
    riskLevel: str
    recoveryTimeMin: int
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class CrisisCommunicationRead(BaseModel):
    id: str
    crisisId: str
    audience: str
    message: str
    channel: str
    sender: str
    approvalStatus: str
    sentAt: str

    model_config = ConfigDict(from_attributes=True)

class CrisisTimelineEventRead(BaseModel):
    id: str
    crisisId: str
    timestamp: str
    actor: str
    eventType: str
    description: str
    evidence: str

    model_config = ConfigDict(from_attributes=True)

class AfterActionReviewRead(BaseModel):
    id: str
    crisisId: str
    whatHappened: str
    whatWorked: str
    whatFailed: str
    unexpectedBehavior: str

    model_config = ConfigDict(from_attributes=True)

class CrisisDrillRead(BaseModel):
    id: str
    name: str
    scenarioType: str
    status: str
    nextDueDate: str

    model_config = ConfigDict(from_attributes=True)

class CrisisQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
