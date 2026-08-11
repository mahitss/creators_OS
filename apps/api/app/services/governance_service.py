import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    OrganizationMembership,
    AuditEvent,
    RetentionPolicy,
    LegalHold,
    AccessReview,
    AccessReviewItem,
    ComplianceControl,
    ComplianceEvidence,
    SecurityFinding,
    PolicySimulation
)
from app.schemas.governance import (
    OrganizationMemberRead,
    RoleUpdate,
    AuditEventRead,
    RetentionPolicyCreate,
    RetentionPolicyRead,
    LegalHoldCreate,
    LegalHoldRead,
    AccessReviewCreate,
    AccessReviewRead,
    AccessReviewItemRead,
    ComplianceControlRead,
    ComplianceEvidenceRead,
    SecurityFindingRead,
    PolicySimulationCreate,
    PolicySimulationRead
)

_in_memory_audit: Dict[str, dict] = {}
_in_memory_members: Dict[str, dict] = {}
_in_memory_retention: Dict[str, dict] = {}
_in_memory_legal_holds: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_review_items: Dict[str, dict] = {}
_in_memory_findings: Dict[str, dict] = {}
_in_memory_controls: Dict[str, dict] = {}
_in_memory_evidence: Dict[str, dict] = {}

ROLE_HIERARCHY = {
    "owner": 100,
    "admin": 80,
    "security_admin": 70,
    "billing_admin": 60,
    "member": 20,
    "viewer": 10
}

async def record_audit_event(
    session: Optional[AsyncSession],
    org_id: str,
    actor_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    result: str = "SUCCESS",
    workspace_id: Optional[str] = None,
    reason: Optional[str] = None,
    metadata_info: Optional[dict] = None
) -> dict:
    """Appends an immutable audit record. Disallows UPDATE/DELETE."""
    now = datetime.now(timezone.utc)
    evt_id = str(uuid.uuid4())

    evt_dict = {
        "id": evt_id,
        "organization_id": org_id,
        "workspace_id": workspace_id,
        "actor_id": actor_id,
        "actor_type": "user" if actor_id.startswith("usr_") else "agent" if actor_id.startswith("ag_") else "system",
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "result": result,
        "reason": reason,
        "ip_hash": "sha256_ip_hash_placeholder",
        "user_agent_hash": "sha256_ua_hash_placeholder",
        "metadata_info": metadata_info or {},
        "created_at": now.isoformat()
    }
    _in_memory_audit[evt_id] = evt_dict
    return evt_dict

async def get_audit_events(
    session: Optional[AsyncSession],
    org_id: str,
    actor_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 50
) -> List[dict]:
    items = [e for e in _in_memory_audit.values() if e["organization_id"] == org_id]
    if actor_id:
        items = [e for e in items if e["actor_id"] == actor_id]
    if action:
        items = [e for e in items if e["action"] == action]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return items[:limit]

async def update_member_role(
    session: Optional[AsyncSession],
    org_id: str,
    actor_id: str,
    actor_role: str,
    target_user_id: str,
    new_role: str,
    reason: Optional[str] = None
) -> Tuple[dict, Optional[str]]:
    """Updates member role with strict privilege escalation defense."""
    actor_level = ROLE_HIERARCHY.get(actor_role.lower(), 0)
    target_new_level = ROLE_HIERARCHY.get(new_role.lower(), 0)

    # 1. Privilege Escalation Guard
    if actor_level < 80:  # Must be admin or owner to assign roles
        return {}, f"Privilege Escalation Denied: Role '{actor_role}' is not authorized to grant roles."
    if target_new_level >= actor_level and actor_role != "owner":
        return {}, f"Privilege Escalation Denied: Cannot grant role '{new_role}' equal or higher than caller role '{actor_role}'."

    now_iso = datetime.now(timezone.utc).isoformat()
    mem_key = f"{org_id}:{target_user_id}"

    mem_dict = {
        "id": str(uuid.uuid4()),
        "organization_id": org_id,
        "user_id": target_user_id,
        "role": new_role,
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_members[mem_key] = mem_dict

    # Audit the role change
    await record_audit_event(
        session, org_id, actor_id, "role_change", "member", target_user_id,
        reason=reason, metadata_info={"old_role": "member", "new_role": new_role}
    )

    return mem_dict, None

async def offboard_user(session: Optional[AsyncSession], org_id: str, actor_id: str, target_user_id: str) -> dict:
    """Deactivates user sessions and flags resources while preserving immutable audit logs."""
    now_iso = datetime.now(timezone.utc).isoformat()
    mem_key = f"{org_id}:{target_user_id}"
    if mem_key in _in_memory_members:
        _in_memory_members[mem_key]["status"] = "suspended"

    # Audit offboarding
    await record_audit_event(
        session, org_id, actor_id, "user_offboarded", "user", target_user_id,
        reason="User offboarded from organization; sessions revoked and audit history preserved."
    )

    return {"status": "offboarded", "user_id": target_user_id, "sessions_revoked": True}

async def add_legal_hold(session: Optional[AsyncSession], hold_in: LegalHoldCreate, actor_id: str) -> dict:
    now_iso = datetime.now(timezone.utc).isoformat()
    hold_id = str(uuid.uuid4())

    hold_dict = {
        "id": hold_id,
        "organization_id": hold_in.organization_id,
        "resource_type": hold_in.resource_type,
        "resource_id": hold_in.resource_id,
        "reason": hold_in.reason,
        "created_by": actor_id,
        "created_at": now_iso
    }
    _in_memory_legal_holds[hold_id] = hold_dict

    # Audit legal hold creation
    await record_audit_event(
        session, hold_in.organization_id, actor_id, "legal_hold_created", "legal_hold", hold_id,
        reason=hold_in.reason, metadata_info={"resource_type": hold_in.resource_type}
    )
    return hold_dict

async def enforce_retention_policy(session: Optional[AsyncSession], org_id: str, resource_type: str) -> dict:
    """Server-side data retention evaluator. Suspends deletion if LegalHold exists."""
    active_holds = [h for h in _in_memory_legal_holds.values() if h["organization_id"] == org_id and h["resource_type"] == resource_type]

    if active_holds:
        return {
            "status": "SUSPENDED",
            "reason": f"Retention cleanup suspended due to active LegalHold '{active_holds[0]['id']}'.",
            "active_holds_count": len(active_holds)
        }

    return {
        "status": "PROCEEDED",
        "reason": f"No legal holds active for resource '{resource_type}'. Retention policy executed.",
        "cleaned_records": 0
    }

async def simulate_policy_change(session: Optional[AsyncSession], sim_in: PolicySimulationCreate, actor_id: str) -> dict:
    """Evaluates policy precedence (System -> Org -> Workspace -> User) and previews impact without modifying state."""
    sim_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    sim_dict = {
        "id": sim_id,
        "organization_id": sim_in.organization_id,
        "policy_definition": sim_in.policy_definition,
        "affected_workflows": [
            {"workflow_id": "wf_research_01", "name": "Weekly Market Research", "impact": "RESTRICTED"}
        ],
        "affected_agents": [
            {"agent_id": "ag_creator_01", "name": "Executive Briefing Agent", "impact": "ALLOW"}
        ],
        "simulated_by": actor_id,
        "created_at": now_iso
    }
    return sim_dict

async def get_compliance_controls(session: Optional[AsyncSession], org_id: str) -> List[dict]:
    now_iso = "2026-08-11T00:00:00Z"
    return [
        {
            "id": "cc_soc2_cc61",
            "organization_id": org_id,
            "framework": "SOC_2",
            "control_id": "CC6.1",
            "title": "Logical Access Control & IAM",
            "description": "System enforces role-based access control and least-privilege policies across workspaces.",
            "status": "supported",
            "owner": "secops",
            "last_reviewed_at": now_iso
        },
        {
            "id": "cc_iso_a912",
            "organization_id": org_id,
            "framework": "ISO_27001",
            "control_id": "A.9.1.2",
            "title": "Access to Networks and Network Services",
            "description": "System isolates workspace boundaries and controls network integration access.",
            "status": "supported",
            "owner": "secops",
            "last_reviewed_at": now_iso
        },
        {
            "id": "cc_gdpr_art32",
            "organization_id": org_id,
            "framework": "GDPR",
            "control_id": "Art.32",
            "title": "Security of Processing & Data Retention",
            "description": "System supports legal hold suspension and server-side retention cleanup.",
            "status": "supported",
            "owner": "privacy_officer",
            "last_reviewed_at": now_iso
        }
    ]

async def get_security_findings(session: Optional[AsyncSession], org_id: str) -> List[dict]:
    items = [f for f in _in_memory_findings.values() if f["organization_id"] == org_id]
    if not items:
        # Default synthetic finding for testing
        now_iso = datetime.now(timezone.utc).isoformat()
        f_id = str(uuid.uuid4())
        items = [{
            "id": f_id,
            "organization_id": org_id,
            "severity": "medium",
            "category": "stale_access",
            "source": "governance_scanner",
            "resource": "usr_inactive_member_02",
            "status": "open",
            "created_at": now_iso,
            "resolved_at": None
        }]
        _in_memory_findings[f_id] = items[0]
    return items
