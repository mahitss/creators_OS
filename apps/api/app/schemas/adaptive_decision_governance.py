from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class ControlLoopCreate(BaseModel):
    name: str
    description: str
    targetEntityType: str = "mission"
    targetEntityId: str = "msn_default"
    mode: str = "monitor_only"
    owner: str
    workspaceId: str = "ws_default"

class ControlLoopRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    targetEntityType: str
    targetEntityId: str
    mode: str
    status: str
    owner: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class ControlSignalRead(BaseModel):
    id: str
    loopId: str
    signalType: str
    value: float
    signalQuality: str
    confidence: str
    observedAt: str
    source: str
    retrievedAt: str
    freshness: str

    model_config = ConfigDict(from_attributes=True)

class DecisionValidityAssessmentRead(BaseModel):
    id: str
    decisionId: str
    validityStatus: str
    validityFactorsJson: Dict[str, Any]
    assessedAt: str

    model_config = ConfigDict(from_attributes=True)

class DecisionReassessmentRead(BaseModel):
    id: str
    decisionId: str
    triggerType: str
    evidence: str
    affectedDecisionId: str
    newConditionsJson: Dict[str, Any]
    recommendedNextStep: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ControlGuardrailRead(BaseModel):
    id: str
    loopId: str
    guardrailType: str
    threshold: float
    severity: str
    action: str
    approvalRequired: bool
    policyReference: str

    model_config = ConfigDict(from_attributes=True)

class GuardrailBreachRead(BaseModel):
    id: str
    guardrailId: str
    observedValue: float
    threshold: float
    evidence: str
    timestamp: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class ControlResponseRead(BaseModel):
    id: str
    loopId: str
    responseType: str
    payloadJson: Dict[str, Any]
    status: str
    confidence: str

    model_config = ConfigDict(from_attributes=True)

class ActionOutcomeObservationRead(BaseModel):
    id: str
    actionId: str
    expectedVal: float
    actualVal: float
    variance: float
    outcomeClass: str
    timestamp: str

    model_config = ConfigDict(from_attributes=True)

class ControlQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
