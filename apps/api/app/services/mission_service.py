import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.mission import MissionCreate, MissionUpdate
from app.core.ai_provider import resolve_ai_provider
from app.services import memory_service

_in_memory_missions: dict[str, dict] = {}
_in_memory_activities: dict[str, list[dict]] = {}
_in_memory_plans: dict[str, list[dict]] = {}

async def list_workspace_missions(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    search_query: Optional[str] = None
) -> Tuple[List[dict], int]:
    results = []
    for m in _in_memory_missions.values():
        if m["workspace_id"] != workspace_id:
            continue
        if status_filter and status_filter != "all" and m["status"] != status_filter:
            continue
        if priority_filter and priority_filter != "all" and m["priority"] != priority_filter:
            continue
        if search_query:
            q = search_query.lower()
            if q not in m["title"].lower() and q not in m["description"].lower():
                continue
        results.append(m)

    results.sort(key=lambda x: x["created_at"], reverse=True)
    return results, len(results)

async def get_mission_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    m = _in_memory_missions.get(mission_id)
    if not m or m["workspace_id"] != workspace_id:
        return None
    m["activities"] = _in_memory_activities.get(mission_id, [])
    return m

async def create_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    payload: MissionCreate
) -> dict:
    m_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    mission = {
        "id": m_id,
        "workspace_id": workspace_id,
        "title": payload.title,
        "description": payload.description,
        "status": "active",
        "priority": payload.priority,
        "created_by": user_id,
        "created_at": now_iso,
        "updated_at": now_iso,
        "completed_at": None,
        "activities": [],
        "latest_plan": None,
    }

    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": m_id,
        "action": "CREATED",
        "details": {"title": payload.title, "priority": payload.priority},
        "created_at": now_iso
    }
    _in_memory_activities[m_id] = [activity]
    mission["activities"] = [activity]

    _in_memory_missions[m_id] = mission
    return mission

async def update_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    payload: MissionUpdate
) -> Optional[dict]:
    m = await get_mission_by_id(session, workspace_id, mission_id)
    if not m:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    changes = {}
    if payload.title is not None:
        m["title"] = payload.title
        changes["title"] = payload.title
    if payload.description is not None:
        m["description"] = payload.description
        changes["description"] = payload.description
    if payload.priority is not None:
        m["priority"] = payload.priority
        changes["priority"] = payload.priority
    if payload.status is not None:
        m["status"] = payload.status
        changes["status"] = payload.status
        if payload.status == "completed":
            m["completed_at"] = now_iso
            await memory_service.create_candidate(
                workspace_id=workspace_id,
                title=f"Learned from Mission: {m['title']}",
                content=f"Key outcome from mission '{m['title']}': {m['description']}",
                type_name="preference",
                source_type="mission",
                source_id=mission_id
            )

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
        
    m["activities"] = _in_memory_activities[mission_id]
    _in_memory_missions[mission_id] = m
    return m

async def complete_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    m = await get_mission_by_id(session, workspace_id, mission_id)
    if not m:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = "completed"
    m["completed_at"] = now_iso
    m["updated_at"] = now_iso

    await memory_service.create_candidate(
        workspace_id=workspace_id,
        title=f"Learned from Mission: {m['title']}",
        content=f"Key outcome from mission '{m['title']}': {m['description']}",
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

    m["activities"] = _in_memory_activities[mission_id]
    _in_memory_missions[mission_id] = m
    return m

async def archive_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    m = await get_mission_by_id(session, workspace_id, mission_id)
    if not m:
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

    m["activities"] = _in_memory_activities[mission_id]
    _in_memory_missions[mission_id] = m
    return m

async def generate_mission_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str,
    is_regeneration: bool = False
) -> Optional[dict]:
    mission = await get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return None

    existing_plans = _in_memory_plans.get(mission_id, [])
    new_version = len(existing_plans) + 1 if is_regeneration else (len(existing_plans) if existing_plans else 1)

    relevant_mems = await memory_service.retrieve_relevant_memories(
        session, workspace_id, query_context=f"{mission['title']} {mission['description']}", limit=3
    )

    context_prompt = mission["description"]
    if relevant_mems:
        mem_text = "\n".join([f"- [{m['type'].upper()}] {m['title']}: {m['content']}" for m in relevant_mems])
        context_prompt += f"\n\nRelevant Workspace Memories:\n{mem_text}"

    provider = resolve_ai_provider()
    output, metadata = await provider.generate_plan(
        mission_title=mission["title"],
        mission_description=context_prompt,
        priority=mission["priority"]
    )

    now_iso = datetime.now(timezone.utc).isoformat()
    plan_dict = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "version": new_version,
        "goal": output.goal,
        "summary": output.summary,
        "steps": [s.model_dump() for s in output.steps],
        "deliverables": output.deliverables,
        "open_questions": output.open_questions,
        "recommendations": output.recommendations,
        "usage_metadata": metadata.model_dump(),
        "created_at": now_iso,
        "updated_at": now_iso
    }

    if mission_id not in _in_memory_plans:
        _in_memory_plans[mission_id] = []
    _in_memory_plans[mission_id].insert(0, plan_dict)

    action_name = "PLAN_REGENERATED" if is_regeneration else "PLAN_GENERATED"
    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": action_name,
        "details": {"version": new_version, "provider": metadata.provider, "relevant_memories_count": len(relevant_mems)},
        "created_at": now_iso
    }
    _in_memory_activities[mission_id].insert(0, activity)
    mission["activities"] = _in_memory_activities[mission_id]
    mission["latest_plan"] = plan_dict
    return plan_dict

async def get_mission_plan(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    mission = await get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return None

    plans = _in_memory_plans.get(mission_id, [])
    return plans[0] if plans else None

get_latest_plan = get_mission_plan
