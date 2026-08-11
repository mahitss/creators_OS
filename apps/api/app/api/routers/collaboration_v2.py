from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.collaboration_v2_service import CollaborationV2Service
from app.schemas.collaboration_v2 import (
    WorkItemCreate, WorkItemRead, WorkHandoffCreate, WorkHandoffRead,
    CollaborationSessionRead, CollaborationEscalationCreate, CollaborationEscalationRead,
    ExpertiseProfileRead, WorkRoutingRecommendationRead,
    CollaborationFeedbackCreate, CollaborationFeedbackRead,
    CollaborationReviewRead, TeamWorkloadSnapshotRead
)

router = APIRouter(tags=["human_ai_collaboration_v2"])

# Work Items Router
@router.get("/work", response_model=List[WorkItemRead])
async def list_work_items(status: Optional[str] = None):
    items = await CollaborationV2Service.list_work_items(None, "org_default_creator", status)
    return [
        WorkItemRead(
            id=w["id"],
            organizationId=w["organization_id"],
            workspaceId=w["workspace_id"],
            teamId=w.get("team_id"),
            missionId=w.get("mission_id"),
            parentWorkItemId=w.get("parent_work_item_id"),
            title=w["title"],
            description=w["description"],
            priority=w["priority"],
            status=w["status"],
            assigneeType=w["assignee_type"],
            assigneeId=w.get("assignee_id"),
            workClassification=w["work_classification"],
            createdAt=w["created_at"],
            updatedAt=w["updated_at"]
        ) for w in items
    ]

@router.post("/work", response_model=WorkItemRead)
async def create_work_item(payload: WorkItemCreate):
    w = await CollaborationV2Service.create_work_item(None, payload.model_dump())
    return WorkItemRead(
        id=w["id"],
        organizationId=w["organization_id"],
        workspaceId=w["workspace_id"],
        teamId=w.get("team_id"),
        missionId=w.get("mission_id"),
        parentWorkItemId=w.get("parent_work_item_id"),
        title=w["title"],
        description=w["description"],
        priority=w["priority"],
        status=w["status"],
        assigneeType=w["assignee_type"],
        assigneeId=w.get("assignee_id"),
        workClassification=w["work_classification"],
        createdAt=w["created_at"],
        updatedAt=w["updated_at"]
    )

@router.get("/work/{work_id}", response_model=WorkItemRead)
async def get_work_item(work_id: str):
    w = await CollaborationV2Service.get_work_item(None, work_id)
    if not w:
        raise HTTPException(status_code=404, detail=f"Work item '{work_id}' not found.")
    return WorkItemRead(
        id=w["id"],
        organizationId=w["organization_id"],
        workspaceId=w["workspace_id"],
        teamId=w.get("team_id"),
        missionId=w.get("mission_id"),
        parentWorkItemId=w.get("parent_work_item_id"),
        title=w["title"],
        description=w["description"],
        priority=w["priority"],
        status=w["status"],
        assigneeType=w["assignee_type"],
        assigneeId=w.get("assignee_id"),
        workClassification=w["work_classification"],
        createdAt=w["created_at"],
        updatedAt=w["updated_at"]
    )

@router.post("/work/{work_id}/route", response_model=WorkRoutingRecommendationRead)
async def route_work_item(work_id: str):
    rec = await CollaborationV2Service.route_work_item(None, work_id)
    if "error" in rec:
        raise HTTPException(status_code=404, detail=rec["error"])
    return WorkRoutingRecommendationRead(
        id=rec["id"],
        workItemId=rec["work_item_id"],
        recommendedExecutorType=rec["recommended_executor_type"],
        recommendedExecutorId=rec["recommended_executor_id"],
        reasonSummary=rec["reason_summary"],
        riskLevel=rec["risk_level"],
        costEstimate=rec["cost_estimate"],
        deadlineImpact=rec["deadline_impact"],
        createdAt=rec["created_at"]
    )

@router.post("/work/{work_id}/handoff", response_model=WorkHandoffRead)
async def create_handoff(work_id: str, payload: WorkHandoffCreate):
    h = await CollaborationV2Service.initiate_handoff(None, payload.model_dump())
    return WorkHandoffRead(
        id=h["id"],
        workItemId=h["work_item_id"],
        fromId=h["from_id"],
        fromType=h["from_type"],
        toId=h["to_id"],
        toType=h["to_type"],
        reason=h["reason"],
        contextReferencesJson=h["context_references_json"],
        expectedOutput=h["expected_output"],
        deadline=h.get("deadline"),
        status=h["status"]
    )

@router.post("/work/{work_id}/feedback", response_model=CollaborationFeedbackRead)
async def submit_feedback(work_id: str, payload: CollaborationFeedbackCreate):
    fb = await CollaborationV2Service.add_feedback(None, work_id, payload.model_dump())
    return CollaborationFeedbackRead(
        id=fb["id"],
        workItemId=fb["work_item_id"],
        feedbackType=fb["feedback_type"],
        ratingScore=fb.get("rating_score"),
        comment=fb["comment"],
        authorUserId=fb["author_user_id"],
        createdAt=fb["created_at"]
    )

# Collaboration Center Router
@router.get("/collaboration")
async def get_collaboration_overview():
    return await CollaborationV2Service.get_collaboration_overview(None)

@router.get("/collaboration/escalations", response_model=List[CollaborationEscalationRead])
async def get_escalations():
    ov = await CollaborationV2Service.get_collaboration_overview(None)
    return [
        CollaborationEscalationRead(
            id=e["id"],
            workItemId=e["work_item_id"],
            escalationType=e["escalation_type"],
            targetRoleOrUser=e["target_role_or_user"],
            reason=e["reason"],
            dueAt=e["due_at"],
            resolvedAt=e.get("resolved_at"),
            status=e["status"]
        ) for e in ov["escalations"]
    ]

@router.get("/collaboration/teams/{team_id}/workload", response_model=TeamWorkloadSnapshotRead)
async def get_team_workload(team_id: str):
    return TeamWorkloadSnapshotRead(
        id="snap_team_01",
        teamId=team_id,
        assignedCount=14,
        activeCount=6,
        blockedCount=1,
        pendingReviewCount=3,
        workloadFairnessScore=0.94,
        createdAt="2026-08-11T04:00:00Z"
    )
