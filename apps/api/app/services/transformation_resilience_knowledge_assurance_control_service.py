import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_adaptive_domains: Dict[str, dict] = {}
_in_memory_plan_baselines: Dict[str, dict] = {}
_in_memory_change_signals: Dict[str, dict] = {}
_in_memory_change_detections: Dict[str, dict] = {}
_in_memory_assumption_impacts: Dict[str, dict] = {}
_in_memory_plan_impacts: Dict[str, dict] = {}
_in_memory_plan_healths: Dict[str, dict] = {}
_in_memory_plan_stalenesses: Dict[str, dict] = {}
_in_memory_replan_triggers: Dict[str, dict] = {}
_in_memory_replan_recommendations: Dict[str, dict] = {}
_in_memory_plan_versions: Dict[str, dict] = {}
_in_memory_plan_diffs: Dict[str, dict] = {}
_in_memory_replan_queues: Dict[str, dict] = {}
_in_memory_emergency_replans: Dict[str, dict] = {}
_in_memory_cross_plan_impacts: Dict[str, dict] = {}
_in_memory_portfolio_drifts: Dict[str, dict] = {}

_EMITTED_CONTROL_EVENTS: List[dict] = []

EMITTED_CONTROL_EVENT_TYPES = [
    "transformation.resilience.knowledge.adaptive_assurance.domain.created",
    "transformation.resilience.knowledge.assurance.plan.baselined",
    "transformation.resilience.knowledge.assurance.change_signal.detected",
    "transformation.resilience.knowledge.assurance.change.assessed",
    "transformation.resilience.knowledge.assurance.assumption.impact.detected",
    "transformation.resilience.knowledge.assurance.plan.impact.detected",
    "transformation.resilience.knowledge.assurance.plan.health.updated",
    "transformation.resilience.knowledge.assurance.plan.staleness.detected",
    "transformation.resilience.knowledge.assurance.replan.triggered",
    "transformation.resilience.knowledge.assurance.replan.option.created",
    "transformation.resilience.knowledge.assurance.replan.simulated",
    "transformation.resilience.knowledge.assurance.replan.recommended",
    "transformation.resilience.knowledge.assurance.plan.version.created",
    "transformation.resilience.knowledge.assurance.plan.diff.created",
    "transformation.resilience.knowledge.assurance.plan.approval.requested",
    "transformation.resilience.knowledge.assurance.plan.approved",
    "transformation.resilience.knowledge.assurance.plan.execution.started",
    "transformation.resilience.knowledge.assurance.plan.execution.paused",
    "transformation.resilience.knowledge.assurance.plan.execution.completed",
    "transformation.resilience.knowledge.assurance.cross_plan.impact.detected",
    "transformation.resilience.knowledge.assurance.portfolio.drift.detected",
    "transformation.resilience.knowledge.assurance.emergency_replan.triggered",
    "transformation.resilience.knowledge.assurance.plan.verified",
    "transformation.resilience.knowledge.assurance.plan.learning.created"
]

def _initialize_seed_resilience_control_data():
    if _in_memory_adaptive_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"
    plan_id = "aplan_01"

    # Adaptive Domain
    adom1 = {
        "id": "adom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Adaptive Knowledge Assurance & Continuous Replanning Control 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Adaptive Assurance Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_adaptive_domains[adom1["id"]] = adom1

    # Plan Baseline (V1.0 Immutable Snapshot)
    base1 = {
        "id": "abase_01",
        "plan_id": plan_id,
        "plan_version": "v1.0",
        "assumptions_json": ["Third-party monitoring vendor API remains accessible."],
        "risks_json": ["rcase_01", "rcase_overdue_01"],
        "capacity_json": {"specialists": 0.75, "simulations": 0.90},
        "sequence_json": ["aopt_01"],
        "options_json": [{"id": "aopt_01", "title": "Parallel Synthetic Telemetry"}],
        "residual_risk": 0.08,
        "approval_state": "approved",
        "created_at": now_iso
    }
    _in_memory_plan_baselines[base1["id"]] = base1

    # Change Signal & Detection
    sig1 = {
        "id": "csig_01",
        "source": "resilience_sensing",
        "change_type": "dependency_change",
        "significance": "material",
        "description": "Secondary Cloud Interconnect SLA shifted from 99.99% to 99.90% following Q3 infrastructure update.",
        "created_at": now_iso
    }
    _in_memory_change_signals[sig1["id"]] = sig1

    cdet1 = {
        "id": "cdet_01",
        "signal_id": sig1["id"],
        "plan_id": plan_id,
        "affected_assumptions_json": ["Third-party monitoring vendor API remains accessible."],
        "affected_risks_json": ["rcase_01"],
        "affected_actions_json": ["aopt_01"],
        "confidence": 0.94,
        "detected_at": now_iso
    }
    _in_memory_change_detections[cdet1["id"]] = cdet1

    # Assumption & Plan Impact
    aimp1 = {
        "id": "aimp_01",
        "plan_id": plan_id,
        "assumption": "Third-party monitoring vendor API remains accessible.",
        "previous_state": "Stable 99.99% interconnect",
        "current_state": "Degraded 99.90% interconnect with periodic latency spikes",
        "impact": "Synthetic telemetry packets require 2x retry buffer.",
        "confidence": 0.92,
        "created_at": now_iso
    }
    _in_memory_assumption_impacts[aimp1["id"]] = aimp1

    pimp1 = {
        "id": "pimp_01",
        "plan_id": plan_id,
        "risk_impact": "Cloud SLA uncertainty increased by 12%",
        "sequence_impact": "Requires synthetic retry buffer preceding revalidation packet submission",
        "capacity_impact": "Simulation compute workload increased by 10%",
        "coverage_impact": "Coverage reduced from 92% to 84% without retry buffer",
        "residual_risk_impact": "Residual risk increased from 8% to 16%",
        "severity": "material"
    }
    _in_memory_plan_impacts[pimp1["id"]] = pimp1

    # Plan Health (Separate Factors, No Collapse Score)
    phealth1 = {
        "id": "phealth_01",
        "plan_id": plan_id,
        "risk_alignment": 0.92,
        "evidence_alignment": 0.88,
        "capacity_alignment": 0.75,
        "sequence_alignment": 0.90,
        "deadline_alignment": 0.95,
        "assumption_alignment": 0.80,
        "created_at": now_iso
    }
    _in_memory_plan_healths[phealth1["id"]] = phealth1

    # Staleness & Replan Trigger
    stale1 = {
        "id": "pstale_01",
        "plan_id": plan_id,
        "status": "materially_stale",
        "outdated_assumptions_json": ["Third-party monitoring vendor API remains accessible."],
        "outdated_evidence_json": ["Interconnect SLA v1.0"],
        "changed_dependencies_json": ["Secondary Cloud SLA Gateway"]
    }
    _in_memory_plan_stalenesses[stale1["id"]] = stale1

    trig1 = {
        "id": "rtrig_01",
        "plan_id": plan_id,
        "trigger_type": "material_plan_impact",
        "description": "Secondary Cloud Interconnect SLA change invalidated V1.0 assumptions.",
        "status": "open",
        "triggered_at": now_iso
    }
    _in_memory_replan_triggers[trig1["id"]] = trig1

    rec1 = {
        "id": "rrec_01",
        "plan_id": plan_id,
        "label": "ANALYTICAL RECOMMENDATION — NOT APPROVAL",
        "recommended_option": "resequence",
        "reason": "Resequence synthetic telemetry execution to add 2x retry buffer prior to Governance submission.",
        "tradeoffs": "Increases execution duration by 2 days; restores risk coverage to 92%.",
        "confidence": 0.94
    }
    _in_memory_replan_recommendations[rec1["id"]] = rec1

    # Plan Versions & Diff
    ver1 = {
        "id": "pver_v1",
        "plan_id": plan_id,
        "version_number": "v1.0",
        "parent_version": "root",
        "change_summary": "Initial approved multi-region cloud SLA assurance plan.",
        "reason": "Baseline release",
        "approval_state": "approved",
        "created_at": now_iso
    }
    _in_memory_plan_versions[ver1["id"]] = ver1

    ver2 = {
        "id": "pver_v2",
        "plan_id": plan_id,
        "version_number": "v2.0",
        "parent_version": "v1.0",
        "change_summary": "Adaptive resequencing adding 2x synthetic retry buffer.",
        "reason": "Remediate interconnect SLA degradation.",
        "approval_state": "approved",
        "created_at": now_iso
    }
    _in_memory_plan_versions[ver2["id"]] = ver2

    pdiff1 = {
        "id": "pdiff_01",
        "plan_id": plan_id,
        "from_version": "v1.0",
        "to_version": "v2.0",
        "added_risks_json": ["Interconnect retry buffer telemetry gap"],
        "removed_risks_json": [],
        "reordered_actions_json": ["aopt_retry_buffer", "aopt_01"],
        "changed_assumptions_json": ["Vendor API retry threshold adjusted to 2000ms"],
        "created_at": now_iso
    }
    _in_memory_plan_diffs[pdiff1["id"]] = pdiff1

    # Replan Queue & Emergency Replans
    qitem1 = {
        "id": "pqueue_01",
        "plan_id": plan_id,
        "trigger_type": "material_plan_impact",
        "severity": "material",
        "priority": 1,
        "recommended_action": "resequence",
        "approval_requirement": "approval_required"
    }
    _in_memory_replan_queues[qitem1["id"]] = qitem1

    emg1 = {
        "id": "emg_01",
        "plan_id": "aplan_critical_99",
        "trigger_reason": "Complete secondary cloud provider regional outage.",
        "status": "active",
        "war_room_session_id": "war_room_resilience_01",
        "created_at": now_iso
    }
    _in_memory_emergency_replans[emg1["id"]] = emg1

    # Cross-Plan Impact & Portfolio Drift
    cplan1 = {
        "id": "cpimp_01",
        "source_plan_id": plan_id,
        "affected_plan_id": "aplan_hr_cloud_02",
        "impact_description": "Resequencing cloud SLA assurance delays HR Cloud Wave 4 validation by 2 days.",
        "severity": "material",
        "recommended_action": "resequence_affected_plan"
    }
    _in_memory_cross_plan_impacts[cplan1["id"]] = cplan1

    pdrift1 = {
        "id": "pdrift_01",
        "risk_drift": 0.12,
        "capacity_drift": 0.15,
        "evidence_drift": 0.08,
        "dependency_drift": 0.10,
        "created_at": now_iso
    }
    _in_memory_portfolio_drifts[pdrift1["id"]] = pdrift1

_initialize_seed_resilience_control_data()


class TransformationResilienceKnowledgeAssuranceControlService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_CONTROL_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may monitor signals, detect staleness, analyze impact, generate replan options, run simulations, prepare diffs, prepare approval packets, and monitor execution
        # Agents may NOT approve replans, change approved plans directly, accept material risk, bypass governance, or execute material actions without authorization
        forbidden_actions = [
            "approve_replan", "modify_approved_plan_directly", "accept_material_risk",
            "bypass_governance", "execute_material_actions_unauthorized"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing adaptive assurance control action '{action}'. Modifying approved plans or approving replans requires human governance authority."
            }
        return {"allowed": True, "reason": "Action permitted for adaptive knowledge assurance agent."}

    @staticmethod
    async def get_knowledge_assurance_control_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_control_data()
        domains = list(_in_memory_adaptive_domains.values())
        baselines = list(_in_memory_plan_baselines.values())
        signals = list(_in_memory_change_signals.values())
        detections = list(_in_memory_change_detections.values())
        assumption_impacts = list(_in_memory_assumption_impacts.values())
        plan_impacts = list(_in_memory_plan_impacts.values())
        healths = list(_in_memory_plan_healths.values())
        stalenesses = list(_in_memory_plan_stalenesses.values())
        triggers = list(_in_memory_replan_triggers.values())
        recommendations = list(_in_memory_replan_recommendations.values())
        versions = list(_in_memory_plan_versions.values())
        diffs = list(_in_memory_plan_diffs.values())
        queues = list(_in_memory_replan_queues.values())
        emergencies = list(_in_memory_emergency_replans.values())
        cross_impacts = list(_in_memory_cross_plan_impacts.values())
        drifts = list(_in_memory_portfolio_drifts.values())

        stale_cnt = sum(1 for s in stalenesses if s.get("status") in ["stale", "materially_stale"])

        return {
            "domainsCount": len(domains),
            "baselinesCount": len(baselines),
            "signalsCount": len(signals),
            "stalePlansCount": stale_cnt,
            "replanTriggersCount": len(triggers),
            "planVersionsCount": len(versions),
            "emergencyReplansCount": len(emergencies),
            "crossPlanImpactsCount": len(cross_impacts),
            "portfolioDriftPct": "12.0% Risk Drift | 15.0% Capacity Drift",
            "domains": domains,
            "baselines": baselines,
            "signals": signals,
            "detections": detections,
            "assumptionImpacts": assumption_impacts,
            "planImpacts": plan_impacts,
            "healths": healths,
            "stalenesses": stalenesses,
            "triggers": triggers,
            "recommendations": recommendations,
            "versions": versions,
            "diffs": diffs,
            "queues": queues,
            "emergencies": emergencies,
            "crossImpacts": cross_impacts,
            "drifts": drifts
        }

    @staticmethod
    async def create_plan_version(session: Optional[AsyncSession], plan_id: str, data: dict) -> dict:
        _initialize_seed_resilience_control_data()
        ver_id = f"pver_{uuid.uuid4().hex[:8]}"
        ver = {
            "id": ver_id,
            "plan_id": plan_id,
            "version_number": data.get("version_number", "v2.0"),
            "parent_version": data.get("parent_version", "v1.0"),
            "change_summary": data.get("change_summary", "Adaptive resequencing based on change signals"),
            "reason": data.get("reason", "Dependency change remediation"),
            "approval_state": "pending_approval",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_plan_versions[ver_id] = ver

        # Create Plan Diff
        diff_id = f"pdiff_{uuid.uuid4().hex[:8]}"
        diff = {
            "id": diff_id,
            "plan_id": plan_id,
            "from_version": ver["parent_version"],
            "to_version": ver["version_number"],
            "added_risks_json": data.get("added_risks_json", ["Secondary Cloud Retry Gap"]),
            "removed_risks_json": [],
            "reordered_actions_json": data.get("reordered_actions_json", ["retry_buffer", "synthetic_test"]),
            "changed_assumptions_json": data.get("changed_assumptions_json", ["Retry threshold 2000ms"]),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_plan_diffs[diff_id] = diff

        TransformationResilienceKnowledgeAssuranceControlService.emit_event(
            "transformation.resilience.knowledge.assurance.plan.version.created", ver
        )
        TransformationResilienceKnowledgeAssuranceControlService.emit_event(
            "transformation.resilience.knowledge.assurance.plan.diff.created", diff
        )
        return {"version": ver, "diff": diff}

    @staticmethod
    async def execute_plan_version(session: Optional[AsyncSession], plan_id: str, version_id: str) -> dict:
        _initialize_seed_resilience_control_data()
        stale_item = next((s for s in _in_memory_plan_stalenesses.values() if s.get("plan_id") == plan_id), None)

        # Stale Execution Protection
        if stale_item and stale_item.get("status") == "materially_stale":
            TransformationResilienceKnowledgeAssuranceControlService.emit_event(
                "transformation.resilience.knowledge.assurance.plan.execution.paused",
                {"plan_id": plan_id, "reason": "Plan is materially stale. Paused execution per policy."}
            )
            return {
                "plan_id": plan_id,
                "version_id": version_id,
                "execution_status": "paused",
                "reason": "Stale Execution Protection triggered: Plan is materially stale. Paused execution pending human review."
            }

        TransformationResilienceKnowledgeAssuranceControlService.emit_event(
            "transformation.resilience.knowledge.assurance.plan.execution.started",
            {"plan_id": plan_id, "version_id": version_id}
        )
        return {
            "plan_id": plan_id,
            "version_id": version_id,
            "execution_status": "executing",
            "action_gateway_routed": True
        }

    @staticmethod
    async def trigger_emergency_replan(session: Optional[AsyncSession], plan_id: str, data: dict) -> dict:
        _initialize_seed_resilience_control_data()
        emg_id = f"emg_{uuid.uuid4().hex[:8]}"
        emg = {
            "id": emg_id,
            "plan_id": plan_id,
            "trigger_reason": data.get("trigger_reason", "Critical external shock or dependency failure"),
            "status": "active",
            "war_room_session_id": "war_room_resilience_01",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_emergency_replans[emg_id] = emg

        TransformationResilienceKnowledgeAssuranceControlService.emit_event(
            "transformation.resilience.knowledge.assurance.emergency_replan.triggered", emg
        )
        return emg

    @staticmethod
    async def process_natural_language_assurance_control_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_control_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking employee adaptive-performance scores, individual worker rankings, or behavioral surveillance)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee adaptive-performance score", "individual worker ranking", "behavioral surveillance",
            "surveil worker", "rank employee", "performance score"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee adaptive-performance scores, worker rankings, or behavioral surveillance."},
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
                    "stale_plans": "Plan 'aplan_01' (Multi-Region Cloud SLA Assurance) is materially stale due to Secondary Cloud Interconnect SLA shift.",
                    "what_changed": "Change Signal 'csig_01': Interconnect SLA shifted from 99.99% to 99.90% with latency spikes.",
                    "assumptions_affected": "Assumption 'Third-party monitoring vendor API remains accessible' requires retry buffer adjustment.",
                    "replan_recommendation": "Recommended Option: Resequence Plan V1.0 to V2.0 adding 2x synthetic retry buffer (Coverage restored to 92%).",
                    "baseline_comparison": "Continue Current Plan V1.0 yields 84% coverage vs Resequencing V2.0 yields 92% coverage.",
                    "version_notice": "Approved Plan V1.0 preserved as immutable baseline. Plan V2.0 requires human governance approval.",
                    "stale_execution_notice": "Stale Execution Protection active. Execution paused pending human review."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Adaptive Knowledge Assurance & Replanning Control 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
