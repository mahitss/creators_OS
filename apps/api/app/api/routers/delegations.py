from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.delegations import (
    AgentDefinitionCreate,
    AgentDefinitionResponse,
    AgentDelegationCreate,
    AgentDelegationResponse,
    AgentHandoffCreate,
    AgentHandoffResponse
)
from app.services import agent_delegation_service

router = APIRouter()

@router.post("/agents", response_model=AgentDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_definition(
    payload: AgentDefinitionCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDefinitionResponse:
    agent_def = await agent_delegation_service.create_agent_definition(
        db, workspace_id=ws_ctx.workspace_id, name=payload.name, description=payload.description, created_by=ws_ctx.user_id, visibility=payload.visibility, default_purpose=payload.default_purpose
    )
    return AgentDefinitionResponse(**agent_def)

@router.get("/agents", response_model=List[AgentDefinitionResponse])
async def list_agent_definitions(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[AgentDefinitionResponse]:
    defs = await agent_delegation_service.list_agent_definitions(db, ws_ctx.workspace_id, ws_ctx.user_id)
    return [AgentDefinitionResponse(**d) for d in defs]

@router.get("/agents/{id}", response_model=AgentDefinitionResponse)
async def get_agent_definition(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDefinitionResponse:
    agent_def = await agent_delegation_service.get_agent_definition(db, ws_ctx.workspace_id, id)
    if not agent_def:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AgentDefinition not found.")
    return AgentDefinitionResponse(**agent_def)

@router.post("/agents/{id}/delegations", response_model=AgentDelegationResponse, status_code=status.HTTP_201_CREATED)
async def create_delegation(
    id: str,
    payload: AgentDelegationCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDelegationResponse:
    try:
        delegation = await agent_delegation_service.create_delegation(
            db, workspace_id=ws_ctx.workspace_id, delegated_by=ws_ctx.user_id, agent_id=id, mission_id=payload.mission_id,
            scope=payload.scope, permissions=payload.permissions, allowed_tools=payload.allowed_tools,
            allowed_resources=payload.allowed_resources, autonomy_level=payload.autonomy_level, expires_at_iso=payload.expires_at
        )
        return AgentDelegationResponse(**delegation)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/agents/{id}/delegations", response_model=List[AgentDelegationResponse])
async def list_delegations(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> List[AgentDelegationResponse]:
    dels = await agent_delegation_service.list_delegations(db, ws_ctx.workspace_id, agent_id=id)
    return [AgentDelegationResponse(**d) for d in dels]

@router.post("/delegations/{id}/revoke", response_model=AgentDelegationResponse)
async def revoke_delegation(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDelegationResponse:
    try:
        d = await agent_delegation_service.revoke_delegation(db, ws_ctx.workspace_id, id, actor_id=ws_ctx.user_id)
        return AgentDelegationResponse(**d)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/delegations/{id}/pause", response_model=AgentDelegationResponse)
async def pause_delegation(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDelegationResponse:
    try:
        d = await agent_delegation_service.pause_delegation(db, ws_ctx.workspace_id, id, actor_id=ws_ctx.user_id)
        return AgentDelegationResponse(**d)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/delegations/{id}/renew", response_model=AgentDelegationResponse)
async def renew_delegation(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentDelegationResponse:
    try:
        d = await agent_delegation_service.renew_delegation(db, ws_ctx.workspace_id, id, actor_id=ws_ctx.user_id)
        return AgentDelegationResponse(**d)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/agent-handoffs", response_model=AgentHandoffResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_handoff(
    payload: AgentHandoffCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> AgentHandoffResponse:
    try:
        handoff = await agent_delegation_service.create_agent_handoff(
            db, workspace_id=ws_ctx.workspace_id, source_agent_run_id=payload.source_agent_run_id,
            target_agent_definition_id=payload.target_agent_definition_id, mission_id=payload.mission_id,
            scope=payload.scope, input_reference=payload.input_reference, current_depth=payload.current_depth
        )
        return AgentHandoffResponse(**handoff)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
