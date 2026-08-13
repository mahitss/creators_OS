from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class TransformationResilienceKnowledgeOperationsDomainRead(BaseModel):
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

class TransformationResilienceKnowledgeRiskCaseRead(BaseModel):
    id: str
    knowledgeObjectId: str
    riskType: str
    severity: str
    impact: str
    urgency: str
    owner: str
    status: str
    detectedAt: str
    dueAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRiskQueueRead(BaseModel):
    id: str
    riskCaseId: str
    severity: str
    impact: str
    owner: str
    deadline: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRiskAssignmentRead(BaseModel):
    id: str
    riskCaseId: str
    owner: str
    assignedBy: str
    assignedAt: str
    reason: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationPlanRead(BaseModel):
    id: str
    riskCaseId: str
    objective: str
    owner: str
    deadline: str
    actionsJson: List[Dict[str, Any]]
    successCriteria: str
    rollbackStrategy: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationActionRead(BaseModel):
    id: str
    planId: str
    actionType: str
    title: str
    owner: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeEvidenceTaskRead(BaseModel):
    id: str
    gapId: str
    requestedEvidence: str
    source: str
    owner: str
    deadline: str
    status: str
    quality: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeReviewTaskRead(BaseModel):
    id: str
    riskCaseId: str
    reviewQuestion: str
    reviewer: str
    deadline: str
    status: str
    result: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationVerificationRead(BaseModel):
    id: str
    riskCaseId: str
    riskBefore: Dict[str, Any]
    riskAfter: Dict[str, Any]
    knowledgeHealthBefore: Dict[str, Any]
    knowledgeHealthAfter: Dict[str, Any]
    evidenceQualityBefore: Dict[str, Any]
    evidenceQualityAfter: Dict[str, Any]
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationEffectivenessRead(BaseModel):
    id: str
    riskCaseId: str
    riskReduction: float
    evidenceImprovement: float
    confidenceImprovement: float
    applicabilityImprovement: float
    reuseImprovement: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRiskEscalationRead(BaseModel):
    id: str
    riskCaseId: str
    trigger: str
    severity: str
    owner: str
    status: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationFailureRead(BaseModel):
    id: str
    riskCaseId: str
    failureCategory: str
    reason: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRecurringRiskPatternRead(BaseModel):
    id: str
    patternTitle: str
    frequency: int
    affectedKnowledgeJson: List[str]
    affectedDecisionsJson: List[str]
    confidence: float

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeRemediationQualityRead(BaseModel):
    id: str
    riskCaseId: str
    completeness: float
    evidenceQuality: float
    verificationQuality: float
    timeliness: float
    repeatability: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeOperatingPatternRead(BaseModel):
    id: str
    title: str
    description: str
    confidence: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TransformationResilienceKnowledgeOperationsQueryResultRead(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    evidenceJson: Dict[str, Any]
    confidencePct: float

    model_config = ConfigDict(from_attributes=True)
