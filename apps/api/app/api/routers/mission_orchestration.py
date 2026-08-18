from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.mission_orchestration import (
    MissionObjectiveCreate,
    MissionObjectiveRead,
    MissionPlanRead,
    MissionStepRead,
    MissionReplanRequest,
    MissionValidateRequest,
    MissionSimulateRequest,
    MissionCostRead,
    MissionRiskRead
)
from app.services import mission_orchestration_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext

router = APIRouter(prefix="/missions", tags=["Enterprise Agent Orchestration & Mission Intelligence 2.0"])

@router.post("/orchestrate", response_model=MissionPlanRead)
async def create_mission_orchestration(
    req: MissionObjectiveCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Creates a mission with objective clarity analysis and initial DAG plan."""
    _, plan = await mission_orchestration_service.create_mission_orchestration(
        db, workspace_id=ws_ctx.workspace_id, user_id=ws_ctx.user_id, req=req
    )
    return plan

@router.get("/{mission_id}/plan", response_model=MissionPlanRead)
async def get_mission_plan(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns the latest active DAG plan for a mission."""
    plan = await mission_orchestration_service.get_plan(db, mission_id=mission_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Mission plan not found")
    return plan

@router.get("/{mission_id}/plan/versions", response_model=List[dict])
async def get_mission_plan_versions(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns immutable plan version snapshots and replan history."""
    return await mission_orchestration_service.get_plan_versions(db, mission_id=mission_id)

@router.post("/{mission_id}/plan/replan", response_model=MissionPlanRead)
async def replan_mission(
    mission_id: str,
    req: MissionReplanRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Triggers event-driven replanning, generating a new plan version snapshot and diff."""
    return await mission_orchestration_service.replan_mission(
        db, workspace_id=ws_ctx.workspace_id, mission_id=mission_id, req=req
    )

@router.post("/{mission_id}/plan/validate")
async def validate_deliverable(
    mission_id: str,
    req: MissionValidateRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """MissionValidator: Verifies deliverable artifact or ActionGateway output before marking complete."""
    return await mission_orchestration_service.validate_deliverable(
        db, mission_id=mission_id, req=req
    )

@router.get("/{mission_id}/costs", response_model=MissionCostRead)
async def get_mission_costs(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns estimated vs actual cost and remaining budget telemetry."""
    cost = await mission_orchestration_service.get_costs(db, mission_id=mission_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Mission cost telemetry not found")
    return cost

@router.get("/{mission_id}/risks", response_model=MissionRiskRead)
async def get_mission_risks(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns multi-dimensional risk scores and active warnings."""
    risk = await mission_orchestration_service.get_risks(db, mission_id=mission_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Mission risk telemetry not found")
    return risk
