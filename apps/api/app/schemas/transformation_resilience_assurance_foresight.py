from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceAssuranceForesightDomainRead(BaseModel):
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

class TransformationResilienceAssuranceForesightSignalRead(BaseModel):
    id: str
    source: str
    type: str
    description: str
    sourceQuality: float
    freshness: float
    consistency: float
    confidence: float
    coverage: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceLeadingIndicatorRead(BaseModel):
    id: str
    name: str
    definition: str
    signalSourcesJson: List[str]
    direction: str
    threshold: float
    warningLevel: float
    criticalLevel: float
    horizon: str
    state: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssurancePressureSignalRead(BaseModel):
    id: str
    riskPressure: float
    capacityPressure: float
    deadlinePressure: float
    evidencePressure: float
    dependencyPressure: float
    governancePressure: float
    conflictPressure: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceEmergingRiskRead(BaseModel):
    id: str
    riskName: str
    signalId: str
    affectedPlansJson: List[str]
    affectedTransformationsJson: List[str]
    horizon: str
    confidence: float
    uncertainty: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForecastRead(BaseModel):
    id: str
    target: str
    horizon: str
    baselineValue: float
    expectedStateValue: float
    lowerBound: float
    centralEstimate: float
    upperBound: float
    confidence: float
    uncertainty: float
    assumptionsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForecastScenarioRead(BaseModel):
    id: str
    forecastId: str
    scenarioType: str
    riskScore: float
    coverageScore: float
    capacityScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForecastComparisonRead(BaseModel):
    id: str
    forecastId: str
    scenarioA: str
    scenarioB: str
    comparisonSummary: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceEarlyWarningRead(BaseModel):
    id: str
    signalId: str
    severity: str
    horizon: str
    affectedPlansJson: List[str]
    recommendedAttention: str
    confidence: float
    status: str
    expiresAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceInterventionWindowRead(BaseModel):
    id: str
    earlyWarningId: str
    opening: str
    closing: str
    estimatedDurationDays: int
    confidence: float
    constraints: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssurancePreventiveOptionRead(BaseModel):
    id: str
    optionType: str
    title: str
    riskReduction: float
    coverage: float
    effort: str
    reversibility: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightRecommendationRead(BaseModel):
    id: str
    label: str
    recommendedOption: str
    reason: str
    forecastId: str
    confidence: float
    uncertainty: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForecastInvalidationConditionRead(BaseModel):
    id: str
    forecastId: str
    conditionDescription: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightQualityRead(BaseModel):
    id: str
    signalQuality: float
    forecastAccuracy: float
    leadTimeDays: float
    falsePositiveRate: float
    falseNegativeRate: float
    interventionUsefulness: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceFalsePositiveRead(BaseModel):
    id: str
    earlyWarningId: str
    expectedEvent: str
    actualResult: str
    cause: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceFalseNegativeRead(BaseModel):
    id: str
    missedCondition: str
    laterMaterialization: str
    cause: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightDriftRead(BaseModel):
    id: str
    driftType: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceContextShiftRead(BaseModel):
    id: str
    dimension: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceRegimeChangeRead(BaseModel):
    id: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightClusterRead(BaseModel):
    id: str
    clusterName: str
    signalIdsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceSystemicEarlyWarningRead(BaseModel):
    id: str
    patternDescription: str
    severity: str
    affectedTransformationsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightCascadeRead(BaseModel):
    id: str
    sourceSignalId: str
    affectedSignalId: str
    depth: int
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightEscalationRead(BaseModel):
    id: str
    earlyWarningId: str
    triggerReason: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightLessonRead(BaseModel):
    id: str
    lessonType: str
    title: str
    description: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceAssuranceForesightQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
