from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationWarRoomRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    scope: str
    owner: str
    status: str
    priority: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWarRoomLiveStateRead(BaseModel):
    id: str
    warRoomId: str
    milestonesJson: Dict[str, Any]
    dependenciesJson: Dict[str, Any]
    risksJson: Dict[str, Any]
    benefitsJson: Dict[str, Any]
    capacityJson: Dict[str, Any]
    governanceJson: Dict[str, Any]
    kpisJson: Dict[str, Any]
    sourceVersionsJson: Dict[str, Any]
    lastUpdated: str
    stalenessStatus: str

    model_config = ConfigDict(from_attributes=True)

class TransformationPlanVarianceRead(BaseModel):
    id: str
    warRoomId: str
    varianceType: str
    plannedSummary: str
    actualSummary: str
    forecastSummary: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationDeviationRead(BaseModel):
    id: str
    warRoomId: str
    entity: str
    metric: str
    expectedValue: float
    actualValue: float
    varianceValue: float
    severity: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationRootCauseHypothesisRead(BaseModel):
    id: str
    warRoomId: str
    deviationId: str
    hypothesisText: str
    evidenceJson: Dict[str, Any]
    confidence: float
    alternativeExplanationsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationLiveImpactAssessmentRead(BaseModel):
    id: str
    warRoomId: str
    affectedTransformationsJson: List[str]
    affectedCapabilitiesJson: List[str]
    affectedDependenciesJson: List[str]
    affectedBenefitsJson: List[str]
    affectedRisksJson: List[str]
    strategicImpact: str

    model_config = ConfigDict(from_attributes=True)

class TransformationInterventionOptionRead(BaseModel):
    id: str
    warRoomId: str
    interventionType: str
    title: str
    description: str
    safetyScore: float
    reversibilityScore: float
    blastRadiusJson: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationInterventionRecommendationRead(BaseModel):
    id: str
    warRoomId: str
    recommendedOptionId: str
    evidenceSummary: str
    riskSummary: str
    uncertaintyLevel: str
    alternativesJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationWarRoomEscalationRead(BaseModel):
    id: str
    warRoomId: str
    triggerReason: str
    escalationPath: str
    priority: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResponsePlanRead(BaseModel):
    id: str
    warRoomId: str
    title: str
    signalSummary: str
    assessmentSummary: str
    optionsSummary: str
    decisionSummary: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResponseCheckpointRead(BaseModel):
    id: str
    responsePlanId: str
    checkpointName: str
    expectedState: str
    actualState: str
    nextCheckpoint: str
    owner: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationTrajectoryRead(BaseModel):
    id: str
    warRoomId: str
    metric: str
    trajectoryDataJson: Dict[str, Any]
    timeHorizon: str
    scenario: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationEarlyWarningRead(BaseModel):
    id: str
    warRoomId: str
    signalName: str
    signalStrength: float
    historicalReliability: float
    modelConfidence: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationSituationSummaryRead(BaseModel):
    id: str
    warRoomId: str
    whatChanged: str
    whyItMatters: str
    affectedAreasJson: List[str]
    uncertaintySummary: str
    recommendedReview: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationWarRoomQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
