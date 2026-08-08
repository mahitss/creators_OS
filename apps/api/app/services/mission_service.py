import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.schemas.mission import MissionCreate, MissionUpdate
from packages.database.models import Mission, MissionActivity

# In-memory fallback store for offline/isolated execution
_in_memory_missions: dict[str, dict] = {}
_in_memory_activities: dict[str, list[dict]] = {}

def _to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()

async def list_workspace_missions(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    search_query: Optional[str] = None,
) -> Tuple[List[dict], int]:
    if session is not None:
        try:
            ws_uuid = uuid.UUID(workspace_id)
            query = select(Mission).where(Mission.workspace_id == ws_uuid)
            
            if status_filter and status_filter != "all":
                query = query.where(Mission.status == status_filter)
            if priority_filter and priority_filter != "all":
                query = query.where(Mission.priority == priority_filter)
            if search_query:
                term = f"%{search_query}%"
                query = query.where(or_(Mission.title.ilike(term), Mission.description.ilike(term)))
                
            query = query.order_by(Mission.created_at.desc())
            result = await session.execute(query)
            db_missions = result.scalars().all()
            
            items = [
                {
                    "id": str(m.id),
                    "workspace_id": str(m.workspace_id),
                    "title": m.title,
                    "description": m.description,
                    "status": m.status,
                    "priority": m.priority,
                    "created_by": str(m.created_by),
                    "created_at": _to_iso(m.created_at),
                    "updated_at": _to_iso(m.updated_at),
                    "completed_at": _to_iso(m.completed_at),
                    "activities": []
                }
                for m in db_missions
            ]
            return items, len(items)
        except Exception:
            pass

    # Fallback in-memory query
    all_items = [
        m for m in _in_memory_missions.values()
        if m["workspace_id"] == workspace_id
    ]
    
    if status_filter and status_filter != "all":
        all_items = [m for m in all_items if m["status"] == status_filter]
    if priority_filter and priority_filter != "all":
        all_items = [m for m in all_items if m["priority"] == priority_filter]
    if search_query:
        sq = search_query.lower()
        all_items = [
            m for m in all_items
            if sq in m["title"].lower() or sq in m["description"].lower()
        ]
        
    all_items.sort(key=lambda x: x["created_at"], reverse=True)
    return all_items, len(all_items)

async def create_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    payload: MissionCreate
) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    mission_id = str(uuid.uuid4())
    
    activity = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "CREATED",
        "details": {"title": payload.title, "priority": payload.priority},
        "created_at": now_iso
    }

    mission_dict = {
        "id": mission_id,
        "workspace_id": workspace_id,
        "title": payload.title,
        "description": payload.description,
        "status": "active",
        "priority": payload.priority,
        "created_by": user_id,
        "created_at": now_iso,
        "updated_at": now_iso,
        "completed_at": None,
        "activities": [activity]
    }

    if session is not None:
        try:
            ws_uuid = uuid.UUID(workspace_id)
            usr_uuid = uuid.UUID(user_id)
            db_mission = Mission(
                id=uuid.UUID(mission_id),
                workspace_id=ws_uuid,
                title=payload.title,
                description=payload.description,
                status="active",
                priority=payload.priority,
                created_by=usr_uuid
            )
            session.add(db_mission)
            db_act = MissionActivity(
                id=uuid.UUID(activity["id"]),
                mission_id=uuid.UUID(mission_id),
                action="CREATED",
                details=activity["details"]
            )
            session.add(db_act)
            await session.commit()
        except Exception:
            pass

    _in_memory_missions[mission_id] = mission_dict
    _in_memory_activities[mission_id] = [activity]
    return mission_dict

async def get_mission_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    if session is not None:
        try:
            m_uuid = uuid.UUID(mission_id)
            ws_uuid = uuid.UUID(workspace_id)
            stmt = select(Mission).where(Mission.id == m_uuid, Mission.workspace_id == ws_uuid)
            res = await session.execute(stmt)
            m = res.scalar_one_or_none()
            if m:
                act_stmt = select(MissionActivity).where(MissionActivity.mission_id == m_uuid).order_by(MissionActivity.created_at.desc())
                act_res = await session.execute(act_stmt)
                db_acts = act_res.scalars().all()
                
                return {
                    "id": str(m.id),
                    "workspace_id": str(m.workspace_id),
                    "title": m.title,
                    "description": m.description,
                    "status": m.status,
                    "priority": m.priority,
                    "created_by": str(m.created_by),
                    "created_at": _to_iso(m.created_at),
                    "updated_at": _to_iso(m.updated_at),
                    "completed_at": _to_iso(m.completed_at),
                    "activities": [
                        {
                            "id": str(a.id),
                            "mission_id": str(a.mission_id),
                            "action": a.action,
                            "details": a.details,
                            "created_at": _to_iso(a.created_at)
                        } for a in db_acts
                    ]
                }
        except Exception:
            pass

    m = _in_memory_missions.get(mission_id)
    if m and m["workspace_id"] == workspace_id:
        m["activities"] = _in_memory_activities.get(mission_id, [])
        return m
    return None

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
