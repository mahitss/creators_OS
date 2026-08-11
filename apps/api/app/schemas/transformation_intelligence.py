from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationGraphNodeRead(BaseModel):
    id: str
    organizationId: str
    entityType: str
    entityId: str
    label: str
    status: str
    source: str
    confidence: float
    freshness: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGraphEdgeRead(BaseModel):
    id: str
    organizationId: str
    fromNodeId: str
    toNodeId: str
    relationshipType: str
    strength: float
    confidence: float
    source: str
    observedAt: str
    expiresAt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TransformationGraphProvenanceRead(BaseModel):
    id: str
    edgeId: str
    sourceSystem: str
    method: str
    evidenceJson: Dict[str, Any]
    confidence: float
    classifiedAs: str

    model_config = ConfigDict(from_attributes=True)

class TransformationImpactMapRead(BaseModel):
    id: str
    transformationId: str
    strategyImpactJson: Dict[str, Any]
    capabilityImpactJson: Dict[str, Any]
    processImpactJson: Dict[str, Any]
    unitImpactJson: Dict[str, Any]
    systemImpactJson: Dict[str, Any]
    downstreamTransformationIdsJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class CrossTransformationImpactRead(BaseModel):
    id: str
    sourceTransformationId: str
    targetTransformationId: str
    impactType: str
    severity: str
    confidence: float
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationCapabilityOverlapRead(BaseModel):
    id: str
    capabilityId: str
    transformationIdsJson: List[Any]
    capacityDemandJson: Dict[str, Any]
    riskScore: float
    conflictFlag: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationAssumptionClusterRead(BaseModel):
    id: str
    sharedAssumption: str
    transformationIdsJson: List[Any]
    exposureLevel: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationScenarioExposureRead(BaseModel):
    id: str
    scenarioId: str
    transformationIdsJson: List[Any]
    vulnerabilityScore: float
    impactDesc: str

    model_config = ConfigDict(from_attributes=True)

class TransformationBenefitGraphRead(BaseModel):
    id: str
    transformationIdsJson: List[Any]
    claimedBenefit: str
    overlapFlag: bool
    outcomeConnection: str

    model_config = ConfigDict(from_attributes=True)

class TransformationConflictGraphRead(BaseModel):
    id: str
    transformationAId: str
    transformationBId: str
    conflictDomain: str
    severity: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationDecisionPropagationRead(BaseModel):
    id: str
    decisionId: str
    affectedTransformationIdsJson: List[Any]
    impactMode: str
    evidenceJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationRiskPropagationRead(BaseModel):
    id: str
    sourceRiskId: str
    affectedTransformationIdsJson: List[Any]
    downstreamEffect: str
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationPatternRead(BaseModel):
    id: str
    patternName: str
    patternType: str
    supportingEvidenceJson: Dict[str, Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationAnalogyRead(BaseModel):
    id: str
    currentTransformationId: str
    historicalTransformationId: str
    similarityScore: float
    keyDifferencesJson: List[Any]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationComplexityHotspotRead(BaseModel):
    id: str
    hotspotName: str
    convergingTransformationIdsJson: List[Any]
    hotspotDomain: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGraphSnapshotRead(BaseModel):
    id: str
    organizationId: str
    snapshotLabel: str
    nodesCount: int
    edgesCount: int
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationGraphDiffRead(BaseModel):
    id: str
    snapshotAId: str
    snapshotBId: str
    addedEdgesJson: List[Any]
    removedEdgesJson: List[Any]
    newConflictsJson: List[Any]
    resolvedConflictsJson: List[Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
