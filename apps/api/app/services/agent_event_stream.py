import json
import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, Any, List, Optional

_event_subscribers: List[asyncio.Queue] = []

async def publish_agent_event(event_type: str, agent_run_id: str, mission_id: str, status: str, step_id: Optional[str] = None, extra: Optional[dict] = None):
    """Publishes a safe operational event to all connected SSE clients."""
    payload = {
        "event_type": event_type,
        "agentRunId": agent_run_id,
        "missionId": mission_id,
        "status": status,
        "stepId": step_id,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    if extra:
        payload["details"] = {k: v for k, v in extra.items() if k not in ["chain_of_thought", "tokens", "secret", "bearer"]}

    msg = f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"
    for q in list(_event_subscribers):
        try:
            q.put_nowait(msg)
        except asyncio.QueueFull:
            pass

async def event_generator(workspace_id: str) -> AsyncGenerator[str, None]:
    """Generates SSE stream formatted messages for connected admin clients."""
    queue = asyncio.Queue(maxsize=50)
    _event_subscribers.append(queue)
    try:
        init_event = f"event: ping\ndata: {json.dumps({'status': 'connected', 'timestamp': datetime.now(timezone.utc).isoformat()})}\n\n"
        yield init_event

        while True:
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=15.0)
                yield msg
            except asyncio.TimeoutError:
                yield f"event: ping\ndata: {json.dumps({'timestamp': datetime.now(timezone.utc).isoformat()})}\n\n"
    finally:
        if queue in _event_subscribers:
            _event_subscribers.remove(queue)
