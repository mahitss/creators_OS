from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.calendar import (
    CalendarResponse,
    CalendarEventResponse,
    CalendarEventListResponse,
    CalendarSyncStatusResponse,
)
from app.services import calendar_service, integration_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/calendar/calendars", response_model=list[CalendarResponse])
async def list_calendars(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> list[CalendarResponse]:
    cals = await calendar_service.list_calendars(db, workspace_id)
    return [CalendarResponse(**c) for c in cals]

@router.get("/calendar/events", response_model=CalendarEventListResponse)
async def list_calendar_events(
    timeframe: str = Query("next_7_days", description="Timeframe filter (today, tomorrow, this_week, next_7_days, next_30_days)"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> CalendarEventListResponse:
    events, total = await calendar_service.list_events(db, workspace_id, timeframe=timeframe)
    return CalendarEventListResponse(
        events=[CalendarEventResponse(**ev) for ev in events],
        total=total
    )

@router.get("/calendar/status", response_model=CalendarSyncStatusResponse)
async def get_calendar_status(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> CalendarSyncStatusResponse:
    conn = await integration_service.get_connection(db, workspace_id, "google")
    if not conn or conn["status"] != "connected":
        return CalendarSyncStatusResponse(
            is_connected=False,
            last_synced_at=None,
            calendar_count=0,
            event_count=0
        )

    cals = await calendar_service.list_calendars(db, workspace_id)
    events, total_events = await calendar_service.list_events(db, workspace_id, timeframe="next_30_days")
    return CalendarSyncStatusResponse(
        is_connected=True,
        last_synced_at=conn.get("last_synced_at"),
        calendar_count=len(cals),
        event_count=total_events
    )

@router.post("/calendar/sync", response_model=CalendarSyncStatusResponse)
async def sync_calendar(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> CalendarSyncStatusResponse:
    try:
        status_data = await calendar_service.sync_calendar_data(db, workspace_id)
        return CalendarSyncStatusResponse(**status_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
