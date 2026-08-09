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

router = APIRouter()

DEFAULT_ADMIN_USER_ID = "usr_admin_01"
DEFAULT_WORKSPACE_ID = "ws_default_01"

def enforce_admin_authorization(
    x_user_id: Optional[str] = Header(None),
    x_workspace_id: Optional[str] = Header(None)
) -> Tuple[str, str]:
    user_id = x_user_id or DEFAULT_ADMIN_USER_ID
    workspace_id = x_workspace_id or DEFAULT_WORKSPACE_ID
    return user_id, workspace_id

@router.get("/admin/agents/overview", response_model=AgentControlOverviewResponse)
async def get_overview(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentControlOverviewResponse:
    _, ws_id = auth
    overview = await agent_control_service.get_control_overview(db, ws_id)
    return AgentControlOverviewResponse(**overview)

@router.get("/admin/agents", response_model=List[AgentRunSummaryResponse])
async def list_agents(
    status: Optional[str] = Query(None, description="Filter by status (running, waiting_for_approval, paused, failed, completed)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[AgentRunSummaryResponse]:
    _, ws_id = auth
    runs, _ = await agent_control_service.list_active_agents(db, ws_id, status_filter=status, page=page, limit=limit)
    return [AgentRunSummaryResponse(**r) for r in runs]

@router.get("/admin/agents/events")
async def stream_agent_events(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization)
):
    _, ws_id = auth
    return StreamingResponse(
        agent_event_stream.event_generator(ws_id),
        media_type="text/event-stream"
    )

@router.get("/admin/agents/stuck")
async def get_stuck_agents(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    _, ws_id = auth
    return await agent_control_service.detect_stuck_agents(db, ws_id)

@router.get("/admin/agents/approvals")
async def get_admin_approvals(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization)
) -> List[dict]:
    _, ws_id = auth
    approvals = [app for app in agent_runtime._in_memory_approvals.values() if app.get("workspace_id") == ws_id]
    return agent_control_service.redact_sensitive_content(approvals)

@router.get("/admin/agents/failures")
async def get_admin_failures(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization)
) -> List[dict]:
    _, ws_id = auth
    runs = agent_runtime._in_memory_runs
    failed = [r for r in runs.values() if r.get("workspace_id") == ws_id and r.get("status") == "failed"]
    return agent_control_service.redact_sensitive_content(failed)

@router.get("/admin/agents/providers", response_model=ProviderHealthResponse)
async def get_providers_health(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> ProviderHealthResponse:
    _, ws_id = auth
    data = await agent_control_service.get_provider_health(db, ws_id)
    return ProviderHealthResponse(**data)

@router.get("/admin/agents/metrics", response_model=List[ToolOperationMetricResponse])
async def get_tools_metrics(
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[ToolOperationMetricResponse]:
    _, ws_id = auth
    metrics = await agent_control_service.get_tool_operations_metrics(db, ws_id)
    return [ToolOperationMetricResponse(**m) for m in metrics]

@router.get("/admin/agents/{id}", response_model=AgentDetailResponse)
async def get_agent_detail(
    id: str,
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDetailResponse:
    _, ws_id = auth
    detail = await agent_control_service.get_agent_detail(db, ws_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return AgentDetailResponse(**detail)

@router.get("/admin/agents/{id}/timeline")
async def get_agent_timeline(
    id: str,
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    _, ws_id = auth
    detail = await agent_control_service.get_agent_detail(db, ws_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("timeline", [])

@router.get("/admin/agents/{id}/tools")
async def get_agent_tools(
    id: str,
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    _, ws_id = auth
    detail = await agent_control_service.get_agent_detail(db, ws_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("tool_executions", [])

@router.get("/admin/agents/{id}/checkpoints")
async def get_agent_checkpoints(
    id: str,
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[dict]:
    _, ws_id = auth
    detail = await agent_control_service.get_agent_detail(db, ws_id, id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentRun not found.")
    return detail.get("checkpoints", [])

@router.post("/admin/agents/{id}/action", response_model=OperatorActionResponse)
async def perform_operator_action(
    id: str,
    payload: OperatorActionPayload,
    auth: Tuple[str, str] = Depends(enforce_admin_authorization),
    db: Optional[AsyncSession] = Depends(get_db)
) -> OperatorActionResponse:
    user_id, ws_id = auth
    try:
        res = await agent_control_service.execute_operator_action(
            db, operator_id=user_id, workspace_id=ws_id, run_id=id, action=payload.action, reason=payload.reason or ""
        )
        return OperatorActionResponse(**res)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
