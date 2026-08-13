from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceAssuranceCommandDomainRead(BaseModel):
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

class TransformationResilienceAssuranceOperationalPictureRead(BaseModel):
    id: str
    commandDomainId: str
    status: str
    activeRisksCount: int
    activeWarningsCount: int
    activeConflictsCount: int
    activeInterventionsCount: int
    blockedActionsCount: int
    criticalDependenciesCount: int
    capacityPressure: str
    decisionBacklogCount: int
    approvalBacklogCount: int
    residualExposure: float
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandEventRead(BaseModel):
    id: str
    eventType: str
    sourceDomain: str
    severity: str
    timestamp: str
    affectedObjectsJson: List[str]
    status: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandPriorityRead(BaseModel):
    id: str
    objectId: str
    objectType: str
    severity: str
    urgency: str
    impact: str
    interventionWindow: str
    confidence: float
    decisionDependency: str
    rankScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCriticalObjectRead(BaseModel):
    id: str
    objectType: str
    objectId: str
    title: str
    severity: str
    owner: str
    deadline: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandAttentionRead(BaseModel):
    id: str
    objectId: str
    reason: str
    urgency: str
    owner: str
    deadline: str
    requiredAction: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceExecutiveDecisionQueueRead(BaseModel):
    id: str
    decisionId: str
    title: str
    impact: str
    deadline: str
    authorityRequired: str
    status: str
    blockingObjectsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceDecisionBottleneckRead(BaseModel):
    id: str
    decisionId: str
    bottleneckType: str
    description: str
    impact: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceApprovalBottleneckRead(BaseModel):
    id: str
    approvalId: str
    requiredAuthority: str
    ageDays: float
    impact: str
    blockingActionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionBottleneckRead(BaseModel):
    id: str
    interventionId: str
    bottleneckCause: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceDependencyHotspotRead(BaseModel):
    id: str
    dependencyId: str
    name: str
    affectedPlansCount: int
    affectedRisksCount: int
    affectedConflictsCount: int
    affectedInterventionsCount: int
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceResourcePressureRead(BaseModel):
    id: str
    resourceCategory: str
    pressureLevel: str
    affectedPlansJson: List[str]
    affectedInterventionsJson: List[str]
    trend: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceKnowledgeHealthProjectionRead(BaseModel):
    id: str
    evidenceFreshness: float
    coverage: float
    validationRate: float
    reviewBacklogCount: int
    stalenessPct: float
    uncertaintyScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssurancePlanHealthProjectionRead(BaseModel):
    id: str
    planId: str
    planHealth: str
    staleness: str
    dependencyHealth: str
    riskExposure: float
    executionStatus: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceTransformationHealthProjectionRead(BaseModel):
    id: str
    transformationName: str
    riskScore: float
    coverageScore: float
    executionHealth: str
    dependencyHealth: str
    activeInterventionsCount: int
    residualExposure: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCrossDomainHeatmapRead(BaseModel):
    id: str
    domainName: str
    riskLevel: float
    knowledgeLevel: float
    capacityLevel: float
    dependencyLevel: float
    deadlineLevel: float
    conflictLevel: float
    interventionLevel: float
    decisionLevel: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceOperationalSceneRead(BaseModel):
    id: str
    title: str
    description: str
    status: str
    containedObjectsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceSceneTimelineRead(BaseModel):
    id: str
    sceneId: str
    stage: str
    eventDescription: str
    timestamp: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceSceneRelationshipRead(BaseModel):
    id: str
    sceneId: str
    sourceObjectId: str
    targetObjectId: str
    relationshipType: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandSnapshotRead(BaseModel):
    id: str
    label: str
    stateDataJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandSnapshotDiffRead(BaseModel):
    id: str
    previousSnapshotId: str
    currentSnapshotId: str
    newRisksJson: List[str]
    resolvedRisksJson: List[str]
    newWarningsJson: List[str]
    resolvedWarningsJson: List[str]
    newConflictsJson: List[str]
    resolvedConflictsJson: List[str]
    newInterventionsJson: List[str]
    completedInterventionsJson: List[str]
    decisionChangesJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandEscalationRead(BaseModel):
    id: str
    triggerReason: str
    status: str
    owner: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceOperationsHandoffRead(BaseModel):
    id: str
    outgoingOwner: str
    incomingOwner: str
    currentStateSummary: str
    openActionsJson: List[str]
    risksJson: List[str]
    decisionsJson: List[str]
    dependenciesJson: List[str]
    nextReview: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandProjectionHealthRead(BaseModel):
    id: str
    lagSeconds: float
    errorsCount: int
    lastProcessedEventId: str
    rebuildStatus: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceCommandQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
