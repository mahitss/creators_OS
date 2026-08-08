import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import mission_service

# In-memory stores for offline execution engine
_in_memory_steps: dict[str, list[dict]] = {}
_in_memory_executions: dict[str, dict] = {}
_in_memory_step_results: dict[str, dict] = {}

def _to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()

async def convert_plan_to_steps(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> dict:
    mission = await mission_service.get_mission_by_id(session, workspace_id, mission_id)
    if not mission or not mission.get("latest_plan"):
        raise ValueError("Mission does not have a generated plan.")

    plan = mission["latest_plan"]
    plan_steps = plan.get("steps", [])
    if not plan_steps:
        raise ValueError("Mission plan contains no steps.")

    now_iso = datetime.now(timezone.utc).isoformat()
    db_steps = []
    
    for idx, ps in enumerate(plan_steps):
        step_id = str(uuid.uuid4())
        status = "ready" if idx == 0 else "pending"
        step_dict = {
            "id": step_id,
            "mission_id": mission_id,
            "plan_version_id": plan["id"],
            "title": ps["title"],
            "description": ps["description"],
            "order": ps["order"],
            "status": status,
            "failure_reason": None,
            "output": None,
            "created_at": now_iso,
            "updated_at": now_iso,
            "started_at": None,
            "completed_at": None
        }
        db_steps.append(step_dict)

    _in_memory_steps[mission_id] = db_steps

    execution_id = str(uuid.uuid4())
    execution_dict = {
        "id": execution_id,
        "mission_id": mission_id,
        "status": "idle",
        "completed_steps_count": 0,
        "total_steps_count": len(db_steps),
        "created_at": now_iso,
        "updated_at": now_iso,
        "started_at": None,
        "completed_at": None
    }
    _in_memory_executions[mission_id] = execution_dict

    await mission_service.update_mission(
        session, workspace_id, mission_id, mission_service.MissionUpdate()
    )
    act = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "STEPS_CREATED",
        "details": {"count": len(db_steps)},
        "created_at": now_iso
    }
    if mission_id in mission_service._in_memory_activities:
        mission_service._in_memory_activities[mission_id].insert(0, act)

    return {"execution": execution_dict, "steps": db_steps}

async def get_mission_steps_and_execution(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> dict:
    mission = await mission_service.get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return {"execution": None, "steps": []}

    steps = _in_memory_steps.get(mission_id, [])
    execution = _in_memory_executions.get(mission_id)
    return {"execution": execution, "steps": steps}

get_execution_state = get_mission_steps_and_execution

async def start_execution(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> dict:
    state = await get_mission_steps_and_execution(session, workspace_id, mission_id)
    execution = state["execution"]
    steps = state["steps"]

    if not steps or not execution:
        raise ValueError("No executable steps exist for this mission.")

    now_iso = datetime.now(timezone.utc).isoformat()
    execution["status"] = "running"
    if not execution["started_at"]:
        execution["started_at"] = now_iso
    execution["updated_at"] = now_iso

    ready_step = next((s for s in steps if s["status"] == "ready"), None)
    if ready_step:
        ready_step["status"] = "in_progress"
        ready_step["started_at"] = now_iso

    act = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "EXECUTION_STARTED",
        "details": {},
        "created_at": now_iso
    }
    mission_service._in_memory_activities[mission_id].insert(0, act)

    return state

async def pause_execution(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> dict:
    state = await get_mission_steps_and_execution(session, workspace_id, mission_id)
    execution = state["execution"]
    steps = state["steps"]

    if not steps or not execution:
        raise ValueError("No active execution to pause.")

    now_iso = datetime.now(timezone.utc).isoformat()
    execution["status"] = "paused"
    execution["updated_at"] = now_iso

    in_progress = next((s for s in steps if s["status"] == "in_progress"), None)
    if in_progress:
        in_progress["status"] = "ready"

    act = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "EXECUTION_PAUSED",
        "details": {},
        "created_at": now_iso
    }
    mission_service._in_memory_activities[mission_id].insert(0, act)
    return state

async def cancel_execution(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> dict:
    state = await get_mission_steps_and_execution(session, workspace_id, mission_id)
    execution = state["execution"]
    steps = state["steps"]

    if not steps or not execution:
        raise ValueError("No active execution to cancel.")

    now_iso = datetime.now(timezone.utc).isoformat()
    execution["status"] = "cancelled"
    execution["updated_at"] = now_iso

    act = {
        "id": str(uuid.uuid4()),
        "mission_id": mission_id,
        "action": "EXECUTION_CANCELLED",
        "details": {},
        "created_at": now_iso
    }
    mission_service._in_memory_activities[mission_id].insert(0, act)
    return state

async def complete_step(
    session: Optional[AsyncSession],
    workspace_id: str,
    step_id: str,
    output: Optional[dict] = None
) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    
    target_step = None
    target_mission_id = None
    
    for m_id, steps in _in_memory_steps.items():
        for s in steps:
            if s["id"] == step_id:
                target_step = s
                target_mission_id = m_id
                break
        if target_step:
            break

    if not target_step or not target_mission_id:
        raise ValueError("Step not found.")

    target_step["status"] = "completed"
    target_step["completed_at"] = now_iso
    target_step["updated_at"] = now_iso
    target_step["output"] = output or {"result": "Step completed successfully."}

    steps = _in_memory_steps[target_mission_id]
    execution = _in_memory_executions[target_mission_id]

    completed_count = sum(1 for s in steps if s["status"] in ["completed", "skipped"])
    execution["completed_steps_count"] = completed_count
    execution["updated_at"] = now_iso

    next_pending = next((s for s in steps if s["status"] == "pending"), None)
    if next_pending:
        next_pending["status"] = "ready"
        if execution["status"] == "running":
            next_pending["status"] = "in_progress"
            next_pending["started_at"] = now_iso

    if completed_count == len(steps):
        execution["status"] = "completed"
        execution["completed_at"] = now_iso
        await mission_service.complete_mission(session, workspace_id, target_mission_id)

    act = {
        "id": str(uuid.uuid4()),
        "mission_id": target_mission_id,
        "action": "STEP_COMPLETED",
        "details": {"step_title": target_step["title"]},
        "created_at": now_iso
    }
    mission_service._in_memory_activities[target_mission_id].insert(0, act)

    return {"execution": execution, "steps": steps}

async def skip_step(
    session: Optional[AsyncSession],
    workspace_id: str,
    step_id: str
) -> dict:
    target_step = None
    target_mission_id = None
    for m_id, steps in _in_memory_steps.items():
        for s in steps:
            if s["id"] == step_id:
                target_step = s
                target_mission_id = m_id
                break

    if not target_step or not target_mission_id:
        raise ValueError("Step not found.")

    target_step["status"] = "skipped"
    return await complete_step(session, workspace_id, step_id, output={"result": "Skipped by user."})
