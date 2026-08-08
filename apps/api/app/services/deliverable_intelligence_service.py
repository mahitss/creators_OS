import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.content import ContentCreate
from app.services import mission_service, execution_service, content_service

_in_memory_suggestions: dict[str, dict] = {}

async def list_suggestions_for_mission(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Tuple[List[dict], int]:
    items = [
        s for s in _in_memory_suggestions.values()
        if s["workspace_id"] == workspace_id and s["mission_id"] == mission_id and s["status"] == "pending"
    ]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return items, len(items)

async def analyze_mission_for_deliverables(
    session: Optional[AsyncSession],
    workspace_id: str,
    mission_id: str
) -> Optional[dict]:
    mission = await mission_service.get_mission_by_id(session, workspace_id, mission_id)
    if not mission:
        return None

    # Step Execution Check
    exec_data = await execution_service.get_mission_steps_and_execution(session, workspace_id, mission_id)
    steps = exec_data.get("steps", [])
    completed_steps = [s for s in steps if s["status"] in ["completed", "skipped"]]

    # Insufficient output guard: no steps or 0 completed steps
    if not steps or len(completed_steps) == 0:
        return None

    # Deterministic classification rule
    title_lower = mission["title"].lower()
    desc_lower = mission["description"].lower()
    text_combined = f"{title_lower} {desc_lower}"

    if "research" in text_combined or "analysis" in text_combined or "competitor" in text_combined:
        deliv_type = "report"
        sugg_title = f"{mission['title']} Research Report"
        reason = f"Completed research steps in mission '{mission['title']}' can be structured into a formal report."
    elif "video" in text_combined or "script" in text_combined or "youtube" in text_combined:
        deliv_type = "script"
        sugg_title = f"{mission['title']} Production Script"
        reason = f"Completed outline and setup in mission '{mission['title']}' can be formatted into a video script."
    elif "post" in text_combined or "social" in text_combined or "tweet" in text_combined:
        deliv_type = "social_post"
        sugg_title = f"{mission['title']} Social Announcement"
        reason = f"Key takeaways from mission '{mission['title']}' can be compiled into a social post."
    else:
        deliv_type = "article"
        sugg_title = f"{mission['title']} Comprehensive Article"
        reason = f"Completed execution steps in mission '{mission['title']}' provide material for an article."

    # Duplicate Prevention Guard
    existing_suggs = [
        s for s in _in_memory_suggestions.values()
        if s["workspace_id"] == workspace_id and s["mission_id"] == mission_id and s["type"] == deliv_type and s["status"] in ["pending", "accepted"]
    ]
    if existing_suggs:
        return existing_suggs[0]

    # Create new suggestion
    sugg_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    sugg = {
        "id": sugg_id,
        "workspace_id": workspace_id,
        "mission_id": mission_id,
        "type": deliv_type,
        "title": sugg_title,
        "reason": reason,
        "source_data": {
            "mission_id": mission_id,
            "completed_steps_count": len(completed_steps),
            "total_steps_count": len(steps)
        },
        "confidence": 0.92,
        "status": "pending",
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_suggestions[sugg_id] = sugg
    return sugg

async def accept_suggestion(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    suggestion_id: str
) -> Tuple[Optional[dict], Optional[dict]]:
    sugg = _in_memory_suggestions.get(suggestion_id)
    if not sugg or sugg["workspace_id"] != workspace_id:
        return None, None

    sugg["status"] = "accepted"
    sugg["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Create draft Content item
    content_payload = ContentCreate(
        title=sugg["title"],
        type=sugg["type"],
        content=f"# {sugg['title']}\n\n*Created from Mission deliverable intelligence suggestion.*\n\n{sugg['reason']}",
        mission_id=sugg["mission_id"]
    )
    new_content = await content_service.create_content(session, workspace_id, user_id, content_payload)

    return sugg, new_content

async def dismiss_suggestion(
    session: Optional[AsyncSession],
    workspace_id: str,
    suggestion_id: str
) -> Optional[dict]:
    sugg = _in_memory_suggestions.get(suggestion_id)
    if not sugg or sugg["workspace_id"] != workspace_id:
        return None

    sugg["status"] = "dismissed"
    sugg["updated_at"] = datetime.now(timezone.utc).isoformat()
    return sugg
