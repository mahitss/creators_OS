from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class SecurityResponseActionCreate(BaseModel):
    actionType: str = Field(..., description="monitor, notify, restrict, rate_limit, quarantine, pause_agent, disable_capability, block_tool, revoke_session, require_approval, revalidate_decision, pause_mission, cancel_mission")
    targetType: str
    targetId: str
    scope: str = "resource"
    reason: str
    authorization: str = "security_policy"
    expiresAt: Optional[str] = None

class SecurityResponseActionRead(BaseModel):
    id: str
    planId: str
    actionType: str
    targetType: str
    targetId: str
    scope: str
    reason: str
    authorization: str
    status: str
    expiresAt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SecurityResponsePlanCreate(BaseModel):
    incidentId: str
    riskLevel: str = "high"
    actions: List[SecurityResponseActionCreate] = []

class SecurityResponsePlanRead(BaseModel):
    id: str
    incidentId: str
    version: int
    status: str
    riskLevel: str
    approvalRequirements: List[str]
    actions: List[SecurityResponseActionRead] = []
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecurityDetectionRuleCreate(BaseModel):
    name: str
    description: str = ""
    conditionsJson: Dict[str, Any] = {}
    severity: str = "high"
    scope: str = "global"

class SecurityDetectionRuleRead(BaseModel):
    id: str
    name: str
    description: str
    conditionsJson: Dict[str, Any]
    severity: str
    scope: str
    status: str
    version: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecurityAutomationRuleCreate(BaseModel):
    name: str
    triggerEventType: str
    conditionJson: Dict[str, Any] = {}
    responseActionType: str
    scope: str = "workspace"
    maxActions: int = 5
    cooldownSeconds: int = 300
    approvalRequired: bool = True

class SecurityAutomationRuleRead(BaseModel):
    id: str
    name: str
    triggerEventType: str
    conditionJson: Dict[str, Any]
    responseActionType: str
    scope: str
    maxActions: int
    cooldownSeconds: int
    approvalRequired: bool
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecurityRunbookCreate(BaseModel):
    name: str
    triggerCondition: str
    investigationStepsJson: List[str] = []
    approvedResponsesJson: List[str] = []
    verificationStepsJson: List[str] = []

class SecurityRunbookRead(BaseModel):
    id: str
    name: str
    triggerCondition: str
    investigationStepsJson: List[str]
    approvedResponsesJson: List[str]
    verificationStepsJson: List[str]
    version: int
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecurityPostIncidentReviewCreate(BaseModel):
    incidentId: str
    rootCauseType: str = Field("confirmed", description="confirmed, likely, unknown")
    rootCauseSummary: str
    detectionQualityScore: float = 4.5
    responseQualityScore: float = 4.8
    lessonsJson: List[str] = []

class SecurityPostIncidentReviewRead(BaseModel):
    id: str
    incidentId: str
    rootCauseType: str
    rootCauseSummary: str
    detectionQualityScore: float
    responseQualityScore: float
    lessonsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecuritySLARead(BaseModel):
    id: str
    incidentId: str
    timeToDetectSeconds: float
    timeToTriageSeconds: float
    timeToContainSeconds: float
    timeToRecoverSeconds: float
    slaBreached: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class SecurityInvestigationNoteCreate(BaseModel):
    investigationId: str
    authorId: str
    authorType: str = "human-authored"
    content: str
