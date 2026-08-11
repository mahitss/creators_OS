from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationRecoveryDomainRead(BaseModel):
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

class TransformationDisruptionRead(BaseModel):
    id: str
    domainId: str
    disruptionType: str
    source: str
    detectedAt: str
    severity: str
    confidence: float
    scope: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryImpactRead(BaseModel):
    id: str
    domainId: str
    disruptionId: str
    affectedTransformationsJson: List[str]
    affectedCapabilitiesJson: List[str]
    affectedDependenciesJson: List[str]
    affectedBenefitsJson: List[str]
    strategicImpact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryCriticalityRead(BaseModel):
    id: str
    domainId: str
    strategicImportance: float
    dependencyCentrality: float
    benefitExposure: float
    recoveryUrgency: float
    reversibility: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryPriorityRead(BaseModel):
    id: str
    domainId: str
    priorityScore: float
    evidenceSummary: str
    criteriaJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationProtectionTargetRead(BaseModel):
    id: str
    domainId: str
    targetType: str
    targetName: str
    protectionLevel: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryObjectiveRead(BaseModel):
    id: str
    domainId: str
    objectiveName: str
    targetRecoveryTimeHours: float
    estimatedRangeJson: Dict[str, Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryPathRead(BaseModel):
    id: str
    domainId: str
    pathName: str
    actionSequenceJson: List[str]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryOptionRead(BaseModel):
    id: str
    pathId: str
    optionType: str
    title: str
    description: str
    safetyScore: float
    secondaryImpactJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryBottleneckRead(BaseModel):
    id: str
    pathId: str
    bottleneckType: str
    entityName: str
    impactDescription: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryTrajectoryRead(BaseModel):
    id: str
    domainId: str
    pathId: str
    metric: str
    trajectoryDataJson: Dict[str, Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryComparisonRead(BaseModel):
    id: str
    domainId: str
    comparedPathIdsJson: List[str]
    timeScore: float
    riskScore: float
    costScore: float
    reversibilityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryCheckpointRead(BaseModel):
    id: str
    pathId: str
    checkpointName: str
    expectedState: str
    actualState: str
    nextDecisionPoint: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryGateRead(BaseModel):
    id: str
    pathId: str
    gateName: str
    criteriaJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationReturnToNormalPlanRead(BaseModel):
    id: str
    domainId: str
    criteriaSummary: str
    actionSequenceJson: List[str]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryDriftRead(BaseModel):
    id: str
    pathId: str
    expectedAction: str
    actualAction: str
    driftSeverity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryEscalationRead(BaseModel):
    id: str
    domainId: str
    triggerReason: str
    escalationPath: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryCommunicationRead(BaseModel):
    id: str
    domainId: str
    audience: str
    messageText: str
    approvalStatus: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceGapRead(BaseModel):
    id: str
    domainId: str
    gapType: str
    description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceImprovementRead(BaseModel):
    id: str
    domainId: str
    improvementType: str
    title: str
    description: str
    recommendationOnly: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryReadinessRead(BaseModel):
    id: str
    domainId: str
    readinessScore: float
    dimensionScoresJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryDrillRead(BaseModel):
    id: str
    domainId: str
    drillName: str
    scenarioDescription: str
    resultsJson: Dict[str, Any]
    noProductionMutation: bool
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationRecoveryQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
