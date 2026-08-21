"""Authoritative Mission Service implementing Mission Engine V1 lifecycle, persistence, and state guards."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from packages.database.models import Mission as DbMission, MissionStep as DbMissionStep
from app.schemas.mission import MissionCreate, MissionUpdate
from app.core.mission_lifecycle import (
    MissionStatus,
    MissionEventType,
    validate_status_transition,
    normalize_status,
)
from app.services.mission_engine import (
    mission_engine,
    _in_memory_engine_missions,
    _in_memory_engine_steps
)
from app.services.mission_events import (
    record_mission_event,
    get_mission_events as fetch_mission_events
)
from app.services.mission_planner import mission_planner
from app.services import memory_service

_in_memory_activities: Dict[str, List[Dict[str, Any]]] = {}
_in_memory_plans: Dict[str, List[Dict[str, Any]]] = {}

def _format_mission_dict(m: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures mission dictionary matches schema contract with all required aliases."""
    title = m.get("title") or m.get("name") or "Untitled Mission"
    name = m.get("name") or title
    agent_id = m.get("agent_id") or m.get("agentId")
    current_step = m.get("current_step", 0)
    progress = m.get("progress", 0.0)
    tok = m.get("token_usage") or {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    cost = m.get("cost", 0.0) or m.get("cost_usd", 0.0)

    res = dict(m)
    res["title"] = title
    res["name"] = name
    res["goal"] = m.get("goal") or title
    res["agent_id"] = agent_id
    res["agentId"] = agent_id
    res["current_step"] = current_step
    res["currentStep"] = current_step
    res["progress"] = progress
    res["token_usage"] = tok
    res["tokenUsage"] = tok
    res["cost"] = cost
    res["cost_usd"] = cost
    res["tenantId"] = m.get("workspace_id")
    res["tenant_id"] = m.get("workspace_id")
    res["createdBy"] = m.get("created_by")
    res["createdAt"] = m.get("created_at")
    res["updatedAt"] = m.get("updated_at")
    res["startedAt"] = m.get("started_at")
    res["completedAt"] = m.get("completed_at")
    res["failedAt"] = m.get("failed_at")
    res["cancelledAt"] = m.get("cancelled_at")
    return res

async def list_workspace_missions(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    search_query: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """Lists missions in workspace with tenant isolation, search, and filtering."""
    results = []
    for m in _in_memory_engine_missions.values():
        if m.get("workspace_id") != workspace_id:
            continue
        curr_status = m.get("status", "DRAFT")
        if status_filter and status_filter != "all":
            # Match both normalized and raw filter strings
            if curr_status.lower() != status_filter.lower() and curr_status.upper() != status_filter.upper():
                continue
        if priority_filter and priority_filter != "all":
            if m.get("priority", "medium").lower() != priority_filter.lower():
                continue
        if search_query:
            q = search_query.lower()
            t = (m.get("title") or m.get("name") or "").lower()
            d = (m.get("description") or "").lower()
            g = (m.get("goal") or "").lower()
            if q not in t and q not in d and q not in g:
                continue
        formatted = _format_mission_dict(m)
        formatted["activities"] = _in_memory_activities.get(m["id"], [])
        formatted["latest_plan"] = _in_memory_plans.get(m["id"], [None])[0]
        results.append(formatted)

    results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return results, len(results)

async def get_mission_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[Dict[str, Any]]:
    """Fetches a single mission with workspace isolation."""
    m = _in_memory_engine_missions.get(mission_id)
    if not m or m.get("workspace_id") != workspace_id:
        return None
    formatted = _format_mission_dict(m)
    formatted["activities"] = _in_memory_activities.get(mission_id, [])
    plans = _in_memory_plans.get(mission_id, [])
    formatted["latest_plan"] = plans[0] if plans else None
    return formatted

async def create_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    payload: MissionCreate
) -> Dict[str, Any]:
    """Creates a new mission in DRAFT state."""
    m_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    title = payload.get_title()
    goal = payload.goal or title
    agent_id = payload.get_agent_id()

    mission = {
        "id": m_id,
        "workspace_id": workspace_id,
        "title": title,
        "name": title,
        "goal": goal,
        "description": payload.description or "",
        "status": MissionStatus.DRAFT.value,
        "priority": payload.priority.upper() if payload.priority else "MEDIUM",
        "agent_id": agent_id,
        "agentId": agent_id,
        "model": payload.model,
        "context": payload.context or {},
        "plan": None,
        "current_step": 0,
        "currentStep": 0,
        "progress": 0.0,
        "created_by": user_id,
        "created_at": now_iso,
        "updated_at": now_iso,
        "started_at": None,
        "completed_at": None,
        "failed_at": None,
        "cancelled_at": None,
        "error": None,
        "result": None,
        "token_usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
        "cost": 0.0,
        "cost_usd": 0.0,
        "metadata": payload.metadata or {},
        "activities": [],
        "latest_plan": None,
    }

    _in_memory_engine_missions[m_id] = mission

    # Record CREATED activity & event
    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": m_id,
        "action": "CREATED",
        "details": {"title": title, "priority": mission["priority"], "goal": goal},
        "created_at": now_iso
    }
    _in_memory_activities[m_id] = [activity]
    mission["activities"] = [activity]

    await record_mission_event(
        session=None,
        workspace_id=workspace_id,
        mission_id=m_id,
        event_type=MissionEventType.MISSION_CREATED.value,
        payload={"title": title, "goal": goal, "status": MissionStatus.DRAFT.value}
    )

    return _format_mission_dict(mission)

async def update_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    payload: MissionUpdate
) -> Optional[Dict[str, Any]]:
    """Updates mission details with state guard validation."""
    m = _in_memory_engine_missions.get(mission_id)
    if not m or m.get("workspace_id") != workspace_id:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    changes = {}

    if payload.title is not None or payload.name is not None:
        new_title = payload.name or payload.title
        m["title"] = new_title
        m["name"] = new_title
        changes["title"] = new_title

    if payload.goal is not None:
        m["goal"] = payload.goal
        changes["goal"] = payload.goal

    if payload.description is not None:
        m["description"] = payload.description
        changes["description"] = payload.description

    if payload.priority is not None:
        m["priority"] = payload.priority.upper()
        changes["priority"] = m["priority"]

    if payload.agent_id is not None:
        m["agent_id"] = payload.agent_id
        m["agentId"] = payload.agent_id
        changes["agent_id"] = payload.agent_id

    if payload.model is not None:
        m["model"] = payload.model
        changes["model"] = payload.model

    if payload.context is not None:
        m["context"] = payload.context
        changes["context"] = payload.context

    if payload.status is not None:
        curr_status = m.get("status", MissionStatus.DRAFT.value)
        validate_status_transition(curr_status, payload.status, mission_id)
        m["status"] = normalize_status(payload.status)
        changes["status"] = m["status"]

    m["updated_at"] = now_iso

    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "UPDATED",
        "details": changes,
        "created_at": now_iso
    }
    if mission_id in _in_memory_activities:
        _in_memory_activities[mission_id].insert(0, activity)
    else:
        _in_memory_activities[mission_id] = [activity]

    return _format_mission_dict(m)

async def launch_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Dict[str, Any]:
    """Enqueues mission to background execution engine."""
    res = await mission_engine.enqueue_mission(session, workspace_id, mission_id)
    return _format_mission_dict(res)

async def pause_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Dict[str, Any]:
    """Pauses mission execution."""
    res = await mission_engine.pause_mission(session, workspace_id, mission_id)
    return _format_mission_dict(res)

async def resume_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Dict[str, Any]:
    """Resumes paused mission."""
    res = await mission_engine.resume_mission(session, workspace_id, mission_id)
    return _format_mission_dict(res)

async def cancel_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Dict[str, Any]:
    """Cancels mission execution."""
    res = await mission_engine.cancel_mission(session, workspace_id, mission_id)
    return _format_mission_dict(res)

async def get_mission_result(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Dict[str, Any]:
    """Retrieves final result and deliverables for a mission."""
    m = await get_mission_by_id(session, workspace_id, mission_id)
    if not m:
        raise ValueError(f"Mission {mission_id} not found in workspace.")
    return {
        "mission_id": mission_id,
        "status": m.get("status"),
        "result": m.get("result"),
        "error": m.get("error"),
        "progress": m.get("progress"),
        "token_usage": m.get("token_usage"),
        "cost_usd": m.get("cost_usd", 0.0),
        "completed_at": m.get("completed_at")
    }

async def complete_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[Dict[str, Any]]:
    m = _in_memory_engine_missions.get(mission_id)
    if not m or m.get("workspace_id") != workspace_id:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = MissionStatus.COMPLETED.value
    m["completed_at"] = now_iso
    m["updated_at"] = now_iso
    m["progress"] = 100.0

    await memory_service.create_candidate(
        workspace_id=workspace_id,
        title=f"Learned from Mission: {m['title']}",
        content=f"Key outcome from mission '{m['title']}': {m.get('description', '')}",
        type_name="preference",
        source_type="mission",
        source_id=mission_id
    )

    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "COMPLETED",
        "details": {"completed_at": now_iso},
        "created_at": now_iso
    }
    if mission_id in _in_memory_activities:
        _in_memory_activities[mission_id].insert(0, activity)
    else:
        _in_memory_activities[mission_id] = [activity]

    return _format_mission_dict(m)

async def archive_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[Dict[str, Any]]:
    m = _in_memory_engine_missions.get(mission_id)
    if not m or m.get("workspace_id") != workspace_id:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = "archived"
    m["updated_at"] = now_iso

    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "ARCHIVED",
        "details": {"archived_at": now_iso},
        "created_at": now_iso
    }
    if mission_id in _in_memory_activities:
        _in_memory_activities[mission_id].insert(0, activity)
    else:
        _in_memory_activities[mission_id] = [activity]

    return _format_mission_dict(m)

async def generate_mission_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    is_regeneration: bool = False
) -> Optional[Dict[str, Any]]:
    mission = await get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return None

    existing_plans = _in_memory_plans.get(mission_id, [])
    new_version = len(existing_plans) + 1 if is_regeneration else (len(existing_plans) if existing_plans else 1)

    plan_struct, plan_telemetry = await mission_planner.plan_mission(
        workspace_id=workspace_id,
        title=mission["title"],
        goal=mission.get("goal") or mission["title"],
        description=mission.get("description", ""),
        priority=mission.get("priority", "MEDIUM"),
        agent_id=mission.get("agent_id"),
        model=mission.get("model"),
        context=mission.get("context", {})
    )

    now_iso = datetime.now(timezone.utc).isoformat()
    plan_dict = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "version": new_version,
        "goal": plan_struct.goal,
        "summary": plan_struct.summary,
        "steps": [s.model_dump() for s in plan_struct.steps],
        "deliverables": plan_struct.deliverables,
        "open_questions": plan_struct.open_questions,
        "recommendations": plan_struct.recommendations,
        "usage_metadata": plan_telemetry,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    if mission_id not in _in_memory_plans:
        _in_memory_plans[mission_id] = []
    _in_memory_plans[mission_id].insert(0, plan_dict)

    if mission_id in _in_memory_engine_missions:
        _in_memory_engine_missions[mission_id]["plan"] = plan_struct.model_dump()
        _in_memory_engine_missions[mission_id]["latest_plan"] = plan_dict

    action_name = "PLAN_REGENERATED" if is_regeneration else "PLAN_GENERATED"
    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": action_name,
        "details": {"version": new_version, "cost_usd": plan_telemetry.get("estimated_cost_usd", 0.0)},
        "created_at": now_iso
    }
    _in_memory_activities.setdefault(mission_id, []).insert(0, activity)

    return plan_dict

async def get_mission_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[Dict[str, Any]]:
    mission = await get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return None
    plans = _in_memory_plans.get(mission_id, [])
    return plans[0] if plans else None

get_latest_plan = get_mission_plan
