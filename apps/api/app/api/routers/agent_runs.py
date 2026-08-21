"""Agent Run Management, Streaming & Execution Router for Kinetiq Agent Runtime V1."""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.agents import (
    AgentRunCreateRequest,
    AgentRunDetailResponse,
    AgentObservationResponse,
    AgentEventResponse,
)
from app.services import agent_run_service, agent_runtime, agent_recovery
from app.core.agent_lifecycle import AgentExecutionNotAllowedError

router = APIRouter(tags=["agent-runs"])


@router.get("/agent-runs", response_model=List[AgentRunDetailResponse])
async def list_agent_runs(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    mission_id: Optional[str] = Query(None, description="Filter by mission ID"),
    status: Optional[str] = Query(None, description="Filter by run status (QUEUED, EXECUTING, COMPLETED, FAILED, CANCELLED)"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentRunDetailResponse]:
    """Lists AgentRuns for active workspace with optional filters."""
    runs = await agent_run_service.list_agent_runs(db, ws_ctx.workspace_id, agent_id=agent_id, mission_id=mission_id, status_filter=status)
    return [AgentRunDetailResponse(**r) for r in runs]


@router.post("/agent-runs", response_model=AgentRunDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_run(
    payload: AgentRunCreateRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunDetailResponse:
    """Initializes and begins autonomous execution of an AgentRun."""
    try:
        run = await agent_run_service.create_and_start_agent_run(
            session=db,
            workspace_id=ws_ctx.workspace_id,
            user_id=ws_ctx.user_id,
            user_role=ws_ctx.role,
            payload=payload
        )
        return AgentRunDetailResponse(**run)
    except AgentExecutionNotAllowedError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/agent-runs/{id}", response_model=AgentRunDetailResponse)
async def get_agent_run(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunDetailResponse:
    """Retrieves single AgentRun with step observations and events."""
    run = await agent_run_service.get_agent_run(db, ws_ctx.workspace_id, id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AgentRun '{id}' not found in active workspace."
        )
    return AgentRunDetailResponse(**run)


@router.get("/agent-runs/{id}/observations", response_model=List[AgentObservationResponse])
async def list_agent_run_observations(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentObservationResponse]:
    """Retrieves step observations produced by the AgentRun."""
    try:
        obs = await agent_run_service.list_agent_run_observations(db, ws_ctx.workspace_id, id)
        return [AgentObservationResponse(**o) for o in obs]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/agent-runs/{id}/events", response_model=List[AgentEventResponse])
async def list_agent_run_events(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentEventResponse]:
    """Retrieves immutable append-only event ledger history for the AgentRun."""
    try:
        evts = await agent_run_service.list_agent_run_events(db, ws_ctx.workspace_id, id)
        return [AgentEventResponse(**e) for e in evts]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/agent-runs/{id}/pause", response_model=AgentRunDetailResponse)
async def pause_agent_run(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunDetailResponse:
    """Pauses an AgentRun at a safe step boundary."""
    try:
        run = await agent_run_service.pause_agent_run(db, ws_ctx.workspace_id, id)
        return AgentRunDetailResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/agent-runs/{id}/resume", response_model=AgentRunDetailResponse)
async def resume_agent_run(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunDetailResponse:
    """Resumes a paused AgentRun."""
    try:
        run = await agent_run_service.resume_agent_run(db, ws_ctx.workspace_id, id)
        return AgentRunDetailResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/agent-runs/{id}/cancel", response_model=AgentRunDetailResponse)
async def cancel_agent_run(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunDetailResponse:
    """Aborts and cancels an AgentRun immediately."""
    try:
        run = await agent_run_service.cancel_agent_run(db, ws_ctx.workspace_id, id)
        return AgentRunDetailResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/agent-runs/{id}/stream")
async def stream_agent_run(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace)
):
    """Server-Sent Events (SSE) live stream for an AgentRun."""
    return StreamingResponse(
        agent_run_service.subscribe_agent_run_stream(ws_ctx.workspace_id, id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# ----------------- LEGACY MISSION AGENT-RUNS COMPATIBILITY -----------------

@router.post("/missions/{id}/agent-runs", status_code=status.HTTP_201_CREATED)
async def create_mission_agent_run_legacy(
    id: str,
    payload: Dict[str, Any],
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Legacy compatibility bridge for mission agent runs."""
    agent_id = payload.get("agent_id") or "ag_revenue_analyst"
    req = AgentRunCreateRequest(
        agent_id=agent_id,
        mission_id=id,
        goal=payload.get("goal"),
        context=payload.get("context")
    )
    try:
        run = await agent_run_service.create_and_start_agent_run(db, ws_ctx.workspace_id, ws_ctx.user_id, ws_ctx.role, req)
        return run
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
