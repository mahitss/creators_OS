import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.memory import MemoryCreate, MemoryUpdate

# In-memory stores for offline execution
_in_memory_memories: dict[str, dict] = {}
_in_memory_candidates: dict[str, dict] = {}

def _to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()

async def list_memories(
    session: Optional[AsyncSession],
    workspace_id: str,
    type_filter: Optional[str] = None,
    importance_filter: Optional[str] = None,
    search_query: Optional[str] = None,
    is_archived: bool = False
) -> Tuple[List[dict], int]:
    all_items = [
        m for m in _in_memory_memories.values()
        if m["workspace_id"] == workspace_id and m["is_archived"] == is_archived
    ]

    if type_filter and type_filter != "all":
        all_items = [m for m in all_items if m["type"] == type_filter]
    if importance_filter and importance_filter != "all":
        all_items = [m for m in all_items if m["importance"] == importance_filter]
    if search_query:
        sq = search_query.lower()
        all_items = [
            m for m in all_items
            if sq in m["title"].lower() or sq in m["content"].lower()
        ]

    all_items.sort(key=lambda x: x["updated_at"], reverse=True)
    return all_items, len(all_items)

async def create_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    payload: MemoryCreate
) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    memory_id = str(uuid.uuid4())

    mem_dict = {
        "id": memory_id,
        "workspace_id": workspace_id,
        "type": payload.type,
        "title": payload.title,
        "content": payload.content,
        "source_type": payload.source_type,
        "source_id": payload.source_id,
        "importance": payload.importance,
        "is_archived": False,
        "created_at": now_iso,
        "updated_at": now_iso,
        "last_accessed_at": now_iso,
        "expires_at": payload.expires_at,
        "metadata_dict": payload.metadata_dict or {}
    }

    _in_memory_memories[memory_id] = mem_dict
    return mem_dict

async def get_memory_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str
) -> Optional[dict]:
    m = _in_memory_memories.get(memory_id)
    if m and m["workspace_id"] == workspace_id:
        m["last_accessed_at"] = datetime.now(timezone.utc).isoformat()
        return m
    return None

async def update_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str,
    payload: MemoryUpdate
) -> Optional[dict]:
    m = await get_memory_by_id(session, workspace_id, memory_id)
    if not m:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    if payload.title is not None:
        m["title"] = payload.title
    if payload.content is not None:
        m["content"] = payload.content
    if payload.type is not None:
        m["type"] = payload.type
    if payload.importance is not None:
        m["importance"] = payload.importance
    if payload.is_archived is not None:
        m["is_archived"] = payload.is_archived

    m["updated_at"] = now_iso
    _in_memory_memories[memory_id] = m
    return m

async def archive_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str
) -> Optional[dict]:
    return await update_memory(session, workspace_id, memory_id, MemoryUpdate(is_archived=True))

async def restore_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str
) -> Optional[dict]:
    return await update_memory(session, workspace_id, memory_id, MemoryUpdate(is_archived=False))

async def delete_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str
) -> bool:
    m = _in_memory_memories.get(memory_id)
    if m and m["workspace_id"] == workspace_id:
        del _in_memory_memories[memory_id]
        return True
    return False

# Candidate Management
async def list_candidates(
    session: Optional[AsyncSession],
    workspace_id: str
) -> Tuple[List[dict], int]:
    all_cand = [
        c for c in _in_memory_candidates.values()
        if c["workspace_id"] == workspace_id and c["status"] == "pending"
    ]
    return all_cand, len(all_cand)

async def create_candidate(
    workspace_id: str,
    title: str,
    content: str,
    type_name: str = "preference",
    source_type: str = "mission",
    source_id: Optional[str] = None
) -> dict:
    cand_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    cand = {
        "id": cand_id,
        "workspace_id": workspace_id,
        "source_type": source_type,
        "source_id": source_id,
        "type": type_name,
        "title": title,
        "content": content,
        "confidence": 0.90,
        "status": "pending",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_candidates[cand_id] = cand
    return cand

async def approve_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    candidate_id: str
) -> Optional[dict]:
    cand = _in_memory_candidates.get(candidate_id)
    if not cand or cand["workspace_id"] != workspace_id:
        return None

    cand["status"] = "approved"
    # Convert into permanent Memory
    mem_payload = MemoryCreate(
        type=cand["type"],
        title=cand["title"],
        content=cand["content"],
        importance="medium",
        source_type=cand["source_type"],
        source_id=cand["source_id"]
    )
    return await create_memory(session, workspace_id, mem_payload)

async def reject_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    candidate_id: str
) -> bool:
    cand = _in_memory_candidates.get(candidate_id)
    if not cand or cand["workspace_id"] != workspace_id:
        return False

    cand["status"] = "rejected"
    return True

# Context Retrieval Algorithm
async def retrieve_relevant_memories(
    session: Optional[AsyncSession],
    workspace_id: str,
    query_context: str,
    limit: int = 5
) -> List[dict]:
    memories, _ = await list_memories(session, workspace_id, is_archived=False)
    if not memories:
        return []

    tokens = [t.lower() for t in query_context.split() if len(t) > 2]
    importance_weight = {"low": 1.0, "medium": 1.5, "high": 2.0, "critical": 3.0}

    scored = []
    for m in memories:
        text = f"{m['title']} {m['content']} {m['type']}".lower()
        keyword_hits = sum(1 for t in tokens if t in text)
        imp_multiplier = importance_weight.get(m["importance"], 1.0)
        score = (keyword_hits + 1) * imp_multiplier
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for s, m in scored[:limit]]
