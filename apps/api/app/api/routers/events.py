from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
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

router = APIRouter(prefix="/events", tags=["Event Mesh"])

@router.get("", response_model=List[EventEnvelopeRead])
async def list_events(
    event_type: Optional[str] = None,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Lists event envelopes for current organization/workspace."""
    return await event_mesh_service.list_events(db, org_id=organization_id, workspace_id=workspace_id, event_type=event_type)

@router.post("", response_model=EventEnvelopeRead)
async def publish_event(
    req: EventEnvelopePublishRequest,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Publishes a new event envelope to the Enterprise Event Mesh."""
    evt, err = await event_mesh_service.publish_event(db, req, publisher_id=x_user_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return evt

@router.get("/catalog", response_model=List[EventCatalogRead])
async def list_catalog(
    db: AsyncSession = Depends(get_db)
):
    """Lists registered event catalog entries."""
    return await event_mesh_service.list_event_catalog(db)

@router.get("/subscriptions", response_model=List[EventSubscriptionRead])
async def list_subscriptions(
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Lists active event subscriptions for the organization."""
    return await event_mesh_service.list_subscriptions(db, org_id=organization_id)

@router.post("/subscriptions", response_model=EventSubscriptionRead)
async def create_subscription(
    req: EventSubscriptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Creates a new event subscription."""
    return await event_mesh_service.create_subscription(
        db,
        org_id=req.organization_id,
        workspace_id=req.workspace_id,
        event_type=req.event_type,
        consumer=req.consumer,
        filter_config=req.filter_config
    )

@router.delete("/subscriptions/{sub_id}")
async def delete_subscription(
    sub_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Deletes an event subscription."""
    ok = await event_mesh_service.delete_subscription(db, sub_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"status": "deleted", "id": sub_id}

@router.get("/health", response_model=EventHealthRead)
async def get_health(
    db: AsyncSession = Depends(get_db)
):
    """Returns real-time Event Mesh health metrics."""
    return await event_mesh_service.get_event_mesh_health(db)

@router.get("/dead-letters", response_model=List[EventDeadLetterRead])
async def list_dead_letters(
    db: AsyncSession = Depends(get_db)
):
    """Lists dead-lettered events."""
    return await event_mesh_service.list_dead_letters(db)

@router.post("/replay/{event_id}", response_model=EventReplayRead)
async def replay_event(
    event_id: str,
    req: EventReplayRequest,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Replays an event under administrative authorization."""
    rep, err = await event_mesh_service.replay_event(db, event_id=event_id, authorized_by=x_user_id, reason=req.reason)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return rep

@router.get("/{event_id}", response_model=EventEnvelopeRead)
async def get_event(
    event_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches an event envelope by event_id."""
    evt = await event_mesh_service.get_event_by_id(db, event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    return evt
