"""Authoritative Append-Only Mission Events & Real-time SSE Stream Engine."""

import os
import uuid
import json
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from packages.database.models import MissionEvent
from app.core.mission_lifecycle import MissionEventType

logger = logging.getLogger("kinetiq.mission.events")

# In-memory buffer for fast event lookup and test scenarios
_in_memory_mission_events: Dict[str, List[Dict[str, Any]]] = {}

# Active SSE listener queues per mission_id: mission_id -> set of asyncio.Queue
_active_mission_subscribers: Dict[str, Set[asyncio.Queue]] = {}

def _get_or_create_subscriber_set(mission_id: str) -> Set[asyncio.Queue]:
    if mission_id not in _active_mission_subscribers:
        _active_mission_subscribers[mission_id] = set()
    return _active_mission_subscribers[mission_id]

async def record_mission_event(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    event_type: str,
    payload: Dict[str, Any],
    step_id: Optional[str] = None
) -> Dict[str, Any]:
    """Appends an event to the immutable mission event ledger and broadcasts to SSE listeners."""
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    evt_id = str(uuid.uuid4())

    event_record = {
        "id": evt_id,
        "mission_id": mission_id,
        "workspace_id": workspace_id,
        "step_id": step_id,
        "event_type": event_type,
        "timestamp": now_iso,
        "payload": payload or {}
    }

    # 1. Update in-memory buffer
    if mission_id not in _in_memory_mission_events:
        _in_memory_mission_events[mission_id] = []
    _in_memory_mission_events[mission_id].append(event_record)

    # 2. Persist to database if in production postgres environment
    if session is not None:
        db_url = os.getenv("DATABASE_URL", "")
        if "postgres" in db_url or "neon.tech" in db_url:
            try:
                db_event = MissionEvent(
                    id=uuid.UUID(evt_id),
                    mission_id=uuid.UUID(mission_id) if isinstance(mission_id, str) and len(mission_id) == 36 else uuid.uuid4(),
                    workspace_id=uuid.UUID(workspace_id) if isinstance(workspace_id, str) and len(workspace_id) == 36 else uuid.uuid4(),
                    step_id=uuid.UUID(step_id) if step_id and isinstance(step_id, str) and len(step_id) == 36 else None,
                    event_type=event_type,
                    timestamp=now_dt,
                    payload=payload or {}
                )
                if hasattr(session, "is_active") and session.is_active:
                    session.add(db_event)
            except Exception as exc:
                logger.debug(f"Could not persist MissionEvent to DB (in-memory fallback active): {exc}")

    # 3. Broadcast to all active SSE subscriber queues
    subscribers = _active_mission_subscribers.get(mission_id, set())
    for q in list(subscribers):
        try:
            q.put_nowait(event_record)
        except asyncio.QueueFull:
            logger.warning(f"Subscriber queue full for mission {mission_id}, dropping real-time frame.")
        except Exception as exc:
            logger.debug(f"Failed to push event to subscriber: {exc}")

    return event_record

async def get_mission_events(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> List[Dict[str, Any]]:
    """Retrieves all append-only events for a mission with workspace isolation."""
    events = _in_memory_mission_events.get(mission_id, [])
    # Verify workspace isolation
    filtered = [e for e in events if e.get("workspace_id") == workspace_id]
    return sorted(filtered, key=lambda x: x["timestamp"])

async def subscribe_mission_events(
    workspace_id: str,
    mission_id: str
) -> AsyncGenerator[str, None]:
    """Server-Sent Events (SSE) generator streaming real-time mission execution events."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    subscribers = _get_or_create_subscriber_set(mission_id)
    subscribers.add(queue)

    try:
        # First send initial connection event
        init_evt = {
            "id": str(uuid.uuid4()),
            "mission_id": mission_id,
            "workspace_id": workspace_id,
            "event_type": "STREAM_CONNECTED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {"status": "STREAMING_ACTIVE"}
        }
        yield f"data: {json.dumps(init_evt)}\n\n"

        # Stream backlog events first
        backlog = _in_memory_mission_events.get(mission_id, [])
        for evt in backlog:
            if evt.get("workspace_id") == workspace_id:
                yield f"data: {json.dumps(evt)}\n\n"

        # Stream incoming events as they happen
        while True:
            try:
                evt = await asyncio.wait_for(queue.get(), timeout=20.0)
                yield f"data: {json.dumps(evt)}\n\n"
                queue.task_done()
            except asyncio.TimeoutError:
                # Send heartbeat keepalive comment
                yield ": keep-alive\n\n"
    except asyncio.CancelledError:
        logger.debug(f"SSE client disconnected from mission {mission_id}")
    finally:
        subscribers.discard(queue)
        if not subscribers and mission_id in _active_mission_subscribers:
            _active_mission_subscribers.pop(mission_id, None)
