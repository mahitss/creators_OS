import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import workspace_service

_in_memory_definitions: Dict[str, dict] = {
    "def_research_01": {
        "id": "def_research_01",
        "workspace_id": "ws_default_01",
        "name": "Research Assistant",
        "description": "Safe read-only context gatherer for project files and emails.",
        "created_by": "usr_alex",
        "visibility": "workspace",
        "default_purpose": "Gather background specs",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    "def_proposal_01": {
        "id": "def_proposal_01",
        "workspace_id": "ws_default_01",
        "name": "Proposal Drafter",
        "description": "Generates draft deliverables and content.",
        "created_by": "usr_alex",
        "visibility": "workspace",
        "default_purpose": "Draft proposals",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
}

_in_memory_delegations: Dict[str, dict] = {}
_in_memory_handoffs: Dict[str, dict] = {}

MAX_HANDOFF_DEPTH = 3
MAX_MISSION_HANDOFFS = 5

async def create_agent_definition(
    session: Optional[AsyncSession],
    workspace_id: str,
    name: str,
    description: str,
    created_by: str,
    visibility: str = "workspace",
    default_purpose: str = ""
) -> dict:
    def_id = f"def_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    agent_def = {
        "id": def_id,
        "workspace_id": workspace_id,
        "name": name,
        "description": description,
        "created_by": created_by,
        "visibility": visibility,
        "default_purpose": default_purpose,
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_definitions[def_id] = agent_def
    return agent_def

async def list_agent_definitions(session: Optional[AsyncSession], workspace_id: str, user_id: str) -> List[dict]:
    res = []
    for d in _in_memory_definitions.values():
        if d.get("workspace_id") != workspace_id or d.get("status") != "active":
            continue
        vis = d.get("visibility", "workspace")
        if vis == "workspace" or d.get("created_by") == user_id:
            res.append(d)
    return res

async def get_agent_definition(session: Optional[AsyncSession], workspace_id: str, def_id: str) -> Optional[dict]:
    d = _in_memory_definitions.get(def_id)
    if not d or d.get("workspace_id") != workspace_id:
        return None
    return d

async def create_delegation(
    session: Optional[AsyncSession],
    workspace_id: str,
    delegated_by: str,
    agent_id: str,
    mission_id: Optional[str] = None,
    scope: str = "mission",
    permissions: Optional[List[str]] = None,
    allowed_tools: Optional[List[str]] = None,
    allowed_resources: Optional[List[str]] = None,
    autonomy_level: str = "FULL_AUTONOMY",
    expires_at_iso: Optional[str] = None
) -> dict:
    # Privilege Escalation Prevention: Verify delegator permissions
    member = await workspace_service.get_workspace_member(session, workspace_id, delegated_by)
    if not member or member.get("status") != "active":
        raise ValueError("Delegator is not an active workspace member.")

    if member.get("role") == "viewer" and any(p in (permissions or []) for p in ["create_draft", "schedule_event", "update_draft"]):
        raise ValueError("Role 'viewer' cannot delegate write or administrative permissions.")

    del_id = f"del_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    if not expires_at_iso:
        expires_at_iso = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    delegation = {
        "id": del_id,
        "workspace_id": workspace_id,
        "delegated_by": delegated_by,
        "agent_id": agent_id,
        "mission_id": mission_id,
        "scope": scope,
        "permissions": permissions or ["read_context", "create_draft"],
        "allowed_tools": allowed_tools or [],
        "allowed_resources": allowed_resources or [],
        "autonomy_level": autonomy_level,
        "expires_at": expires_at_iso,
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_delegations[del_id] = delegation
    return delegation

async def list_delegations(session: Optional[AsyncSession], workspace_id: str, agent_id: Optional[str] = None) -> List[dict]:
    res = []
    for d in _in_memory_delegations.values():
        if d.get("workspace_id") != workspace_id:
            continue
        if agent_id and d.get("agent_id") != agent_id:
            continue
        res.append(d)
    return res

async def get_delegation(session: Optional[AsyncSession], del_id: str) -> Optional[dict]:
    return _in_memory_delegations.get(del_id)

async def revoke_delegation(session: Optional[AsyncSession], workspace_id: str, del_id: str, actor_id: str) -> dict:
    d = _in_memory_delegations.get(del_id)
    if not d or d.get("workspace_id") != workspace_id:
        raise ValueError("Delegation not found.")

    d["status"] = "revoked"
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    return d

async def pause_delegation(session: Optional[AsyncSession], workspace_id: str, del_id: str, actor_id: str) -> dict:
    d = _in_memory_delegations.get(del_id)
    if not d or d.get("workspace_id") != workspace_id:
        raise ValueError("Delegation not found.")

    d["status"] = "paused"
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    return d

async def renew_delegation(session: Optional[AsyncSession], workspace_id: str, del_id: str, actor_id: str, new_expires_at_iso: Optional[str] = None) -> dict:
    d = _in_memory_delegations.get(del_id)
    if not d or d.get("workspace_id") != workspace_id:
        raise ValueError("Delegation not found.")

    # Re-evaluate delegator active status
    member = await workspace_service.get_workspace_member(session, workspace_id, actor_id)
    if not member or member.get("status") != "active":
        raise ValueError("Delegator is not an active workspace member.")

    if not new_expires_at_iso:
        new_expires_at_iso = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    d["expires_at"] = new_expires_at_iso
    d["status"] = "active"
    d["updated_at"] = datetime.now(timezone.utc).isoformat()
    return d

async def create_agent_handoff(
    session: Optional[AsyncSession],
    workspace_id: str,
    source_agent_run_id: str,
    target_agent_definition_id: str,
    mission_id: str,
    scope: str = "mission",
    input_reference: Optional[dict] = None,
    current_depth: int = 1
) -> dict:
    # 1. Enforce Handoff Depth Limit
    if current_depth > MAX_HANDOFF_DEPTH:
        raise ValueError(f"Max agent handoff depth ({MAX_HANDOFF_DEPTH}) exceeded. Recursive spawning is blocked.")

    # 2. Enforce Max Active Mission Handoffs Limit
    mission_handoffs = [h for h in _in_memory_handoffs.values() if h.get("mission_id") == mission_id and h.get("status") in ["pending", "running"]]
    if len(mission_handoffs) >= MAX_MISSION_HANDOFFS:
        raise ValueError(f"Max active handoffs per mission ({MAX_MISSION_HANDOFFS}) reached.")

    handoff_id = f"ho_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    handoff = {
        "id": handoff_id,
        "source_agent_run_id": source_agent_run_id,
        "target_agent_definition_id": target_agent_definition_id,
        "mission_id": mission_id,
        "scope": scope,
        "input_reference": input_reference or {},
        "depth": current_depth,
        "status": "pending",
        "created_at": now_iso,
        "completed_at": None
    }
    _in_memory_handoffs[handoff_id] = handoff
    return handoff
