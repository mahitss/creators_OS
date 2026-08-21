"""Agent Management Router for Kinetiq Agent Runtime V1."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.agents import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentVersionCreate,
    AgentVersionResponse,
)
from app.services import agent_service
from app.core.agent_lifecycle import (
    AgentStatus,
    InvalidAgentStateTransitionError,
)

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=List[AgentResponse])
async def list_agents(
    status: Optional[str] = Query(None, description="Filter by status (DRAFT, ACTIVE, PAUSED, DISABLED, ARCHIVED)"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentResponse]:
    """Lists authorized agents in active workspace."""
    agents = await agent_service.list_agents(db, ws_ctx.workspace_id, status_filter=status)
    return [AgentResponse(**a) for a in agents]


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: AgentCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Creates a new agent and initial immutable version v1."""
    try:
        agent = await agent_service.create_agent(db, ws_ctx.workspace_id, user_id=ws_ctx.user_id, payload=payload)
        return AgentResponse(**agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{id}", response_model=AgentResponse)
async def get_agent(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Retrieves an agent by ID with workspace boundary check."""
    agent = await agent_service.get_agent_by_id(db, ws_ctx.workspace_id, id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{id}' not found in active workspace."
        )
    return AgentResponse(**agent)


@router.patch("/{id}", response_model=AgentResponse)
async def update_agent(
    id: str,
    payload: AgentUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Updates agent metadata and creates new immutable version if runtime configuration changed."""
    try:
        agent = await agent_service.update_agent(db, ws_ctx.workspace_id, user_id=ws_ctx.user_id, agent_id=id, payload=payload)
        return AgentResponse(**agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidAgentStateTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{id}/pause", response_model=AgentResponse)
async def pause_agent(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Transitions agent to PAUSED status."""
    try:
        agent = await agent_service.set_agent_status(db, ws_ctx.workspace_id, id, AgentStatus.PAUSED.value)
        return AgentResponse(**agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidAgentStateTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{id}/resume", response_model=AgentResponse)
async def resume_agent(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Transitions agent back to ACTIVE status."""
    try:
        agent = await agent_service.set_agent_status(db, ws_ctx.workspace_id, id, AgentStatus.ACTIVE.value)
        return AgentResponse(**agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidAgentStateTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{id}/disable", response_model=AgentResponse)
async def disable_agent(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentResponse:
    """Transitions agent to DISABLED status, preventing any further execution."""
    try:
        agent = await agent_service.set_agent_status(db, ws_ctx.workspace_id, id, AgentStatus.DISABLED.value)
        return AgentResponse(**agent)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidAgentStateTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{id}/versions", response_model=List[AgentVersionResponse])
async def list_agent_versions(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[AgentVersionResponse]:
    """Returns the immutable version history of the agent."""
    try:
        versions = await agent_service.list_agent_versions(db, ws_ctx.workspace_id, id)
        return [AgentVersionResponse(**v) for v in versions]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{id}/versions", response_model=AgentVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_version(
    id: str,
    payload: AgentVersionCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AgentVersionResponse:
    """Explicitly publishes an immutable new AgentVersion."""
    try:
        v = await agent_service.create_agent_version(db, ws_ctx.workspace_id, user_id=ws_ctx.user_id, agent_id=id, payload=payload)
        return AgentVersionResponse(**v)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
