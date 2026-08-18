from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.event_mesh import (
    EventEnvelopePublishRequest,
    EventEnvelopeRead,
    EventSchemaRead,
    EventSubscriptionCreate,
    EventSubscriptionRead,
    EventDeliveryRead,
    EventDeadLetterRead,
    EventReplayRequest,
    EventReplayRead,
    EventHealthRead,
    EventCatalogRead
)
from app.services import event_mesh_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, require_admin, WorkspaceContext

router = APIRouter(prefix="/events", tags=["Event Mesh"])

@router.get("", response_model=List[EventEnvelopeRead])
async def list_events(
    event_type: Optional[str] = None,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists event envelopes for current workspace."""
    return await event_mesh_service.list_events(db, org_id=ws_ctx.workspace_id, workspace_id=ws_ctx.workspace_id, event_type=event_type)

@router.post("", response_model=EventEnvelopeRead)
async def publish_event(
    req: EventEnvelopePublishRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Publishes a new event envelope to the Enterprise Event Mesh."""
    evt, err = await event_mesh_service.publish_event(db, req, publisher_id=ws_ctx.user_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return evt

@router.get("/catalog", response_model=List[EventCatalogRead])
async def list_catalog(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists registered event catalog entries."""
    return await event_mesh_service.list_event_catalog(db)

@router.get("/subscriptions", response_model=List[EventSubscriptionRead])
async def list_subscriptions(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists active event subscriptions for the workspace."""
    return await event_mesh_service.list_subscriptions(db, org_id=ws_ctx.workspace_id)

@router.post("/subscriptions", response_model=EventSubscriptionRead)
async def create_subscription(
    req: EventSubscriptionCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Creates a new event subscription."""
    return await event_mesh_service.create_subscription(
        db,
        org_id=ws_ctx.workspace_id,
        workspace_id=ws_ctx.workspace_id,
        event_type=req.event_type,
        consumer=req.consumer,
        filter_config=req.filter_config
    )

@router.delete("/subscriptions/{sub_id}")
async def delete_subscription(
    sub_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Deletes an event subscription."""
    ok = await event_mesh_service.delete_subscription(db, sub_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"status": "deleted", "id": sub_id}

@router.get("/health", response_model=EventHealthRead)
async def get_health(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns real-time Event Mesh health metrics."""
    return await event_mesh_service.get_event_mesh_health(db)

@router.get("/dead-letters", response_model=List[EventDeadLetterRead])
async def list_dead_letters(
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Lists dead-lettered events."""
    return await event_mesh_service.list_dead_letters(db)

@router.post("/replay/{event_id}", response_model=EventReplayRead)
async def replay_event(
    event_id: str,
    req: EventReplayRequest,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Replays an event under administrative authorization."""
    rep, err = await event_mesh_service.replay_event(db, event_id=event_id, authorized_by=ws_ctx.user_id, reason=req.reason)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return rep

@router.get("/{event_id}", response_model=EventEnvelopeRead)
async def get_event(
    event_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Fetches an event envelope by event_id."""
    evt = await event_mesh_service.get_event_by_id(db, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    return evt
