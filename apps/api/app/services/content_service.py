import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.content import ContentCreate, ContentUpdate, ContentGenerateRequest
from app.services import mission_service, memory_service
from app.core.ai_provider import resolve_ai_provider

_in_memory_content: dict[str, dict] = {}

def _to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()

async def list_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    type_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    mission_id_filter: Optional[str] = None,
    search_query: Optional[str] = None
) -> Tuple[List[dict], int]:
    all_items = [
        c for c in _in_memory_content.values()
        if c["workspace_id"] == workspace_id
    ]

    if type_filter and type_filter != "all":
        all_items = [c for c in all_items if c["type"] == type_filter]
    if status_filter and status_filter != "all":
        all_items = [c for c in all_items if c["status"] == status_filter]
    if mission_id_filter:
        all_items = [c for c in all_items if c.get("mission_id") == mission_id_filter]
    if search_query:
        sq = search_query.lower()
        all_items = [
            c for c in all_items
            if sq in c["title"].lower() or sq in c["content"].lower()
        ]

    all_items.sort(key=lambda x: x["updated_at"], reverse=True)
    return all_items, len(all_items)

async def create_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    payload: ContentCreate
) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    content_id = str(uuid.uuid4())

    mission_title = None
    if payload.mission_id:
        mission = await mission_service.get_mission_by_id(session, workspace_id, payload.mission_id)
        if mission:
            mission_title = mission["title"]

    content_dict = {
        "id": content_id,
        "workspace_id": workspace_id,
        "mission_id": payload.mission_id,
        "mission_title": mission_title,
        "title": payload.title,
        "type": payload.type,
        "status": "draft",
        "content": payload.content or "",
        "created_by": user_id,
        "created_at": now_iso,
        "updated_at": now_iso,
        "published_at": None,
        "archived_at": None
    }

    _in_memory_content[content_id] = content_dict
    return content_dict

async def get_content_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    content_id: str
) -> Optional[dict]:
    c = _in_memory_content.get(content_id)
    if c and c["workspace_id"] == workspace_id:
        return c
    return None

async def update_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    content_id: str,
    payload: ContentUpdate
) -> Optional[dict]:
    c = await get_content_by_id(session, workspace_id, content_id)
    if not c:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    if payload.title is not None:
        c["title"] = payload.title
    if payload.type is not None:
        c["type"] = payload.type
    if payload.status is not None:
        c["status"] = payload.status
        if payload.status == "archived":
            c["archived_at"] = now_iso
    if payload.content is not None:
        c["content"] = payload.content
    if payload.mission_id is not None:
        c["mission_id"] = payload.mission_id
        mission = await mission_service.get_mission_by_id(session, workspace_id, payload.mission_id)
        c["mission_title"] = mission["title"] if mission else None

    c["updated_at"] = now_iso
    _in_memory_content[content_id] = c
    return c

async def archive_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    content_id: str
) -> Optional[dict]:
    return await update_content(session, workspace_id, content_id, ContentUpdate(status="archived"))

async def approve_content(
    session: Optional[AsyncSession],
    workspace_id: str,
    content_id: str
) -> Optional[dict]:
    return await update_content(session, workspace_id, content_id, ContentUpdate(status="approved"))

async def generate_content_ai(
    session: Optional[AsyncSession],
    workspace_id: str,
    content_id: str,
    payload: ContentGenerateRequest
) -> Optional[dict]:
    c = await get_content_by_id(session, workspace_id, content_id)
    if not c:
        return None

    # Fetch mission context if linked
    mission_ctx = ""
    if c.get("mission_id"):
        m = await mission_service.get_mission_by_id(session, workspace_id, c["mission_id"])
        if m:
            mission_ctx = f"Linked Mission Title: {m['title']}\nMission Description: {m['description']}"

    # Fetch relevant approved memories
    mems = await memory_service.retrieve_relevant_memories(session, workspace_id, c["title"], limit=2)
    mem_ctx = ""
    if mems:
        mem_ctx = "\nWorkspace Memories:\n" + "\n".join([f"- {m['title']}: {m['content']}" for m in mems])

    prompt = f"Intent: {payload.intent.upper()}\nDeliverable Type: {c['type'].upper()}\nTitle: {c['title']}\nExisting Content: {c['content']}\n{mission_ctx}\n{mem_ctx}"
    if payload.custom_prompt:
        prompt += f"\nCustom Prompt Instruction: {payload.custom_prompt}"

    provider = resolve_ai_provider()
    try:
        # Use provider to generate draft text
        plan_out, _ = await provider.generate_plan(
            mission_title=f"Draft {c['type']} for '{c['title']}'",
            mission_description=prompt,
            priority="medium"
        )
        generated_text = f"# {c['title']}\n\n## Goal\n{plan_out.goal}\n\n## Overview\n{plan_out.summary}\n\n## Content Outline\n" + "\n".join([f"### Step {s.order}: {s.title}\n{s.description}" for s in plan_out.steps])
        
        now_iso = datetime.now(timezone.utc).isoformat()
        c["content"] = generated_text
        c["updated_at"] = now_iso
        _in_memory_content[content_id] = c
        return c
    except Exception as err:
        # On failure, preserve existing content safely!
        print(f"AI Provider generation failed cleanly: {err}")
        return c
