from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.agent_runtime_v2 import (
    AgentExecutionCreate,
    AgentExecutionRead,
    ExecutionCheckpointRead,
    UnknownOutcomeResolveRequest,
    UnknownOutcomeRead,
    ExecutionTraceRead,
    ExecutionActionRequest
)
from app.services import agent_runtime_v2_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/agents/executions", tags=["Enterprise Agent Runtime 2.0 & Durable Cognitive Execution"])

@router.get("", response_model=List[AgentExecutionRead])
async def list_executions(
    db: AsyncSession = Depends(get_db)
):
    """Lists agent executions."""
    return await agent_runtime_v2_service.list_executions(db)

@router.post("", response_model=AgentExecutionRead)
async def create_execution(
    req: AgentExecutionCreate,
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new durable Agent Execution 2.0 instance."""
    exec_inst, _ = await agent_runtime_v2_service.create_execution(
        db, workspace_id=workspace_id, req=req, organization_id=organization_id
    )
    return exec_inst

@router.get("/{execution_id}", response_model=AgentExecutionRead)
async def get_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches agent execution details."""
    e = await agent_runtime_v2_service.get_execution(db, execution_id=execution_id)
    if not e:
        raise HTTPException(status_code=404, detail="Agent Execution not found")
    return e

@router.get("/{execution_id}/trace", response_model=ExecutionTraceRead)
async def get_execution_trace(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Returns complete execution trace including state, steps, checkpoints, and unknown outcomes."""
    trace = await agent_runtime_v2_service.get_execution_trace(db, execution_id=execution_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Execution trace not found")
    return trace

@router.post("/{execution_id}/pause", response_model=AgentExecutionRead)
async def pause_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Pauses a running execution."""
    e = await agent_runtime_v2_service.pause_execution(db, execution_id=execution_id)
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return e

@router.post("/{execution_id}/resume", response_model=AgentExecutionRead)
async def resume_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Resumes a paused execution."""
    e = await agent_runtime_v2_service.resume_execution(db, execution_id=execution_id)
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return e

@router.post("/{execution_id}/cancel", response_model=AgentExecutionRead)
async def cancel_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Cancels an execution."""
    e = await agent_runtime_v2_service.cancel_execution(db, execution_id=execution_id)
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return e

@router.post("/{execution_id}/recover", response_model=AgentExecutionRead)
async def recover_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Recovers a crashed or stale execution."""
    e = await agent_runtime_v2_service.recover_execution(db, execution_id=execution_id)
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return e

@router.get("/{execution_id}/checkpoints", response_model=List[ExecutionCheckpointRead])
async def list_checkpoints(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Lists checkpoints for execution."""
    return await agent_runtime_v2_service.list_checkpoints(db, execution_id=execution_id)

@router.get("/{execution_id}/unknown-outcomes", response_model=List[UnknownOutcomeRead])
async def list_unknown_outcomes(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Lists unknown outcomes requiring operator resolution."""
    return await agent_runtime_v2_service.list_unknown_outcomes(db, execution_id=execution_id)

@router.post("/{execution_id}/unknown-outcomes/{step_id}/resolve", response_model=UnknownOutcomeRead)
async def resolve_unknown_outcome(
    execution_id: str,
    step_id: str,
    req: UnknownOutcomeResolveRequest,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Resolves an unknown outcome with explicit operator evidence notes."""
    return await agent_runtime_v2_service.resolve_unknown_outcome(
        db, execution_id=execution_id, step_id=step_id, req=req, user_id=x_user_id
    )
