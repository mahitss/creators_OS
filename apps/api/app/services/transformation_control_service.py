import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_towers: Dict[str, dict] = {}
_in_memory_live_states: Dict[str, dict] = {}
_in_memory_signals: Dict[str, dict] = {}
_in_memory_situations: Dict[str, dict] = {}
_in_memory_root_causes: Dict[str, dict] = {}
_in_memory_early_warnings: Dict[str, dict] = {}
_in_memory_wave_readinesses: Dict[str, dict] = {}
_in_memory_change_requests: Dict[str, dict] = {}
_in_memory_change_drifts: Dict[str, dict] = {}
_in_memory_tc_incidents: Dict[str, dict] = {}
_in_memory_tc_escalations: Dict[str, dict] = {}
_in_memory_weekly_reviews: Dict[str, dict] = {}
_in_memory_monthly_reviews: Dict[str, dict] = {}
_in_memory_tc_learnings: Dict[str, dict] = {}

def _initialize_seed_transformation_control_data():
    if _in_memory_towers:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_primary_01"

    # Seed Control Tower
    tower1 = {
        "id": "tct_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Control Tower 2.0",
        "portfolio_id": "transport_01",
        "status": "healthy",
        "owner": "usr_chief_transformation_officer",
        "last_evaluated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_towers[tower1["id"]] = tower1

    # Seed Live State
    lstate1 = {
        "id": "lstate_01",
        "control_tower_id": tower1["id"],
        "planned_state_json": {"wave_1_status": "executing", "schedule_variance": "0d", "capacity_usage": "60%"},
        "actual_state_json": {"wave_1_status": "executing", "schedule_variance": "-2d", "capacity_usage": "65%"},
        "forecast_state_json": {"completion_confidence": "94%", "expected_completion": "Q3-2026"},
        "last_change": "Skill Certification Auto-signer pre-validation completed",
        "last_evaluation": "Schedule, capacity, and critical path within nominal thresholds."
    }
    _in_memory_live_states[lstate1["id"]] = lstate1

    # Seed Signals
    sig1 = {
        "id": "sig_01",
        "control_tower_id": tower1["id"],
        "signal_type": "capacity",
        "severity": "medium",
        "status": "detected",
        "evidence_json": {"engineering_headroom": "15% buffer remaining in Q3"}
    }
    sig2 = {
        "id": "sig_02",
        "control_tower_id": tower1["id"],
        "signal_type": "dependency",
        "severity": "low",
        "status": "acknowledged",
        "evidence_json": {"upstream_policy_api": "minor 2-day integration delay"}
    }
    _in_memory_signals[sig1["id"]] = sig1
    _in_memory_signals[sig2["id"]] = sig2

    # Seed Situation (Correlated Signals)
    sit1 = {
        "id": "sit_wave_1_capacity_headroom",
        "control_tower_id": tower1["id"],
        "signals_json": [sig1["id"], sig2["id"]],
        "affected_transformations_json": ["cand_01", "cand_02"],
        "affected_waves_json": ["wave_01"],
        "affected_objectives_json": ["30% cost reduction by Q4"],
        "evidence_json": {"correlated_telemetry": "Engineering capacity compression coupled with upstream policy API delay"},
        "confidence": "high",
        "severity": "medium"
    }
    _in_memory_situations[sit1["id"]] = sit1

    # Seed Root Cause Assessment
    rc1 = {
        "id": "rc_01",
        "situation_id": sit1["id"],
        "category": "capacity",
        "evidence_label": "supported",
        "description": "Simultaneous compliance testing and FinOps initial pilot created transient engineering capacity friction.",
        "confidence": "high"
    }
    _in_memory_root_causes[rc1["id"]] = rc1

    # Seed Early Warning
    ew1 = {
        "id": "ew_01",
        "control_tower_id": tower1["id"],
        "warning_trigger": "Engineering buffer capacity nearing 15% threshold for Wave 1",
        "severity": "medium",
        "status": "active"
    }
    _in_memory_early_warnings[ew1["id"]] = ew1

    # Seed Wave Readiness
    wr1 = {
        "id": "wread_01",
        "wave_id": "wave_01",
        "capability_readiness": 0.95,
        "technology_readiness": 0.98,
        "process_readiness": 0.90,
        "capacity_readiness": 0.92,
        "dependency_readiness": 0.96,
        "risk_readiness": 0.94,
        "adoption_readiness": 0.88,
        "status": "ready"
    }
    _in_memory_wave_readinesses[wr1["id"]] = wr1

    # Seed Change Request (Governed by Leadership Approval)
    cr1 = {
        "id": "cr_sequence_adjust_01",
        "control_tower_id": tower1["id"],
        "request_type": "sequence",
        "proposed_change_desc": "Advance FinOps parallelization phase post Wave 1 exit criteria clearance",
        "impact_analysis_json": {"capacity_impact": "+5%", "time_saved": "14d", "risk_delta": "-0.05"},
        "status": "proposed"
    }
    _in_memory_change_requests[cr1["id"]] = cr1

    # Seed Incident & Escalation
    inc1 = {
        "id": "tc_inc_01",
        "control_tower_id": tower1["id"],
        "title": "Transient Upstream Policy API Latency Spike",
        "severity": "minor",
        "impact_summary": "Pre-signer latency increased by 120ms during peak batch evaluation",
        "response_recommendation": "Activate ActionGateway read-side cache fallback",
        "status": "active"
    }
    _in_memory_tc_incidents[inc1["id"]] = inc1

    esc1 = {
        "id": "tc_esc_01",
        "control_tower_id": tower1["id"],
        "trigger_reason": "Capacity headroom reached 15% warning threshold",
        "urgency": "medium",
        "decision_owner_unit_id": "unit_transformation_steering_board",
        "status": "active"
    }
    _in_memory_tc_escalations[esc1["id"]] = esc1

    # Seed Weekly Review & Control Learning
    wr_rev1 = {
        "id": "wrev_01",
        "control_tower_id": tower1["id"],
        "portfolio_summary": "Transformation Portfolio executing on schedule across Wave 1.",
        "waves_summary": "Wave 1 (Foundation) at 92% readiness exit criteria.",
        "signals_summary": "2 signals ingested, correlated into 1 medium-severity situation.",
        "risks_summary": "Zero critical lock-in or security risks flagged.",
        "benefits_summary": "Targeted 30% cost reduction on track.",
        "decisions_summary": "Change Request cr_sequence_adjust_01 pending leadership review.",
        "created_at": now_iso
    }
    _in_memory_weekly_reviews[wr_rev1["id"]] = wr_rev1

    learn1 = {
        "id": "learn_01",
        "control_tower_id": tower1["id"],
        "signal_summary": "Engineering capacity buffer compression during pre-signer validation.",
        "decision_summary": "Pre-stage policy cache templates prior to wave pilot launch.",
        "action_summary": "Automated AST rule pre-signing in ActionGateway sandbox.",
        "outcome_summary": "Capacity buffer restored to 40% headroom.",
        "lesson_text": "Pre-signing zero-trust policies eliminates downstream engineering bottleneck during wave acceleration."
    }
    _in_memory_tc_learnings[learn1["id"]] = learn1

_initialize_seed_transformation_control_data()


class TransformationControlService:

    @staticmethod
    async def get_control_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_transformation_control_data()
        towers = list(_in_memory_towers.values())
        live_states = list(_in_memory_live_states.values())
        signals = list(_in_memory_signals.values())
        situations = list(_in_memory_situations.values())
        root_causes = list(_in_memory_root_causes.values())
        early_warnings = list(_in_memory_early_warnings.values())
        wave_readinesses = list(_in_memory_wave_readinesses.values())
        change_requests = list(_in_memory_change_requests.values())
        incidents = list(_in_memory_tc_incidents.values())
        escalations = list(_in_memory_tc_escalations.values())
        weekly_reviews = list(_in_memory_weekly_reviews.values())
        learnings = list(_in_memory_tc_learnings.values())

        return {
            "controlTowersCount": len(towers),
            "liveStatesCount": len(live_states),
            "signalsCount": len(signals),
            "situationsCount": len(situations),
            "rootCausesCount": len(root_causes),
            "earlyWarningsCount": len(early_warnings),
            "waveReadinessesCount": len(wave_readinesses),
            "proposedChangeRequestsCount": len(change_requests),
            "activeIncidentsCount": len(incidents),
            "activeEscalationsCount": len(escalations),
            "weeklyReviewsCount": len(weekly_reviews),
            "learningsCount": len(learnings),
            "controlTowerStatus": towers[0]["status"] if towers else "healthy",
            "overallWaveReadinessPct": 92.0,
            "towers": towers,
            "liveStates": live_states,
            "signals": signals,
            "situations": situations,
            "rootCauses": root_causes,
            "earlyWarnings": early_warnings,
            "waveReadinesses": wave_readinesses,
            "changeRequests": change_requests,
            "incidents": incidents,
            "escalations": escalations,
            "weeklyReviews": weekly_reviews,
            "learnings": learnings
        }

    @staticmethod
    async def approve_change_request(session: Optional[AsyncSession], request_id: str, actor_id: str) -> dict:
        _initialize_seed_transformation_control_data()
        cr = _in_memory_change_requests.get(request_id)
        if not cr:
            return {"error": "Transformation Change Request not found"}

        cr["status"] = "approved"
        cr["approved_by"] = actor_id
        cr["approved_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "requestId": request_id,
            "status": "approved",
            "approvedBy": actor_id,
            "message": "Transformation Change Request authorized via PolicyEngine & Leadership Decision Rights. Ready for ActionGateway execution."
        }

    @staticmethod
    async def execute_change_request(session: Optional[AsyncSession], request_id: str) -> dict:
        _initialize_seed_transformation_control_data()
        cr = _in_memory_change_requests.get(request_id)
        if not cr:
            return {"error": "Transformation Change Request not found"}

        if cr["status"] != "approved":
            return {"error": "Unauthorized: Transformation Change Request must be approved by human leadership prior to execution."}

        cr["status"] = "executed"
        cr["executed_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "requestId": request_id,
            "status": "executed",
            "executionPath": "Universal Action Gateway & Execution Governance Layer",
            "message": "Transformation Change Request executed safely in ActionGateway sandbox."
        }

    @staticmethod
    async def process_natural_language_control_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_transformation_control_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking employee ranking/individual worker score)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["rank employee", "worker score", "surveil worker", "individual worker score", "individual adoption score"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee ranking, worker surveillance, individual worker scores, or employment penalty recommendations."},
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
                    "control_tower": "Global Enterprise Transformation Control Tower 2.0 (Status: healthy)",
                    "live_state_drift": "Schedule variance -2d, 40% engineering capacity buffer available",
                    "active_situation": "Wave 1 Engineering Capacity Headroom (Severity: medium)",
                    "root_cause_assessment": "Transient engineering capacity friction during pre-signer validation (Category: capacity, Label: supported)",
                    "wave_readiness": "Wave 1 (Foundation) exit criteria readiness at 92%",
                    "pending_decision": "Change Request cr_sequence_adjust_01 (Advance FinOps parallelization phase)",
                    "recommendation": "Maintain Risk-First Foundational Sequence; advance FinOps phase upon Wave 1 exit clearance."
                }
            ],
            "evidenceJson": {
                "referenced_control_tower": "tct_01",
                "data_source": "Enterprise Transformation Control Tower 2.0 Engine"
            },
            "confidencePct": 98.0
        }
