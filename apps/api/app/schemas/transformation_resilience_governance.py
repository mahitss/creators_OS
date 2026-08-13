from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceGovernanceDomainRead(BaseModel):
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

class TransformationResilienceGovernanceControlRead(BaseModel):
    id: str
    controlCode: str
    title: str
    category: str
    owner: str
    responsibility: str
    reviewFrequency: str
    lastReview: str
    nextReview: str
    status: str
    validationMethod: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceControlRequirementRead(BaseModel):
    id: str
    controlId: str
    requirementText: str
    source: str
    severity: str
    mandatory: bool
    validationMethod: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceControlEvidenceRead(BaseModel):
    id: str
    controlId: str
    evidenceType: str
    source: str
    timestamp: str
    freshnessDays: int
    integrityHash: str
    confidence: float
    reviewStatus: str
    evidenceDataJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceEvidenceValidityRead(BaseModel):
    id: str
    evidenceId: str
    status: str
    expiresAt: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceControlTestRead(BaseModel):
    id: str
    controlId: str
    testType: str
    version: str
    environment: str
    startTime: str
    endTime: str
    result: str
    evidenceId: Optional[str] = None
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceControlAttestationRead(BaseModel):
    id: str
    controlId: str
    evidenceId: str
    attestor: str
    timestamp: str
    validUntil: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceAssuranceClaimRead(BaseModel):
    id: str
    claimText: str
    controlId: str
    evidenceId: Optional[str] = None
    status: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceAssurancePacketRead(BaseModel):
    id: str
    version: str
    packetHash: str
    claimsJson: List[Dict[str, Any]]
    controlsJson: List[Dict[str, Any]]
    testsJson: List[Dict[str, Any]]
    evidenceJson: List[Dict[str, Any]]
    attestationsJson: List[Dict[str, Any]]
    exceptionsJson: List[Dict[str, Any]]
    knownLimitationsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceProductionReadinessAssessmentRead(BaseModel):
    id: str
    verdict: str
    assessor: str
    securityScore: float
    privacyScore: float
    reliabilityScore: float
    resilienceScore: float
    observabilityScore: float
    governanceScore: float
    dataIntegrityScore: float
    modelIntegrityScore: float
    simulationSafetyScore: float
    operationalReadinessScore: float
    summary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceReadinessCriterionRead(BaseModel):
    id: str
    assessmentId: str
    requirement: str
    evidenceId: str
    testId: str
    owner: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceReadinessBlockerRead(BaseModel):
    id: str
    assessmentId: str
    blockerType: str
    severity: str
    description: str
    remediationRequired: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceExceptionRead(BaseModel):
    id: str
    controlId: str
    reason: str
    riskLevel: str
    owner: str
    approvalAuthority: str
    expirationDate: str
    mitigationControlsJson: List[str]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceRiskAcceptanceRead(BaseModel):
    id: str
    riskDescription: str
    impactScore: float
    rationale: str
    owner: str
    approvalAuthority: str
    expiration: str
    reviewDate: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceFindingRead(BaseModel):
    id: str
    findingType: str
    title: str
    description: str
    severity: str
    controlId: Optional[str] = None
    owner: str
    deadline: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceRemediationRead(BaseModel):
    id: str
    controlId: str
    findingId: str
    actionPlan: str
    owner: str
    deadline: str
    status: str
    evidenceId: Optional[str] = None
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceAuditReadinessRead(BaseModel):
    id: str
    auditScope: str
    evidenceAvailabilityPct: float
    controlCoveragePct: float
    openFindingsCount: int
    exceptionsCount: int
    attestationsCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceReleaseAssessmentRead(BaseModel):
    id: str
    releaseTag: str
    gateStatus: str
    criticalTestsPassed: bool
    securityTestsPassed: bool
    privacyTestsPassed: bool
    tenantIsolationPassed: bool
    auditPassed: bool
    rollbackValidated: bool
    observabilityActive: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceRecoveryReadinessRead(BaseModel):
    id: str
    backupEvidenceId: str
    restoreEvidenceId: str
    failoverEvidenceId: str
    recoveryTimeHours: float
    recoveryPointMinutes: float
    dataIntegrityValidated: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGovernanceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
