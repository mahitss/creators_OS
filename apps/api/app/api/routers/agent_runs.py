from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.agent_runs import (
    AgentRunCreate,
    AgentRunResponse,
    AgentStepResponse,
    AgentApprovalResponse,
    AgentCheckpointResponse
)
from app.services import agent_runtime, agent_recovery

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.post("/missions/{id}/agent-runs", response_model=AgentRunResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_run(
    id: str,
    payload: AgentRunCreate,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunResponse:
    try:
        run = await agent_runtime.create_agent_run(
            db, workspace_id, mission_id=id, goal=payload.goal, max_iterations=payload.max_iterations or 20
        )
        return AgentRunResponse(**run)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/agent-runs/{id}", response_model=AgentRunResponse)
async def get_agent_run(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunResponse:
    run = await agent_runtime.get_agent_run(db, workspace_id, id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent run not found in active workspace."
        )
    return AgentRunResponse(**run)

@router.get("/agent-runs/{id}/steps", response_model=List[AgentStepResponse])
async def list_agent_steps(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentStepResponse]:
    steps = await agent_runtime.list_agent_steps(db, workspace_id, id)
    return [AgentStepResponse(**s) for s in steps]

@router.get("/agent-runs/{id}/checkpoints", response_model=List[AgentCheckpointResponse])
async def list_agent_checkpoints(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentCheckpointResponse]:
    run = await agent_runtime.get_agent_run(db, workspace_id, id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")
    cps = agent_recovery._in_memory_checkpoints.get(id, [])
    return [AgentCheckpointResponse(**c) for c in cps]

@router.post("/agent-runs/{id}/pause", response_model=AgentRunResponse)
async def pause_agent_run(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunResponse:
    run = await agent_runtime.pause_agent_run(db, workspace_id, id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")
    return AgentRunResponse(**run)

@router.post("/agent-runs/{id}/resume", response_model=AgentRunResponse)
async def resume_agent_run(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunResponse:
    run = await agent_runtime.resume_agent_run(db, workspace_id, id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")
    return AgentRunResponse(**run)

@router.post("/agent-runs/{id}/cancel", response_model=AgentRunResponse)
async def cancel_agent_run(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentRunResponse:
    run = await agent_runtime.cancel_agent_run(db, workspace_id, id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found.")
    return AgentRunResponse(**run)

@router.post("/agent-runs/{id}/approvals/{approval_id}/approve", response_model=AgentApprovalResponse)
async def approve_approval_request(
    id: str,
    approval_id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentApprovalResponse:
    try:
        app_req = await agent_runtime.approve_approval_request(db, workspace_id, id, approval_id)
        return AgentApprovalResponse(**app_req)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/agent-runs/{id}/approvals/{approval_id}/reject", response_model=AgentApprovalResponse)
async def reject_approval_request(
    id: str,
    approval_id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentApprovalResponse:
    try:
        app_req = await agent_runtime.reject_approval_request(db, workspace_id, id, approval_id)
        return AgentApprovalResponse(**app_req)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
