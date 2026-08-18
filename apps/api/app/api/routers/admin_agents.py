from typing import Optional, List, Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.admin_agents import (
    AgentControlOverviewResponse,
    AgentRunSummaryResponse,
    AgentDetailResponse,
    OperatorActionPayload,
    OperatorActionResponse,
    ToolOperationMetricResponse,
    ProviderHealthResponse
)
from app.services import agent_control_service, agent_event_stream, agent_runtime

from app.dependencies.auth import require_admin, WorkspaceContext

router = APIRouter()

@router.get("/admin/agents/overview", response_model=AgentControlOverviewResponse)
async def get_overview(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentControlOverviewResponse:
    overview = await agent_control_service.get_control_overview(db, ws_ctx.workspace_id)
    return AgentControlOverviewResponse(**overview)

@router.get("/admin/agents", response_model=List[AgentRunSummaryResponse])
async def list_agents(
    status: Optional[str] = Query(None, description="Filter by status (running, waiting_for_approval, paused, failed, completed)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[AgentRunSummaryResponse]:
    runs, _ = await agent_control_service.list_active_agents(db, ws_ctx.workspace_id, status_filter=status, page=page, limit=limit)
    return [AgentRunSummaryResponse(**r) for r in runs]

@router.get("/admin/agents/events")
async def stream_agent_events(
    ws_ctx: WorkspaceContext = Depends(require_admin)
):
    return StreamingResponse(
        agent_event_stream.event_generator(ws_ctx.workspace_id),
        media_type="text/event-stream"
    )

@router.get("/admin/agents/stuck")
async def get_stuck_agents(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    return await agent_control_service.detect_stuck_agents(db, ws_ctx.workspace_id)

@router.get("/admin/agents/approvals")
async def get_admin_approvals(
    ws_ctx: WorkspaceContext = Depends(require_admin)
) -> List[dict]:
    approvals = [app for app in agent_runtime._in_memory_approvals.values() if app.get("workspace_id") == ws_ctx.workspace_id]
    return agent_control_service.redact_sensitive_content(approvals)

@router.get("/admin/agents/failures")
async def get_admin_failures(
    ws_ctx: WorkspaceContext = Depends(require_admin)
) -> List[dict]:
    runs = agent_runtime._in_memory_runs
    failed = [r for r in runs.values() if r.get("workspace_id") == ws_ctx.workspace_id and r.get("status") == "failed"]
    return agent_control_service.redact_sensitive_content(failed)

@router.get("/admin/agents/providers", response_model=ProviderHealthResponse)
async def get_providers_health(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> ProviderHealthResponse:
    data = await agent_control_service.get_provider_health(db, ws_ctx.workspace_id)
    return ProviderHealthResponse(**data)

@router.get("/admin/agents/metrics", response_model=List[ToolOperationMetricResponse])
async def get_tools_metrics(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[ToolOperationMetricResponse]:
    metrics = await agent_control_service.get_tool_operations_metrics(db, ws_ctx.workspace_id)
    return [ToolOperationMetricResponse(**m) for m in metrics]

@router.get("/admin/agents/{id}", response_model=AgentDetailResponse)
async def get_agent_detail(
    id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDetailResponse:
    detail = await agent_control_service.get_agent_detail(db, ws_ctx.workspace_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return AgentDetailResponse(**detail)

@router.get("/admin/agents/{id}/timeline")
async def get_agent_timeline(
    id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    detail = await agent_control_service.get_agent_detail(db, ws_ctx.workspace_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("timeline", [])

@router.get("/admin/agents/{id}/tools")
async def get_agent_tools(
    id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    detail = await agent_control_service.get_agent_detail(db, ws_ctx.workspace_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("tool_executions", [])

@router.get("/admin/agents/{id}/checkpoints")
async def get_agent_checkpoints(
    id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    detail = await agent_control_service.get_agent_detail(db, ws_ctx.workspace_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("checkpoints", [])

@router.post("/admin/agents/{id}/action", response_model=OperatorActionResponse)
async def perform_operator_action(
    id: str,
    payload: OperatorActionPayload,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: Optional[AsyncSession] = Depends(get_db)
) -> OperatorActionResponse:
    try:
        res = await agent_control_service.execute_operator_action(
            db, operator_id=ws_ctx.user_id, workspace_id=ws_ctx.workspace_id, run_id=id, action=payload.action, reason=payload.reason or ""
        )
        return OperatorActionResponse(**res)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
