from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceAssuranceInterventionDomainRead(BaseModel):
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

class TransformationResilienceAssuranceInterventionCaseRead(BaseModel):
    id: str
    warningId: str
    forecastId: str
    riskId: str
    affectedPlansJson: List[str]
    affectedTransformationsJson: List[str]
    severity: str
    horizon: str
    interventionWindow: str
    status: str
    owner: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionTriggerRead(BaseModel):
    id: str
    type: str
    signalId: str
    evidenceDescription: str
    confidence: float
    freshness: float
    thresholdValue: float
    validationStatus: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionOptionRead(BaseModel):
    id: str
    caseId: str
    optionType: str
    title: str
    reversibility: str
    riskReduction: float
    coverage: float
    effort: str
    capacityRequired: str
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRollbackPlanRead(BaseModel):
    id: str
    optionId: str
    rollbackTrigger: str
    rollbackActionsJson: List[str]
    authorizationRequired: str
    expectedRecoveryTimeHours: int
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceContingencyPlanRead(BaseModel):
    id: str
    caseId: str
    activationCriteria: str
    actionsJson: List[str]
    ownersJson: List[str]
    capacityReserved: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceContingencyReadinessRead(BaseModel):
    id: str
    contingencyId: str
    evidenceReadiness: str
    resourceReadiness: str
    dependencyReadiness: str
    executionReadiness: str
    governanceReadiness: str
    overallStatus: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionRecommendationRead(BaseModel):
    id: str
    caseId: str
    label: str
    recommendedOptionId: str
    reason: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionDecisionPacketRead(BaseModel):
    id: str
    caseId: str
    governanceRequirement: str
    packetSummary: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionPlanRead(BaseModel):
    id: str
    caseId: str
    objective: str
    selectedOptionId: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionActionRead(BaseModel):
    id: str
    planId: str
    actionType: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionExpirationRead(BaseModel):
    id: str
    caseId: str
    reason: str
    expiresAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionConflictRead(BaseModel):
    id: str
    caseId: str
    conflictingPlanId: str
    severity: str
    conflictSummary: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionCascadeRead(BaseModel):
    id: str
    sourceActionId: str
    affectedPlanId: str
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionImpactRead(BaseModel):
    id: str
    caseId: str
    riskReduction: float
    coverageChange: float
    capacityImpact: str
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionEffectivenessRead(BaseModel):
    id: str
    caseId: str
    leadTimeDays: float
    riskReduction: float
    coveragePreservation: float
    rollbackSuccess: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionFailureRead(BaseModel):
    id: str
    caseId: str
    failureType: str
    description: str
    cause: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionLessonRead(BaseModel):
    id: str
    lessonType: str
    title: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
