from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceDecisionDomainRead(BaseModel):
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

class TransformationResilienceDecisionQuestionRead(BaseModel):
    id: str
    domainId: str
    question: str
    contextDescription: str
    trigger: str
    scope: str
    deadline: str
    decisionOwner: str
    requiredApproversJson: List[str]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionContextRead(BaseModel):
    id: str
    decisionId: str
    portfolioStateJson: Dict[str, Any]
    resilienceStateJson: Dict[str, Any]
    dependenciesJson: List[str]
    capacityJson: Dict[str, Any]
    recoveryJson: Dict[str, Any]
    riskJson: Dict[str, Any]
    assumptionsJson: List[str]
    scenarioVersionsJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionEvidencePackRead(BaseModel):
    id: str
    decisionId: str
    evidenceItemsJson: List[Dict[str, Any]]
    source: str
    freshness: float
    quality: float
    confidence: float
    conflictsJson: List[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionAssumptionRead(BaseModel):
    id: str
    decisionId: str
    assumption: str
    source: str
    confidence: float
    sensitivity: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionOptionRead(BaseModel):
    id: str
    decisionId: str
    optionType: str
    title: str
    benefitsJson: List[str]
    risksJson: List[str]
    cost: float
    capacityImpactJson: Dict[str, Any]
    dependenciesJson: List[str]
    reversibility: str
    optionalityScore: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionTradeoffRead(BaseModel):
    id: str
    decisionId: str
    tradeoffMatrixJson: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionRecommendationRead(BaseModel):
    id: str
    decisionId: str
    recommendedOptionId: str
    supportingEvidenceJson: Dict[str, Any]
    confidence: float
    alternativesJson: List[str]
    limitations: str
    requiredApproval: str
    label: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionRead(BaseModel):
    id: str
    domainId: str
    decisionTitle: str
    owner: str
    status: str
    selectedOptionId: Optional[str] = None
    rationaleSummary: str
    approvalState: str
    deadline: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceDecisionQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
