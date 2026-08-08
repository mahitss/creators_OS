import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.attention import ActionLink
from app.services import (
    mission_service,
    execution_service,
    memory_service,
    deliverable_intelligence_service,
    content_service,
)

_in_memory_attention: dict[str, dict] = {}

def _get_primary_action(source_type: str, source_id: str, type_name: str) -> ActionLink:
    if source_type == "mission":
        if type_name == "mission_paused":
            return ActionLink(label="Resume Execution", href=f"/missions/{source_id}")
        return ActionLink(label="Review Mission", href=f"/missions/{source_id}")
    elif source_type == "memory_candidate":
        return ActionLink(label="Review Memories", href="/memory")
    elif source_type == "deliverable_suggestion":
        return ActionLink(label="View Deliverable", href=f"/missions/{source_id}")
    elif source_type == "content":
        return ActionLink(label="Review Deliverable", href=f"/content/{source_id}")
    return ActionLink(label="Open Workspace", href="/home")

async def reconcile_attention(
    session: Optional[AsyncSession],
    workspace_id: str
) -> List[dict]:
    now_iso = datetime.now(timezone.utc).isoformat()

    # Track active sources found in current state
    active_sources = set()

    # 1. Probe Active Missions & Executions
    active_missions, _ = await mission_service.list_workspace_missions(session, workspace_id, status_filter="active")
    for m in active_missions:
        m_id = m["id"]
        exec_data = await execution_service.get_mission_steps_and_execution(session, workspace_id, m_id)
        execution = exec_data.get("execution")
        steps = exec_data.get("steps", [])

        if execution:
            e_status = execution.get("status")
            if e_status == "paused":
                active_sources.add(("mission", m_id, "mission_paused"))
                await _upsert_attention_item(
                    workspace_id=workspace_id,
                    type_name="mission_paused",
                    title=f"Execution Paused: '{m['title']}'",
                    description="Execution pipeline is currently paused with steps waiting.",
                    severity="high",
                    source_type="mission",
                    source_id=m_id
                )
            elif e_status == "failed":
                active_sources.add(("mission", m_id, "mission_failed"))
                await _upsert_attention_item(
                    workspace_id=workspace_id,
                    type_name="mission_failed",
                    title=f"Execution Failed: '{m['title']}'",
                    description="A step in this execution pipeline encountered an error.",
                    severity="urgent",
                    source_type="mission",
                    source_id=m_id
                )

    # 2. Probe Pending Memory Candidates
    candidates, _ = await memory_service.list_candidates(session, workspace_id)
    if candidates:
        active_sources.add(("memory_candidate", "all", "memory_review"))
        await _upsert_attention_item(
            workspace_id=workspace_id,
            type_name="memory_review",
            title=f"{len(candidates)} Memory Candidates Awaiting Review",
            description="Vapor extracted insights from completed missions requiring your approval.",
            severity="medium",
            source_type="memory_candidate",
            source_id="all"
        )

    # 3. Auto-resolve stale open items whose source problem is cleared
    for item in list(_in_memory_attention.values()):
        if item["workspace_id"] == workspace_id and item["status"] == "open":
            source_key = (item["source_type"], item["source_id"], item["type"])
            if source_key not in active_sources:
                item["status"] = "resolved"
                item["resolved_at"] = now_iso
                item["updated_at"] = now_iso

    items = [
        item for item in _in_memory_attention.values()
        if item["workspace_id"] == workspace_id and item["status"] == "open"
    ]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return items

async def _upsert_attention_item(
    workspace_id: str,
    type_name: str,
    title: str,
    description: str,
    severity: str,
    source_type: str,
    source_id: str
) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()

    # Idempotency Check: Existing open item for same source
    for item in _in_memory_attention.values():
        if (
            item["workspace_id"] == workspace_id
            and item["source_type"] == source_type
            and item["source_id"] == source_id
            and item["type"] == type_name
            and item["status"] in ["open", "snoozed"]
        ):
            # Check snooze expiration
            if item["status"] == "snoozed" and item.get("snoozed_until"):
                if datetime.now(timezone.utc).isoformat() > item["snoozed_until"]:
                    item["status"] = "open"
            return item

    item_id = str(uuid.uuid4())
    item = {
        "id": item_id,
        "workspace_id": workspace_id,
        "type": type_name,
        "title": title,
        "description": description,
        "severity": severity,
        "source_type": source_type,
        "source_id": source_id,
        "status": "open",
        "primary_action": _get_primary_action(source_type, source_id, type_name).model_dump(),
        "created_at": now_iso,
        "updated_at": now_iso,
        "resolved_at": None,
        "expires_at": None,
        "snoozed_until": None,
        "metadata_dict": {}
    }

    _in_memory_attention[item_id] = item
    return item

async def list_attention_items(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: str = "open"
) -> Tuple[List[dict], int, int]:
    await reconcile_attention(session, workspace_id)

    all_items = [
        item for item in _in_memory_attention.values()
        if item["workspace_id"] == workspace_id
    ]

    open_count = sum(1 for item in all_items if item["status"] == "open")

    if status_filter != "all":
        all_items = [item for item in all_items if item["status"] == status_filter]

    all_items.sort(key=lambda x: x["created_at"], reverse=True)
    return all_items, len(all_items), open_count

async def get_open_attention_count(
    session: Optional[AsyncSession],
    workspace_id: str
) -> int:
    await reconcile_attention(session, workspace_id)
    return sum(
        1 for item in _in_memory_attention.values()
        if item["workspace_id"] == workspace_id and item["status"] == "open"
    )

async def resolve_attention_item(
    session: Optional[AsyncSession],
    workspace_id: str,
    item_id: str
) -> Optional[dict]:
    item = _in_memory_attention.get(item_id)
    if not item or item["workspace_id"] != workspace_id:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    item["status"] = "resolved"
    item["resolved_at"] = now_iso
    item["updated_at"] = now_iso
    return item

async def dismiss_attention_item(
    session: Optional[AsyncSession],
    workspace_id: str,
    item_id: str
) -> Optional[dict]:
    item = _in_memory_attention.get(item_id)
    if not item or item["workspace_id"] != workspace_id:
        return None

    item["status"] = "dismissed"
    item["updated_at"] = datetime.now(timezone.utc).isoformat()
    return item

async def snooze_attention_item(
    session: Optional[AsyncSession],
    workspace_id: str,
    item_id: str,
    minutes: int = 60
) -> Optional[dict]:
    item = _in_memory_attention.get(item_id)
    if not item or item["workspace_id"] != workspace_id:
        return None

    now = datetime.now(timezone.utc)
    snooze_until = (now + timedelta(minutes=minutes)).isoformat()
    item["status"] = "snoozed"
    item["snoozed_until"] = snooze_until
    item["updated_at"] = now.isoformat()
    return item
