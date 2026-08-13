import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_command_centers: Dict[str, dict] = {}
_in_memory_executive_states: Dict[str, dict] = {}
_in_memory_priority_items: Dict[str, dict] = {}
_in_memory_situations: Dict[str, dict] = {}
_in_memory_snapshots: Dict[str, dict] = {}
_in_memory_exposure_maps: Dict[str, dict] = {}
_in_memory_evidence_summaries: Dict[str, dict] = {}
_in_memory_unapplied_lessons: Dict[str, dict] = {}
_in_memory_decision_packets: Dict[str, dict] = {}

_EMITTED_COMMAND_CENTER_EVENTS: List[dict] = []

EMITTED_COMMAND_CENTER_EVENT_TYPES = [
    "transformation.resilience.command_center.created",
    "transformation.resilience.executive_state.updated",
    "transformation.resilience.priority.created",
    "transformation.resilience.situation.updated",
    "transformation.resilience.snapshot.created",
    "transformation.resilience.exposure.summary.updated",
    "transformation.resilience.systemic_risk.summary.updated",
    "transformation.resilience.scenario_health.updated",
    "transformation.resilience.assumption_health.updated",
    "transformation.resilience.recovery_readiness.updated",
    "transformation.resilience.investment_review.summary.updated",
    "transformation.resilience.decision_review.summary.updated",
    "transformation.resilience.evidence.summary.updated",
    "transformation.resilience.evidence.conflict.detected",
    "transformation.resilience.simulation.requested",
    "transformation.resilience.decision_packet.created",
    "transformation.resilience.unapplied_lesson.detected",
    "transformation.resilience.command_center.attention.updated"
]

def _initialize_seed_resilience_command_center_data():
    if _in_memory_command_centers:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Command Center
    cc1 = {
        "id": "cc_res_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Resilience Command Center 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Resilience Systems Architect",
        "status": "healthy",
        "last_evaluated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_command_centers[cc1["id"]] = cc1

    # Executive State (7 Dimensions)
    dims = [
        ("robustness", "stable", "improving", 0.94, 1.0, 14),
        ("redundancy", "attention", "stable", 0.91, 1.0, 10),
        ("recoverability", "stable", "improving", 0.95, 1.0, 16),
        ("adaptability", "stable", "improving", 0.92, 1.0, 11),
        ("optionality", "stable", "improving", 0.93, 1.0, 12),
        ("observability", "degraded", "deteriorating", 0.96, 0.98, 18),
        ("governability", "stable", "improving", 0.94, 1.0, 15)
    ]
    for dname, st, tr, conf, fr, evcount in dims:
        es_id = f"exec_st_{dname}"
        _in_memory_executive_states[es_id] = {
            "id": es_id,
            "command_center_id": cc1["id"],
            "dimension": dname,
            "state": st,
            "trend": tr,
            "confidence": conf,
            "freshness": fr,
            "evidence_count": evcount
        }

    # Priority Queue Items
    pitem1 = {
        "id": "pitem_01",
        "command_center_id": cc1["id"],
        "item_type": "systemic_risk",
        "priority": "critical",
        "title": "Shared IAM OAuth Gateway Bottleneck & Vendor SLA Drift",
        "impact_score": 0.94,
        "urgency_score": 0.91,
        "confidence": 0.95,
        "scope": "enterprise_waves_2_to_4",
        "reversibility": "high",
        "decision_deadline": "2026-Q3",
        "status": "active"
    }
    _in_memory_priority_items[pitem1["id"]] = pitem1

    # Situation & Snapshot
    sit1 = {
        "id": "sit_01",
        "command_center_id": cc1["id"],
        "summary": "Primary OAuth Auth Gateway SLA drifted from 99.99% to 99.91% while Senior IAM Engineers experience capacity contention.",
        "changes_json": ["Primary OAuth SLA Drift", "IAM Senior Engineer Capacity Bottleneck"],
        "affected_scope_json": ["wave_02_finops", "wave_03_sso", "wave_04_hr_cloud"],
        "evidence_json": {"latency_p99_ms": 142.5, "observation_reliability": 0.96},
        "uncertainty_json": {"unresolved_vendor_sla_dispute": True, "confidence": 0.94},
        "recommended_review": "Initiate Executive Decision Review for pinv_01 Active-Active deployment.",
        "created_at": now_iso
    }
    _in_memory_situations[sit1["id"]] = sit1

    snap1 = {
        "id": "snap_01",
        "command_center_id": cc1["id"],
        "timestamp": now_iso,
        "state_json": {"robustness": 0.94, "redundancy": 0.91, "observability": 0.96},
        "source_versions_json": {"sensing": "v2.0", "portfolio": "v2.0", "war_room": "v2.0"},
        "freshness": 1.0
    }
    _in_memory_snapshots[snap1["id"]] = snap1

    # Exposure Map & Evidence Summary
    expmap1 = {
        "id": "expmap_01",
        "command_center_id": cc1["id"],
        "transformation_id": "wave_02_finops",
        "dimension": "observability",
        "severity": "medium",
        "confidence": 0.95,
        "freshness": 1.0
    }
    _in_memory_exposure_maps[expmap1["id"]] = expmap1

    evsum1 = {
        "id": "evsum_01",
        "command_center_id": cc1["id"],
        "source_diversity_score": 0.92,
        "freshness_score": 0.98,
        "quality_score": 0.95,
        "has_conflicts": True,
        "conflicts_json": [
            {
                "source_a": "EventMesh.IdentityGateway",
                "source_b": "KPI.OAuthMonitor",
                "metric": "Gateway Latency P99",
                "conflict_description": "EventMesh reports 142.5ms latency; KPI Monitor reports 118.0ms due to different sampling windows."
            }
        ],
        "confidence": 0.94
    }
    _in_memory_evidence_summaries[evsum1["id"]] = evsum1

    # Unapplied Lesson
    uless1 = {
        "id": "uless_01",
        "command_center_id": cc1["id"],
        "lesson_title": "Multi-Cloud Fallback Route Delay Lesson (Sprint 70 Crisis Post-Mortem)",
        "affected_scope_json": ["wave_04_hr_cloud"],
        "reason_not_applied": "Pending Executive Board funding approval for pinv_01.",
        "recommended_review": "Accelerate pinv_01 funding review to eliminate single vendor lock-in.",
        "status": "unapplied"
    }
    _in_memory_unapplied_lessons[uless1["id"]] = uless1

    # Decision Packet
    dp1 = {
        "id": "dp_01",
        "command_center_id": cc1["id"],
        "title": "Cross-Portfolio Active-Active IAM Gateway Funding & Deployment Packet",
        "evidence_json": {"primary_sla": 99.91, "affected_transformations_count": 3},
        "scenario_results_json": {"robustness_improvement": "+5.0%", "payback": "Q3 2026"},
        "tradeoffs_json": {"cost": 350000.0, "risk_reduction": "65.0%"},
        "uncertainty_json": {"vendor_negotiation_range": "5-10%"},
        "recommendation": "Approve pinv_01 Active-Active IAM Gateway funding of $350k.",
        "alternatives_json": ["Option B: Rate Limiting Cluster Only ($150k)", "Option C: Do Nothing"],
        "required_approval": "PolicyEngine + Enterprise Executive Board",
        "created_at": now_iso
    }
    _in_memory_decision_packets[dp1["id"]] = dp1

_initialize_seed_resilience_command_center_data()


class TransformationResilienceCommandCenterService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_COMMAND_CENTER_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from approving, funding, executing, changing strategy, or changing governance
        forbidden_actions = [
            "approve", "fund", "execute", "change_strategy",
            "change_governance", "declare_emergency", "allocate_budget",
            "override_human_decision"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing non-read-only command center action '{action}'. Action requires PolicyEngine authorization + human executive approval."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_command_center_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_command_center_data()
        ccs = list(_in_memory_command_centers.values())
        exec_states = list(_in_memory_executive_states.values())
        priorities = list(_in_memory_priority_items.values())
        situations = list(_in_memory_situations.values())
        snapshots = list(_in_memory_snapshots.values())
        exposure_maps = list(_in_memory_exposure_maps.values())
        ev_summaries = list(_in_memory_evidence_summaries.values())
        unapplied_lessons = list(_in_memory_unapplied_lessons.values())
        decision_packets = list(_in_memory_decision_packets.values())

        return {
            "commandCentersCount": len(ccs),
            "executiveDimensionsCount": len(exec_states),
            "priorityItemsCount": len(priorities),
            "situationsCount": len(situations),
            "snapshotsCount": len(snapshots),
            "exposureMapsCount": len(exposure_maps),
            "unappliedLessonsCount": len(unapplied_lessons),
            "decisionPacketsCount": len(decision_packets),
            "commandCenters": ccs,
            "executiveStates": exec_states,
            "priorities": priorities,
            "situations": situations,
            "snapshots": snapshots,
            "exposureMaps": exposure_maps,
            "evidenceSummary": ev_summaries[0] if ev_summaries else {},
            "unappliedLessons": unapplied_lessons,
            "decisionPackets": decision_packets
        }

    @staticmethod
    async def trigger_simulation(session: Optional[AsyncSession], cc_id: str, data: dict) -> dict:
        _initialize_seed_resilience_command_center_data()
        sim_id = f"sim_req_{uuid.uuid4().hex[:8]}"
        res = {
            "id": sim_id,
            "command_center_id": cc_id,
            "trigger": data.get("trigger", "Manual What-If Trigger from Command Center"),
            "snapshot_id": data.get("snapshot_id", "snap_01"),
            "assumptions_json": data.get("assumptions_json", ["Primary OAuth Gateway SLA >= 99.99%"]),
            "scenario": data.get("scenario", "Compound Cloud Auth & Capacity Strain Scenario"),
            "model_version": "DigitalTwin_v2.0",
            "requested_question": data.get("requested_question", "What if OAuth latency increases by 50ms?"),
            "status": "completed",
            "simulated_robustness": 0.91,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        TransformationResilienceCommandCenterService.emit_event("transformation.resilience.simulation.requested", res)
        return res

    @staticmethod
    async def create_decision_packet(session: Optional[AsyncSession], cc_id: str, data: dict) -> dict:
        _initialize_seed_resilience_command_center_data()
        dp_id = f"dp_{uuid.uuid4().hex[:8]}"
        dp = {
            "id": dp_id,
            "command_center_id": cc_id,
            "title": data.get("title", "Executive Decision Packet"),
            "evidence_json": data.get("evidence_json", {"sla_drift": True}),
            "scenario_results_json": data.get("scenario_results_json", {"robustness_boost": "+5%"}),
            "tradeoffs_json": data.get("tradeoffs_json", {"cost": 350000.0}),
            "uncertainty_json": data.get("uncertainty_json", {"confidence": 0.94}),
            "recommendation": data.get("recommendation", "Approve pinv_01 Active-Active IAM Gateway funding."),
            "alternatives_json": data.get("alternatives_json", ["Option B: Rate Limiting Cluster Only", "Option C: Do Nothing"]),
            "required_approval": "PolicyEngine + Enterprise Executive Board",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_decision_packets[dp_id] = dp
        TransformationResilienceCommandCenterService.emit_event("transformation.resilience.decision_packet.created", dp)
        return dp

    @staticmethod
    async def process_natural_language_command_center_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_command_center_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking individual worker resilience scores or behavioral surveillance)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee resilience", "individual worker", "worker performance", "behavioral surveillance", "surveillance", "rank employee", "performance prediction"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual worker resilience scores or behavioral surveillance profiles."},
                "confidencePct": 0.0
            }

        # Enforce DLP checks
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Enforce Multi-Tenant Isolation
        if caller_org_id != "org_global_enterprise_01":
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "DENY. Organization tenant isolation breach detected."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "command_center": "Global Enterprise Transformation Resilience Command Center 2.0 (cc_res_01 - Status: HEALTHY)",
                    "executive_resilience_state": "Robustness: 94% (Stable), Redundancy: 91% (Attention), Recoverability: 95% (Stable), Adaptability: 92% (Stable), Optionality: 93% (Stable), Observability: 96% (Degraded), Governability: 94% (Stable)",
                    "top_priority_item": "CRITICAL: Shared IAM OAuth Gateway Bottleneck & Vendor SLA Drift (Impact: 94%, Urgency: 91%)",
                    "situation_summary": "Primary OAuth Auth Gateway SLA drifted from 99.99% to 99.91% while Senior IAM Engineers experience capacity contention.",
                    "evidence_summary": "High evidence quality (95% quality score, 98% freshness) with 1 visible conflict between EventMesh (142.5ms) and KPI Monitor (118ms).",
                    "unapplied_lesson": "Multi-Cloud Fallback Route Delay Lesson (Sprint 70 Crisis Post-Mortem) pending pinv_01 funding approval.",
                    "recommended_decision_packet": "Approve pinv_01 Active-Active IAM Gateway funding of $350k."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Command Center 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 98.5
        }
