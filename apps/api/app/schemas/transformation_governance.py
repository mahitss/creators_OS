from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationGovernanceProfileRead(BaseModel):
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

class TransformationGovernanceDomainRead(BaseModel):
    id: str
    profileId: str
    domainType: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionRightRead(BaseModel):
    id: str
    profileId: str
    decisionType: str
    scope: str
    authorityLevel: str
    requiredEvidence: str
    approvalRequirement: str
    escalationRequirement: str
    delegationAllowed: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionRightMatrixRead(BaseModel):
    id: str
    profileId: str
    decisionType: str
    authorityLevel: str
    approvalRule: str
    escalationRule: str
    delegationRule: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionRightConflictRead(BaseModel):
    id: str
    profileId: str
    authorityA: str
    authorityB: str
    conflictDescription: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceControlRead(BaseModel):
    id: str
    profileId: str
    controlType: str
    purpose: str
    scope: str
    trigger: str
    owner: str
    policyReference: str
    effectivenessMethod: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceFrictionRead(BaseModel):
    id: str
    profileId: str
    frictionType: str
    cause: str
    affectedDecisions: str
    timeImpactHours: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceGapRead(BaseModel):
    id: str
    profileId: str
    gapType: str
    riskDescription: str
    severity: str
    recommendation: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceOvercontrolRead(BaseModel):
    id: str
    profileId: str
    controlId: str
    overcontrolReason: str
    recommendation: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceLoadRead(BaseModel):
    id: str
    profileId: str
    decisionsCount: int
    approvalsCount: int
    reviewsCount: int
    escalationsCount: int
    exceptionsCount: int
    timeSpentHours: float
    timeWindow: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceBottleneckRead(BaseModel):
    id: str
    profileId: str
    bottleneckType: str
    cause: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDelegationCandidateRead(BaseModel):
    id: str
    profileId: str
    decisionType: str
    rationale: str
    safetyScore: float
    policyCoverage: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationEscalationPatternRead(BaseModel):
    id: str
    profileId: str
    patternDescription: str
    frequency: int
    impact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceExceptionRead(BaseModel):
    id: str
    profileId: str
    reason: str
    scope: str
    durationDays: int
    approver: str
    risk: str
    expiresAt: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceChangeRequestRead(BaseModel):
    id: str
    profileId: str
    changeType: str
    description: str
    proposedState: str
    simulationResultsJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceDriftRead(BaseModel):
    id: str
    profileId: str
    driftType: str
    approvedSummary: str
    actualSummary: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceReviewRead(BaseModel):
    id: str
    profileId: str
    cadence: str
    triggerReason: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGovernanceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
