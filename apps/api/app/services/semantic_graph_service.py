import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    SemanticEntity,
    SemanticRelationship,
    RelationshipEvidence,
    RelationshipConflict,
    ContextPack,
    GraphSyncState,
    GraphHealthSnapshot
)
from app.schemas.semantic_graph import (
    SemanticRelationshipCreate,
    ContextPackCreate
)

_in_memory_entities: Dict[str, dict] = {} # id -> entity_dict
_in_memory_entity_resolver: Dict[str, str] = {} # "provider:external_id:resource_type" -> entity_id
_in_memory_relationships: Dict[str, dict] = {} # id -> relationship_dict
_in_memory_conflicts: Dict[str, dict] = {} # id -> conflict_dict
_in_memory_context_packs: Dict[str, dict] = {} # id -> pack_dict
_in_memory_sync_states: Dict[str, dict] = {}

VALID_ENTITY_TYPES = {
    "user", "team", "workspace", "organization", "project", "mission", "task",
    "workflow", "workflow_run", "agent", "agent_run", "document", "knowledge_source",
    "artifact", "integration", "integration_action", "event", "incident", "decision",
    "recommendation", "policy", "security_finding"
}

VALID_RELATIONSHIP_TYPES = {
    "belongs_to", "member_of", "owns", "manages", "contains", "depends_on", "uses",
    "created_by", "assigned_to", "related_to", "references", "produces", "consumes",
    "triggered_by", "triggered", "caused_by", "supports", "implements", "blocked_by",
    "reviewed_by", "approved_by", "derived_from"
}

# Populate initial seed graph entities & relationships for testing & operation
def _initialize_seed_graph():
    if _in_memory_entities:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"
    ws_id = "ws_default_01"

    seeds = [
        {"id": "ent_usr_01", "entity_type": "user", "entity_id": "usr_executive_01", "display_name": "Principal Architect"},
        {"id": "ent_ws_01", "entity_type": "workspace", "entity_id": "ws_default_01", "display_name": "Primary Vapor Workspace"},
        {"id": "ent_proj_01", "entity_type": "project", "entity_id": "proj_platform_45", "display_name": "Vapor Platform Core"},
        {"id": "ent_miss_01", "entity_type": "mission", "entity_id": "m_sprint_45", "display_name": "Sprint 45 Mission"},
        {"id": "ent_wf_01", "entity_type": "workflow", "entity_id": "wf_agent_sync_01", "display_name": "Agent Sync Workflow"},
        {"id": "ent_agent_01", "entity_type": "agent", "entity_id": "ag_mesh_orchestrator", "display_name": "Mesh Orchestrator Agent"},
        {"id": "ent_doc_01", "entity_type": "document", "entity_id": "doc_arch_spec_01", "display_name": "Semantic Graph Spec"},
        {"id": "ent_integ_01", "entity_type": "integration", "entity_id": "integ_github_01", "display_name": "GitHub Integration"},
        {"id": "ent_event_01", "entity_type": "event", "entity_id": "evt_graph_sync_01", "display_name": "Graph Sync Event"},
        {"id": "ent_inc_01", "entity_type": "incident", "entity_id": "inc_circuit_breaker_01", "display_name": "API Gateway Incident"}
    ]

    for s in seeds:
        ent = {
            "id": s["id"],
            "organization_id": org_id,
            "workspace_id": ws_id,
            "entity_type": s["entity_type"],
            "entity_id": s["entity_id"],
            "display_name": s["display_name"],
            "status": "active",
            "source": "native",
            "provider": None,
            "external_id": None,
            "resource_type": s["entity_type"],
            "metadata_info": {},
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_entities[s["id"]] = ent

    edges = [
        ("rel_01", "ent_usr_01", "member_of", "ent_ws_01", "native", "active"),
        ("rel_02", "ent_ws_01", "contains", "ent_proj_01", "native", "active"),
        ("rel_03", "ent_proj_01", "contains", "ent_miss_01", "native", "active"),
        ("rel_04", "ent_miss_01", "executes", "ent_wf_01", "native", "active"),
        ("rel_05", "ent_wf_01", "uses", "ent_agent_01", "native", "active"),
        ("rel_06", "ent_agent_01", "references", "ent_doc_01", "native", "active"),
        ("rel_07", "ent_wf_01", "uses", "ent_integ_01", "native", "active"),
        ("rel_08", "ent_integ_01", "triggered", "ent_event_01", "native", "active")
    ]

    for rel_id, f_id, r_type, t_id, src, st in edges:
        _in_memory_relationships[rel_id] = {
            "id": rel_id,
            "organization_id": org_id,
            "workspace_id": ws_id,
            "from_entity_id": f_id,
            "relationship_type": r_type,
            "to_entity_id": t_id,
            "source": src,
            "status": st,
            "confidence": "high",
            "evidence_references": [{"type": "system", "id": "sys_bootstrap"}],
            "valid_from": now_iso,
            "valid_until": None,
            "created_at": now_iso,
            "updated_at": now_iso
        }

_initialize_seed_graph()

async def resolve_or_create_entity(
    session: Optional[AsyncSession],
    org_id: str,
    workspace_id: Optional[str],
    entity_type: str,
    entity_id: str,
    display_name: str,
    source: str = "native",
    provider: Optional[str] = None,
    external_id: Optional[str] = None,
    resource_type: Optional[str] = None
) -> dict:
    """EntityResolver: Maps external/provider references to canonical semantic entities to prevent duplication."""
    _initialize_seed_graph()

    if provider and external_id:
        resolver_key = f"{provider}:{external_id}:{resource_type or entity_type}"
        if resolver_key in _in_memory_entity_resolver:
            existing_id = _in_memory_entity_resolver[resolver_key]
            return _in_memory_entities[existing_id]

    # Search existing entity by domain entity_id and entity_type
    for ent in _in_memory_entities.values():
        if ent["entity_type"] == entity_type and ent["entity_id"] == entity_id and ent["organization_id"] == org_id:
            return ent

    # Create new entity
    new_id = f"ent_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    ent = {
        "id": new_id,
        "organization_id": org_id,
        "workspace_id": workspace_id,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "display_name": display_name,
        "status": "active",
        "source": source,
        "provider": provider,
        "external_id": external_id,
        "resource_type": resource_type or entity_type,
        "metadata_info": {},
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_entities[new_id] = ent

    if provider and external_id:
        resolver_key = f"{provider}:{external_id}:{resource_type or entity_type}"
        _in_memory_entity_resolver[resolver_key] = new_id

    return ent

async def create_relationship(
    session: Optional[AsyncSession],
    org_id: str,
    workspace_id: Optional[str],
    req: SemanticRelationshipCreate
) -> Tuple[dict, Optional[str]]:
    """Creates or updates a semantic relationship between entities."""
    _initialize_seed_graph()

    if req.from_entity_id not in _in_memory_entities:
        return {}, f"From entity '{req.from_entity_id}' not found."

    if req.to_entity_id not in _in_memory_entities:
        return {}, f"To entity '{req.to_entity_id}' not found."

    if req.relationship_type not in VALID_RELATIONSHIP_TYPES:
        return {}, f"Invalid relationship_type '{req.relationship_type}'."

    # Determine status: AI suggested starts as proposed, native starts as active
    source = req.source or "native"
    status = "proposed" if source == "ai_suggested" else "active"

    rel_id = f"rel_{uuid.uuid4().hex[:12]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    rel = {
        "id": rel_id,
        "organization_id": org_id,
        "workspace_id": workspace_id,
        "from_entity_id": req.from_entity_id,
        "relationship_type": req.relationship_type,
        "to_entity_id": req.to_entity_id,
        "source": source,
        "status": status,
        "confidence": req.confidence or "high",
        "evidence_references": req.evidence_references,
        "valid_from": now_iso,
        "valid_until": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_relationships[rel_id] = rel
    return rel, None

async def query_neighbors(
    session: Optional[AsyncSession],
    entity_id: str,
    org_id: str = "org_default_creator",
    workspace_id: str = "ws_default_01",
    user_permissions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Authorization-aware neighbor discovery."""
    _initialize_seed_graph()

    root = _in_memory_entities.get(entity_id)
    if not root or root["organization_id"] != org_id:
        return {"entity": None, "neighbors": []}

    neighbors = []
    for rel in _in_memory_relationships.values():
        if rel["organization_id"] != org_id:
            continue
        if rel["status"] not in ["active", "verified"]:
            continue

        target_ent_id = None
        direction = None
        if rel["from_entity_id"] == entity_id:
            target_ent_id = rel["to_entity_id"]
            direction = "outgoing"
        elif rel["to_entity_id"] == entity_id:
            target_ent_id = rel["from_entity_id"]
            direction = "incoming"

        if target_ent_id and target_ent_id in _in_memory_entities:
            target_ent = _in_memory_entities[target_ent_id]

            # Security / Authorization Filter: Hide restricted entities if user lacks permission
            if target_ent["metadata_info"].get("classification") == "restricted" and user_permissions and "read_restricted" not in user_permissions:
                continue

            neighbors.append({
                "relationship": rel,
                "entity": target_ent,
                "direction": direction
            })

    return {"entity": root, "neighbors": neighbors}

async def find_path(
    session: Optional[AsyncSession],
    from_entity_id: str,
    to_entity_id: str,
    max_depth: int = 4,
    org_id: str = "org_default_creator"
) -> List[dict]:
    """Bounded graph traversal path finder with cycle detection."""
    _initialize_seed_graph()

    if from_entity_id not in _in_memory_entities or to_entity_id not in _in_memory_entities:
        return []

    # BFS path search
    queue = [[from_entity_id]]
    visited = {from_entity_id}

    while queue:
        path = queue.pop(0)
        curr = path[-1]

        if curr == to_entity_id:
            # Build entity path
            return [_in_memory_entities[e_id] for e_id in path if e_id in _in_memory_entities]

        if len(path) > max_depth:
            continue

        for rel in _in_memory_relationships.values():
            if rel["organization_id"] != org_id or rel["status"] not in ["active", "verified"]:
                continue

            next_id = None
            if rel["from_entity_id"] == curr:
                next_id = rel["to_entity_id"]
            elif rel["to_entity_id"] == curr:
                next_id = rel["from_entity_id"]

            if next_id and next_id not in visited:
                visited.add(next_id)
                queue.append(path + [next_id])

    return []

async def calculate_impact(
    session: Optional[AsyncSession],
    entity_id: str,
    org_id: str = "org_default_creator"
) -> dict:
    """Impact Analysis & Blast Radius calculation."""
    _initialize_seed_graph()

    direct_deps = []
    indirect_deps = []
    visited = {entity_id}

    # Direct dependencies (depth 1)
    for rel in _in_memory_relationships.values():
        if rel["organization_id"] == org_id and rel["from_entity_id"] == entity_id and rel["status"] in ["active", "verified"]:
            to_id = rel["to_entity_id"]
            if to_id in _in_memory_entities and to_id not in visited:
                visited.add(to_id)
                direct_deps.append(_in_memory_entities[to_id])

    # Indirect dependencies (depth 2)
    for d in list(direct_deps):
        for rel in _in_memory_relationships.values():
            if rel["organization_id"] == org_id and rel["from_entity_id"] == d["id"] and rel["status"] in ["active", "verified"]:
                to_id = rel["to_entity_id"]
                if to_id in _in_memory_entities and to_id not in visited:
                    visited.add(to_id)
                    indirect_deps.append(_in_memory_entities[to_id])

    all_impacted = direct_deps + indirect_deps
    affected_workflows = [e for e in all_impacted if e["entity_type"] == "workflow"]
    affected_agents = [e for e in all_impacted if e["entity_type"] == "agent"]
    affected_integrations = [e for e in all_impacted if e["entity_type"] == "integration"]

    return {
        "rootEntityId": entity_id,
        "directDependencies": direct_deps,
        "indirectDependencies": indirect_deps,
        "affectedWorkflows": affected_workflows,
        "affectedAgents": affected_agents,
        "affectedIntegrations": affected_integrations,
        "totalImpactedCount": len(all_impacted)
    }

async def build_context_pack(
    session: Optional[AsyncSession],
    org_id: str,
    workspace_id: str,
    req: ContextPackCreate
) -> dict:
    """Generates an expiring, authorization-filtered subgraph ContextPack for AI Agents and RAG."""
    _initialize_seed_graph()

    pack_id = f"pack_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)
    expires_at = (now + timedelta(hours=1)).isoformat()

    neighbors_res = await query_neighbors(session, req.root_entity_id, org_id, workspace_id)
    root_ent = neighbors_res.get("entity")

    entities = [root_ent] if root_ent else []
    relationships = []

    for item in neighbors_res.get("neighbors", []):
        entities.append(item["entity"])
        relationships.append(item["relationship"])

    pack = {
        "id": pack_id,
        "organization_id": org_id,
        "workspace_id": workspace_id,
        "entities": entities,
        "relationships": relationships,
        "evidence": [{"source": "SemanticGraphEngine"}],
        "scope": req.scope,
        "generated_at": now.isoformat(),
        "expires_at": expires_at
    }
    _in_memory_context_packs[pack_id] = pack
    return pack

async def approve_ai_relationship_proposal(
    session: Optional[AsyncSession],
    rel_id: str,
    approver_id: str
) -> Tuple[Optional[dict], Optional[str]]:
    """Human approval promoting an AI-suggested relationship to verified."""
    _initialize_seed_graph()
    rel = _in_memory_relationships.get(rel_id)
    if not rel:
        return None, f"Relationship '{rel_id}' not found."

    rel["status"] = "verified"
    rel["updated_at"] = datetime.now(timezone.utc).isoformat()
    return rel, None

async def list_ai_proposals(session: Optional[AsyncSession], org_id: str = "org_default_creator") -> List[dict]:
    """Lists pending AI relationship proposals."""
    _initialize_seed_graph()
    return [r for r in _in_memory_relationships.values() if r["organization_id"] == org_id and r["status"] == "proposed"]

async def get_graph_health(session: Optional[AsyncSession]) -> dict:
    """Calculates graph health metrics."""
    _initialize_seed_graph()
    ent_count = len(_in_memory_entities)
    rel_count = len(_in_memory_relationships)

    # Orphan rate calculation (entities with 0 relationships)
    connected_ids = set()
    for r in _in_memory_relationships.values():
        connected_ids.add(r["from_entity_id"])
        connected_ids.add(r["to_entity_id"])

    orphans = sum(1 for e in _in_memory_entities if e not in connected_ids)
    orphan_rate = (orphans / ent_count) if ent_count > 0 else 0.0

    return {
        "entity_count": ent_count,
        "relationship_count": rel_count,
        "orphan_rate": round(orphan_rate, 4),
        "invalid_relationship_rate": 0.0,
        "sync_lag_seconds": 0.5,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
