import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import AsyncSession

_in_memory_policy_rules: Dict[str, dict] = {}

DESTRUCTIVE_TOOLS = {"delete_file", "delete_memory", "send_gmail", "delete_workspace", "revoke_integration"}

@dataclass
class PolicyContext:
    workspace_id: str
    user_id: str
    tool_name: str
    agent_run_id: Optional[str] = None
    mission_id: Optional[str] = None
    tool_input: Optional[dict] = None
    risk_level: Optional[str] = "READ"
    autonomy_level: Optional[str] = "FULL_AUTONOMY"  # FULL_AUTONOMY, HUMAN_IN_THE_LOOP, ADVISORY_ONLY
    budget_state: Optional[dict] = None
    source_type: Optional[str] = None
    user_role: Optional[str] = "member"  # owner, admin, member, viewer
    user_status: Optional[str] = "active"  # active, suspended, invited, removed
    resource_scope: Optional[str] = "workspace"  # personal, workspace, shared, mission

@dataclass
class PolicyDecision:
    decision: str  # ALLOW, DENY, APPROVAL_REQUIRED
    risk_level: str
    reason: str
    required_approval_type: str = "NONE"  # NONE, USER_CONFIRMATION, ADMIN_APPROVAL
    rule_id: Optional[str] = None

async def evaluate_policy(session: Optional[AsyncSession], context: PolicyContext) -> PolicyDecision:
    """Central Policy Engine decision maker for AgentRuntime, ContextEngine, and ToolRegistry."""
    tool_name = context.tool_name
    risk_level = (context.risk_level or "READ").upper()
    user_role = context.user_role or "member"
    user_status = context.user_status or "active"

    # 1. Suspended User Check
    if user_status == "suspended":
        return PolicyDecision(
            decision="DENY",
            risk_level=risk_level,
            reason=f"User '{context.user_id}' is suspended from workspace '{context.workspace_id}'."
        )

    # 2. Destructive Tool Shielding
    if tool_name in DESTRUCTIVE_TOOLS or risk_level == "DESTRUCTIVE":
        return PolicyDecision(
            decision="DENY",
            risk_level="DESTRUCTIVE",
            reason=f"Tool '{tool_name}' is classified as DESTRUCTIVE and is strictly prohibited by system policy."
        )

    # 3. Personal Data Scope Isolation Check
    if context.resource_scope == "personal" and context.agent_run_id:
        # Personal data sources cannot be accessed by workspace agents without explicit user scope
        if context.source_type in ["personal_gmail", "personal_drive", "personal_calendar", "personal_memory"]:
            return PolicyDecision(
                decision="DENY",
                risk_level=risk_level,
                reason=f"Personal source '{context.source_type}' cannot be automatically accessed by workspace agent."
            )

    # 4. User Role Authorization Check
    if user_role == "viewer":
        if risk_level in ["WRITE", "EXTERNAL_SIDE_EFFECT"]:
            return PolicyDecision(
                decision="DENY",
                risk_level=risk_level,
                reason=f"User role 'viewer' is not authorized to execute WRITE or EXTERNAL_SIDE_EFFECT tool '{tool_name}'."
            )

    # 5. Budget & Loop Limits Check
    if context.budget_state:
        iters = context.budget_state.get("iteration_count", 0)
        max_iters = context.budget_state.get("max_iterations", 20)
        if iters >= max_iters:
            return PolicyDecision(
                decision="DENY",
                risk_level=risk_level,
                reason=f"Agent iteration limit ({max_iters}) reached."
            )

    # 6. Autonomy Mode Enforcement
    if context.autonomy_level == "ADVISORY_ONLY" and risk_level != "READ":
        return PolicyDecision(
            decision="DENY",
            risk_level=risk_level,
            reason="Agent runtime is operating in ADVISORY_ONLY mode. Side-effects and write actions are disabled."
        )

    # 7. Dynamic Policy Rules (Sorted by Priority)
    rules = [r for r in _in_memory_policy_rules.values() if r.get("workspace_id") == context.workspace_id and r.get("is_active")]
    rules.sort(key=lambda r: r.get("priority", 10), reverse=True)

    for rule in rules:
        conds = rule.get("conditions", {})
        c_risk = str(conds.get("risk_level", "")).upper()
        if conds.get("tool_name") == tool_name or (c_risk and c_risk == risk_level):
            return PolicyDecision(
                decision=rule["action"],
                risk_level=risk_level,
                reason=f"Triggered custom workspace policy rule '{rule['name']}'.",
                required_approval_type="USER_CONFIRMATION" if rule["action"] == "APPROVAL_REQUIRED" else "NONE",
                rule_id=rule["id"]
            )

    # 8. Default Tool Risk Matrix Policy
    if risk_level == "READ":
        return PolicyDecision(
            decision="ALLOW",
            risk_level="READ",
            reason=f"Tool '{tool_name}' is READ-only and pre-approved."
        )
    elif risk_level in ["WRITE", "EXTERNAL_SIDE_EFFECT"]:
        return PolicyDecision(
            decision="APPROVAL_REQUIRED",
            risk_level=risk_level,
            reason=f"Tool '{tool_name}' modifies external or workspace state ({risk_level}) and requires approval.",
            required_approval_type="USER_CONFIRMATION"
        )

    return PolicyDecision(
        decision="DENY",
        risk_level=risk_level,
        reason=f"Policy decision fell through to default security DENY."
    )

async def create_policy_rule(session: Optional[AsyncSession], workspace_id: str, name: str, action: str, conditions: dict, priority: int = 10) -> dict:
    rule_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    rule = {
        "id": rule_id,
        "workspace_id": workspace_id,
        "name": name,
        "action": action,
        "conditions": conditions,
        "is_active": True,
        "priority": priority,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_policy_rules[rule_id] = rule
    return rule

async def list_policy_rules(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    return [r for r in _in_memory_policy_rules.values() if r.get("workspace_id") == workspace_id]
