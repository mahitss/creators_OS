from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class OutcomeCreate(BaseModel):
    name: str
    description: str
    owner: str
    target: str
    currentState: str
    workspaceId: str = "ws_default"

class OutcomeRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    owner: str
    status: str
    target: str
    currentState: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class OperatingChangeEventRead(BaseModel):
    id: str
    organizationId: str
    changeType: str
    targetRef: str
    impactSummary: str
    confidence: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class OperatingScenarioCreate(BaseModel):
    name: str
    assumptionsJson: Dict[str, Any] = {}

class OperatingScenarioRead(BaseModel):
    id: str
    organizationId: str
    name: str
    assumptionsJson: Dict[str, Any]
    affectedNodesJson: List[str]
    expectedImpactJson: Dict[str, Any]
    confidencePct: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class OperatingRiskRead(BaseModel):
    id: str
    organizationId: str
    dimension: str
    title: str
    description: str
    sourceRef: str
    evidenceJson: Dict[str, Any]
    status: str
    mitigationRecommendationsJson: List[str]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CapabilityGapRead(BaseModel):
    id: str
    organizationId: str
    capabilityId: str
    requiredByRef: str
    gapClassification: str
    impactSummary: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class OperatingBottleneckRead(BaseModel):
    id: str
    organizationId: str
    blockerType: str
    rootDependencyRef: str
    affectedWorkJson: List[str]
    durationHours: float
    evidenceJson: Dict[str, Any]
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class OperatingDependencyRead(BaseModel):
    id: str
    organizationId: str
    sourceId: str
    sourceType: str
    targetId: str
    targetType: str
    relationshipType: str
    health: str
    isCriticalPath: bool
    freshnessPolicyHours: int
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class GraphValidationIssueRead(BaseModel):
    id: str
    organizationId: str
    issueType: str
    nodeRef: str
    suggestedRepair: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class GraphQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
