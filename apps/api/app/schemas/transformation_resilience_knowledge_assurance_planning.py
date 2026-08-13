from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceKnowledgeAssurancePlanningDomainRead(BaseModel):
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

class TransformationResilienceKnowledgeAssurancePortfolioRead(BaseModel):
    id: str
    domainId: str
    riskIdsJson: List[str]
    affectedTransformationsJson: List[str]
    dependenciesJson: List[str]
    decisionDomainsJson: List[str]
    exposureScore: float
    currentCapacity: float
    plannedCapacity: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeSystemicRiskRead(BaseModel):
    id: str
    title: str
    breadth: int
    dependencyCentrality: float
    decisionInfluence: float
    recurrence: int
    uncertainty: float
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRootCauseGroupRead(BaseModel):
    id: str
    rootCauseType: str
    description: str
    frequency: int
    affectedRiskIdsJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationLeverRead(BaseModel):
    id: str
    leverType: str
    title: str
    riskCoverage: float
    confidence: float
    limitations: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCapacityRead(BaseModel):
    id: str
    availableCapacity: float
    requiredCapacity: float
    specialistCapacity: float
    simulationCapacity: float
    reviewCapacity: float
    evidenceCapacity: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceCapacityConstraintRead(BaseModel):
    id: str
    constraintType: str
    description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceDemandRead(BaseModel):
    id: str
    riskWorkload: float
    evidenceWorkload: float
    reviewWorkload: float
    simulationWorkload: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceOptionRead(BaseModel):
    id: str
    optionType: str
    title: str
    coverage: float
    effort: str
    timeEst: str
    riskReduction: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceSequenceRead(BaseModel):
    id: str
    sequenceOrderJson: List[str]
    dependenciesJson: Dict[str, Any]
    deadline: str
    rationale: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceScenarioRead(BaseModel):
    id: str
    scenarioType: str
    coverage: float
    residualRisk: float
    capacityRequired: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanRead(BaseModel):
    id: str
    objective: str
    scope: str
    selectedOptionsJson: List[Dict[str, Any]]
    sequenceId: str
    capacityAllocationJson: Dict[str, Any]
    riskCoverage: float
    residualRisk: float
    assumptions: str
    owner: str
    deadline: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceResidualRiskRead(BaseModel):
    id: str
    planId: str
    unaddressedRisk: str
    reason: str
    severity: str
    owner: str
    reviewDate: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceTradeoffRead(BaseModel):
    id: str
    planId: str
    tradeoffDescription: str
    coverageVsEffort: str
    speedVsUncertainty: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssuranceRecommendationRead(BaseModel):
    id: str
    planId: str
    label: str
    recommendationText: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanVerificationRead(BaseModel):
    id: str
    planId: str
    plannedCoverage: float
    actualCoverage: float
    plannedRiskReduction: float
    actualRiskReduction: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanEffectivenessRead(BaseModel):
    id: str
    planId: str
    riskReduction: float
    coverageImprovement: float
    assuranceQuality: float
    timeliness: float
    capacityEfficiency: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanFailureRead(BaseModel):
    id: str
    planId: str
    failureType: str
    reason: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeAssurancePlanningQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
