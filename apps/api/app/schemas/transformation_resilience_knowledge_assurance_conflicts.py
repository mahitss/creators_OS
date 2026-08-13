from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceKnowledgeAssuranceConflictIntelligenceDomainRead(BaseModel):
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

class TransformationResilienceKnowledgeAssuranceConflictCaseRead(BaseModel):
    id: str
    conflictType: str
    severity: str
    status: str
    source: str
    affectedPlanIdsJson: List[str]
    affectedResourcesJson: List[str]
    affectedDependenciesJson: List[str]
    affectedDeadlinesJson: List[str]
    detectedAt: str
    owner: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictImpactRead(BaseModel):
    id: str
    conflictCaseId: str
    riskExposure: float
    coverageLoss: float
    deadlineExposureDays: int
    capacityExposurePct: float
    dependencyExposure: str
    residualUncertainty: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictRootCauseRead(BaseModel):
    id: str
    conflictCaseId: str
    rootCauseCategory: str
    description: str
    frequency: int

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionOptionRead(BaseModel):
    id: str
    conflictCaseId: str
    optionType: str
    title: str
    riskScore: float
    coverageScore: float
    deadlineShiftDays: int
    effort: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictTradeoffRead(BaseModel):
    id: str
    conflictCaseId: str
    dimensionA: str
    dimensionB: str
    tradeoffDescription: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictScenarioResultRead(BaseModel):
    id: str
    conflictCaseId: str
    scenarioType: str
    risk: float
    coverage: float
    residualRisk: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictRecommendationRead(BaseModel):
    id: str
    conflictCaseId: str
    label: str
    recommendedOption: str
    reason: str
    tradeoffs: str
    confidence: float
    unresolvedConcerns: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictDecisionPacketRead(BaseModel):
    id: str
    conflictCaseId: str
    summary: str
    affectedPlansJson: List[str]
    rootCauseDescription: str
    optionsSummaryJson: List[Dict[str, Any]]
    recommendation: str
    residualRisk: float
    requiredAuthority: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionPlanRead(BaseModel):
    id: str
    conflictCaseId: str
    selectedOption: str
    owner: str
    status: str
    rollbackPlan: str
    residualConflicts: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionActionRead(BaseModel):
    id: str
    resolutionPlanId: str
    actionType: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResidualConflictRead(BaseModel):
    id: str
    conflictCaseId: str
    remainingConflict: str
    reason: str
    owner: str
    reviewDate: str
    impact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictCascadeRead(BaseModel):
    id: str
    sourceConflictId: str
    affectedConflictId: str
    depth: int
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictClusterRead(BaseModel):
    id: str
    clusterType: str
    name: str
    conflictIdsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceSystemicConflictRead(BaseModel):
    id: str
    patternDescription: str
    affectedTransformationsJson: List[str]
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictDriftRead(BaseModel):
    id: str
    triggerReason: str
    severityChange: str
    recommendedResponse: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictEscalationRead(BaseModel):
    id: str
    conflictCaseId: str
    triggerReason: str
    status: str
    routedTo: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionEffectivenessRead(BaseModel):
    id: str
    conflictCaseId: str
    riskReduction: float
    coveragePreservation: float
    deadlineRecovery: float
    capacityRelief: float
    dependencyStabilization: float
    uncertaintyReduction: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionFailureRead(BaseModel):
    id: str
    conflictCaseId: str
    failureType: str
    reason: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictResolutionPatternRead(BaseModel):
    id: str
    name: str
    patternDescription: str
    reusabilityScore: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceConflictQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
