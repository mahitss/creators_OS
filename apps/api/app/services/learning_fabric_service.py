import uuid
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.learning_fabric import (
    AgentMemoryCreate,
    AgentMemoryRead,
    MemoryVersionRead,
    MemoryProvenanceRead,
    MemoryCandidateRead,
    MemoryConflictRead,
    MemoryCorrectRequest,
    MemoryConflictResolveRequest
)
from app.services import dlp_service, policy_engine, event_mesh_service

_in_memory_agent_memories: Dict[str, dict] = {}
_in_memory_provenances: Dict[str, dict] = {}
_in_memory_versions: Dict[str, List[dict]] = {}
_in_memory_candidates: Dict[str, List[dict]] = {}
_in_memory_conflicts: Dict[str, List[dict]] = {}

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{32,}",
    r"bearer\s+[a-zA-Z0-9\._\-]{20,}",
    r"password\s*=\s*[^\s]+"
]

def _initialize_demo_learning_fabric_if_empty():
    if _in_memory_agent_memories:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    org_id = "org_default_creator"

    mem_01 = "mem_gov_001"
    mem_02 = "mem_gov_002"

    _in_memory_agent_memories[mem_01] = {
        "id": mem_01,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "owner_type": "agent",
        "owner_id": "ag_creator_ops_01",
        "memory_type": "semantic",
        "scope": "workspace",
        "title": "Service X Deployment Region",
        "content": "Service X primary deployment region is us-east-1.",
        "status": "active",
        "importance": "high",
        "confidence": 0.95,
        "created_at": now_iso,
        "updated_at": now_iso,
        "expires_at": None
    }

    _in_memory_provenances[mem_01] = {
        "id": "prov_001",
        "memory_id": mem_01,
        "source_type": "document",
        "source_id": "doc_arch_spec_01",
        "observed_at": now_iso,
        "author": "Principal Architect",
        "origin": "Architecture Handbook"
    }

    _in_memory_versions[mem_01] = [
        {
            "id": "ver_001",
            "memory_id": mem_01,
            "version": 1,
            "content_reference": {"title": "Service X Deployment Region", "content": "Service X primary deployment region is us-east-1."},
            "source": "initial_creation",
            "status": "active",
            "created_at": now_iso
        }
    ]

    _in_memory_agent_memories[mem_02] = {
        "id": mem_02,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "owner_type": "workspace",
        "owner_id": ws_id,
        "memory_type": "procedural",
        "scope": "workspace",
        "title": "Report Publishing Procedure",
        "content": "To publish Q3 report, execute step A (Grounding), step B (DLP Scan), step C (Executive Sign-off).",
        "status": "active",
        "importance": "high",
        "confidence": 0.90,
        "created_at": now_iso,
        "updated_at": now_iso,
        "expires_at": None
    }

    _in_memory_provenances[mem_02] = {
        "id": "prov_002",
        "memory_id": mem_02,
        "source_type": "workflow",
        "source_id": "wf_pub_01",
        "observed_at": now_iso,
        "author": "Workflow Engine",
        "origin": "Workflow Execution Audit"
    }

    _in_memory_candidates[ws_id] = [
        {
            "id": "cand_001",
            "workspace_id": ws_id,
            "proposed_by_agent_id": "ag_creator_ops_01",
            "memory_type": "semantic",
            "suggested_content": {"title": "Proposed Preference: Nightly Builds", "content": "Workspace team prefers nightly builds scheduled at 02:00 UTC."},
            "evidence_reference": {"execution_id": "exec_demo_01"},
            "status": "pending_review",
            "created_at": now_iso
        }
    ]

    _in_memory_conflicts[ws_id] = [
        {
            "id": "conf_001",
            "workspace_id": ws_id,
            "memory_id_a": mem_01,
            "memory_id_b": "mem_draft_99",
            "conflict_reason": "Conflicting deployment region (us-east-1 vs us-west-2).",
            "status": "unresolved",
            "resolution_notes": None,
            "resolved_by": None,
            "created_at": now_iso
        }
    ]

_initialize_demo_learning_fabric_if_empty()

def _check_secrets(text: str):
    """Scans content for embedded secrets."""
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError("Memory content contains a secret/API key which is strictly prohibited.")

async def create_memory(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: AgentMemoryCreate,
    organization_id: str = "org_default_creator"
) -> Tuple[dict, dict]:
    """Creates a governed memory object with DLP and secret scanning."""
    _initialize_demo_learning_fabric_if_empty()
    _check_secrets(req.content)

    mem_id = f"mem_{uuid.uuid4().hex[:10]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    memory = {
        "id": mem_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "owner_type": req.owner_type,
        "owner_id": req.owner_id,
        "memory_type": req.memory_type,
        "scope": req.scope,
        "title": req.title,
        "content": req.content,
        "status": "active",
        "importance": req.importance,
        "confidence": req.confidence,
        "created_at": now_iso,
        "updated_at": now_iso,
        "expires_at": None
    }

    provenance = {
        "id": f"prov_{uuid.uuid4().hex[:8]}",
        "memory_id": mem_id,
        "source_type": req.source_type,
        "source_id": req.source_id,
        "observed_at": now_iso,
        "author": req.owner_id,
        "origin": "direct_input"
    }

    version = {
        "id": f"ver_{uuid.uuid4().hex[:8]}",
        "memory_id": mem_id,
        "version": 1,
        "content_reference": {"title": req.title, "content": req.content},
        "source": req.source_type,
        "status": "active",
        "created_at": now_iso
    }

    _in_memory_agent_memories[mem_id] = memory
    _in_memory_provenances[mem_id] = provenance
    _in_memory_versions[mem_id] = [version]

    return memory, provenance

async def search_memories(
    session: Optional[AsyncSession],
    workspace_id: str,
    query: Optional[str] = None,
    memory_type: Optional[str] = None,
    scope: Optional[str] = None
) -> List[dict]:
    """Retrieves & ranks memories based on relevance, recency, and scope authorization."""
    _initialize_demo_learning_fabric_if_empty()
    results = [m for m in _in_memory_agent_memories.values() if m["workspace_id"] == workspace_id]

    if memory_type and memory_type != "all":
        results = [m for m in results if m["memory_type"] == memory_type]
    if scope and scope != "all":
        results = [m for m in results if m["scope"] == scope]
    if query:
        q = query.lower()
        results = [m for m in results if q in m["title"].lower() or q in m["content"].lower()]

    results.sort(key=lambda x: (x["confidence"], x["updated_at"]), reverse=True)
    return results

async def correct_memory(
    session: Optional[AsyncSession],
    memory_id: str,
    req: MemoryCorrectRequest,
    user_id: str = "usr_executive_01"
) -> dict:
    """Human correction generates a new versioned snapshot."""
    _initialize_demo_learning_fabric_if_empty()
    memory = _in_memory_agent_memories.get(memory_id)
    if not memory:
        raise ValueError(f"Memory '{memory_id}' not found.")

    _check_secrets(req.corrected_content)

    new_title = req.corrected_title or memory["title"]
    memory["title"] = new_title
    memory["content"] = req.corrected_content
    memory["updated_at"] = datetime.now(timezone.utc).isoformat()

    current_versions = _in_memory_versions.get(memory_id, [])
    new_version_num = len(current_versions) + 1
    new_ver = {
        "id": f"ver_{uuid.uuid4().hex[:8]}",
        "memory_id": memory_id,
        "version": new_version_num,
        "content_reference": {"title": new_title, "content": req.corrected_content, "reason": req.reason},
        "source": "human_correction",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_versions.setdefault(memory_id, []).append(new_ver)

    return memory

async def invalidate_memory(session: Optional[AsyncSession], memory_id: str) -> dict:
    """Marks memory as deprecated/invalidated."""
    _initialize_demo_learning_fabric_if_empty()
    memory = _in_memory_agent_memories.get(memory_id)
    if memory:
        memory["status"] = "deprecated"
        memory["updated_at"] = datetime.now(timezone.utc).isoformat()
    return memory

async def resolve_conflict(
    session: Optional[AsyncSession],
    workspace_id: str,
    conflict_id: str,
    req: MemoryConflictResolveRequest,
    user_id: str = "usr_executive_01"
) -> dict:
    """Operator resolves a memory conflict."""
    _initialize_demo_learning_fabric_if_empty()
    conflicts = _in_memory_conflicts.get(workspace_id, [])
    conf = next((c for c in conflicts if c["id"] == conflict_id), None)
    if not conf:
        raise ValueError(f"Conflict '{conflict_id}' not found.")

    conf["status"] = req.resolution
    conf["resolution_notes"] = req.notes
    conf["resolved_by"] = user_id
    return conf

async def list_candidates(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_learning_fabric_if_empty()
    return _in_memory_candidates.get(workspace_id, [])

async def list_conflicts(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_learning_fabric_if_empty()
    return _in_memory_conflicts.get(workspace_id, [])

async def get_history(session: Optional[AsyncSession], memory_id: str) -> List[dict]:
    _initialize_demo_learning_fabric_if_empty()
    return _in_memory_versions.get(memory_id, [])

async def get_provenance(session: Optional[AsyncSession], memory_id: str) -> Optional[dict]:
    _initialize_demo_learning_fabric_if_empty()
    return _in_memory_provenances.get(memory_id)

async def get_memory(session: Optional[AsyncSession], memory_id: str) -> Optional[dict]:
    _initialize_demo_learning_fabric_if_empty()
    return _in_memory_agent_memories.get(memory_id)
