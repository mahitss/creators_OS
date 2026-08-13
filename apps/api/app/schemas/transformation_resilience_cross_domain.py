from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceCrossDomainIntelligenceDomainRead(BaseModel):
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

class TransformationResilienceCrossDomainResilienceGraphRead(BaseModel):
    id: str
    domainId: str
    totalNodesCount: int
    totalEdgesCount: int
    status: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainGraphNodeRead(BaseModel):
    id: str
    nodeType: str
    nodeId: str
    domain: str
    severity: str
    state: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainGraphEdgeRead(BaseModel):
    id: str
    sourceNodeId: str
    targetNodeId: str
    relationship: str
    confidence: float
    evidenceCount: int
    evidenceQuality: float
    lastValidatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainPropagationPathRead(BaseModel):
    id: str
    source: str
    target: str
    intermediateNodesJson: List[str]
    relationshipsJson: List[str]
    depth: int
    confidence: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainPropagationRead(BaseModel):
    id: str
    sourceCondition: str
    propagationType: str
    affectedObjectsJson: List[str]
    propagationPathJson: List[str]
    estimatedImpact: str
    confidence: float
    uncertainty: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainSystemicExposureRead(BaseModel):
    id: str
    title: str
    affectedDomainsJson: List[str]
    affectedTransformationsJson: List[str]
    affectedPlansJson: List[str]
    sharedDependenciesJson: List[str]
    sharedResourcesJson: List[str]
    severity: str
    exposureState: str
    confidence: float
    uncertainty: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainConcentrationRead(BaseModel):
    id: str
    concentrationType: str
    objectId: str
    description: str
    concentrationScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainSinglePointExposureRead(BaseModel):
    id: str
    componentType: str
    componentId: str
    affectedSystemsJson: List[str]
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainFragilityRead(BaseModel):
    id: str
    objectId: str
    dependentsJson: List[str]
    alternativePathsCount: int
    recoveryOptionsJson: List[str]
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainRedundancyRead(BaseModel):
    id: str
    objectId: str
    alternativeEvidenceJson: List[str]
    alternativeDependenciesJson: List[str]
    alternativeResourcesJson: List[str]
    alternativeExecutionPathsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainResilienceGapRead(BaseModel):
    id: str
    gapType: str
    description: str
    severity: str
    recommendedMitigation: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainCompoundRiskRead(BaseModel):
    id: str
    title: str
    contributingConditionsJson: List[str]
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainCompoundConditionRead(BaseModel):
    id: str
    compoundRiskId: str
    conditionDescription: str
    relationship: str
    threshold: float
    confidence: float
    evidenceRef: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainCascadeProjectionRead(BaseModel):
    id: str
    sourceId: str
    pathJson: List[str]
    affectedDomainsJson: List[str]
    depth: int
    severity: str
    confidence: float
    interventionPointsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainCascadeBreakpointRead(BaseModel):
    id: str
    cascadeId: str
    locationNodeId: str
    optionType: str
    expectedEffect: str
    confidence: float
    cost: str
    reversibility: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainSecondOrderEffectRead(BaseModel):
    id: str
    interventionId: str
    affectedObjectId: str
    effectDescription: str
    direction: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainInterventionCollisionRead(BaseModel):
    id: str
    interventionAId: str
    interventionBId: str
    collisionType: str
    affectedDomainsJson: List[str]
    resolution: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainGovernanceContextRead(BaseModel):
    id: str
    requiredAuthoritiesJson: List[str]
    decisionDependenciesJson: List[str]
    approvalDependenciesJson: List[str]
    policyEvaluationRef: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainSystemicWarningRead(BaseModel):
    id: str
    triggerReason: str
    status: str
    severity: str
    evidenceCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceCrossDomainQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
