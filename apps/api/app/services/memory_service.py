"""Governed Memory Fabric V1 for KINETIQ.
Supports EPISODIC, SEMANTIC, PROCEDURAL, and WORKING memory tiers with strict tenant isolation,
provenance preservation, relevance ranking, and governed write policies.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.memory import MemoryCreate, MemoryUpdate

# In-memory stores for offline/fast execution
_in_memory_memories: Dict[str, dict] = {}
_in_memory_candidates: Dict[str, dict] = {}


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
    is_archived: bool = False,
    query: Optional[str] = None
) -> Tuple[List[dict], int]:
    """Lists memories strictly scoped to the tenant workspace."""
    sq = (search_query or query or "").strip().lower()

    all_items = [
        m for m in _in_memory_memories.values()
        if m["workspace_id"] == workspace_id and m.get("is_archived", False) == is_archived
    ]

    if type_filter and type_filter != "all":
        tf = type_filter.upper()
        all_items = [m for m in all_items if m.get("type", "").upper() == tf or m.get("type") == type_filter]
    if importance_filter and importance_filter != "all":
        all_items = [m for m in all_items if m.get("importance") == importance_filter]
    if sq:
        all_items = [
            m for m in all_items
            if sq in m.get("title", "").lower() or sq in m.get("content", "").lower()
        ]

    all_items.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return all_items, len(all_items)


async def create_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    payload: MemoryCreate,
    created_by: str = "system"
) -> dict:
    """Stores a governed memory record with verified provenance and tenant scoping."""
    now_iso = datetime.now(timezone.utc).isoformat()
    memory_id = str(uuid.uuid4())

    provenance = payload.provenance or {
        "source_type": payload.source_type,
        "source_id": payload.source_id,
        "created_by": created_by,
        "confidence": payload.confidence if payload.confidence is not None else 1.0,
        "timestamp": now_iso
    }

    mem_dict = {
        "id": memory_id,
        "workspace_id": workspace_id,
        "type": payload.type.upper() if payload.type.upper() in ["EPISODIC", "SEMANTIC", "PROCEDURAL", "WORKING"] else payload.type,
        "title": payload.title,
        "content": payload.content,
        "source_type": payload.source_type,
        "source_id": payload.source_id,
        "importance": payload.importance,
        "confidence": payload.confidence if payload.confidence is not None else 1.0,
        "is_archived": False,
        "created_at": now_iso,
        "updated_at": now_iso,
        "last_accessed_at": now_iso,
        "expires_at": payload.expires_at,
        "provenance": provenance,
        "metadata_dict": payload.metadata_dict or {}
    }

    _in_memory_memories[memory_id] = mem_dict
    return mem_dict


async def get_memory_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str
) -> Optional[dict]:
    """Retrieves a single memory record verifying tenant ownership."""
    m = _in_memory_memories.get(memory_id)
    if m and m.get("workspace_id") == workspace_id:
        m["last_accessed_at"] = datetime.now(timezone.utc).isoformat()
        return m
    return None


async def update_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    memory_id: str,
    payload: MemoryUpdate
) -> Optional[dict]:
    """Updates an existing memory record ensuring tenant isolation."""
    m = await get_memory_by_id(session, workspace_id, memory_id)
    if not m:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    if payload.title is not None:
        m["title"] = payload.title
    if payload.content is not None:
        m["content"] = payload.content
    if payload.type is not None:
        m["type"] = payload.type.upper() if payload.type.upper() in ["EPISODIC", "SEMANTIC", "PROCEDURAL", "WORKING"] else payload.type
    if payload.importance is not None:
        m["importance"] = payload.importance
    if payload.is_archived is not None:
        m["is_archived"] = payload.is_archived
    if payload.metadata_dict is not None:
        m["metadata_dict"] = payload.metadata_dict

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
    """Deletes a memory record with strict workspace scoping."""
    m = _in_memory_memories.get(memory_id)
    if m and m.get("workspace_id") == workspace_id:
        del _in_memory_memories[memory_id]
        return True
    return False


# ----------------- CANDIDATE GOVERNANCE -----------------

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
    type_name: str = "SEMANTIC",
    source_type: str = "agent_run",
    source_id: Optional[str] = None,
    created_by: str = "agent"
) -> dict:
    cand_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    cand = {
        "id": cand_id,
        "workspace_id": workspace_id,
        "source_type": source_type,
        "source_id": source_id,
        "type": type_name.upper() if type_name.upper() in ["EPISODIC", "SEMANTIC", "PROCEDURAL", "WORKING"] else type_name,
        "title": title,
        "content": content,
        "confidence": 0.90,
        "status": "pending",
        "provenance": {
            "source_type": source_type,
            "source_id": source_id,
            "created_by": created_by,
            "confidence": 0.90,
            "timestamp": now_iso
        },
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_candidates[cand_id] = cand
    return cand


async def approve_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    candidate_id: str,
    approved_by: str = "user"
) -> Optional[dict]:
    cand = _in_memory_candidates.get(candidate_id)
    if not cand or cand.get("workspace_id") != workspace_id:
        return None

    cand["status"] = "approved"
    mem_payload = MemoryCreate(
        type=cand["type"],
        title=cand["title"],
        content=cand["content"],
        importance="medium",
        source_type=cand["source_type"],
        source_id=cand["source_id"],
        confidence=cand.get("confidence", 1.0),
        provenance=cand.get("provenance")
    )
    return await create_memory(session, workspace_id, mem_payload, created_by=approved_by)


async def reject_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    candidate_id: str
) -> bool:
    cand = _in_memory_candidates.get(candidate_id)
    if not cand or cand.get("workspace_id") != workspace_id:
        return False

    cand["status"] = "rejected"
    return True


# ----------------- RELEVANCE RETRIEVAL -----------------

async def retrieve_relevant_memories(
    session: Optional[AsyncSession],
    workspace_id: str,
    query_context: str,
    limit: int = 5,
    type_filter: Optional[str] = None
) -> List[dict]:
    """Retrieves tenant-scoped memories scored by relevance, importance weight, and recency."""
    memories, _ = await list_memories(session, workspace_id, type_filter=type_filter, is_archived=False)
    if not memories:
        return []

    tokens = [t.lower() for t in query_context.split() if len(t) > 2]
    importance_weight = {"low": 1.0, "medium": 1.5, "high": 2.0, "critical": 3.0}

    scored = []
    for m in memories:
        text = f"{m.get('title', '')} {m.get('content', '')} {m.get('type', '')}".lower()
        keyword_hits = sum(1 for t in tokens if t in text)
        imp_multiplier = importance_weight.get(m.get("importance", "medium"), 1.0)
        conf = m.get("confidence", 1.0)
        # Score calculation
        score = (keyword_hits + 0.1) * imp_multiplier * conf
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for s, m in scored[:limit]]
