import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_loops: Dict[str, dict] = {}
_in_memory_objectives: Dict[str, dict] = {}
_in_memory_signals: Dict[str, dict] = {}
_in_memory_snapshots: Dict[str, dict] = {}
_in_memory_changes: Dict[str, dict] = {}
_in_memory_assessments: Dict[str, dict] = {}
_in_memory_reassessments: Dict[str, dict] = {}
_in_memory_responses: Dict[str, dict] = {}
_in_memory_guardrails: Dict[str, dict] = {}
_in_memory_breaches: Dict[str, dict] = {}
_in_memory_observations: Dict[str, dict] = {}
_in_memory_regrets: Dict[str, dict] = {}
_in_memory_performances: Dict[str, dict] = {}

def _initialize_seed_control_data():
    if _in_memory_loops:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Control Loop (Default: monitor_only)
    loop1 = {
        "id": "loop_ctrl_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Enterprise Security SLA & Threat Remediation Control Loop",
        "description": "Closed-loop monitoring of threat remediation latency, cluster node health, and model routing SLA.",
        "target_entity_type": "infrastructure",
        "target_entity_id": "infra_sec_cluster_01",
        "mode": "monitor_only", # Default mode
        "status": "active",
        "owner": "usr_sec_lead",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_loops[loop1["id"]] = loop1

    # Seed Control Objective
    obj1 = {
        "id": "cobj_01",
        "loop_id": loop1["id"],
        "metric": "p99 Remediation Latency (sec)",
        "target": 180.0,
        "acceptable_range": "[120.0, 240.0]",
        "priority": 1,
        "source": "KPI Operating System 2.0"
    }
    _in_memory_objectives[obj1["id"]] = obj1

    # Seed Real-Time Signal
    sig1 = {
        "id": "sig_ctrl_01",
        "loop_id": loop1["id"],
        "signal_type": "kpi",
        "value": 215.0,
        "signal_quality": "verified",
        "confidence": "high",
        "observed_at": now_iso,
        "source": "Prometheus Telemetry Mesh",
        "retrieved_at": now_iso,
        "freshness": "fresh"
    }
    _in_memory_signals[sig1["id"]] = sig1

    # Seed Control Guardrail
    g1 = {
        "id": "grd_01",
        "loop_id": loop1["id"],
        "guardrail_type": "max_delay",
        "threshold": 300.0,
        "severity": "high",
        "action": "require_approval",
        "approval_required": True,
        "policy_reference": "policy_sec_sla_v2"
    }
    _in_memory_guardrails[g1["id"]] = g1

    # Seed Decision Validity Assessment & Reassessment
    ass1 = {
        "id": "dva_01",
        "decision_id": "dec_01",
        "validity_status": "valid",
        "validity_factors_json": {
            "latency_within_bounds": True,
            "cost_within_budget": True,
            "data_freshness": "fresh"
        },
        "assessed_at": now_iso
    }
    _in_memory_assessments[ass1["id"]] = ass1

    reass1 = {
        "id": "dreass_01",
        "decision_id": "dec_01",
        "trigger_type": "forecast_change",
        "evidence": "Forecast predicts +25% latency increase in 14 days due to node capacity bottleneck.",
        "affected_decision_id": "dec_01",
        "new_conditions_json": {"projected_latency": 260.0},
        "recommended_next_step": "Request Executive Review & Re-optimization via Prescriptive Intelligence.",
        "status": "pending"
    }
    _in_memory_reassessments[reass1["id"]] = reass1

    # Seed Governed Control Response
    resp1 = {
        "id": "cresp_01",
        "loop_id": loop1["id"],
        "response_type": "recommend",
        "payload_json": {
            "action": "Scale replica pool from 48 to 64 nodes",
            "required_approval": "usr_sec_lead"
        },
        "status": "proposed",
        "confidence": "high"
    }
    _in_memory_responses[resp1["id"]] = resp1

    # Seed Post-Action Verification Observation
    obs1 = {
        "id": "aobs_01",
        "action_id": "act_plan_01",
        "expected_val": 210.0,
        "actual_val": 204.0,
        "variance": -6.0,
        "outcome_class": "success",
        "timestamp": now_iso
    }
    _in_memory_observations[obs1["id"]] = obs1

    # Seed Counterfactual Regret Analysis
    reg1 = {
        "id": "reg_01",
        "decision_id": "dec_01",
        "selected_option": "Option 1 (A100_SXM)",
        "alternative_options_json": ["Option 2 (H100_SXM)"],
        "actual_outcome": 952.0,
        "regret_score": 0.04,
        "counterfactual_label": "simulated"
    }
    _in_memory_regrets[reg1["id"]] = reg1

    # Seed Performance Metrics
    perf1 = {
        "id": "cperf_01",
        "loop_id": loop1["id"],
        "false_alerts": 0,
        "missed_alerts": 0,
        "successful_interventions": 14,
        "unnecessary_interventions": 1,
        "reassessment_frequency": 0.8,
        "health_score": 0.98
    }
    _in_memory_performances[perf1["id"]] = perf1

_initialize_seed_control_data()


class AdaptiveDecisionGovernanceService:

    @staticmethod
    async def get_control_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_control_data()
        loops = list(_in_memory_loops.values())
        signals = list(_in_memory_signals.values())
        guardrails = list(_in_memory_guardrails.values())
        reassessments = list(_in_memory_reassessments.values())
        responses = list(_in_memory_responses.values())
        observations = list(_in_memory_observations.values())
        regrets = list(_in_memory_regrets.values())
        performances = list(_in_memory_performances.values())

        active_loops = sum(1 for l in loops if l["status"] == "active")

        return {
            "loopsCount": len(loops),
            "activeLoopsCount": active_loops,
            "signalsCount": len(signals),
            "guardrailsCount": len(guardrails),
            "reassessmentsCount": len(reassessments),
            "responsesCount": len(responses),
            "observationsCount": len(observations),
            "loops": loops,
            "signals": signals,
            "guardrails": guardrails,
            "reassessments": reassessments,
            "responses": responses,
            "observations": observations,
            "regrets": regrets,
            "performances": performances,
            "loopHealthScore": 0.98
        }

    @staticmethod
    async def create_control_loop(session: Optional[AsyncSession], loop_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_control_data()
        l_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        loop = {
            "id": l_id,
            "organization_id": org_id,
            "workspace_id": loop_data.get("workspaceId", "ws_default"),
            "name": loop_data["name"],
            "description": loop_data["description"],
            "target_entity_type": loop_data.get("targetEntityType", "mission"),
            "target_entity_id": loop_data.get("targetEntityId", "msn_default"),
            "mode": loop_data.get("mode", "monitor_only"), # Default monitor_only
            "status": "active",
            "owner": loop_data["owner"],
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_loops[l_id] = loop
        return loop

    @staticmethod
    async def pause_control_loop(session: Optional[AsyncSession], loop_id: str, actor_id: str = "usr_sec_lead") -> dict:
        _initialize_seed_control_data()
        loop = _in_memory_loops.get(loop_id)
        if not loop:
            return {"error": "Control loop not found"}

        loop["status"] = "paused"
        loop["updated_at"] = datetime.now(timezone.utc).isoformat()
        return {
            "loopId": loop_id,
            "status": "paused",
            "pausedBy": actor_id,
            "message": "Control loop paused. All automated signals will remain in monitor mode."
        }

    @staticmethod
    async def resume_control_loop(session: Optional[AsyncSession], loop_id: str, actor_id: str = "usr_sec_lead") -> dict:
        _initialize_seed_control_data()
        loop = _in_memory_loops.get(loop_id)
        if not loop:
            return {"error": "Control loop not found"}

        loop["status"] = "active"
        loop["updated_at"] = datetime.now(timezone.utc).isoformat()
        return {
            "loopId": loop_id,
            "status": "active",
            "resumedBy": actor_id,
            "message": "Control loop resumed cleanly."
        }

    @staticmethod
    async def process_natural_language_control_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_control_data()

        # Enforce DLP checks on natural language query
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Privacy Anti-Surveillance Safeguard (No hidden worker scores or employee profiling)
        lower_q = query_str.lower()
        if any(p in lower_q for p in ["worker score", "employee profiling", "surveillance score", "worker ranking", "track employee"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Denied. Employee surveillance, worker scoring, or individual profiling is strictly prohibited by policy."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "control_loop": "Enterprise Security SLA Control Loop",
                    "mode": "monitor_only",
                    "status": "active",
                    "latest_signal": "p99 Remediation Latency: 215.0s (verified)",
                    "decision_validity": "valid",
                    "pending_reassessments": 1
                }
            ],
            "evidenceJson": {
                "referenced_loop": "loop_ctrl_01",
                "data_source": "Adaptive Decision Governance 2.0 Engine"
            },
            "confidencePct": 98.0
        }
