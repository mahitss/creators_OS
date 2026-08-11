import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.security_fabric_service import SecurityFabricService

_in_memory_plans: Dict[str, dict] = {}
_in_memory_plan_actions: Dict[str, dict] = {}
_in_memory_detection_rules: Dict[str, dict] = {}
_in_memory_automation_rules: Dict[str, dict] = {}
_in_memory_runbooks: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_slas: Dict[str, dict] = {}
_in_memory_notes: Dict[str, dict] = {}
_in_memory_response_locks: Dict[str, str] = {}
_automation_execution_counts: Dict[str, int] = {}
_emitted_secops_events: List[dict] = []

def _initialize_demo_secops_data():
    if _in_memory_detection_rules:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    inc_id = "inc_demo_01"

    # Seed Runbook
    rb_id = "rb_prompt_inj_01"
    _in_memory_runbooks[rb_id] = {
        "id": rb_id,
        "name": "Standard Indirect Prompt Injection Response",
        "trigger_condition": "event_type == 'prompt_injection'",
        "investigation_steps_json": [
            "1. Inspect untrusted source document for instruction boundary override",
            "2. Audit agent execution log for unauthorized tool calls",
            "3. Verify DLP exfiltration boundary status"
        ],
        "approved_responses_json": ["quarantine_agent", "pause_mission", "revalidate_decision"],
        "verification_steps_json": [
            "1. Confirm untrusted document context is purged",
            "2. Verify agent baseline telemetry returned to normal"
        ],
        "version": 1,
        "status": "active",
        "created_at": now_iso
    }

    # Seed Detection Rule
    dr_id = "dr_bulk_exfil_01"
    _in_memory_detection_rules[dr_id] = {
        "id": dr_id,
        "name": "Unusual Data Exfiltration Spike",
        "description": "Detects agent transferring over 100MB of sensitive document data within 1 minute",
        "conditions_json": {"data_volume_bytes_gt": 104857600, "resource_scope": "restricted"},
        "severity": "critical",
        "scope": "global",
        "status": "active",
        "version": 1,
        "created_at": now_iso
    }

    # Seed Automation Rule
    ar_id = "ar_auto_quarantine_01"
    _in_memory_automation_rules[ar_id] = {
        "id": ar_id,
        "name": "Auto-Quarantine High Confidence Injection Agent",
        "trigger_event_type": "prompt_injection",
        "condition_json": {"confidence_gte": 0.90},
        "response_action_type": "quarantine",
        "scope": "workspace",
        "max_actions": 5,
        "cooldown_seconds": 300,
        "approval_required": True,
        "status": "active",
        "created_at": now_iso
    }

    # Seed Response Plan
    plan_id = "plan_demo_01"
    act_id = "act_demo_01"
    _in_memory_plans[plan_id] = {
        "id": plan_id,
        "incident_id": inc_id,
        "version": 1,
        "status": "approved",
        "risk_level": "high",
        "approval_requirements": ["sec_admin_01"],
        "created_at": now_iso,
        "action_ids": [act_id]
    }

    _in_memory_plan_actions[act_id] = {
        "id": act_id,
        "plan_id": plan_id,
        "action_type": "quarantine",
        "target_type": "agent",
        "target_id": "agent_analyst_01",
        "scope": "workspace",
        "reason": "Indirect prompt injection detected in Vendor Quote ingestion pipeline",
        "authorization": "security_policy",
        "status": "completed",
        "expires_at": None
    }

    # Seed SLA
    sla_id = "sla_demo_01"
    _in_memory_slas[sla_id] = {
        "id": sla_id,
        "incident_id": inc_id,
        "time_to_detect_seconds": 30.0,
        "time_to_triage_seconds": 90.0,
        "time_to_contain_seconds": 240.0,
        "time_to_recover_seconds": 1200.0,
        "sla_breached": False,
        "created_at": now_iso
    }

_initialize_demo_secops_data()


class SecOpsService:

    @staticmethod
    def _emit_event(event_type: str, data: dict):
        _emitted_secops_events.append({
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    @staticmethod
    async def get_operations_dashboard(session: Optional[AsyncSession]) -> dict:
        _initialize_demo_secops_data()
        incidents = await SecurityFabricService.get_incidents(session, "org_default_creator")
        threats = await SecurityFabricService.get_threats(session)
        quarantines = await SecurityFabricService.get_quarantines(session, "active")

        active_incidents = [i for i in incidents if i.get("status") not in ["closed", "resolved"]]
        critical_threats = [t for t in threats if t.get("severity") in ["high", "critical"]]
        active_plans = [p for p in _in_memory_plans.values() if p.get("status") in ["approved", "executing"]]
        breached_slas = [s for s in _in_memory_slas.values() if s.get("sla_breached")]

        return {
            "activeIncidentsCount": len(active_incidents),
            "criticalThreatsCount": len(critical_threats),
            "activeResponsePlansCount": len(active_plans),
            "quarantinedResourcesCount": len(quarantines),
            "breachedSLACount": len(breached_slas),
            "activeDetectionRulesCount": len([r for r in _in_memory_detection_rules.values() if r.get("status") == "active"]),
            "incidents": active_incidents,
            "responsePlans": list(_in_memory_plans.values()),
            "threatIntelligenceCount": len(await SecurityFabricService.get_threat_intel(session))
        }

    @staticmethod
    async def generate_response_plan(session: Optional[AsyncSession], incident_id: str, payload: dict) -> dict:
        _initialize_demo_secops_data()
        plan_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        req_approvals = ["sec_admin_01"]
        if payload.get("riskLevel") == "critical":
            req_approvals.append("ciso_dual_approval_02")

        action_records = []
        act_ids = []
        for act in payload.get("actions", []):
            a_id = str(uuid.uuid4())
            action_rec = {
                "id": a_id,
                "plan_id": plan_id,
                "action_type": act.get("actionType", "monitor"),
                "target_type": act.get("targetType", "agent"),
                "target_id": act.get("targetId", "agent_unspecified"),
                "scope": act.get("scope", "resource"),
                "reason": act.get("reason", "SecOps Automated Response"),
                "authorization": act.get("authorization", "security_policy"),
                "status": "pending",
                "expires_at": act.get("expiresAt")
            }
            _in_memory_plan_actions[a_id] = action_rec
            action_records.append(action_rec)
            act_ids.append(a_id)

        plan = {
            "id": plan_id,
            "incident_id": incident_id,
            "version": 1,
            "status": "draft",
            "risk_level": payload.get("riskLevel", "high"),
            "approval_requirements": req_approvals,
            "created_at": now_iso,
            "action_ids": act_ids
        }
        _in_memory_plans[plan_id] = plan

        SecOpsService._emit_event("security.response.created", {"plan_id": plan_id, "incident_id": incident_id})
        return {**plan, "actions": action_records}

    @staticmethod
    async def simulate_response_plan(session: Optional[AsyncSession], plan_id: str) -> dict:
        _initialize_demo_secops_data()
        plan = _in_memory_plans.get(plan_id)
        if not plan:
            return {"error": f"Response plan '{plan_id}' not found"}

        plan["status"] = "simulated"
        actions = [_in_memory_plan_actions[aid] for aid in plan.get("action_ids", []) if aid in _in_memory_plan_actions]

        return {
            "plan_id": plan_id,
            "simulation_result": "SUCCESS",
            "production_impact": "NONE (Dry Run)",
            "affected_components_count": len(actions),
            "simulated_actions": actions
        }

    @staticmethod
    async def approve_response_plan(session: Optional[AsyncSession], plan_id: str, approver_id: str) -> dict:
        _initialize_demo_secops_data()
        plan = _in_memory_plans.get(plan_id)
        if not plan:
            return {"error": f"Response plan '{plan_id}' not found"}

        plan["status"] = "approved"
        for aid in plan.get("action_ids", []):
            if aid in _in_memory_plan_actions:
                _in_memory_plan_actions[aid]["status"] = "approved"

        SecOpsService._emit_event("security.response.approved", {"plan_id": plan_id, "approved_by": approver_id})
        return plan

    @staticmethod
    async def execute_response_plan(session: Optional[AsyncSession], plan_id: str) -> dict:
        _initialize_demo_secops_data()
        plan = _in_memory_plans.get(plan_id)
        if not plan:
            return {"error": f"Response plan '{plan_id}' not found"}

        # Response Lock to prevent race conditions
        lock_key = f"lock_plan_{plan_id}"
        if lock_key in _in_memory_response_locks:
            return {"status": "blocked", "reason": "Response execution lock already active"}
        _in_memory_response_locks[lock_key] = datetime.now(timezone.utc).isoformat()

        try:
            plan["status"] = "executing"
            SecOpsService._emit_event("security.response.started", {"plan_id": plan_id})

            actions = [_in_memory_plan_actions[aid] for aid in plan.get("action_ids", []) if aid in _in_memory_plan_actions]
            for act in actions:
                # If quarantine action, call SecurityFabricService.quarantine_target
                if act["action_type"] == "quarantine":
                    await SecurityFabricService.quarantine_target(session, {
                        "targetType": act["target_type"],
                        "targetId": act["target_id"],
                        "reason": act["reason"],
                        "scope": act["scope"],
                        "createdBy": "secops_service"
                    })
                act["status"] = "completed"

            plan["status"] = "completed"
            SecOpsService._emit_event("security.response.completed", {"plan_id": plan_id})
            return plan
        finally:
            _in_memory_response_locks.pop(lock_key, None)

    @staticmethod
    async def verify_recovery(session: Optional[AsyncSession], incident_id: str) -> dict:
        _initialize_demo_secops_data()
        incidents = await SecurityFabricService.get_incidents(session, "org_default_creator")
        for i in incidents:
            if i["id"] == incident_id:
                i["status"] = "recovering"
                SecOpsService._emit_event("security.incident.resolved", {"incident_id": incident_id})
                return {
                    "incident_id": incident_id,
                    "status": "recovering",
                    "verification_result": "PASS",
                    "security_signals_cleared": True,
                    "behavior_normal": True
                }
        return {"error": f"Incident '{incident_id}' not found"}

    @staticmethod
    async def close_incident_secops(session: Optional[AsyncSession], incident_id: str) -> dict:
        _initialize_demo_secops_data()
        incidents = await SecurityFabricService.get_incidents(session, "org_default_creator")
        for i in incidents:
            if i["id"] == incident_id:
                i["status"] = "closed"
                i["resolved_at"] = datetime.now(timezone.utc).isoformat()
                SecOpsService._emit_event("security.incident.closed", {"incident_id": incident_id})
                return i
        return {"error": f"Incident '{incident_id}' not found"}

    @staticmethod
    async def create_detection_rule(session: Optional[AsyncSession], rule_data: dict) -> dict:
        _initialize_demo_secops_data()
        dr_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": dr_id,
            "name": rule_data.get("name", "Custom Detection Rule"),
            "description": rule_data.get("description", ""),
            "conditions_json": rule_data.get("conditionsJson", {}),
            "severity": rule_data.get("severity", "high"),
            "scope": rule_data.get("scope", "global"),
            "status": "shadow", # Shadow mode by default
            "version": 1,
            "created_at": now_iso
        }
        _in_memory_detection_rules[dr_id] = record
        SecOpsService._emit_event("security.detection.changed", {"rule_id": dr_id, "status": "shadow"})
        return record

    @staticmethod
    async def get_detection_rules(session: Optional[AsyncSession]) -> List[dict]:
        _initialize_demo_secops_data()
        return list(_in_memory_detection_rules.values())

    @staticmethod
    async def activate_detection_rule(session: Optional[AsyncSession], rule_id: str) -> Optional[dict]:
        _initialize_demo_secops_data()
        r = _in_memory_detection_rules.get(rule_id)
        if not r:
            return None
        r["status"] = "active"
        SecOpsService._emit_event("security.detection.changed", {"rule_id": rule_id, "status": "active"})
        return r

    @staticmethod
    async def create_automation_rule(session: Optional[AsyncSession], auto_data: dict) -> dict:
        _initialize_demo_secops_data()
        ar_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": ar_id,
            "name": auto_data.get("name", "Automation Rule"),
            "trigger_event_type": auto_data.get("triggerEventType", "prompt_injection"),
            "condition_json": auto_data.get("conditionJson", {}),
            "response_action_type": auto_data.get("responseActionType", "quarantine"),
            "scope": auto_data.get("scope", "workspace"),
            "max_actions": auto_data.get("maxActions", 5),
            "cooldown_seconds": auto_data.get("cooldownSeconds", 300),
            "approval_required": auto_data.get("approvalRequired", True),
            "status": "active",
            "created_at": now_iso
        }
        _in_memory_automation_rules[ar_id] = record
        return record

    @staticmethod
    async def get_automation_rules(session: Optional[AsyncSession]) -> List[dict]:
        _initialize_demo_secops_data()
        return list(_in_memory_automation_rules.values())

    @staticmethod
    async def create_runbook(session: Optional[AsyncSession], rb_data: dict) -> dict:
        _initialize_demo_secops_data()
        rb_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        record = {
            "id": rb_id,
            "name": rb_data.get("name", "Custom Security Runbook"),
            "trigger_condition": rb_data.get("triggerCondition", "true"),
            "investigation_steps_json": rb_data.get("investigationStepsJson", []),
            "approved_responses_json": rb_data.get("approvedResponsesJson", []),
            "verification_steps_json": rb_data.get("verificationStepsJson", []),
            "version": 1,
            "status": "active",
            "created_at": now_iso
        }
        _in_memory_runbooks[rb_id] = record
        return record

    @staticmethod
    async def get_runbooks(session: Optional[AsyncSession]) -> List[dict]:
        _initialize_demo_secops_data()
        return list(_in_memory_runbooks.values())
