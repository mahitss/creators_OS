from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class WorkItemCreate(BaseModel):
    title: str
    description: str
    priority: str = Field("medium", description="low, medium, high, urgent")
    assigneeType: str = Field("agent", description="human, agent, team, hybrid")
    assigneeId: Optional[str] = None
    workClassification: str = Field("agent_suitable", description="automatable, agent_suitable, human_required, hybrid, restricted")
    workspaceId: str = "ws_default"
    teamId: Optional[str] = None
    missionId: Optional[str] = None
    parentWorkItemId: Optional[str] = None

class WorkItemRead(BaseModel):
    id: str
    organizationId: str
    workspaceId: str
    teamId: Optional[str] = None
    missionId: Optional[str] = None
    parentWorkItemId: Optional[str] = None
    title: str
    description: str
    priority: str
    status: str
    assigneeType: str
    assigneeId: Optional[str] = None
    workClassification: str
    createdAt: str
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class WorkHandoffCreate(BaseModel):
    workItemId: str
    fromId: str
    fromType: str = Field(..., description="human, agent")
    toId: str
    toType: str = Field(..., description="human, agent")
    reason: str
    contextReferencesJson: Dict[str, Any] = {}
    expectedOutput: str
    deadline: Optional[str] = None

class WorkHandoffRead(BaseModel):
    id: str
    workItemId: str
    fromId: str
    fromType: str
    toId: str
    toType: str
    reason: str
    contextReferencesJson: Dict[str, Any]
    expectedOutput: str
    deadline: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class CollaborationSessionRead(BaseModel):
    id: str
    workItemId: Optional[str] = None
    missionId: Optional[str] = None
    role: str
    userId: Optional[str] = None
    agentId: Optional[str] = None
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CollaborationEscalationCreate(BaseModel):
    workItemId: str
    escalationType: str = Field(..., description="risk, deadline, uncertainty, approval, dependency, capacity, conflict")
    targetRoleOrUser: str
    reason: str
    dueAt: str

class CollaborationEscalationRead(BaseModel):
    id: str
    workItemId: str
    escalationType: str
    targetRoleOrUser: str
    reason: str
    dueAt: str
    resolvedAt: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class ExpertiseProfileRead(BaseModel):
    id: str
    userId: str
    skillsJson: List[str]
    capabilitiesJson: List[str]
    domainsJson: List[str]
    verifiedExperienceJson: Dict[str, Any]
    confidencePct: float
    updatedAt: str

    model_config = ConfigDict(from_attributes=True)

class WorkRoutingRecommendationRead(BaseModel):
    id: str
    workItemId: str
    recommendedExecutorType: str
    recommendedExecutorId: str
    reasonSummary: str
    riskLevel: str
    costEstimate: float
    deadlineImpact: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CollaborationFeedbackCreate(BaseModel):
    feedbackType: str = Field(..., description="correction, approval, rejection, suggestion, rating")
    ratingScore: Optional[float] = None
    comment: str

class CollaborationFeedbackRead(BaseModel):
    id: str
    workItemId: str
    feedbackType: str
    ratingScore: Optional[float] = None
    comment: str
    authorUserId: str
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class CollaborationReviewRead(BaseModel):
    id: str
    workItemId: str
    reviewType: str
    artifactRef: str
    reviewerId: str
    status: str
    comments: Optional[str] = None
    createdAt: str

    model_config = ConfigDict(from_attributes=True)

class TeamWorkloadSnapshotRead(BaseModel):
    id: str
    teamId: str
    assignedCount: int
    activeCount: int
    blockedCount: int
    pendingReviewCount: int
    workloadFairnessScore: float
    createdAt: str

    model_config = ConfigDict(from_attributes=True)
