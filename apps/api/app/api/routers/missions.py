from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.mission import (
    MissionCreate,
    MissionUpdate,
    MissionResponse,
    MissionListResponse,
    MissionPlanResponse,
    MissionStepsPayload,
)
from app.services import mission_service, execution_service, dag_scheduler

router = APIRouter()

@router.get("/missions", response_model=MissionListResponse)
async def list_missions(
    status: Optional[str] = Query(None, description="Filter by status (active, draft, completed, archived)"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high, urgent)"),
    search: Optional[str] = Query(None, description="Text search in title or description"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionListResponse:
    items, total = await mission_service.list_workspace_missions(
        db, ws_ctx.workspace_id, status_filter=status, priority_filter=priority, search_query=search
    )
    return MissionListResponse(
        missions=[MissionResponse(**m) for m in items],
        total=total
    )

@router.post("/missions", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission(
    payload: MissionCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.create_mission(db, ws_ctx.workspace_id, ws_ctx.user_id, payload)
    return MissionResponse(**m)

@router.get("/missions/{id}", response_model=MissionResponse)
async def get_mission(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.get_mission_by_id(db, ws_ctx.workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.patch("/missions/{id}", response_model=MissionResponse)
async def update_mission(
    id: str,
    payload: MissionUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.update_mission(db, ws_ctx.workspace_id, id, payload)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.post("/missions/{id}/complete", response_model=MissionResponse)
async def complete_mission(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.complete_mission(db, ws_ctx.workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.post("/missions/{id}/archive", response_model=MissionResponse)
async def archive_mission(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionResponse:
    m = await mission_service.archive_mission(db, ws_ctx.workspace_id, id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found in active workspace."
        )
    return MissionResponse(**m)

@router.post("/missions/{id}/plan", response_model=MissionPlanResponse)
async def generate_plan(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionPlanResponse:
    try:
        plan = await mission_service.generate_mission_plan(db, ws_ctx.workspace_id, id)
        return MissionPlanResponse(**plan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/missions/{id}/plan/regenerate", response_model=MissionPlanResponse)
async def regenerate_plan(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionPlanResponse:
    try:
        plan = await mission_service.generate_mission_plan(db, ws_ctx.workspace_id, id, is_regeneration=True)
        return MissionPlanResponse(**plan)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/missions/{id}/plan", response_model=MissionPlanResponse)
async def get_plan(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionPlanResponse:
    plan = await mission_service.get_latest_plan(db, ws_ctx.workspace_id, id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found for mission.")
    return MissionPlanResponse(**plan)

# ----------------- DAG PLAN ENDPOINTS -----------------

@router.post("/missions/{id}/dag-plans", status_code=status.HTTP_201_CREATED)
async def create_dag_plan(
    id: str,
    payload: Dict[str, Any],
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> dict:
    try:
        nodes = payload.get("nodes", [])
        goal = payload.get("goal", "Execute DAG Mission")
        plan = await dag_scheduler.create_dag_plan(db, ws_ctx.workspace_id, mission_id=id, goal=goal, nodes=nodes)
        return plan
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/missions/{id}/dag-plans/{plan_id}/nodes")
async def get_dag_plan_nodes(
    id: str,
    plan_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[dict]:
    return await dag_scheduler.get_plan_nodes(plan_id)

@router.post("/missions/{id}/dag-plans/{plan_id}/execute")
async def execute_dag_plan(
    id: str,
    plan_id: str,
    run_id: str = Query(..., description="Target AgentRun ID"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> dict:
    try:
        plan = await dag_scheduler.execute_dag_plan(db, ws_ctx.workspace_id, run_id=run_id, plan_id=plan_id)
        return plan
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

# ----------------- STEPS & EXECUTION ENDPOINTS -----------------

@router.post("/missions/{id}/steps", response_model=MissionStepsPayload)
async def create_steps(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.convert_plan_to_steps(db, ws_ctx.workspace_id, id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/missions/{id}/steps", response_model=MissionStepsPayload)
async def list_steps(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    data = await execution_service.get_execution_state(db, ws_ctx.workspace_id, id)
    return MissionStepsPayload(**data)

@router.post("/missions/{id}/start", response_model=MissionStepsPayload)
async def start_execution(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.start_execution(db, ws_ctx.workspace_id, id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/missions/{id}/pause", response_model=MissionStepsPayload)
async def pause_execution(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.pause_execution(db, ws_ctx.workspace_id, id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/missions/{id}/resume", response_model=MissionStepsPayload)
async def resume_execution(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    return await start_execution(id, ws_ctx, db)

@router.post("/missions/{id}/cancel", response_model=MissionStepsPayload)
async def cancel_execution(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.cancel_execution(db, ws_ctx.workspace_id, id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/mission-steps/{step_id}/complete", response_model=MissionStepsPayload)
async def complete_step(
    step_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.complete_step(db, ws_ctx.workspace_id, step_id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/mission-steps/{step_id}/skip", response_model=MissionStepsPayload)
async def skip_step(
    step_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionStepsPayload:
    try:
        data = await execution_service.skip_step(db, ws_ctx.workspace_id, step_id)
        return MissionStepsPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
