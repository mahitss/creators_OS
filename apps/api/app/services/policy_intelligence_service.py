import uuid
import asyncio
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.policy_intelligence import (
    PolicyCreate,
    PolicyRead,
    PolicyVersionRead,
    PolicyEvaluateRequest,
    PolicyEvaluateResponse,
    PolicyControlRead,
    RiskAssessmentRead,
    PolicyRequestRead,
    PolicyConflictRead,
    PolicyGapRead,
    PolicySimulationCreate,
    PolicySimulationRead,
    PolicyOverrideCreate,
    PolicyOverrideRead,
    TemporaryAccessGrantCreate,
    TemporaryAccessGrantRead,
    BreakGlassGrantCreate,
    BreakGlassGrantRead
)
from app.services import (
    dlp_service,
    governance_service,
    identity_service,
    workspace_service
)

_in_memory_policies: Dict[str, dict] = {}
_in_memory_policy_versions: Dict[str, List[dict]] = {}
_in_memory_evaluations: Dict[str, dict] = {}
_in_memory_requests: Dict[str, dict] = {}
_in_memory_conflicts: Dict[str, dict] = {}
_in_memory_gaps: Dict[str, dict] = {}
_in_memory_simulations: Dict[str, dict] = {}
_in_memory_overrides: Dict[str, dict] = {}
_in_memory_temp_grants: Dict[str, dict] = {}
_in_memory_breakglass_grants: Dict[str, dict] = {}
_policy_cache: Dict[str, dict] = {}

HIERARCHY_WEIGHTS = {
    "organization": 1000,
    "workspace": 800,
    "team": 600,
    "agent": 400,
    "mission": 200,
    "capability": 100
}

DESTRUCTIVE_ACTIONS = {"delete", "export", "deploy", "publish", "share"}

def _initialize_demo_policies_if_empty():
    if _in_memory_policies:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    org_id = "org_default_creator"

    # Seed Default Security Policy (Org Level)
    pol_sec_id = "pol_default_security_01"
    _in_memory_policies[pol_sec_id] = {
        "id": pol_sec_id,
        "organization_id": org_id,
        "workspace_id": None,
        "name": "Org Baseline Security Policy",
        "description": "Denies unauthorized bulk export and destructive actions across all workspaces",
        "policy_type": "security",
        "status": "active",
        "priority": 100,
        "version": 1,
        "hierarchy_level": "organization",
        "conditions": {
            "action_in": ["delete", "export"],
            "resource_type_in": ["database", "document", "knowledge_object"]
        },
        "actions": ["deny"],
        "created_at": now_iso,
        "updated_at": now_iso
    }

    # Seed Default Read Policy (Workspace Level)
    pol_read_id = "pol_default_read_01"
    _in_memory_policies[pol_read_id] = {
        "id": pol_read_id,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Workspace Standard Access Policy",
        "description": "Allows standard read operations for workspace members",
        "policy_type": "access",
        "status": "active",
        "priority": 80,
        "version": 1,
        "hierarchy_level": "workspace",
        "conditions": {
            "action_in": ["read"],
            "user_status": "active"
        },
        "actions": ["allow"],
        "created_at": now_iso,
        "updated_at": now_iso
    }

    # Seed Default Write/Execute Approval Policy (Workspace Level)
    pol_write_id = "pol_default_write_01"
    _in_memory_policies[pol_write_id] = {
        "id": pol_write_id,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Workspace Side-Effect Approval Policy",
        "description": "Requires approval for write, send, and execute actions on tools",
        "policy_type": "tool",
        "status": "active",
        "priority": 70,
        "version": 1,
        "hierarchy_level": "workspace",
        "conditions": {
            "action_in": ["write", "execute", "send"],
            "user_status": "active"
        },
        "actions": ["approval_required"],
        "created_at": now_iso,
        "updated_at": now_iso
    }

    # Seed Policy Gap
    gap_id = "gap_demo_01"
    _in_memory_gaps[gap_id] = {
        "id": gap_id,
        "action": "send",
        "resource_type": "email",
        "risk_level": "high",
        "frequency": 14,
        "recommended_control": "dual_approval",
        "status": "open"
    }

    # Seed Policy Conflict
    conf_id = "conf_demo_01"
    _in_memory_conflicts[conf_id] = {
        "id": conf_id,
        "policy_a_id": pol_sec_id,
        "policy_b_id": pol_read_id,
        "conflict_description": "Org baseline security denies export vs Workspace access allows bulk read export",
        "precedence_applied": "Explicit DENY from Org Baseline Security Policy (priority 100, org level)",
        "status": "resolved_deny_wins"
    }

_initialize_demo_policies_if_empty()

def _clear_cache():
    _policy_cache.clear()

async def create_policy(
    session: Optional[AsyncSession],
    workspace_id: Optional[str],
    user_id: str,
    req: PolicyCreate,
    organization_id: str = "org_default_creator"
) -> dict:
    """Creates a new policy draft or active policy."""
    _initialize_demo_policies_if_empty()
    p_id = f"pol_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    # Broad policy check
    if not req.conditions or req.conditions == {} or "allow_all" in req.conditions:
        req.conditions["broad_policy_flagged"] = True

    pol = {
        "id": p_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "name": req.name,
        "description": req.description,
        "policy_type": req.policy_type,
        "status": "active",
        "priority": req.priority,
        "version": 1,
        "hierarchy_level": req.hierarchy_level,
        "conditions": req.conditions,
        "actions": req.actions,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_policies[p_id] = pol

    # Version snapshot
    ver = {
        "id": f"pver_{uuid.uuid4().hex[:8]}",
        "policy_id": p_id,
        "version": 1,
        "name": req.name,
        "description": req.description,
        "conditions": req.conditions,
        "actions": req.actions,
        "priority": req.priority,
        "status": "active",
        "created_at": now_iso
    }
    _in_memory_policy_versions[p_id] = [ver]

    _clear_cache()
    return pol

async def evaluate_request(
    session: Optional[AsyncSession],
    req: PolicyEvaluateRequest,
    organization_id: str = "org_default_creator",
    workspace_id: str = "ws_default_01"
) -> dict:
    """Core Policy Engine 2.0 evaluation pipeline with deterministic precedence, risk scoring, and control chains."""
    start_t = time.time()
    _initialize_demo_policies_if_empty()
    req_id = f"preq_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    # Log request
    p_req = {
        "id": req_id,
        "request_id": req_id,
        "actor_id": req.actor_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "action": req.action.lower(),
        "resource_id": req.resource_id,
        "resource_type": req.resource_type.lower(),
        "context": req.context,
        "timestamp": now_iso
    }
    _in_memory_requests[req_id] = p_req

    # 1. Break-Glass / Active Temporary Access Check
    bg_active = [bg for bg in _in_memory_breakglass_grants.values() if bg["actor_id"] == req.actor_id and bg["status"] == "active"]
    if bg_active:
        bg = bg_active[0]
        exp_dt = datetime.fromisoformat(bg["expires_at"])
        if datetime.now(timezone.utc) < exp_dt:
            latency_ms = (time.time() - start_t) * 1000
            eval_res = {
                "request_id": req_id,
                "decision": "allow",
                "policy_references": ["break_glass_emergency_grant"],
                "controls": [{
                    "id": f"ctrl_{uuid.uuid4().hex[:8]}",
                    "evaluation_id": req_id,
                    "control_type": "time_limit",
                    "parameters": {"break_glass": True, "expires_at": bg["expires_at"]},
                    "status": "enforced"
                }],
                "risk_assessment": {
                    "id": f"risk_{uuid.uuid4().hex[:8]}",
                    "request_id": req_id,
                    "overall_risk_level": "high",
                    "data_risk": "high",
                    "financial_risk": "low",
                    "security_risk": "high",
                    "privacy_risk": "medium",
                    "operational_risk": "low",
                    "compliance_risk": "high",
                    "reputational_risk": "medium",
                    "score": 0.85
                },
                "reason": f"Emergency Break-Glass Grant active for actor '{req.actor_id}'. Full audit logging enforced.",
                "latency_ms": round(latency_ms, 2),
                "timestamp": now_iso
            }
            _in_memory_evaluations[req_id] = eval_res
            return eval_res

    # 2. Risk Classification
    act = req.action.lower()
    res_type = req.resource_type.lower()
    is_destructive = act in DESTRUCTIVE_ACTIONS or req.context.get("risk_level") == "critical"

    risk_level = "low"
    if is_destructive or res_type in ["database", "financial"]:
        risk_level = "high"
    elif act in ["write", "send", "execute"]:
        risk_level = "medium"

    risk_assess = {
        "id": f"risk_{uuid.uuid4().hex[:8]}",
        "request_id": req_id,
        "overall_risk_level": risk_level,
        "data_risk": "high" if res_type in ["database", "document"] else "low",
        "financial_risk": "high" if res_type == "financial" else "low",
        "security_risk": "high" if is_destructive else "low",
        "privacy_risk": "medium",
        "operational_risk": "medium" if act == "execute" else "low",
        "compliance_risk": "medium",
        "reputational_risk": "medium" if act == "send" else "low",
        "score": 0.85 if risk_level == "high" else 0.40 if risk_level == "medium" else 0.10
    }

    # 3. Policy Precedence & Hierarchy Evaluation
    active_policies = [p for p in _in_memory_policies.values() if p.get("status") == "active"]

    # Sort policies by (Hierarchy Level Weight DESC, Priority DESC)
    def policy_sort_key(p):
        h_weight = HIERARCHY_WEIGHTS.get(p.get("hierarchy_level", "workspace"), 500)
        return (h_weight, p.get("priority", 100))

    active_policies.sort(key=policy_sort_key, reverse=True)

    matched_policy = None
    final_decision = "deny"
    reason = "No matching policy allowed action. Default DENY enforced."
    controls = []
    matched_refs = []

    for pol in active_policies:
        conds = pol.get("conditions", {})
        actions_allowed = pol.get("actions", [])

        # Check action match
        act_match = False
        if "action_in" in conds:
            act_match = act in conds["action_in"]
        else:
            act_match = True

        # Check resource match
        res_match = False
        if "resource_type_in" in conds:
            res_match = res_type in conds["resource_type_in"]
        else:
            res_match = True

        if act_match and res_match:
            matched_policy = pol
            matched_refs.append(pol["id"])

            if "deny" in actions_allowed:
                final_decision = "deny"
                reason = f"Explicit DENY by policy '{pol['name']}' ({pol['hierarchy_level']} level, priority {pol['priority']})."
                break # Explicit DENY wins immediately
            elif "allow" in actions_allowed:
                final_decision = "allow"
                reason = f"Allowed by policy '{pol['name']}' ({pol['hierarchy_level']} level)."
                break
            elif "approval_required" in actions_allowed or "require_approval" in actions_allowed:
                final_decision = "approval_required"
                reason = f"Policy '{pol['name']}' requires human approval."
                controls.append({
                    "id": f"ctrl_{uuid.uuid4().hex[:8]}",
                    "evaluation_id": req_id,
                    "control_type": "approval",
                    "parameters": {"approval_type": "user_confirmation"},
                    "status": "enforced"
                })
                break

    # High-Risk / Destructive Safeguard (Forces approval_required if low-level policy allowed high risk)
    if is_destructive and final_decision == "allow":
        final_decision = "approval_required"
        reason = f"Action '{act}' on '{res_type}' is high-risk. High-risk safety policy mandates human approval."
        controls.append({
            "id": f"ctrl_{uuid.uuid4().hex[:8]}",
            "evaluation_id": req_id,
            "control_type": "human_review",
            "parameters": {"risk_level": risk_level},
            "status": "enforced"
        })

    # Policy Gap Detection
    if not matched_policy and risk_level in ["medium", "high"]:
        gap_id = f"gap_{uuid.uuid4().hex[:8]}"
        _in_memory_gaps[gap_id] = {
            "id": gap_id,
            "action": act,
            "resource_type": res_type,
            "risk_level": risk_level,
            "frequency": 1,
            "recommended_control": "approval_required",
            "status": "open"
        }

    latency_ms = (time.time() - start_t) * 1000

    eval_res = {
        "request_id": req_id,
        "decision": final_decision,
        "policy_references": matched_refs,
        "controls": controls,
        "risk_assessment": risk_assess,
        "reason": reason,
        "latency_ms": round(latency_ms, 2),
        "timestamp": now_iso
    }

    _in_memory_evaluations[req_id] = eval_res
    return eval_res

async def create_breakglass_grant(
    session: Optional[AsyncSession],
    req: BreakGlassGrantCreate,
    authorized_by: str
) -> dict:
    """Grants emergency Break-Glass access with explicit audit trail and expiration."""
    _initialize_demo_policies_if_empty()
    bg_id = f"bg_{uuid.uuid4().hex[:8]}"
    now_dt = datetime.now(timezone.utc)
    exp_dt = now_dt + timedelta(minutes=req.duration_minutes)

    bg = {
        "id": bg_id,
        "actor_id": req.actor_id,
        "reason": req.reason,
        "authorized_by": authorized_by,
        "starts_at": now_dt.isoformat(),
        "expires_at": exp_dt.isoformat(),
        "audit_trail_id": f"audit_bg_{uuid.uuid4().hex[:8]}",
        "status": "active"
    }
    _in_memory_breakglass_grants[bg_id] = bg
    _clear_cache()
    return bg

async def list_policies(session: Optional[AsyncSession], workspace_id: Optional[str] = None) -> List[dict]:
    _initialize_demo_policies_if_empty()
    if workspace_id:
        return [p for p in _in_memory_policies.values() if p["workspace_id"] == workspace_id or p["workspace_id"] is None]
    return list(_in_memory_policies.values())

async def get_policy_by_id(session: Optional[AsyncSession], policy_id: str) -> Optional[dict]:
    _initialize_demo_policies_if_empty()
    return _in_memory_policies.get(policy_id)

async def list_conflicts(session: Optional[AsyncSession]) -> List[dict]:
    _initialize_demo_policies_if_empty()
    return list(_in_memory_conflicts.values())

async def list_gaps(session: Optional[AsyncSession]) -> List[dict]:
    _initialize_demo_policies_if_empty()
    return list(_in_memory_gaps.values())

async def list_overrides(session: Optional[AsyncSession]) -> List[dict]:
    _initialize_demo_policies_if_empty()
    return list(_in_memory_overrides.values())
