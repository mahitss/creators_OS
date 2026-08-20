import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import identity_service

_in_memory_members: Dict[str, dict] = {}
_in_memory_invitations: Dict[str, dict] = {}
_in_memory_mission_members: Dict[str, dict] = {}

VALID_ROLES = {"owner", "admin", "member", "viewer"}

async def get_workspace_member(session: Optional[AsyncSession], workspace_id: str, user_id: str) -> Optional[dict]:
    key = f"{workspace_id}_{user_id}"
    mem = _in_memory_members.get(key)
    if mem:
        return mem

    # Also check identity_service store
    id_mem = identity_service._in_memory_workspace_memberships.get(f"{user_id}:{workspace_id}")
    if id_mem and id_mem.get("status") == "active":
        mem_dict = {
            "id": id_mem.get("id", f"mem_{uuid.uuid4().hex[:6]}"),
            "workspace_id": workspace_id,
            "user_id": user_id,
            "email": f"{user_id}@vapor.internal",
            "role": id_mem.get("role", "member"),
            "status": id_mem.get("status", "active"),
            "joined_at": id_mem.get("created_at", datetime.now(timezone.utc).isoformat())
        }
        _in_memory_members[key] = mem_dict
        return mem_dict

    return None

async def list_workspace_members(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    # Aggregate from both stores
    members_map: Dict[str, dict] = {}
    for m in _in_memory_members.values():
        if m.get("workspace_id") == workspace_id and m.get("status") != "removed":
            members_map[m["user_id"]] = m

    for k, im in identity_service._in_memory_workspace_memberships.items():
        if im.get("workspace_id") == workspace_id and im.get("status") == "active":
            uid = im.get("user_id")
            if uid and uid not in members_map:
                members_map[uid] = {
                    "id": im.get("id", f"mem_{uuid.uuid4().hex[:6]}"),
                    "workspace_id": workspace_id,
                    "user_id": uid,
                    "email": f"{uid}@vapor.internal",
                    "role": im.get("role", "member"),
                    "status": "active",
                    "joined_at": im.get("created_at", datetime.now(timezone.utc).isoformat())
                }

    return list(members_map.values())

async def invite_workspace_member(session: Optional[AsyncSession], workspace_id: str, email: str, role: str, invited_by: str) -> dict:
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role '{role}'. Allowed: {list(VALID_ROLES)}")

    inv_id = f"inv_{uuid.uuid4().hex[:8]}"
    raw_token = uuid.uuid4().hex
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    now_iso = datetime.now(timezone.utc).isoformat()
    expires_at = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

    invitation = {
        "id": inv_id,
        "workspace_id": workspace_id,
        "email": email,
        "role": role,
        "invited_by": invited_by,
        "token_hash": token_hash,
        "raw_token_preview": raw_token,
        "status": "pending",
        "expires_at": expires_at,
        "created_at": now_iso
    }
    _in_memory_invitations[inv_id] = invitation
    return invitation

async def accept_workspace_invitation(session: Optional[AsyncSession], workspace_id: str, token: str, user_id: str) -> dict:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    inv = None
    for item in _in_memory_invitations.values():
        if item.get("token_hash") == token_hash and item.get("workspace_id") == workspace_id:
            inv = item
            break

    if not inv or inv.get("status") != "pending":
        raise ValueError("Invalid or expired invitation token.")

    inv["status"] = "accepted"
    key = f"{workspace_id}_{user_id}"
    now_iso = datetime.now(timezone.utc).isoformat()

    member = {
        "id": f"mem_{uuid.uuid4().hex[:6]}",
        "workspace_id": workspace_id,
        "user_id": user_id,
        "email": inv["email"],
        "role": inv["role"],
        "status": "active",
        "joined_at": now_iso
    }
    _in_memory_members[key] = member
    identity_service._in_memory_workspace_memberships[f"{user_id}:{workspace_id}"] = {
        "id": member["id"],
        "workspace_id": workspace_id,
        "user_id": user_id,
        "role": member["role"],
        "status": "active",
        "created_at": now_iso
    }
    return member

async def count_active_owners(workspace_id: str) -> int:
    active_in_mem = sum(1 for m in _in_memory_members.values() if m.get("workspace_id") == workspace_id and m.get("role") == "owner" and m.get("status") == "active")
    active_in_id = sum(1 for m in identity_service._in_memory_workspace_memberships.values() if m.get("workspace_id") == workspace_id and m.get("role") == "owner" and m.get("status") == "active")
    return max(active_in_mem, active_in_id)

async def update_member_role(session: Optional[AsyncSession], workspace_id: str, member_user_id: str, new_role: str, actor_id: str) -> dict:
    if new_role not in VALID_ROLES:
        raise ValueError(f"Invalid role '{new_role}'.")

    key = f"{workspace_id}_{member_user_id}"
    mem = _in_memory_members.get(key)
    if not mem:
        id_mem = identity_service._in_memory_workspace_memberships.get(f"{member_user_id}:{workspace_id}")
        if id_mem and id_mem.get("status") == "active":
            mem = {
                "id": id_mem.get("id", f"mem_{uuid.uuid4().hex[:6]}"),
                "workspace_id": workspace_id,
                "user_id": member_user_id,
                "email": f"{member_user_id}@vapor.internal",
                "role": id_mem.get("role", "member"),
                "status": "active",
                "joined_at": id_mem.get("created_at", datetime.now(timezone.utc).isoformat())
            }
            _in_memory_members[key] = mem

    if not mem:
        raise ValueError("Member not found in workspace.")

    # Last Owner Protection
    if mem["role"] == "owner" and new_role != "owner":
        owners_count = await count_active_owners(workspace_id)
        if owners_count <= 1:
            raise ValueError("Cannot demote the last owner of the workspace.")

    mem["role"] = new_role
    if f"{member_user_id}:{workspace_id}" in identity_service._in_memory_workspace_memberships:
        identity_service._in_memory_workspace_memberships[f"{member_user_id}:{workspace_id}"]["role"] = new_role
    return mem

async def suspend_workspace_member(session: Optional[AsyncSession], workspace_id: str, member_user_id: str, actor_id: str) -> dict:
    key = f"{workspace_id}_{member_user_id}"
    mem = _in_memory_members.get(key)
    if not mem:
        id_mem = identity_service._in_memory_workspace_memberships.get(f"{member_user_id}:{workspace_id}")
        if id_mem:
            mem = {
                "id": id_mem.get("id", f"mem_{uuid.uuid4().hex[:6]}"),
                "workspace_id": workspace_id,
                "user_id": member_user_id,
                "email": f"{member_user_id}@vapor.internal",
                "role": id_mem.get("role", "member"),
                "status": id_mem.get("status", "active"),
                "joined_at": id_mem.get("created_at", datetime.now(timezone.utc).isoformat())
            }
            _in_memory_members[key] = mem

    if not mem:
        raise ValueError("Member not found in workspace.")

    if mem["role"] == "owner":
        owners_count = await count_active_owners(workspace_id)
        if owners_count <= 1:
            raise ValueError("Cannot suspend the last owner of the workspace.")

    mem["status"] = "suspended"
    if f"{member_user_id}:{workspace_id}" in identity_service._in_memory_workspace_memberships:
        identity_service._in_memory_workspace_memberships[f"{member_user_id}:{workspace_id}"]["status"] = "suspended"
    return mem

async def remove_workspace_member(session: Optional[AsyncSession], workspace_id: str, member_user_id: str, actor_id: str) -> dict:
    key = f"{workspace_id}_{member_user_id}"
    mem = _in_memory_members.get(key)
    if not mem:
        id_mem = identity_service._in_memory_workspace_memberships.get(f"{member_user_id}:{workspace_id}")
        if id_mem:
            mem = {
                "id": id_mem.get("id", f"mem_{uuid.uuid4().hex[:6]}"),
                "workspace_id": workspace_id,
                "user_id": member_user_id,
                "email": f"{member_user_id}@vapor.internal",
                "role": id_mem.get("role", "member"),
                "status": id_mem.get("status", "active"),
                "joined_at": id_mem.get("created_at", datetime.now(timezone.utc).isoformat())
            }
            _in_memory_members[key] = mem

    if not mem:
        raise ValueError("Member not found in workspace.")

    if mem["role"] == "owner":
        owners_count = await count_active_owners(workspace_id)
        if owners_count <= 1:
            raise ValueError("Cannot remove the last owner of the workspace.")

    mem["status"] = "removed"
    if f"{member_user_id}:{workspace_id}" in identity_service._in_memory_workspace_memberships:
        identity_service._in_memory_workspace_memberships[f"{member_user_id}:{workspace_id}"]["status"] = "removed"
    return mem

async def add_mission_member(session: Optional[AsyncSession], mission_id: str, user_id: str, role: str = "contributor") -> dict:
    key = f"{mission_id}_{user_id}"
    m_mem = {
        "id": f"mm_{uuid.uuid4().hex[:6]}",
        "mission_id": mission_id,
        "user_id": user_id,
        "role": role,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_mission_members[key] = m_mem
    return m_mem

async def get_mission_member(session: Optional[AsyncSession], mission_id: str, user_id: str) -> Optional[dict]:
    key = f"{mission_id}_{user_id}"
    return _in_memory_mission_members.get(key)
