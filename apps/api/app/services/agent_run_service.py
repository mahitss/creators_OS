"""Agent Run Orchestration, SSE Streaming, and Execution Lifecycle Service."""

import os
import uuid
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.agent_lifecycle import (
    AgentStatus,
    AgentRunStatus,
    AgentEventType,
    validate_agent_executable,
    validate_agent_run_status_transition,
    InvalidAgentRunStateTransitionError,
)
from app.schemas.agents import AgentRunCreateRequest
from app.services.agent_service import get_agent_by_id
from app.services.agent_runtime_engine import (
    agent_runtime_engine,
    record_agent_event,
    _in_memory_agent_runs,
    _in_memory_agent_observations,
    _in_memory_agent_events,
    _active_run_tasks,
    _run_cancel_flags,
    _run_pause_events,
    _get_or_create_subscriber_set,
    _active_agent_subscribers
)

logger = logging.getLogger("kinetiq.agent.run.service")


async def create_and_start_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    user_role: str,
    payload: AgentRunCreateRequest
) -> Dict[str, Any]:
    """Validates agent executable status, creates AgentRun, and starts background execution."""
    agent = await get_agent_by_id(session, workspace_id, payload.agent_id)
    if not agent:
        raise ValueError(f"Agent '{payload.agent_id}' not found in active workspace.")

    # Guard: DISABLED and ARCHIVED agents cannot execute
    validate_agent_executable(agent["id"], agent["status"])

    run_id = str(uuid.uuid4())
    version_id = payload.agent_version_id or agent.get("latest_version_id") or f"ver_{agent['id']}_v1"
    now_iso = datetime.now(timezone.utc).isoformat()

    run = {
        "id": run_id,
        "agent_id": payload.agent_id,
        "agent_version_id": version_id,
        "mission_id": payload.mission_id,
        "workspace_id": workspace_id,
        "status": AgentRunStatus.QUEUED.value,
        "goal": payload.goal or f"Autonomous execution for {agent['name']}",
        "context": payload.context or {},
        "current_step": 0,
        "started_at": None,
        "completed_at": None,
        "duration_ms": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
        "error_info": None,
        "result_data": None,
        "created_at": now_iso
    }

    _in_memory_agent_runs[run_id] = run
    _in_memory_agent_observations[run_id] = []
    _in_memory_agent_events[run_id] = []

    # Initial event
    await record_agent_event(
        session=None,
        workspace_id=workspace_id,
        agent_run_id=run_id,
        mission_id=payload.mission_id,
        event_type=AgentEventType.AGENT_RUN_CREATED.value,
        payload={"agent_id": payload.agent_id, "version_id": version_id, "status": AgentRunStatus.QUEUED.value}
    )

    # Spawn background async execution task
    try:
        task = asyncio.create_task(
            agent_runtime_engine.execute_agent_run(
                session=None,
                workspace_id=workspace_id,
                run_id=run_id,
                user_id=user_id,
                user_role=user_role
            )
        )
        _active_run_tasks[run_id] = task
    except RuntimeError:
        pass # No active event loop in test/sync caller

    return run


async def get_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> Optional[Dict[str, Any]]:
    """Retrieves an AgentRun with observations and events."""
    run = _in_memory_agent_runs.get(run_id)
    if not run or run.get("workspace_id") != workspace_id:
        return None

    run_copy = dict(run)
    run_copy["observations"] = _in_memory_agent_observations.get(run_id, [])
    run_copy["events"] = _in_memory_agent_events.get(run_id, [])
    return run_copy


async def list_agent_runs(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_id: Optional[str] = None,
    mission_id: Optional[str] = None,
    status_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Lists AgentRuns for workspace with optional filtering."""
    runs = [
        r for r in _in_memory_agent_runs.values()
        if r.get("workspace_id") == workspace_id
    ]

    if agent_id:
        runs = [r for r in runs if r.get("agent_id") == agent_id]
    if mission_id:
        runs = [r for r in runs if r.get("mission_id") == mission_id]
    if status_filter and status_filter.lower() != "all":
        st_norm = status_filter.upper()
        runs = [r for r in runs if r.get("status", "").upper() == st_norm]

    return sorted(runs, key=lambda x: x.get("created_at", ""), reverse=True)


async def list_agent_run_observations(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> List[Dict[str, Any]]:
    """Returns step observations for an AgentRun."""
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        raise ValueError(f"AgentRun {run_id} not found in workspace.")
    return _in_memory_agent_observations.get(run_id, [])


async def list_agent_run_events(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> List[Dict[str, Any]]:
    """Returns append-only events for an AgentRun."""
    run = await get_agent_run(session, workspace_id, run_id)
    if not run:
        raise ValueError(f"AgentRun {run_id} not found in workspace.")
    return _in_memory_agent_events.get(run_id, [])


async def pause_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> Dict[str, Any]:
    """Pauses an active AgentRun at a safe step boundary."""
    run = _in_memory_agent_runs.get(run_id)
    if not run or run.get("workspace_id") != workspace_id:
        raise ValueError(f"AgentRun {run_id} not found in workspace.")

    curr_status = run.get("status", AgentRunStatus.QUEUED.value)
    if curr_status in [AgentRunStatus.COMPLETED.value, AgentRunStatus.CANCELLED.value, AgentRunStatus.FAILED.value]:
        return run # Idempotent

    if run_id in _run_pause_events:
        _run_pause_events[run_id].clear()

    run["status"] = AgentRunStatus.WAITING_TOOL.value
    await record_agent_event(
        session=None,
        workspace_id=workspace_id,
        agent_run_id=run_id,
        mission_id=run.get("mission_id"),
        event_type=AgentEventType.AGENT_PAUSED.value,
        payload={"status": "PAUSED"}
    )
    return run


async def resume_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> Dict[str, Any]:
    """Resumes a paused AgentRun."""
    run = _in_memory_agent_runs.get(run_id)
    if not run or run.get("workspace_id") != workspace_id:
        raise ValueError(f"AgentRun {run_id} not found in workspace.")

    if run_id in _run_pause_events:
        _run_pause_events[run_id].set()

    run["status"] = AgentRunStatus.EXECUTING.value
    await record_agent_event(
        session=None,
        workspace_id=workspace_id,
        agent_run_id=run_id,
        mission_id=run.get("mission_id"),
        event_type=AgentEventType.AGENT_STEP_STARTED.value,
        payload={"status": "RESUMED"}
    )
    return run


async def cancel_agent_run(
    session: Optional[AsyncSession],
    workspace_id: str,
    run_id: str
) -> Dict[str, Any]:
    """Cancels an AgentRun and halts further step execution."""
    run = _in_memory_agent_runs.get(run_id)
    if not run or run.get("workspace_id") != workspace_id:
        raise ValueError(f"AgentRun {run_id} not found in workspace.")

    curr_status = run.get("status", AgentRunStatus.QUEUED.value)
    if curr_status in [AgentRunStatus.CANCELLED.value, AgentRunStatus.COMPLETED.value]:
        return run # Idempotent

    _run_cancel_flags[run_id] = True
    if run_id in _run_pause_events:
        _run_pause_events[run_id].set() # Unblock if paused

    run["status"] = AgentRunStatus.CANCELLED.value
    run["completed_at"] = datetime.now(timezone.utc).isoformat()

    active_task = _active_run_tasks.get(run_id)
    if active_task and not active_task.done():
        active_task.cancel()

    await record_agent_event(
        session=None,
        workspace_id=workspace_id,
        agent_run_id=run_id,
        mission_id=run.get("mission_id"),
        event_type=AgentEventType.AGENT_COMPLETED.value,
        payload={"status": AgentRunStatus.CANCELLED.value, "reason": "Cancelled by user."}
    )
    return run


async def subscribe_agent_run_stream(
    workspace_id: str,
    run_id: str
) -> AsyncGenerator[str, None]:
    """Server-Sent Events generator streaming live events for an AgentRun."""
    run = _in_memory_agent_runs.get(run_id)
    if not run or run.get("workspace_id") != workspace_id:
        yield f"event: error\ndata: {json.dumps({'error': 'AgentRun not found'})}\n\n"
        return

    q: asyncio.Queue = asyncio.Queue()
    subscriber_set = _get_or_create_subscriber_set(run_id)
    subscriber_set.add(q)

    try:
        # Replay existing events for instant synchronization
        existing_events = _in_memory_agent_events.get(run_id, [])
        for evt in existing_events:
            yield f"event: {evt['event_type']}\ndata: {json.dumps(evt)}\n\n"

        while True:
            try:
                evt = await asyncio.wait_for(q.get(), timeout=15.0)
                yield f"event: {evt['event_type']}\ndata: {json.dumps(evt)}\n\n"
                if evt.get("event_type") in [AgentEventType.AGENT_COMPLETED.value, AgentEventType.AGENT_FAILED.value]:
                    break
            except asyncio.TimeoutError:
                yield ": ping\n\n"
    finally:
        subscriber_set.discard(q)
