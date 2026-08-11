import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_war_rooms: Dict[str, dict] = {}
_in_memory_live_states: Dict[str, dict] = {}
_in_memory_plan_variances: Dict[str, dict] = {}
_in_memory_deviations: Dict[str, dict] = {}
_in_memory_root_cause_hypotheses: Dict[str, dict] = {}
_in_memory_impact_assessments: Dict[str, dict] = {}
_in_memory_intervention_options: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_escalations: Dict[str, dict] = {}
_in_memory_response_plans: Dict[str, dict] = {}
_in_memory_checkpoints: Dict[str, dict] = {}
_in_memory_trajectories: Dict[str, dict] = {}
_in_memory_early_warnings: Dict[str, dict] = {}
_in_memory_situation_summaries: Dict[str, dict] = {}

def _initialize_seed_war_room_data():
    if _in_memory_war_rooms:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    next_check_iso = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # War Room & Live State
    wr1 = {
        "id": "wr_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Transformation Operations War Room",
        "scope": "enterprise",
        "owner": "Chief Transformation Officer",
        "status": "attention",
        "priority": "high",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_war_rooms[wr1["id"]] = wr1

    ls1 = {
        "id": "ls_01",
        "war_room_id": wr1["id"],
        "milestones_json": {"active_milestones": 24, "delayed_milestones": 2},
        "dependencies_json": {"critical_dependencies": 18, "bottlenecked_dependencies": 1},
        "risks_json": {"high_risks": 3, "mitigated_risks": 12},
        "benefits_json": {"target_q4_benefits_millions": 5.4, "realized_q4_benefits_millions": 4.2},
        "capacity_json": {"available_fte": 140, "capacity_utilization_pct": 89.2},
        "governance_json": {"active_controls": 8, "approval_backlog_hours": 48.0},
        "kpis_json": {"on_time_wave_delivery_pct": 91.8},
        "source_versions_json": {"control_tower": "v2.0", "event_mesh": "v2.0", "digital_twin": "v2.0"},
        "last_updated": now_iso,
        "staleness_status": "fresh"
    }
    _in_memory_live_states[ls1["id"]] = ls1

    # Plan Variance & Deviation
    pv1 = {
        "id": "pv_01",
        "war_room_id": wr1["id"],
        "variance_type": "schedule",
        "planned_summary": "Wave 2 completion scheduled for Q3 2026",
        "actual_summary": "Wave 2 execution 14 days behind schedule",
        "forecast_summary": "Wave 2 forecast delivery pushed to Q4 2026 without intervention",
        "severity": "medium"
    }
    _in_memory_plan_variances[pv1["id"]] = pv1

    dev1 = {
        "id": "dev_01",
        "war_room_id": wr1["id"],
        "entity": "Wave 2 FinOps Migration",
        "metric": "Execution Schedule (Days)",
        "expected_value": 0.0,
        "actual_value": -14.0,
        "variance_value": -14.0,
        "severity": "high",
        "confidence": 0.95
    }
    _in_memory_deviations[dev1["id"]] = dev1

    # Root Cause Hypothesis & Live Impact Assessment
    rc1 = {
        "id": "rc_01",
        "war_room_id": wr1["id"],
        "deviation_id": dev1["id"],
        "hypothesis_text": "Manual CISO review queue backlog (48h delay) coupled with 15 FTE capacity shortfall in Core IAM integration team",
        "evidence_json": {"governance_friction_hours": 48.0, "capacity_shortfall_fte": 15},
        "confidence": 0.88,
        "alternative_explanations_json": ["Third-party API vendor gateway rate limiting", "Unexpected database migration schema mismatch"]
    }
    _in_memory_root_cause_hypotheses[rc1["id"]] = rc1

    imp1 = {
        "id": "imp_01",
        "war_room_id": wr1["id"],
        "affected_transformations_json": ["Wave 2 FinOps Migration", "Global IAM Single Sign-On Wave 3"],
        "affected_capabilities_json": ["Cloud FinOps Governance", "Identity Access Automation"],
        "affected_dependencies_json": ["Core IAM API Gateway v2"],
        "affected_benefits_json": ["Q4 $1.2M FinOps cost optimization delay"],
        "affected_risks_json": ["Increased compliance exposure during migration window"],
        "strategic_impact": "High. Threatens Q4 enterprise cloud cost reduction targets if unmitigated."
    }
    _in_memory_impact_assessments[imp1["id"]] = imp1

    # Intervention Options & Recommendation
    io1 = {
        "id": "io_01",
        "war_room_id": wr1["id"],
        "intervention_type": "resequence",
        "title": "Delegate Regional Pilot Approvals & Reallocate 15 FTEs from Wave 3",
        "description": "Simulated intervention: Reduces governance latency by 36 hours and accelerates Wave 2 path by 14 days.",
        "safety_score": 0.92,
        "reversibility_score": 0.90,
        "blast_radius_json": {"direct_impact": "Wave 2 accelerated 14 days", "downstream_impact": "Wave 3 start delayed 30 days"},
        "status": "recommended"
    }
    _in_memory_intervention_options[io1["id"]] = io1

    rec1 = {
        "id": "rec_01",
        "war_room_id": wr1["id"],
        "recommended_option_id": io1["id"],
        "evidence_summary": "Digital Twin simulation sim_run_01 confirms 14-day schedule recovery with zero policy breach risk",
        "risk_summary": "Wave 3 start delayed by 30 days ($150k cost impact, optionality score 0.88)",
        "uncertainty_level": "low",
        "alternatives_json": ["Do nothing (14-day slip)", "Outsource IAM tasks ($350k cost)"]
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    # Escalation, Response Plan, Checkpoints, Trajectory, Warning, Summary
    esc1 = {
        "id": "esc_wr_01",
        "war_room_id": wr1["id"],
        "trigger_reason": "Wave 2 schedule variance exceeds 10-day threshold",
        "escalation_path": "Transformation Steering Committee",
        "priority": "high",
        "status": "acknowledged"
    }
    _in_memory_escalations[esc1["id"]] = esc1

    rp1 = {
        "id": "rp_01",
        "war_room_id": wr1["id"],
        "title": "Wave 2 Schedule Recovery & Governance Acceleration Plan",
        "signal_summary": "14-day schedule slip in Wave 2 FinOps migration",
        "assessment_summary": "Capacity shortage + CISO review backlog causing milestone delay",
        "options_summary": "Option 1: Delegate regional approvals + FTE reallocation (Recommended)",
        "decision_summary": "Awaiting Steering Committee approval",
        "status": "awaiting_approval"
    }
    _in_memory_response_plans[rp1["id"]] = rp1

    cp1 = {
        "id": "cp_01",
        "response_plan_id": rp1["id"],
        "checkpoint_name": "Post-Delegation Verification Checkpoint",
        "expected_state": "Governance backlog reduced to < 12 hours",
        "actual_state": "Pending execution",
        "next_checkpoint": next_check_iso,
        "owner": "Chief Information Officer",
        "status": "pending"
    }
    _in_memory_checkpoints[cp1["id"]] = cp1

    traj1 = {
        "id": "traj_01",
        "war_room_id": wr1["id"],
        "metric": "Wave 2 Delivery Trajectory",
        "trajectory_data_json": {"current_day_offset": -14, "simulated_intervention_offset": 0},
        "time_horizon": "Q4 2026",
        "scenario": "baseline",
        "confidence": 0.94
    }
    _in_memory_trajectories[traj1["id"]] = traj1

    ew1 = {
        "id": "ew_01",
        "war_room_id": wr1["id"],
        "signal_name": "IAM Integration Queue Pressure Early Warning",
        "signal_strength": 0.88,
        "historical_reliability": 0.92,
        "model_confidence": 0.95,
        "status": "active"
    }
    _in_memory_early_warnings[ew1["id"]] = ew1

    sit1 = {
        "id": "sit_01",
        "war_room_id": wr1["id"],
        "what_changed": "Wave 2 FinOps migration schedule slipped by 14 days due to IAM capacity bottleneck & CISO review backlog.",
        "why_it_matters": "Threatens Q4 $1.2M cloud benefit realization if not mitigated within 14 days.",
        "affected_areas_json": ["Wave 2 FinOps", "Wave 3 IAM", "Q4 Cloud Benefits"],
        "uncertainty_summary": "Low uncertainty. Simulation sim_run_01 confirms 94% confidence in 14-day schedule recovery under recommended intervention.",
        "recommended_review": "Steering Committee review required to approve Governance CR-01 & FTE reallocation.",
        "created_at": now_iso
    }
    _in_memory_situation_summaries[sit1["id"]] = sit1

_initialize_seed_war_room_data()


class TransformationWarRoomService:

    @staticmethod
    async def get_war_room_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_war_room_data()
        war_rooms = list(_in_memory_war_rooms.values())
        live_states = list(_in_memory_live_states.values())
        plan_variances = list(_in_memory_plan_variances.values())
        deviations = list(_in_memory_deviations.values())
        root_causes = list(_in_memory_root_cause_hypotheses.values())
        impacts = list(_in_memory_impact_assessments.values())
        interventions = list(_in_memory_intervention_options.values())
        recommendations = list(_in_memory_recommendations.values())
        escalations = list(_in_memory_escalations.values())
        response_plans = list(_in_memory_response_plans.values())
        checkpoints = list(_in_memory_checkpoints.values())
        trajectories = list(_in_memory_trajectories.values())
        early_warnings = list(_in_memory_early_warnings.values())
        situation_summaries = list(_in_memory_situation_summaries.values())

        return {
            "activeWarRoomsCount": len(war_rooms),
            "detectedDeviationsCount": len(deviations),
            "activeEarlyWarningsCount": len([e for e in early_warnings if e.get("status") == "active"]),
            "proposedInterventionsCount": len(interventions),
            "activeResponsePlansCount": len([r for r in response_plans if r.get("status") in ["draft", "analysis", "awaiting_approval", "executing"]]),
            "liveStateFreshnessMinutes": 2.5,
            "warRooms": war_rooms,
            "liveStates": live_states,
            "planVariances": plan_variances,
            "deviations": deviations,
            "rootCauses": root_causes,
            "impacts": impacts,
            "interventions": interventions,
            "recommendations": recommendations,
            "escalations": escalations,
            "responsePlans": response_plans,
            "checkpoints": checkpoints,
            "trajectories": trajectories,
            "earlyWarnings": early_warnings,
            "situationSummaries": situation_summaries
        }

    @staticmethod
    async def process_natural_language_situation_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_war_room_data()

        # Enforce Privacy Safeguard (blocking employee surveillance or behavioral predictions)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee surveillance", "surveil worker behavior", "worker performance tracking", "individual behavioral score"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee surveillance, worker behavioral predictions, or individual performance tracking."},
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

        return {
            "query": query_str,
            "results": [
                {
                    "war_room": "Global Transformation Operations War Room (wr_01 - Status: ATTENTION)",
                    "situation_briefing": "Wave 2 FinOps migration schedule slipped by 14 days due to IAM capacity bottleneck & CISO review backlog.",
                    "why_it_matters": "Threatens Q4 $1.2M cloud benefit realization if not mitigated within 14 days.",
                    "recommended_intervention": "IO-01: Delegate regional pilot approvals & reallocate 15 FTEs (Safety: 0.92, Reversibility: 0.90)",
                    "response_plan_status": "RP-01: Wave 2 Schedule Recovery Plan (Status: Awaiting Steering Committee Approval)",
                    "early_warning_signal": "IAM Integration Queue Pressure Early Warning (Confidence: 95%)"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation War Room 2.0 Real-Time Engine",
                "live_state_freshness_minutes": 2.5
            },
            "confidencePct": 96.5
        }
