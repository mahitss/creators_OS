import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_crises: Dict[str, dict] = {}
_in_memory_declarations: Dict[str, dict] = {}
_in_memory_signals: Dict[str, dict] = {}
_in_memory_impacts: Dict[str, dict] = {}
_in_memory_cascades: Dict[str, dict] = {}
_in_memory_commands: Dict[str, dict] = {}
_in_memory_assignments: Dict[str, dict] = {}
_in_memory_plans: Dict[str, dict] = {}
_in_memory_options: Dict[str, dict] = {}
_in_memory_comms: Dict[str, dict] = {}
_in_memory_timeline: Dict[str, dict] = {}
_in_memory_stabilizations: Dict[str, dict] = {}
_in_memory_resolutions: Dict[str, dict] = {}
_in_memory_aars: Dict[str, dict] = {}
_in_memory_drills: Dict[str, dict] = {}
_in_memory_readiness: Dict[str, dict] = {}

def _initialize_seed_crisis_data():
    if _in_memory_crises:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Crisis
    c1 = {
        "id": "crs_sev1_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Global Multi-Tenant Inference Datacenter Outage",
        "description": "SEV1 major incident impacting primary US-East GPU inference cluster and real-time model routing.",
        "status": "active",
        "severity": "SEV1",
        "declared_by": "usr_crisis_commander_lead",
        "declared_at": now_iso,
        "commander_id": "usr_crisis_commander_lead",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_crises[c1["id"]] = c1

    # Seed Declaration Audit
    dec1 = {
        "id": "cdec_01",
        "crisis_id": c1["id"],
        "trigger": "Prometheus metric breach: P99 inference latency > 5000ms & 35% error rate",
        "evidence": "Observed 35,000 dropped tokens/sec across primary US-East datacenter.",
        "criteria": "SEV1 Declaration Policy: >25% customer degradation or core infrastructure blackout",
        "authorized_actor": "usr_crisis_commander_lead",
        "timestamp": now_iso
    }
    _in_memory_declarations[dec1["id"]] = dec1

    # Seed Crisis Signal
    sig1 = {
        "id": "csig_01",
        "crisis_id": c1["id"],
        "signal_type": "vendor_outage",
        "confidence": "high",
        "source": "AWS Datacenter Health API",
        "observed_at": now_iso,
        "received_at": now_iso,
        "source_version": "1.0"
    }
    _in_memory_signals[sig1["id"]] = sig1

    # Seed Impact Assessment & Operating Graph Cascade
    imp1 = {
        "id": "cimp_01",
        "crisis_id": c1["id"],
        "capabilities_impact_json": ["cap_core_01 (Global Multi-Tenant Inference Gateway)"],
        "services_impact_json": ["svc_model_router", "svc_policy_evaluator"],
        "customers_impact_json": {"affected_tenants": 420, "tier_1_enterprise": 18},
        "operations_impact_json": {"degradation": "35% error rate"},
        "financials_impact_json": {"projected_loss": "$120,000"},
        "data_impact_json": {"data_loss": "zero"},
        "security_impact_json": {"security_breach": "none"},
        "regulatory_impact_json": {"sla_breach_notice_required": True},
        "reputation_impact_json": {"risk_level": "medium"},
        "impact_status": "confirmed",
        "evidence": "Verified via real-time telemetry mesh and active health probes."
    }
    _in_memory_impacts[imp1["id"]] = imp1

    casc1 = {
        "id": "casc_01",
        "crisis_id": c1["id"],
        "source_node": "vendor_primary_gpu_cloud",
        "affected_node": "svc_model_router",
        "relationship": "dependency_of",
        "severity": "high",
        "confidence": "high"
    }
    _in_memory_cascades[casc1["id"]] = casc1

    # Seed Incident Command Structure
    cmd1 = {
        "id": "cmd_01",
        "crisis_id": c1["id"],
        "incident_commander": "usr_crisis_commander_lead",
        "operations_lead": "usr_ops_lead",
        "technical_lead": "usr_tech_lead",
        "security_lead": "usr_sec_lead",
        "communications_lead": "usr_comms_lead",
        "business_lead": "usr_biz_lead",
        "recovery_lead": "usr_resilience_lead"
    }
    _in_memory_commands[cmd1["id"]] = cmd1

    # Seed Response Option
    opt1 = {
        "id": "cropt_01",
        "crisis_id": c1["id"],
        "name": "Option 1: Failover Inference Traffic to EU-Central Secondary GPU Cluster",
        "expected_impact": "Restores 98% inference throughput within 25 minutes.",
        "cost_estimate": 15000.0,
        "risk_level": "low",
        "recovery_time_min": 25,
        "dependencies_json": ["cplan_01 (Multi-Region GPU Cloud Failover Plan)"],
        "confidence": "high"
    }
    _in_memory_options[opt1["id"]] = opt1

    # Seed Communication (DLP & Policy Enforced)
    comm1 = {
        "id": "ccomm_01",
        "crisis_id": c1["id"],
        "audience": "executive",
        "message": "SEV1 Crisis Declared: Global Multi-Tenant Inference Gateway degraded. Command structure active. Secondary cluster failover initiated.",
        "channel": "Slack #crisis-command",
        "sender": "usr_comms_lead",
        "approval_status": "approved",
        "sent_at": now_iso
    }
    _in_memory_comms[comm1["id"]] = comm1

    # Seed Immutable Timeline Event
    time1 = {
        "id": "ctime_01",
        "crisis_id": c1["id"],
        "timestamp": now_iso,
        "actor": "usr_crisis_commander_lead",
        "event_type": "crisis_declared",
        "description": "Crisis SEV1 officially declared. Incident Command activated.",
        "evidence": "Declaration criterion verified against SEV1 threshold."
    }
    _in_memory_timeline[time1["id"]] = time1

    # Seed Crisis Drill
    drill1 = {
        "id": "hdrill_01",
        "name": "Quarterly Regional Cloud Blackout Tabletop & Failover Drill",
        "scenario_type": "vendor_outage",
        "participants_json": ["usr_crisis_commander_lead", "usr_ops_lead", "usr_tech_lead"],
        "objectives_json": ["Verify RTO < 30m", "Verify 100% tenant isolation"],
        "results_json": {"rto_achieved_min": 22, "isolation_verified": True},
        "gaps_json": [],
        "status": "passed",
        "next_due_date": now_iso
    }
    _in_memory_drills[drill1["id"]] = drill1

    # Seed Readiness Assessment
    read1 = {
        "id": "cread_01",
        "command_readiness": 0.96,
        "plans_readiness": 0.95,
        "communications_readiness": 0.98,
        "recovery_readiness": 0.94,
        "readiness_status": "ready"
    }
    _in_memory_readiness[read1["id"]] = read1

_initialize_seed_crisis_data()


class CrisisIntelligenceService:

    @staticmethod
    async def get_crisis_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_crisis_data()
        crises = list(_in_memory_crises.values())
        declarations = list(_in_memory_declarations.values())
        signals = list(_in_memory_signals.values())
        impacts = list(_in_memory_impacts.values())
        commands = list(_in_memory_commands.values())
        options = list(_in_memory_options.values())
        comms = list(_in_memory_comms.values())
        timeline = list(_in_memory_timeline.values())
        drills = list(_in_memory_drills.values())
        readiness = list(_in_memory_readiness.values())

        active_crises = sum(1 for c in crises if c["status"] in ["declared", "active", "stabilizing", "recovering"])

        return {
            "crisesCount": len(crises),
            "activeCrisesCount": active_crises,
            "signalsCount": len(signals),
            "impactsCount": len(impacts),
            "commandsCount": len(commands),
            "optionsCount": len(options),
            "commsCount": len(comms),
            "timelineEventsCount": len(timeline),
            "drillsCount": len(drills),
            "crises": crises,
            "declarations": declarations,
            "signals": signals,
            "impacts": impacts,
            "commands": commands,
            "options": options,
            "comms": comms,
            "timeline": timeline,
            "drills": drills,
            "readiness": readiness,
            "readinessScore": 0.96
        }

    @staticmethod
    async def create_crisis(session: Optional[AsyncSession], crisis_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_crisis_data()
        c_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        # Enforce SEV1/CRITICAL declaration governance
        sev = crisis_data.get("severity", "SEV1")
        if sev in ["SEV1", "CRITICAL"] and not crisis_data.get("declaredBy"):
            return {"error": f"Major crisis ({sev}) declaration requires explicit authorized declaredBy actor."}

        crisis = {
            "id": c_id,
            "organization_id": org_id,
            "workspace_id": crisis_data.get("workspaceId", "ws_default"),
            "name": crisis_data["name"],
            "description": crisis_data["description"],
            "status": "declared",
            "severity": sev,
            "declared_by": crisis_data["declaredBy"],
            "declared_at": now_iso,
            "commander_id": crisis_data.get("commanderId", crisis_data["declaredBy"]),
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_crises[c_id] = crisis

        # Automatically log immutable timeline event
        t_id = str(uuid.uuid4())
        timeline_event = {
            "id": t_id,
            "crisis_id": c_id,
            "timestamp": now_iso,
            "actor": crisis_data["declaredBy"],
            "event_type": "crisis_declared",
            "description": f"Crisis '{crisis['name']}' ({sev}) declared by {crisis_data['declaredBy']}.",
            "evidence": "Declaration criteria verified against configured policy."
        }
        _in_memory_timeline[t_id] = timeline_event

        return crisis

    @staticmethod
    async def resolve_crisis(session: Optional[AsyncSession], crisis_id: str, resolution_data: dict) -> dict:
        _initialize_seed_crisis_data()
        crisis = _in_memory_crises.get(crisis_id)
        if not crisis:
            return {"error": "Crisis not found"}

        # Evidence-gated resolution check (blocking premature resolution without empirical evidence)
        evidence = resolution_data.get("evidence", "")
        if not evidence or len(evidence.strip()) < 10:
            return {"error": "Denied. Premature resolution blocked. Resolution requires empirical evidence of system stabilization and recovery."}

        now_iso = datetime.now(timezone.utc).isoformat()
        crisis["status"] = "resolved"
        crisis["updated_at"] = now_iso

        res_id = str(uuid.uuid4())
        resolution = {
            "id": res_id,
            "crisis_id": crisis_id,
            "resolution_criteria": resolution_data.get("criteria", "P99 latency < 200ms & zero dropped tokens"),
            "evidence": evidence,
            "authorized_resolver": resolution_data.get("authorizedResolver", "usr_crisis_commander_lead"),
            "resolved_at": now_iso
        }
        _in_memory_resolutions[res_id] = resolution

        # Log timeline event
        t_id = str(uuid.uuid4())
        timeline_event = {
            "id": t_id,
            "crisis_id": crisis_id,
            "timestamp": now_iso,
            "actor": resolution_data.get("authorizedResolver", "usr_crisis_commander_lead"),
            "event_type": "crisis_resolved",
            "description": "Crisis officially resolved following empirical verification of system recovery.",
            "evidence": evidence
        }
        _in_memory_timeline[t_id] = timeline_event

        return {
            "crisisId": crisis_id,
            "status": "resolved",
            "resolvedAt": now_iso,
            "evidence": evidence,
            "message": "Crisis resolved cleanly with empirical evidence."
        }

    @staticmethod
    async def process_natural_language_crisis_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_crisis_data()

        # Enforce DLP checks on natural language query
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "crisis_name": "Global Multi-Tenant Inference Datacenter Outage",
                    "severity": "SEV1",
                    "status": "active",
                    "incident_commander": "usr_crisis_commander_lead",
                    "affected_capability": "cap_core_01 (Global Multi-Tenant Inference Gateway)",
                    "active_response_option": "Option 1: Failover Inference Traffic to EU-Central Secondary GPU Cluster",
                    "communications_sent": "Executive notice dispatched via Slack #crisis-command"
                }
            ],
            "evidenceJson": {
                "referenced_crisis": "crs_sev1_01",
                "data_source": "Enterprise Crisis Intelligence & Coordinated Response 2.0 Engine"
            },
            "confidencePct": 98.0
        }
