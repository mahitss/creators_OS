from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceAdaptiveKnowledgeAssuranceDomainRead(BaseModel):
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

class TransformationResilienceKnowledgeAssurancePlanBaselineRead(BaseModel):
    id: str
    planId: str
    planVersion: str
    assumptionsJson: List[str]
    risksJson: List[str]
    capacityJson: Dict[str, Any]
    sequenceJson: List[str]
    optionsJson: List[Dict[str, Any]]
    residualRisk: float
    approvalState: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceChangeSignalRead(BaseModel):
    id: str
    source: str
    changeType: str
    significance: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceChangeDetectionRead(BaseModel):
    id: str
    signalId: str
    planId: str
    affectedAssumptionsJson: List[str]
    affectedRisksJson: List[str]
    affectedActionsJson: List[str]
    confidence: float
    detectedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceAssumptionImpactRead(BaseModel):
    id: str
    planId: str
    assumption: str
    previousState: str
    currentState: str
    impact: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanImpactRead(BaseModel):
    id: str
    planId: str
    riskImpact: str
    sequenceImpact: str
    capacityImpact: str
    coverageImpact: str
    residualRiskImpact: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanHealthRead(BaseModel):
    id: str
    planId: str
    riskAlignment: float
    evidenceAlignment: float
    capacityAlignment: float
    sequenceAlignment: float
    deadlineAlignment: float
    assumptionAlignment: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanStalenessRead(BaseModel):
    id: str
    planId: str
    status: str
    outdatedAssumptionsJson: List[str]
    outdatedEvidenceJson: List[str]
    changedDependenciesJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReplanTriggerRead(BaseModel):
    id: str
    planId: str
    triggerType: str
    description: str
    status: str
    triggeredAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReplanRecommendationRead(BaseModel):
    id: str
    planId: str
    label: str
    recommendedOption: str
    reason: str
    tradeoffs: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanVersionRead(BaseModel):
    id: str
    planId: str
    versionNumber: str
    parentVersion: str
    changeSummary: str
    reason: str
    approvalState: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanDiffRead(BaseModel):
    id: str
    planId: str
    fromVersion: str
    toVersion: str
    addedRisksJson: List[str]
    removedRisksJson: List[str]
    reorderedActionsJson: List[str]
    changedAssumptionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReplanQueueRead(BaseModel):
    id: str
    planId: str
    triggerType: str
    severity: str
    priority: int
    recommendedAction: str
    approvalRequirement: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceEmergencyReplanRead(BaseModel):
    id: str
    planId: str
    triggerReason: str
    status: str
    warRoomSessionId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCrossPlanImpactRead(BaseModel):
    id: str
    sourcePlanId: str
    affectedPlanId: str
    impactDescription: str
    severity: str
    recommendedAction: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePortfolioDriftRead(BaseModel):
    id: str
    riskDrift: float
    capacityDrift: float
    evidenceDrift: float
    dependencyDrift: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceControlQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
