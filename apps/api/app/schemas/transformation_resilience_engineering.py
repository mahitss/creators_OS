from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceEngineeringDomainRead(BaseModel):
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

class TransformationResilienceBaselineRead(BaseModel):
    id: str
    domainId: str
    robustnessScore: float
    redundancyScore: float
    recoverabilityScore: float
    adaptabilityScore: float
    optionalityScore: float
    observabilityScore: float
    governabilityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationFailureModeRead(BaseModel):
    id: str
    domainId: str
    failureType: str
    frequency: int
    severity: str
    recoveryTimeHours: float
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationFailureModeAnalysisRead(BaseModel):
    id: str
    failureModeId: str
    triggerDescription: str
    conditionsJson: Dict[str, Any]
    propagationPathJson: List[str]
    recoveryBehavior: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSystemicWeaknessRead(BaseModel):
    id: str
    domainId: str
    affectedTransformationsJson: List[str]
    affectedCapabilitiesJson: List[str]
    description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSinglePointOfFailureRead(BaseModel):
    id: str
    domainId: str
    entityType: str
    entityName: str
    criticalityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRedundancyOptionRead(BaseModel):
    id: str
    domainId: str
    redundancyType: str
    title: str
    description: str
    costEstimate: float
    riskReductionScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationSubstitutionOptionRead(BaseModel):
    id: str
    domainId: str
    substitutionType: str
    primaryEntity: str
    substituteEntity: str
    feasibilityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationCapacityBufferOptionRead(BaseModel):
    id: str
    domainId: str
    requiredBufferFte: float
    costEstimate: float
    activationCondition: str

    model_config = ConfigDict(from_attributes=True)

class TransformationOptionalityAnalysisRead(BaseModel):
    id: str
    domainId: str
    pathCount: int
    dimensionScoresJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInvestmentCandidateRead(BaseModel):
    id: str
    domainId: str
    problemStatement: str
    improvementTitle: str
    investmentAmount: float
    expectedBenefit: str
    riskReductionPct: float
    uncertaintyLevel: str
    priority: str

    model_config = ConfigDict(from_attributes=True)

class TransformationCascadingFailureAnalysisRead(BaseModel):
    id: str
    domainId: str
    initialTrigger: str
    propagationGraphJson: Dict[str, Any]
    uncertaintyLabel: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceInterventionRead(BaseModel):
    id: str
    domainId: str
    interventionType: str
    title: str
    description: str
    priorityScore: float
    recommendationOnly: bool

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceRoadmapRead(BaseModel):
    id: str
    domainId: str
    milestonesJson: List[str]
    investmentTotal: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceComparisonRead(BaseModel):
    id: str
    domainId: str
    baselineScoresJson: Dict[str, Any]
    improvedScoresJson: Dict[str, Any]
    actualScoresJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceLessonRead(BaseModel):
    id: str
    domainId: str
    failureTrigger: str
    observedBehavior: str
    lessonText: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResiliencePatternRead(BaseModel):
    id: str
    domainId: str
    patternName: str
    patternType: str
    description: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceWarningRead(BaseModel):
    id: str
    domainId: str
    warningSignal: str
    severity: str
    metricsJson: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
