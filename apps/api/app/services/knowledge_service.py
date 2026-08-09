import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import memory_service, policy_engine

_in_memory_knowledge_objects: Dict[str, dict] = {}
_in_memory_conflicts: Dict[str, dict] = {}
_in_memory_relations: Dict[str, dict] = {}

def _compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

async def ingest_knowledge_object(
    session: Optional[AsyncSession],
    workspace_id: str,
    scope: str,
    owner_id: str,
    source_type: str,
    source_id: str,
    title: str,
    content: str,
    mission_id: Optional[str] = None,
    confidence: float = 1.0
) -> dict:
    k_id = f"kn_{uuid.uuid4().hex[:8]}"
    content_hash = _compute_hash(content)
    now_iso = datetime.now(timezone.utc).isoformat()

    k_obj = {
        "id": k_id,
        "workspace_id": workspace_id,
        "scope": scope,
        "owner_id": owner_id,
        "mission_id": mission_id,
        "source_type": source_type,
        "source_id": source_id,
        "title": title,
        "content_reference": {"snippet": content[:300], "length": len(content)},
        "content_hash": content_hash,
        "status": "fresh",
        "confidence": confidence,
        "freshness": "fresh",
        "visibility": "workspace" if scope != "personal" else "private",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_knowledge_objects[k_id] = k_obj
    return k_obj

async def propose_memory_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    owner_id: str,
    statement: str,
    type_name: str = "fact",
    scope: str = "workspace",
    source_references: Optional[List[dict]] = None,
    confidence: float = 1.0,
    reason: str = "",
    mission_id: Optional[str] = None
) -> dict:
    # Memory candidates must go through human approval flow before becoming active
    candidate_id = f"mem_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    candidate = {
        "id": candidate_id,
        "workspace_id": workspace_id,
        "scope": scope,
        "owner_id": owner_id,
        "mission_id": mission_id,
        "type": type_name if type_name in ["preference", "fact", "decision", "goal", "insight", "lesson", "relationship", "context"] else "fact",
        "title": statement[:50],
        "content": statement,
        "statement": statement,
        "importance": "medium",
        "source_type": "ai_extraction",
        "source_id": candidate_id,
        "is_archived": False,
        "source_references": source_references or [],
        "confidence": confidence,
        "reason": reason,
        "status": "candidate",
        "created_at": now_iso,
        "updated_at": now_iso,
        "last_accessed_at": now_iso,
        "metadata_dict": {}
    }

    # Register candidate in memory_service
    memory_service._in_memory_memories[candidate_id] = candidate

    # Detect potential memory conflicts with active memories
    await detect_memory_conflicts(session, workspace_id, candidate)

    return candidate

async def approve_memory_candidate(
    session: Optional[AsyncSession],
    workspace_id: str,
    candidate_id: str,
    user_id: str
) -> dict:
    mem = memory_service._in_memory_memories.get(candidate_id)
    if not mem or mem.get("workspace_id") != workspace_id:
        raise ValueError("Memory candidate not found.")

    if mem.get("status") != "candidate":
        raise ValueError(f"Memory is in status '{mem.get('status')}', not candidate.")

    now_iso = datetime.now(timezone.utc).isoformat()
    mem["status"] = "active"
    mem["approved_by"] = user_id
    mem["approved_at"] = now_iso
    mem["updated_at"] = now_iso
    return mem

async def detect_memory_conflicts(
    session: Optional[AsyncSession],
    workspace_id: str,
    new_mem: dict
) -> List[dict]:
    conflicts = []
    statement = new_mem.get("statement", "").lower()
    now_iso = datetime.now(timezone.utc).isoformat()

    active_mems = [m for m in memory_service._in_memory_memories.values() if m.get("workspace_id") == workspace_id and m.get("status") == "active" and m["id"] != new_mem["id"]]

    for existing in active_mems:
        ex_stmt = existing.get("statement", "").lower()
        # Conflict heuristic: shared subject/keyword with opposing terms (e.g. deadline Friday vs Monday)
        if ("deadline" in statement and "deadline" in ex_stmt and statement != ex_stmt) or \
           ("postgres" in statement and "mysql" in ex_stmt):
            cid = f"cnf_{uuid.uuid4().hex[:8]}"
            cnf = {
                "id": cid,
                "workspace_id": workspace_id,
                "memory_a_id": existing["id"],
                "memory_b_id": new_mem["id"],
                "reason": f"Conflicting memory statements: '{existing['statement']}' vs '{new_mem['statement']}'",
                "status": "open",
                "created_at": now_iso
            }
            _in_memory_conflicts[cid] = cnf
            conflicts.append(cnf)

    return conflicts

async def resolve_memory_conflict(
    session: Optional[AsyncSession],
    workspace_id: str,
    conflict_id: str,
    choice: str, # keep_a, keep_b, supersede
    user_id: str
) -> dict:
    cnf = _in_memory_conflicts.get(conflict_id)
    if not cnf or cnf.get("workspace_id") != workspace_id:
        raise ValueError("Memory conflict not found.")

    mem_a = memory_service._in_memory_memories.get(cnf["memory_a_id"])
    mem_b = memory_service._in_memory_memories.get(cnf["memory_b_id"])

    now_iso = datetime.now(timezone.utc).isoformat()
    if choice == "keep_a":
        if mem_b: mem_b["status"] = "rejected"
    elif choice == "keep_b":
        if mem_a: mem_a["status"] = "superseded"
        if mem_b: mem_b["status"] = "active"

    cnf["status"] = "resolved"
    cnf["resolved_at"] = now_iso
    return cnf

async def list_memory_conflicts(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    return [c for c in _in_memory_conflicts.values() if c.get("workspace_id") == workspace_id]

async def invalidate_source_knowledge(session: Optional[AsyncSession], workspace_id: str, source_id: str, new_content_hash: Optional[str] = None) -> List[dict]:
    updated = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for k in _in_memory_knowledge_objects.values():
        if k.get("workspace_id") == workspace_id and k.get("source_id") == source_id:
            if not new_content_hash or k.get("content_hash") != new_content_hash:
                k["status"] = "stale"
                k["freshness"] = "stale"
                k["updated_at"] = now_iso
                updated.append(k)
    return updated

async def get_memory_provenance(session: Optional[AsyncSession], workspace_id: str, memory_id: str) -> dict:
    mem = memory_service._in_memory_memories.get(memory_id)
    if not mem or mem.get("workspace_id") != workspace_id:
        raise ValueError("Memory not found.")

    return {
        "memory_id": memory_id,
        "statement": mem.get("statement", mem.get("content", "")),
        "scope": mem.get("scope", "workspace"),
        "owner_id": mem.get("owner_id", "usr_alex"),
        "confidence": mem.get("confidence", 1.0),
        "status": mem.get("status", "active"),
        "source_references": mem.get("source_references", []),
        "created_at": mem.get("created_at"),
        "approved_by": mem.get("approved_by")
    }
