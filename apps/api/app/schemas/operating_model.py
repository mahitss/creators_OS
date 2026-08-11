from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class OperatingModelRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    name: str
    description: str
    version: str
    status: str
    owner: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class OrganizationalUnitRead(BaseModel):
    id: str
    organizationId: str
    parentId: Optional[str]
    name: str
    type: str
    purpose: str
    scope: str
    responsibilities: str
    status: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class DecisionRightRead(BaseModel):
    id: str
    modelId: str
    decisionType: str
    scope: str
    authorityLevel: str
    constraintsJson: Dict[str, Any]
    escalationPath: str

    model_config = ConfigDict(from_attributes=True)

class DecisionRightsMatrixRead(BaseModel):
    id: str
    decisionRightId: str
    unitId: str
    roleType: str

    model_config = ConfigDict(from_attributes=True)

class OperatingProcessRead(BaseModel):
    id: str
    name: str
    purpose: str
    ownerUnitId: str
    inputsJson: List[Any]
    outputsJson: List[Any]
    systemsJson: List[Any]
    status: str

    model_config = ConfigDict(from_attributes=True)

class ProcessHandoffRead(BaseModel):
    id: str
    processId: str
    fromUnitId: str
    toUnitId: str
    artifactName: str
    waitTimeHours: float
    failureRate: float
    frictionFlag: bool

    model_config = ConfigDict(from_attributes=True)

class OperatingModelGapRead(BaseModel):
    id: str
    modelId: str
    gapType: str
    description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)

class OperatingModelChangeProposalRead(BaseModel):
    id: str
    modelId: str
    problemSummary: str
    evidenceJson: Dict[str, Any]
    optionsJson: List[Any]
    tradeoffsJson: Dict[str, Any]
    expectedEffect: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class OperatingModelQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float
