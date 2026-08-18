from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.automations import (
    AgentTriggerCreate,
    AgentTriggerUpdate,
    AgentTriggerRead,
    SystemEventCreate,
    SystemEventRead,
    AutomationExecutionRead,
    DryRunTestRequest,
    DryRunTestResponse
)
from app.services import proactive_service, workspace_service

router = APIRouter(prefix="/automations", tags=["automations"])

@router.get("", response_model=List[AgentTriggerRead])
async def list_automations(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists all active and paused automation triggers for a workspace."""
    triggers = await proactive_service.list_workspace_triggers(session, ws_ctx.workspace_id)
    return triggers

@router.post("", response_model=AgentTriggerRead, status_code=201)
async def create_automation(
    trigger_in: AgentTriggerCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Creates a new structured trigger for event-driven automation."""
    trigger_in.workspace_id = ws_ctx.workspace_id
    trigger = await proactive_service.create_trigger(session, trigger_in, created_by=ws_ctx.user_id)
    return trigger

@router.get("/{trigger_id}", response_model=AgentTriggerRead)
async def get_automation(
    trigger_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves an automation trigger by ID."""
    trigger = await proactive_service.get_trigger(session, trigger_id)
    if not trigger or trigger.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    return trigger

@router.patch("/{trigger_id}", response_model=AgentTriggerRead)
async def update_automation(
    trigger_id: str,
    update_in: AgentTriggerUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Updates an automation trigger's conditions, scope, action, or status."""
    existing = await proactive_service.get_trigger(session, trigger_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    trigger = await proactive_service.update_trigger(session, trigger_id, update_in)
    return trigger

@router.post("/{trigger_id}/test", response_model=DryRunTestResponse)
async def test_automation(
    trigger_id: str,
    test_in: DryRunTestRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Performs a dry-run simulation test on a trigger without executing side effects."""
    existing = await proactive_service.get_trigger(session, trigger_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    payload = {
        "event_type": test_in.event_type,
        "resource_type": test_in.resource_type,
        "resource_id": test_in.resource_id,
        "metadata_dict": test_in.metadata_dict
    }
    result = await proactive_service.dry_run_trigger(session, trigger_id, payload)
    return result

@router.post("/{trigger_id}/pause", response_model=AgentTriggerRead)
async def pause_automation(
    trigger_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Pauses an active automation trigger."""
    existing = await proactive_service.get_trigger(session, trigger_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    update_in = AgentTriggerUpdate(enabled=False, status="paused")
    trigger = await proactive_service.update_trigger(session, trigger_id, update_in)
    return trigger

@router.post("/{trigger_id}/enable", response_model=AgentTriggerRead)
async def enable_automation(
    trigger_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Enables a paused automation trigger."""
    existing = await proactive_service.get_trigger(session, trigger_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    update_in = AgentTriggerUpdate(enabled=True, status="active")
    trigger = await proactive_service.update_trigger(session, trigger_id, update_in)
    return trigger

@router.get("/{trigger_id}/history", response_model=List[AutomationExecutionRead])
async def list_automation_history(
    trigger_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves execution audit history for a trigger."""
    existing = await proactive_service.get_trigger(session, trigger_id)
    if not existing or existing.get("workspace_id") != ws_ctx.workspace_id:
        raise HTTPException(status_code=404, detail="Automation trigger not found.")
    history = await proactive_service.list_trigger_history(session, trigger_id)
    return history

@router.get("/dead-letters", response_model=List[dict])
async def get_dead_letters(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves unprocessable / dead-letter events for operational visibility."""
    letters = await proactive_service.list_dead_letters(session, ws_ctx.workspace_id)
    return letters

@router.post("/events/webhooks/{source}", response_model=SystemEventRead, status_code=202)
async def ingest_webhook_event(
    source: str,
    event_in: SystemEventCreate,
    session: AsyncSession = Depends(get_db)
):
    """Fast-ACK ingestion endpoint for external webhooks (Gmail, Calendar, Drive, etc.)."""
    event, _ = await proactive_service.ingest_event(session, event_in)
    return event
