import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import integration_service

_in_memory_calendars: Dict[str, dict] = {}
_in_memory_events: Dict[str, dict] = {}

async def sync_calendar_data(
    session: Optional[AsyncSession],
    workspace_id: str
) -> dict:
    conn = await integration_service.get_connection(session, workspace_id, "google")
    if not conn or conn["status"] != "connected":
        raise ValueError("Google integration is not connected. Calendar sync requires Google OAuth.")

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Discover Primary Calendar
    cal_id = f"cal_primary_{workspace_id}"
    calendar = {
        "id": cal_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "external_calendar_id": "primary",
        "name": f"{conn.get('external_account_name', 'Alex')}'s Calendar",
        "timezone": "UTC",
        "is_primary": True,
        "sync_token": f"sync_tok_{str(uuid.uuid4())[:8]}",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_calendars[cal_id] = calendar

    # 2. Sync Sample Events for Active Window (-7 days to +30 days)
    ev_1_id = f"ev_meeting_01_{workspace_id}"
    ev_1 = {
        "id": ev_1_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "calendar_id": cal_id,
        "external_event_id": "ext_evt_01",
        "title": "Vapor Architecture & Strategy Review",
        "description": "Weekly alignment on system execution & planning.",
        "location": "Vapor Huddle",
        "start_at": (now + timedelta(hours=2)).isoformat(),
        "end_at": (now + timedelta(hours=3)).isoformat(),
        "timezone": "UTC",
        "status": "confirmed",
        "organizer": conn.get("external_account_name", "Alex"),
        "attendee_count": 3,
        "is_all_day": False,
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    ev_2_id = f"ev_standup_02_{workspace_id}"
    ev_2 = {
        "id": ev_2_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "calendar_id": cal_id,
        "external_event_id": "ext_evt_02",
        "title": "Executive Product Demo",
        "description": "Demonstrate Mission Execution Engine.",
        "location": "Main Room",
        "start_at": (now + timedelta(days=1, hours=4)).isoformat(),
        "end_at": (now + timedelta(days=1, hours=5)).isoformat(),
        "timezone": "UTC",
        "status": "confirmed",
        "organizer": conn.get("external_account_name", "Alex"),
        "attendee_count": 5,
        "is_all_day": False,
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_events[ev_1_id] = ev_1
    _in_memory_events[ev_2_id] = ev_2

    # Update Connection last_synced_at
    await integration_service.refresh_connection(session, workspace_id, "google")

    return {
        "is_connected": True,
        "last_synced_at": now_iso,
        "calendar_count": 1,
        "event_count": 2
    }

async def list_calendars(
    session: Optional[AsyncSession],
    workspace_id: str
) -> List[dict]:
    cals = [
        c for c in _in_memory_calendars.values()
        if c["workspace_id"] == workspace_id
    ]
    return cals

async def list_events(
    session: Optional[AsyncSession],
    workspace_id: str,
    timeframe: str = "next_7_days"
) -> Tuple[List[dict], int]:
    now = datetime.now(timezone.utc)

    if timeframe == "today":
        start_bound = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_bound = start_bound + timedelta(days=1)
    elif timeframe == "tomorrow":
        start_bound = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_bound = start_bound + timedelta(days=1)
    elif timeframe == "next_30_days":
        start_bound = now - timedelta(days=1)
        end_bound = now + timedelta(days=30)
    else: # next_7_days / default
        start_bound = now - timedelta(days=1)
        end_bound = now + timedelta(days=7)

    events = []
    for ev in _in_memory_events.values():
        if ev["workspace_id"] == workspace_id and ev["status"] != "cancelled":
            ev_start = datetime.fromisoformat(ev["start_at"])
            if start_bound <= ev_start <= end_bound:
                events.append(ev)

    events.sort(key=lambda x: x["start_at"])
    return events, len(events)

async def get_calendar_context_for_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> List[dict]:
    """Prepares minimal, privacy-safe calendar context for AI Mission Planning.
    Excludes sensitive attendee emails or private attachments.
    """
    events, _ = await list_events(session, workspace_id, timeframe="next_7_days")
    context_items = []
    for ev in events:
        context_items.append({
            "title": ev["title"],
            "start_at": ev["start_at"],
            "end_at": ev["end_at"],
            "timezone": ev["timezone"],
            "is_all_day": ev["is_all_day"]
        })
    return context_items
