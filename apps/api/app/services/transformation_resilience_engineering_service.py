import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_resilience_domains: Dict[str, dict] = {}
_in_memory_baselines: Dict[str, dict] = {}
_in_memory_failure_modes: Dict[str, dict] = {}
_in_memory_failure_analyses: Dict[str, dict] = {}
_in_memory_weaknesses: Dict[str, dict] = {}
_in_memory_spofs: Dict[str, dict] = {}
_in_memory_redundancies: Dict[str, dict] = {}
_in_memory_substitutions: Dict[str, dict] = {}
_in_memory_buffers: Dict[str, dict] = {}
_in_memory_optionalities: Dict[str, dict] = {}
_in_memory_investments: Dict[str, dict] = {}
_in_memory_cascades: Dict[str, dict] = {}
_in_memory_interventions: Dict[str, dict] = {}
_in_memory_roadmaps: Dict[str, dict] = {}
_in_memory_comparisons: Dict[str, dict] = {}
_in_memory_lessons: Dict[str, dict] = {}
_in_memory_patterns: Dict[str, dict] = {}
_in_memory_warnings: Dict[str, dict] = {}

def _initialize_seed_resilience_engineering_data():
    if _in_memory_resilience_domains:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Domain & Baseline
    dom1 = {
        "id": "red_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Transformation Resilience Engineering Domain",
        "scope": "enterprise",
        "owner": "Chief Resilience Engineer",
        "status": "baseline",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_resilience_domains[dom1["id"]] = dom1

    base1 = {
        "id": "base_01",
        "domain_id": dom1["id"],
        "robustness_score": 0.91,
        "redundancy_score": 0.86,
        "recoverability_score": 0.94,
        "adaptability_score": 0.89,
        "optionality_score": 0.88,
        "observability_score": 0.95,
        "governability_score": 0.92
    }
    _in_memory_baselines[base1["id"]] = base1

    # Failure Mode, Analysis, Weakness, SPOF
    fm1 = {
        "id": "fm_01",
        "domain_id": dom1["id"],
        "failure_type": "single_dependency",
        "frequency": 4,
        "severity": "high",
        "recovery_time_hours": 48.0,
        "confidence": 0.93
    }
    _in_memory_failure_modes[fm1["id"]] = fm1

    fma1 = {
        "id": "fma_01",
        "failure_mode_id": fm1["id"],
        "trigger_description": "Single OAuth Gateway API rate-limit exhaustion during migration wave surge",
        "conditions_json": {"concurrent_wave_requests": 15000, "rate_limit_per_min": 10000},
        "propagation_path_json": ["IAM API Gateway", "Wave 2 FinOps Auth", "Wave 3 SSO"],
        "recovery_behavior": "Manual cluster failover required (48h delay)"
    }
    _in_memory_failure_analyses[fma1["id"]] = fma1

    weak1 = {
        "id": "weak_01",
        "domain_id": dom1["id"],
        "affected_transformations_json": ["Wave 2 FinOps Migration", "Wave 3 IAM Single Sign-On"],
        "affected_capabilities_json": ["Cloud FinOps", "IAM Federation"],
        "description": "Systemic concentration of identity federation requests through single regional gateway.",
        "severity": "high"
    }
    _in_memory_weaknesses[weak1["id"]] = weak1

    spof1 = {
        "id": "spof_01",
        "domain_id": dom1["id"],
        "entity_type": "dependency",
        "entity_name": "Core IAM OAuth Gateway v2",
        "criticality_score": 0.95
    }
    _in_memory_spofs[spof1["id"]] = spof1

    # Redundancy, Substitution, Buffer, Optionality, Investment
    red1 = {
        "id": "red_option_01",
        "domain_id": dom1["id"],
        "redundancy_type": "dependency",
        "title": "Deploy Active-Active Multi-Region IAM Gateway Redundancy",
        "description": "Eliminates single-point dependency risk by deploying automated cross-region gateway failover.",
        "cost_estimate": 150000.0,
        "risk_reduction_score": 0.88
    }
    _in_memory_redundancies[red1["id"]] = red1

    sub1 = {
        "id": "sub_01",
        "domain_id": dom1["id"],
        "substitution_type": "technology",
        "primary_entity": "Legacy OAuth Rate-Limiter",
        "substitute_entity": "Distributed Mesh Rate-Limiter Cluster",
        "feasibility_score": 0.90
    }
    _in_memory_substitutions[sub1["id"]] = sub1

    buf1 = {
        "id": "buf_01",
        "domain_id": dom1["id"],
        "required_buffer_fte": 15.0,
        "cost_estimate": 180000.0,
        "activation_condition": "Migration wave queue pressure exceeds 85% capacity threshold"
    }
    _in_memory_buffers[buf1["id"]] = buf1

    opt1 = {
        "id": "opt_01",
        "domain_id": dom1["id"],
        "path_count": 3,
        "dimension_scores_json": {"path_a_score": 0.91, "path_b_score": 0.85, "path_c_score": 0.88},
        "created_at": now_iso
    }
    _in_memory_optionalities[opt1["id"]] = opt1

    inv1 = {
        "id": "inv_01",
        "domain_id": dom1["id"],
        "problem_statement": "Single IAM gateway vulnerability threatens $1.2M Q4 FinOps benefit realization.",
        "improvement_title": "Multi-Region Active-Active IAM Gateway & 15 FTE Capacity Buffer",
        "investment_amount": 250000.0,
        "expected_benefit": "Eliminates 92% of single-point IAM failure risk across Wave 2 and Wave 3.",
        "risk_reduction_pct": 45.0,
        "uncertainty_level": "low",
        "priority": "high"
    }
    _in_memory_investments[inv1["id"]] = inv1

    # Cascade, Intervention, Roadmap, Comparison, Lesson, Pattern, Warning
    casc1 = {
        "id": "casc_01",
        "domain_id": dom1["id"],
        "initial_trigger": "IAM Rate-Limiter Failure",
        "propagation_graph_json": {"nodes": ["IAM Gateway", "FinOps Wave 2", "Wave 3 SSO"], "edges": [["IAM Gateway", "FinOps Wave 2"], ["FinOps Wave 2", "Wave 3 SSO"]]},
        "uncertainty_label": "estimated",
        "created_at": now_iso
    }
    _in_memory_cascades[casc1["id"]] = casc1

    inter1 = {
        "id": "inter_01",
        "domain_id": dom1["id"],
        "intervention_type": "redundancy",
        "title": "Proactive Active-Active Gateway Redundancy Implementation",
        "description": "Resilience recommendation: Eliminates recurring IAM failure mode.",
        "priority_score": 0.92,
        "recommendation_only": True
    }
    _in_memory_interventions[inter1["id"]] = inter1

    road1 = {
        "id": "road_01",
        "domain_id": dom1["id"],
        "milestones_json": ["Q3 Gateway Redundancy Deploy", "Q4 Capacity Buffer Provisioning"],
        "investment_total": 430000.0,
        "status": "draft"
    }
    _in_memory_roadmaps[road1["id"]] = road1

    comp1 = {
        "id": "comp_01",
        "domain_id": dom1["id"],
        "baseline_scores_json": {"robustness": 0.91, "redundancy": 0.86},
        "improved_scores_json": {"robustness": 0.98, "redundancy": 0.96},
        "actual_scores_json": {"robustness": 0.97, "redundancy": 0.95}
    }
    _in_memory_comparisons[comp1["id"]] = comp1

    les1 = {
        "id": "les_01",
        "domain_id": dom1["id"],
        "failure_trigger": "IAM API Rate-Limiter Exhaustion",
        "observed_behavior": "Manual failover caused 48h schedule slip",
        "lesson_text": "Automated active-active failover is mandatory for central identity federation dependencies.",
        "confidence": 0.94
    }
    _in_memory_lessons[les1["id"]] = les1

    pat1 = {
        "id": "pat_01",
        "domain_id": dom1["id"],
        "pattern_name": "Shared Identity Dependency Concentration Pattern",
        "pattern_type": "weak_dependency",
        "description": "Multiple parallel waves bottleneck on un-redundant IAM gateway endpoints.",
        "confidence": 0.95
    }
    _in_memory_patterns[pat1["id"]] = pat1

    warn1 = {
        "id": "warn_01",
        "domain_id": dom1["id"],
        "warning_signal": "IAM Gateway Concentration Risk Warning",
        "severity": "high",
        "metrics_json": {"dependency_concentration_pct": 89.5, "capacity_margin_pct": 10.5}
        }
    _in_memory_warnings[warn1["id"]] = warn1

_initialize_seed_resilience_engineering_data()

_EMITTED_EVENTS: List[dict] = []

EMITTED_EVENT_TYPES = [
    "transformation.resilience.domain.created",
    "transformation.resilience.baseline.created",
    "transformation.failure_mode.detected",
    "transformation.failure_mode.analyzed",
    "transformation.systemic_weakness.detected",
    "transformation.single_point_failure.detected",
    "transformation.redundancy.option.created",
    "transformation.substitution.option.created",
    "transformation.capacity_buffer.option.created",
    "transformation.optionality.analyzed",
    "transformation.resilience.investment_candidate.created",
    "transformation.resilience.simulation.started",
    "transformation.resilience.simulation.completed",
    "transformation.resilience.cascading_failure.detected",
    "transformation.resilience.intervention.created",
    "transformation.resilience.roadmap.created",
    "transformation.resilience.verification.completed",
    "transformation.resilience.warning.created",
    "transformation.resilience.drill.completed",
    "transformation.resilience.lesson.created",
    "transformation.resilience.pattern.detected"
]


class TransformationResilienceEngineeringService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_EVENTS.append(evt)
        return evt

    @staticmethod
    def check_tenant_access(caller_org_id: str, target_org_id: str) -> bool:
        if caller_org_id != target_org_id:
            return False
        return True

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from autonomous structural changes, funding allocations, or governance edits
        forbidden_actions = ["allocate_investment", "change_architecture", "change_governance", "remove_dependencies", "restructure_teams", "purchase_capacity", "approve_resilience_program", "execute_material_resilience_change"]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing non-read-only action '{action}'. Action requires PolicyEngine authorization + human approval."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_resilience_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_engineering_data()
        domains = list(_in_memory_resilience_domains.values())
        baselines = list(_in_memory_baselines.values())
        failure_modes = list(_in_memory_failure_modes.values())
        failure_analyses = list(_in_memory_failure_analyses.values())
        weaknesses = list(_in_memory_weaknesses.values())
        spofs = list(_in_memory_spofs.values())
        redundancies = list(_in_memory_redundancies.values())
        substitutions = list(_in_memory_substitutions.values())
        buffers = list(_in_memory_buffers.values())
        optionalities = list(_in_memory_optionalities.values())
        investments = list(_in_memory_investments.values())
        cascades = list(_in_memory_cascades.values())
        interventions = list(_in_memory_interventions.values())
        roadmaps = list(_in_memory_roadmaps.values())
        comparisons = list(_in_memory_comparisons.values())
        lessons = list(_in_memory_lessons.values())
        patterns = list(_in_memory_patterns.values())
        warnings = list(_in_memory_warnings.values())

        return {
            "activeResilienceDomainsCount": len(domains),
            "detectedFailureModesCount": len(failure_modes),
            "systemicWeaknessesCount": len(weaknesses),
            "singlePointsOfFailureCount": len(spofs),
            "investmentCandidatesCount": len(investments),
            "resilienceRobustnessScore": 0.91,
            "domains": domains,
            "baselines": baselines,
            "failureModes": failure_modes,
            "failureAnalyses": failure_analyses,
            "weaknesses": weaknesses,
            "spofs": spofs,
            "redundancies": redundancies,
            "substitutions": substitutions,
            "buffers": buffers,
            "optionalities": optionalities,
            "investments": investments,
            "cascades": cascades,
            "interventions": interventions,
            "roadmaps": roadmaps,
            "comparisons": comparisons,
            "lessons": lessons,
            "patterns": patterns,
            "warnings": warnings
        }

    @staticmethod
    async def create_investment_candidate(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_resilience_engineering_data()
        inv_id = data.get("id", f"inv_{uuid.uuid4().hex[:8]}")
        item = {
            "id": inv_id,
            "domain_id": data.get("domain_id", "red_01"),
            "problem_statement": data.get("problem_statement", "Vulnerability in central component"),
            "improvement_title": data.get("improvement_title", data.get("improvementTitle", "Resilience Improvement")),
            "investment_amount": float(data.get("investment_amount", data.get("investmentAmount", 250000.0))),
            "expected_benefit": data.get("expected_benefit", "Reduces risk across transformations"),
            "risk_reduction_pct": float(data.get("risk_reduction_pct", data.get("riskReductionPct", 45.0))),
            "uncertainty_level": data.get("uncertainty_level", "low"),
            "priority": data.get("priority", "high")
        }
        _in_memory_investments[inv_id] = item
        TransformationResilienceEngineeringService.emit_event("transformation.resilience.investment_candidate.created", item)
        return item

    @staticmethod
    async def simulate_investment(session: Optional[AsyncSession], inv_id: str) -> dict:
        _initialize_seed_resilience_engineering_data()
        TransformationResilienceEngineeringService.emit_event("transformation.resilience.simulation.started", {"investment_id": inv_id})
        res = {
            "investmentId": inv_id,
            "simulationCompleted": True,
            "baselineRobustness": 0.91,
            "simulatedRobustness": 0.98,
            "riskReductionPct": 45.0,
            "paybackHorizon": "Q4 2026",
            "crossTransformationProtectionCount": 3
        }
        TransformationResilienceEngineeringService.emit_event("transformation.resilience.simulation.completed", res)
        return res

    @staticmethod
    async def run_resilience_drill(session: Optional[AsyncSession], domain_id: str, drill_name: str) -> dict:
        _initialize_seed_resilience_engineering_data()
        drill = {
            "id": f"drill_{uuid.uuid4().hex[:8]}",
            "domain_id": domain_id,
            "drill_name": drill_name,
            "no_production_mutation": True,
            "status": "completed",
            "observed_recovery_time_hours": 12.0,
            "expected_recovery_time_hours": 12.0,
            "learning_summary": "Automated failover verified; zero production state mutated."
        }
        TransformationResilienceEngineeringService.emit_event("transformation.resilience.drill.completed", drill)
        return drill

    @staticmethod
    async def process_natural_language_resilience_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_engineering_data()

        # Enforce Anti-Surveillance / Privacy safeguard (blocking individual employee resilience ranking)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee resilience ranking", "individual worker resilience", "worker performance surveillance", "rank employee resilience"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee resilience rankings or worker performance surveillance."},
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
                    "domain": "Global Transformation Resilience Engineering Domain (red_01 - Status: BASELINE)",
                    "systemic_weakness": "Systemic concentration of identity federation requests through single regional gateway.",
                    "single_point_of_failure": "Core IAM OAuth Gateway v2 (Criticality: 95%)",
                    "redundancy_proposal": "Active-Active Multi-Region IAM Gateway Redundancy (Cost: $150k, Risk Reduction: 88%)",
                    "investment_candidate": "Multi-Region Active-Active IAM Gateway & 15 FTE Capacity Buffer ($250k investment, 45% risk reduction)",
                    "resilience_roadmap": "Roadmap 01 ($430k total investment, Status: Draft)"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Engineering 2.0 Engine",
                "robustness_score": 0.91
            },
            "confidencePct": 96.2
        }

