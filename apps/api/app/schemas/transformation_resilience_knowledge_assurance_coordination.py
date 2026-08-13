from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceKnowledgeAssuranceCoordinationDomainRead(BaseModel):
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

class TransformationResilienceKnowledgeAssuranceActivePlanSetRead(BaseModel):
    id: str
    domainId: str
    activePlanIdsJson: List[str]
    activeVersionsJson: Dict[str, Any]
    ownersJson: Dict[str, Any]
    deadlinesJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanRelationshipRead(BaseModel):
    id: str
    sourcePlanId: str
    targetPlanId: str
    relationshipType: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResourceRead(BaseModel):
    id: str
    resourceType: str
    name: str
    totalCapacity: float
    unit: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResourceDemandRead(BaseModel):
    id: str
    planId: str
    resourceId: str
    requiredAmount: float
    timeWindow: str
    criticality: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResourceAvailabilityRead(BaseModel):
    id: str
    resourceId: str
    availableCapacity: float
    timeWindow: str
    source: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResourceContentionRead(BaseModel):
    id: str
    resourceId: str
    competingPlanIdsJson: List[str]
    demandDeficit: float
    severity: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceEvidenceContentionRead(BaseModel):
    id: str
    evidenceSourceId: str
    competingPlanIdsJson: List[str]
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceReviewContentionRead(BaseModel):
    id: str
    reviewDomain: str
    competingPlanIdsJson: List[str]
    reviewCapacityDeficit: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceSimulationContentionRead(BaseModel):
    id: str
    simulationCluster: str
    competingPlanIdsJson: List[str]
    computeDeficitPct: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceDeadlineCollisionRead(BaseModel):
    id: str
    collidingPlanIdsJson: List[str]
    sharedDeadline: str
    impactDescription: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationOptionRead(BaseModel):
    id: str
    optionType: str
    title: str
    coverage: float
    riskReduction: float
    effort: str
    timeEst: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationRecommendationRead(BaseModel):
    id: str
    coordinationPlanId: str
    label: str
    recommendedOption: str
    reason: str
    tradeoffs: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationPlanRead(BaseModel):
    id: str
    objective: str
    coordinatingPlanIdsJson: List[str]
    relationshipsJson: List[Dict[str, Any]]
    resourceAssumptions: str
    sequenceJson: List[str]
    residualConflicts: str
    owner: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationActionRead(BaseModel):
    id: str
    coordinationPlanId: str
    actionType: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationConflictRead(BaseModel):
    id: str
    conflictType: str
    description: str
    severity: str
    selectedResolution: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationCascadeRead(BaseModel):
    id: str
    sourcePlanId: str
    affectedPlanId: str
    depth: int
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationDriftRead(BaseModel):
    id: str
    triggerReason: str
    impact: str
    recommendedResponse: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceBottleneckRead(BaseModel):
    id: str
    bottleneckType: str
    description: str
    affectedPlanIdsJson: List[str]
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationEffectivenessRead(BaseModel):
    id: str
    coordinationPlanId: str
    contentionReduction: float
    riskReduction: float
    coverageImprovement: float
    timeliness: float
    capacityEfficiency: float
    coordinationStability: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationFailureRead(BaseModel):
    id: str
    coordinationPlanId: str
    failureType: str
    reason: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCoordinationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
