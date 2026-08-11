import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_recovery_domains: Dict[str, dict] = {}
_in_memory_disruptions: Dict[str, dict] = {}
_in_memory_impacts: Dict[str, dict] = {}
_in_memory_criticalities: Dict[str, dict] = {}
_in_memory_priorities: Dict[str, dict] = {}
_in_memory_protection_targets: Dict[str, dict] = {}
_in_memory_objectives: Dict[str, dict] = {}
_in_memory_paths: Dict[str, dict] = {}
_in_memory_options: Dict[str, dict] = {}
_in_memory_bottlenecks: Dict[str, dict] = {}
_in_memory_trajectories: Dict[str, dict] = {}
_in_memory_comparisons: Dict[str, dict] = {}
_in_memory_checkpoints: Dict[str, dict] = {}
_in_memory_gates: Dict[str, dict] = {}
_in_memory_return_plans: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}
_in_memory_escalations: Dict[str, dict] = {}
_in_memory_communications: Dict[str, dict] = {}
_in_memory_resilience_gaps: Dict[str, dict] = {}
_in_memory_improvements: Dict[str, dict] = {}
_in_memory_readinesses: Dict[str, dict] = {}
_in_memory_drills: Dict[str, dict] = {}

def _initialize_seed_recovery_data():
    if _in_memory_recovery_domains:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    next_check_iso = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Recovery Domain & Disruption
    dom1 = {
        "id": "rd_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Enterprise Core IAM & FinOps Resilience Domain",
        "scope": "enterprise",
        "owner": "Head of Enterprise Resilience",
        "status": "recovery_active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_recovery_domains[dom1["id"]] = dom1

    dis1 = {
        "id": "dis_01",
        "domain_id": dom1["id"],
        "disruption_type": "dependency_failure",
        "source": "Core IAM Gateway API Rate-Limiter Failure",
        "detected_at": now_iso,
        "severity": "high",
        "confidence": 0.95,
        "scope": "enterprise",
        "status": "confirmed"
    }
    _in_memory_disruptions[dis1["id"]] = dis1

    # Impact, Criticality, Priority, Target, Objective
    imp1 = {
        "id": "imp_01",
        "domain_id": dom1["id"],
        "disruption_id": dis1["id"],
        "affected_transformations_json": ["Wave 2 FinOps Migration", "Wave 3 IAM Single Sign-On"],
        "affected_capabilities_json": ["Cloud IAM Federation", "Automated Billing Governance"],
        "affected_dependencies_json": ["IAM OAuth Gateway v2"],
        "affected_benefits_json": ["Q4 $1.2M FinOps cost reduction delay"],
        "strategic_impact": "High. Threatens Q4 enterprise cloud cost reduction targets if unmitigated."
    }
    _in_memory_impacts[imp1["id"]] = imp1

    crit1 = {
        "id": "crit_01",
        "domain_id": dom1["id"],
        "strategic_importance": 0.92,
        "dependency_centrality": 0.88,
        "benefit_exposure": 0.90,
        "recovery_urgency": 0.95,
        "reversibility": 0.85
    }
    _in_memory_criticalities[crit1["id"]] = crit1

    prio1 = {
        "id": "prio_01",
        "domain_id": dom1["id"],
        "priority_score": 0.94,
        "evidence_summary": "Core IAM API failure blocks 2 downstream wave deployments; recovery urgency rated 95%.",
        "criteria_json": {"benefit_exposure_millions": 1.2, "urgency": "P1"}
    }
    _in_memory_priorities[prio1["id"]] = prio1

    targ1 = {
        "id": "targ_01",
        "domain_id": dom1["id"],
        "target_type": "critical_capability",
        "target_name": "IAM Federation API Gateway",
        "protection_level": "maximum"
    }
    _in_memory_protection_targets[targ1["id"]] = targ1

    obj1 = {
        "id": "obj_01",
        "domain_id": dom1["id"],
        "objective_name": "Restore IAM Gateway Federation & Accelerate Wave 2 Path",
        "target_recovery_time_hours": 72.0,
        "estimated_range_json": {"low_hours": 48.0, "expected_hours": 72.0, "high_hours": 96.0},
        "confidence": 0.93
    }
    _in_memory_objectives[obj1["id"]] = obj1

    # Recovery Path, Option, Bottleneck, Trajectory, Comparison
    path1 = {
        "id": "path_01",
        "domain_id": dom1["id"],
        "path_name": "Path A: Reroute via Secondary OAuth Cluster & Reallocate 15 FTEs",
        "action_sequence_json": ["Deploy secondary OAuth cluster", "Delegate regional pilot approvals", "Reallocate 15 FTEs"],
        "status": "recommended"
    }
    _in_memory_paths[path1["id"]] = path1

    opt1 = {
        "id": "opt_01",
        "path_id": path1["id"],
        "option_type": "substitute",
        "title": "Failover to Secondary IAM Cluster & Delegate Approvals",
        "description": "Restores IAM capability within 48 hours and mitigates 14-day schedule slip.",
        "safety_score": 0.91,
        "secondary_impact_json": {"wave_3_start_delay_days": 15, "cost_impact": 120000.0},
        "status": "simulated"
    }
    _in_memory_options[opt1["id"]] = opt1

    bot1 = {
        "id": "bot_01",
        "path_id": path1["id"],
        "bottleneck_type": "capacity",
        "entity_name": "IAM Security Operations Specialist FTEs",
        "impact_description": "15 FTE capacity shortfall in IAM integration team during cluster failover window."
    }
    _in_memory_bottlenecks[bot1["id"]] = bot1

    traj1 = {
        "id": "traj_01",
        "domain_id": dom1["id"],
        "path_id": path1["id"],
        "metric": "IAM Capability Availability %",
        "trajectory_data_json": {"t0": 40.0, "t24h": 75.0, "t48h": 99.9},
        "confidence": 0.94
    }
    _in_memory_trajectories[traj1["id"]] = traj1

    comp1 = {
        "id": "comp_01",
        "domain_id": dom1["id"],
        "compared_path_ids_json": [path1["id"], "path_02_do_nothing"],
        "time_score": 0.90,
        "risk_score": 0.08,
        "cost_score": 120000.0,
        "reversibility_score": 0.92
    }
    _in_memory_comparisons[comp1["id"]] = comp1

    # Checkpoint, Gate, Return to Normal Plan, Escalation, Communication, Gap, Readiness, Drill
    cp1 = {
        "id": "cp_01",
        "path_id": path1["id"],
        "checkpoint_name": "Secondary OAuth Cluster Synchronization Verification",
        "expected_state": "Secondary cluster latency < 15ms, zero auth errors",
        "actual_state": "Verification passed in simulation",
        "next_decision_point": next_check_iso,
        "status": "pending"
    }
    _in_memory_checkpoints[cp1["id"]] = cp1

    gate1 = {
        "id": "gate_01",
        "path_id": path1["id"],
        "gate_name": "Stabilization Complete Gate",
        "criteria_json": {"auth_success_rate": 99.9, "error_budget_remaining_pct": 85.0},
        "status": "open"
    }
    _in_memory_gates[gate1["id"]] = gate1

    ret1 = {
        "id": "ret_01",
        "domain_id": dom1["id"],
        "criteria_summary": "All IAM endpoints verified healthy for 48 consecutive hours; Wave 2 milestones resynced.",
        "action_sequence_json": ["Switch back to primary OAuth cluster", "Release 15 FTEs back to Wave 3"],
        "status": "draft"
    }
    _in_memory_return_plans[ret1["id"]] = ret1

    esc1 = {
        "id": "esc_01",
        "domain_id": dom1["id"],
        "trigger_reason": "Core IAM disruption severity escalated to HIGH",
        "escalation_path": "Enterprise Transformation Steering Committee",
        "status": "escalated"
    }
    _in_memory_escalations[esc1["id"]] = esc1

    comm1 = {
        "id": "comm_01",
        "domain_id": dom1["id"],
        "audience": "Transformation Lead Officers & CIO",
        "message_text": "Draft Recovery Briefing: Failover to Secondary IAM Cluster initiated under Path A.",
        "approval_status": "draft"
    }
    _in_memory_communications[comm1["id"]] = comm1

    gap1 = {
        "id": "gap_01",
        "domain_id": dom1["id"],
        "gap_type": "single_point_dependency",
        "description": "Core IAM OAuth Gateway v2 lacks automated cross-region failover route.",
        "severity": "high"
    }
    _in_memory_resilience_gaps[gap1["id"]] = gap1

    imp_rec1 = {
        "id": "imp_rec_01",
        "domain_id": dom1["id"],
        "improvement_type": "redundancy",
        "title": "Implement Multi-Region Active-Active IAM Gateway Cluster",
        "description": "Resilience recommendation: Eliminates single-point dependency risk for future waves.",
        "recommendation_only": True
    }
    _in_memory_improvements[imp_rec1["id"]] = imp_rec1

    read1 = {
        "id": "read_01",
        "domain_id": dom1["id"],
        "readiness_score": 0.92,
        "dimension_scores_json": {"dependency_coverage": 0.94, "capacity_buffer": 0.88, "simulation_coverage": 0.95},
        "created_at": now_iso
    }
    _in_memory_readinesses[read1["id"]] = read1

    drill1 = {
        "id": "drill_01",
        "domain_id": dom1["id"],
        "drill_name": "Q3 Enterprise IAM Gateway Outage Simulation Exercise",
        "scenario_description": "Simulated 100% loss of primary IAM cluster during peak Wave 2 migration window.",
        "results_json": {"simulated_recovery_time_hours": 42.0, "zero_production_mutation": True},
        "no_production_mutation": True,
        "created_at": now_iso
    }
    _in_memory_drills[drill1["id"]] = drill1

_initialize_seed_recovery_data()


class TransformationRecoveryService:

    @staticmethod
    async def get_recovery_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_recovery_data()
        domains = list(_in_memory_recovery_domains.values())
        disruptions = list(_in_memory_disruptions.values())
        impacts = list(_in_memory_impacts.values())
        criticalities = list(_in_memory_criticalities.values())
        priorities = list(_in_memory_priorities.values())
        protection_targets = list(_in_memory_protection_targets.values())
        objectives = list(_in_memory_objectives.values())
        paths = list(_in_memory_paths.values())
        options = list(_in_memory_options.values())
        bottlenecks = list(_in_memory_bottlenecks.values())
        trajectories = list(_in_memory_trajectories.values())
        comparisons = list(_in_memory_comparisons.values())
        checkpoints = list(_in_memory_checkpoints.values())
        gates = list(_in_memory_gates.values())
        return_plans = list(_in_memory_return_plans.values())
        escalations = list(_in_memory_escalations.values())
        communications = list(_in_memory_communications.values())
        resilience_gaps = list(_in_memory_resilience_gaps.values())
        improvements = list(_in_memory_improvements.values())
        readinesses = list(_in_memory_readinesses.values())
        drills = list(_in_memory_drills.values())

        return {
            "activeRecoveryDomainsCount": len(domains),
            "confirmedDisruptionsCount": len([d for d in disruptions if d.get("status") == "confirmed"]),
            "recommendedRecoveryPathsCount": len(paths),
            "simulatedOptionsCount": len(options),
            "activeReturnToNormalPlansCount": len(return_plans),
            "recoveryReadinessScore": 0.92,
            "domains": domains,
            "disruptions": disruptions,
            "impacts": impacts,
            "criticalities": criticalities,
            "priorities": priorities,
            "protectionTargets": protection_targets,
            "objectives": objectives,
            "paths": paths,
            "options": options,
            "bottlenecks": bottlenecks,
            "trajectories": trajectories,
            "comparisons": comparisons,
            "checkpoints": checkpoints,
            "gates": gates,
            "returnPlans": return_plans,
            "escalations": escalations,
            "communications": communications,
            "resilienceGaps": resilience_gaps,
            "improvements": improvements,
            "readinesses": readinesses,
            "drills": drills
        }

    @staticmethod
    async def process_natural_language_recovery_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_recovery_data()

        # Enforce Anti-Surveillance / Privacy safeguard (blocking individual employee recovery scoring)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee recovery score", "individual worker recovery", "worker performance surveillance"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee recovery scoring or worker performance surveillance."},
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
                    "domain": "Enterprise Core IAM & FinOps Resilience Domain (rd_01 - Status: RECOVERY_ACTIVE)",
                    "disruption": "Core IAM Gateway API Rate-Limiter Failure (Severity: HIGH, Status: CONFIRMED)",
                    "impact": "Wave 2 FinOps Migration & Wave 3 IAM Single Sign-On (Strategic Impact: High)",
                    "recommended_path": "Path A: Reroute via Secondary OAuth Cluster & Reallocate 15 FTEs (Safety: 0.91)",
                    "recovery_objective": "Restore IAM Gateway Federation & Accelerate Wave 2 Path within 72 hours",
                    "return_to_normal_status": "Draft Plan (Verify all IAM endpoints healthy for 48h before closing)"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience & Recovery 2.0 Engine",
                "recovery_readiness_score": 0.92
            },
            "confidencePct": 95.8
        }
