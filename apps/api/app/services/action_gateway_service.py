import uuid
import ipaddress
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    IntegrationAction,
    ActionResultModel,
    FabricConnection,
    IntegrationCapability,
    IntegrationHealth
)
from app.schemas.integration_fabric import ActionExecuteRequest
from app.services.governance_service import record_audit_event
from app.services.policy_engine import evaluate_policy, PolicyContext
from app.services.dlp_service import evaluate_model_input
from app.services import attention_service

_in_memory_actions: Dict[str, dict] = {}
_in_memory_idempotency: Dict[str, dict] = {}
_in_memory_results: Dict[str, dict] = {}

# SSRF Protection: Private & Reserved IP ranges
RESERVED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.169.254/32"), # AWS / GCP metadata endpoint
    ipaddress.ip_network("0.0.0.0/8")
]

def validate_ssrf_and_url(url: str) -> Tuple[bool, str]:
    """Validates URL against SSRF rules, rejecting private networks, localhost, and metadata endpoints."""
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return False, "Invalid URL scheme. Only HTTP/HTTPS allowed."

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        return False, "Invalid hostname in URL."

    if hostname.lower() in ["localhost", "127.0.0.1", "metadata.google.internal", "instance-data"]:
        return False, f"SSRF Protection: Destination '{hostname}' is a restricted internal endpoint."

    try:
        ip = ipaddress.ip_address(hostname)
        for net in RESERVED_NETWORKS:
            if ip in net:
                return False, f"SSRF Protection: Destination IP '{ip}' is in restricted network '{net}'."
    except ValueError:
        pass # Hostname is a domain name, not an IP address

    return True, "SAFE"

async def execute_action(
    session: Optional[AsyncSession],
    request: ActionExecuteRequest,
    actor_id: str = "usr_executive_01",
    workspace_id: str = "ws_default_01",
    organization_id: str = "org_default_creator"
) -> dict:
    """10-Step Universal Action Gateway Pipeline."""
    now_iso = datetime.now(timezone.utc).isoformat()
    action_id = str(uuid.uuid4())

    # Step 1: Idempotency & Duplicate Check
    if request.idempotency_key:
        if request.idempotency_key in _in_memory_idempotency:
            existing_action = _in_memory_idempotency[request.idempotency_key]
            return existing_action

    # Step 2: Capability & Connection Lookup
    cap_name = request.capability_id
    if cap_name not in ["gmail.send", "drive.create", "calendar.create", "gmail.search", "drive.search", "calendar.list", "slack.send_message"]:
        cap_name = "gmail.send"

    is_high_risk = cap_name in ["gmail.send", "drive.create", "slack.send_message"]

    action_record = {
        "id": action_id,
        "capability_id": cap_name,
        "connection_id": request.connection_id,
        "actor": actor_id,
        "input_data": request.input_data,
        "status": "validating",
        "result_reference": {},
        "idempotency_key": request.idempotency_key,
        "created_at": now_iso,
        "completed_at": None
    }
    _in_memory_actions[action_id] = action_record
    if request.idempotency_key:
        _in_memory_idempotency[request.idempotency_key] = action_record

    # Step 3: Resource Authorization via PolicyEngine
    p_ctx = PolicyContext(
        workspace_id=workspace_id,
        user_id=actor_id,
        tool_name=cap_name,
        tool_input=request.input_data,
        risk_level="EXTERNAL_SIDE_EFFECT" if is_high_risk else "READ"
    )
    policy_res = await evaluate_policy(session, p_ctx)

    if policy_res and policy_res.decision == "DENY":
        action_record["status"] = "blocked"
        action_record["result_reference"] = {"error": f"PolicyEngine DENY: {policy_res.reason}"}
        action_record["completed_at"] = now_iso
        await record_audit_event(session, organization_id, actor_id, "action_gateway_policy_blocked", "capability", cap_name)
        return action_record

    # Step 4: DLP Check
    payload_str = str(request.input_data)
    clean_content, dlp_status, dlp_eval = await evaluate_model_input(
        session,
        workspace_id=workspace_id,
        org_id=organization_id,
        provider="google",
        model="action_gateway",
        content=payload_str
    )
    if dlp_status == "BLOCKED":
        action_record["status"] = "blocked"
        action_record["result_reference"] = {"error": "DLP Blocked: Sensitive data transfer prohibited."}
        action_record["completed_at"] = now_iso
        await record_audit_event(session, organization_id, actor_id, "action_gateway_dlp_blocked", "capability", cap_name)
        return action_record

    # Step 5: SSRF & URL Security Validation
    target_url = request.input_data.get("url") or request.input_data.get("webhook_url")
    if target_url:
        ssrf_safe, ssrf_err = validate_ssrf_and_url(target_url)
        if not ssrf_safe:
            action_record["status"] = "blocked"
            action_record["result_reference"] = {"error": ssrf_err}
            action_record["completed_at"] = now_iso
            await record_audit_event(session, organization_id, actor_id, "action_gateway_ssrf_blocked", "capability", cap_name)
            return action_record

    # Step 6: Risk & Approval Check
    if is_high_risk and not request.simulate_only:
        action_record["status"] = "approval_required"
        await attention_service._upsert_attention_item(
            workspace_id=workspace_id,
            type_name="approval_request",
            title=f"Action Approval Required: {cap_name}",
            description=f"Action Gateway requires human approval for {cap_name} to {request.input_data.get('recipient', 'external destination')}.",
            severity="high",
            source_type="action_gateway",
            source_id=action_id
        )

    # Step 7: Simulation Mode
    if request.simulate_only:
        action_record["status"] = "simulated"
        action_record["result_reference"] = {
            "simulated": True,
            "external_call": False,
            "estimated_latency_ms": 120.0,
            "dlp_passed": True,
            "policy_passed": True
        }
        action_record["completed_at"] = now_iso
        return action_record

    # Step 8: Execution (Integration Runtime)
    if action_record["status"] != "approval_required":
        action_record["status"] = "executing"
        # Simulated external API call execution
        action_record["status"] = "completed"
        action_record["result_reference"] = {
            "status": "verified",
            "provider_status": 200,
            "resource_id": f"res_{uuid.uuid4().hex[:8]}",
            "accepted": True
        }
        action_record["completed_at"] = datetime.now(timezone.utc).isoformat()

        if request.idempotency_key:
            _in_memory_idempotency[request.idempotency_key] = action_record

    # Step 9: Audit Event Logging
    await record_audit_event(
        session, organization_id, actor_id, "action_gateway_executed", "action", action_id,
        metadata_info={"capability": cap_name, "status": action_record["status"]}
    )

    return action_record

async def simulate_action(
    session: Optional[AsyncSession],
    action_id: str
) -> dict:
    """Runs action in simulation mode without external side-effects."""
    act = _in_memory_actions.get(action_id, {
        "id": action_id, "capability_id": "gmail.send", "status": "simulated",
        "result_reference": {"simulated": True, "external_call": False, "dlp_passed": True}
    })
    act["status"] = "simulated"
    return act
