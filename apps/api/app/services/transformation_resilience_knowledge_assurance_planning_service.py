import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_assurance_planning_domains: Dict[str, dict] = {}
_in_memory_assurance_portfolios: Dict[str, dict] = {}
_in_memory_systemic_risks: Dict[str, dict] = {}
_in_memory_root_cause_groups: Dict[str, dict] = {}
_in_memory_remediation_levers: Dict[str, dict] = {}
_in_memory_assurance_capacities: Dict[str, dict] = {}
_in_memory_capacity_constraints: Dict[str, dict] = {}
_in_memory_assurance_demands: Dict[str, dict] = {}
_in_memory_assurance_options: Dict[str, dict] = {}
_in_memory_assurance_sequences: Dict[str, dict] = {}
_in_memory_assurance_scenarios: Dict[str, dict] = {}
_in_memory_assurance_plans: Dict[str, dict] = {}
_in_memory_assurance_residual_risks: Dict[str, dict] = {}
_in_memory_assurance_tradeoffs: Dict[str, dict] = {}
_in_memory_assurance_recommendations: Dict[str, dict] = {}
_in_memory_plan_verifications: Dict[str, dict] = {}
_in_memory_plan_effectivenesses: Dict[str, dict] = {}
_in_memory_plan_failures: Dict[str, dict] = {}

_EMITTED_PLANNING_EVENTS: List[dict] = []

EMITTED_PLANNING_EVENT_TYPES = [
    "transformation.resilience.knowledge.assurance_planning.domain.created",
    "transformation.resilience.knowledge.assurance_portfolio.created",
    "transformation.resilience.knowledge.systemic_risk.detected",
    "transformation.resilience.knowledge.root_cause_group.created",
    "transformation.resilience.knowledge.remediation_lever.created",
    "transformation.resilience.knowledge.coverage.analyzed",
    "transformation.resilience.knowledge.capacity.updated",
    "transformation.resilience.knowledge.capacity_constraint.detected",
    "transformation.resilience.knowledge.demand.updated",
    "transformation.resilience.knowledge.capacity_gap.detected",
    "transformation.resilience.knowledge.assurance_option.created",
    "transformation.resilience.knowledge.assurance_sequence.created",
    "transformation.resilience.knowledge.assurance_scenario.created",
    "transformation.resilience.knowledge.assurance_plan.created",
    "transformation.resilience.knowledge.assurance_plan.submitted",
    "transformation.resilience.knowledge.assurance_plan.approved",
    "transformation.resilience.knowledge.assurance_plan.execution.started",
    "transformation.resilience.knowledge.assurance_plan.execution.completed",
    "transformation.resilience.knowledge.assurance_plan.verified",
    "transformation.resilience.knowledge.assurance_plan.effectiveness.updated",
    "transformation.resilience.knowledge.assurance_plan.failure.detected",
    "transformation.resilience.knowledge.assurance_plan.learning.created",
    "transformation.resilience.knowledge.assurance_plan.reuse.detected"
]

def _initialize_seed_resilience_planning_data():
    if _in_memory_assurance_planning_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    due_iso = (now + timedelta(days=14)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Assurance Planning Domain
    pdom1 = {
        "id": "pdom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Knowledge Assurance Planning & Risk Optimization 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Knowledge Assurance Planning Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_assurance_planning_domains[pdom1["id"]] = pdom1

    # Portfolio
    port1 = {
        "id": "aport_01",
        "domain_id": pdom1["id"],
        "risk_ids_json": ["rcase_01", "rcase_overdue_01"],
        "affected_transformations_json": ["Global Enterprise Multi-Region Cloud Wave 4", "HR Systems Transformation"],
        "dependencies_json": ["Secondary Cloud SLA", "OAuth Token Gateway"],
        "decision_domains_json": ["Resilience Engineering", "Vendor Operations"],
        "exposure_score": 0.88,
        "current_capacity": 0.75,
        "planned_capacity": 0.95,
        "created_at": now_iso
    }
    _in_memory_assurance_portfolios[port1["id"]] = port1

    # Systemic Risk (explicit factors, no black box score)
    sysr1 = {
        "id": "sysr_01",
        "title": "Systemic Secondary Cloud SLA Telemetry Deficit Across Multi-Region Implementations",
        "breadth": 5,
        "dependency_centrality": 0.92,
        "decision_influence": 0.95,
        "recurrence": 4,
        "uncertainty": 0.25,
        "severity": "critical"
    }
    _in_memory_systemic_risks[sysr1["id"]] = sysr1

    # Root Cause Group
    rcg1 = {
        "id": "rcg_01",
        "root_cause_type": "stale_source",
        "description": "Lack of direct synthetic monitoring integration with vendor interconnect telemetry.",
        "frequency": 4,
        "affected_risk_ids_json": ["rcase_01", "rcase_overdue_01"]
    }
    _in_memory_root_cause_groups[rcg1["id"]] = rcg1

    # Remediation Lever
    rlev1 = {
        "id": "rlev_01",
        "lever_type": "shared_evidence_source",
        "title": "Deploy Third-Party Independent Synthetic Telemetry Mesh",
        "risk_coverage": 0.85,
        "confidence": 0.94,
        "limitations": "Requires third-party vendor API access authorization."
    }
    _in_memory_remediation_levers[rlev1["id"]] = rlev1

    # Capacity, Constraints & Demand
    cap1 = {
        "id": "acap_01",
        "available_capacity": 0.80,
        "required_capacity": 0.95,
        "specialist_capacity": 0.75,
        "simulation_capacity": 0.90,
        "review_capacity": 0.70,
        "evidence_capacity": 0.85,
        "created_at": now_iso
    }
    _in_memory_assurance_capacities[cap1["id"]] = cap1

    ccons1 = {
        "id": "ccons_01",
        "constraint_type": "limited_experts",
        "description": "Specialist bandwidth for cloud SLA verification is constrained in Q3.",
        "severity": "high"
    }
    _in_memory_capacity_constraints[ccons1["id"]] = ccons1

    dem1 = {
        "id": "adem_01",
        "risk_workload": 0.90,
        "evidence_workload": 0.95,
        "review_workload": 0.85,
        "simulation_workload": 0.80,
        "created_at": now_iso
    }
    _in_memory_assurance_demands[dem1["id"]] = dem1

    # Options & Sequences & Scenarios
    opt1 = {
        "id": "aopt_01",
        "option_type": "parallel",
        "title": "Parallel Synthetic Telemetry & Revalidation Packet Execution",
        "coverage": 0.90,
        "effort": "medium",
        "time_est": "14 days",
        "risk_reduction": 0.85,
        "created_at": now_iso
    }
    _in_memory_assurance_options[opt1["id"]] = opt1

    seq1 = {
        "id": "aseq_01",
        "sequence_order_json": ["aopt_01"],
        "dependencies_json": {"aopt_01": []},
        "deadline": due_iso,
        "rationale": "Deploy synthetic telemetry prior to submitting revalidation packet to Governance Board.",
        "created_at": now_iso
    }
    _in_memory_assurance_sequences[seq1["id"]] = seq1

    scen1 = {
        "id": "ascen_01",
        "scenario_type": "full_capacity",
        "coverage": 0.95,
        "residual_risk": 0.05,
        "capacity_required": 0.90,
        "created_at": now_iso
    }
    _in_memory_assurance_scenarios[scen1["id"]] = scen1

    # Assurance Plan & Recommendation (explicitly labeled ANALYTICAL RECOMMENDATION — NOT APPROVAL)
    plan1 = {
        "id": "aplan_01",
        "objective": "Execute multi-region cloud SLA assurance plan to remediate high-influence knowledge risks.",
        "scope": "enterprise",
        "selected_options_json": [opt1],
        "sequence_id": seq1["id"],
        "capacity_allocation_json": {"specialists": 0.75, "simulations": 0.90},
        "risk_coverage": 0.92,
        "residual_risk": 0.08,
        "assumptions": "Third-party monitoring vendor API remains accessible.",
        "owner": "Principal Enterprise Knowledge Assurance Planning Architect",
        "deadline": due_iso,
        "status": "approved"
    }
    _in_memory_assurance_plans[plan1["id"]] = plan1

    resr1 = {
        "id": "aresr_01",
        "plan_id": plan1["id"],
        "unaddressed_risk": "Minor SLA jitter on legacy non-critical SSO background sync",
        "reason": "Intentionally deferred to Q4 migration.",
        "severity": "low",
        "owner": "Legacy Systems Lead",
        "review_date": (now + timedelta(days=90)).isoformat()
    }
    _in_memory_assurance_residual_risks[resr1["id"]] = resr1

    trade1 = {
        "id": "atrade_01",
        "plan_id": plan1["id"],
        "tradeoff_description": "Parallel execution increases short-term specialist workload by 15% but reduces time to assurance by 10 days.",
        "coverage_vs_effort": "High coverage (92%) for moderate effort boost",
        "speed_vs_uncertainty": "Faster resolution reduces decision uncertainty prior to Wave 4 deployment",
        "created_at": now_iso
    }
    _in_memory_assurance_tradeoffs[trade1["id"]] = trade1

    rec1 = {
        "id": "arec_01",
        "plan_id": plan1["id"],
        "label": "ANALYTICAL RECOMMENDATION — NOT APPROVAL",
        "recommendation_text": "Proceed with Parallel Synthetic Telemetry & Revalidation Option to achieve 92% risk coverage prior to Wave 4 HR rollout.",
        "confidence": 0.94
    }
    _in_memory_assurance_recommendations[rec1["id"]] = rec1

    # Verification & Effectiveness
    pverif1 = {
        "id": "apverif_01",
        "plan_id": plan1["id"],
        "planned_coverage": 0.92,
        "actual_coverage": 0.90,
        "planned_risk_reduction": 0.85,
        "actual_risk_reduction": 0.82,
        "created_at": now_iso
    }
    _in_memory_plan_verifications[pverif1["id"]] = pverif1

    peff1 = {
        "id": "apeff_01",
        "plan_id": plan1["id"],
        "risk_reduction": 0.85,
        "coverage_improvement": 0.90,
        "assurance_quality": 0.94,
        "timeliness": 0.88,
        "capacity_efficiency": 0.92,
        "created_at": now_iso
    }
    _in_memory_plan_effectivenesses[peff1["id"]] = peff1

    pfail1 = {
        "id": "apfail_01",
        "plan_id": "aplan_failed_02",
        "failure_type": "capacity_failure",
        "reason": "Specialist bandwidth unavailable during Q2 freeze period.",
        "created_at": now_iso
    }
    _in_memory_plan_failures[pfail1["id"]] = pfail1

_initialize_seed_resilience_planning_data()


class TransformationResilienceKnowledgeAssurancePlanningService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_PLANNING_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may aggregate risks, identify systemic patterns, draft options, simulate sequences, prepare assurance plans, monitor execution, and prepare verification
        # Agents may NOT approve plans, accept risk, allocate organizational budget, change governance, or execute material changes without authorization
        forbidden_actions = [
            "approve_plan", "accept_risk", "allocate_budget",
            "change_governance", "execute_material_changes"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing assurance planning governance action '{action}'. Plan approval and budget allocation require human governance authority."
            }
        return {"allowed": True, "reason": "Action permitted for knowledge assurance planning agent."}

    @staticmethod
    async def get_knowledge_assurance_planning_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_planning_data()
        domains = list(_in_memory_assurance_planning_domains.values())
        portfolios = list(_in_memory_assurance_portfolios.values())
        systemic = list(_in_memory_systemic_risks.values())
        root_causes = list(_in_memory_root_cause_groups.values())
        levers = list(_in_memory_remediation_levers.values())
        capacities = list(_in_memory_assurance_capacities.values())
        constraints = list(_in_memory_capacity_constraints.values())
        demands = list(_in_memory_assurance_demands.values())
        options = list(_in_memory_assurance_options.values())
        sequences = list(_in_memory_assurance_sequences.values())
        scenarios = list(_in_memory_assurance_scenarios.values())
        plans = list(_in_memory_assurance_plans.values())
        residuals = list(_in_memory_assurance_residual_risks.values())
        tradeoffs = list(_in_memory_assurance_tradeoffs.values())
        recommendations = list(_in_memory_assurance_recommendations.values())
        verifications = list(_in_memory_plan_verifications.values())
        effectivenesses = list(_in_memory_plan_effectivenesses.values())
        failures = list(_in_memory_plan_failures.values())

        approved_cnt = sum(1 for p in plans if p.get("status") == "approved")
        pending_cnt = sum(1 for p in plans if p.get("status") == "pending_approval")

        return {
            "domainsCount": len(domains),
            "portfoliosCount": len(portfolios),
            "systemicRisksCount": len(systemic),
            "rootCausesCount": len(root_causes),
            "leversCount": len(levers),
            "optionsCount": len(options),
            "plansCount": len(plans),
            "approvedPlansCount": approved_cnt,
            "pendingPlansCount": pending_cnt,
            "capacityGap": "15.0% Specialist Capacity Deficit in Q3",
            "domains": domains,
            "portfolios": portfolios,
            "systemicRisks": systemic,
            "rootCauses": root_causes,
            "levers": levers,
            "capacities": capacities,
            "constraints": constraints,
            "demands": demands,
            "options": options,
            "sequences": sequences,
            "scenarios": scenarios,
            "plans": plans,
            "residuals": residuals,
            "tradeoffs": tradeoffs,
            "recommendations": recommendations,
            "verifications": verifications,
            "effectivenesses": effectivenesses,
            "failures": failures
        }

    @staticmethod
    async def create_assurance_plan(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_resilience_planning_data()
        plan_id = f"aplan_{uuid.uuid4().hex[:8]}"
        due_iso = (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()

        plan = {
            "id": plan_id,
            "objective": data.get("objective", "Multi-region knowledge risk assurance plan"),
            "scope": data.get("scope", "enterprise"),
            "selected_options_json": data.get("selected_options_json", []),
            "sequence_id": data.get("sequence_id", "aseq_01"),
            "capacity_allocation_json": data.get("capacity_allocation_json", {"specialists": 0.80}),
            "risk_coverage": 0.92,
            "residual_risk": 0.08,
            "assumptions": data.get("assumptions", "Standard telemetry availability"),
            "owner": data.get("owner", "Principal Assurance Planning Architect"),
            "deadline": due_iso,
            "status": "draft"
        }
        _in_memory_assurance_plans[plan_id] = plan

        # Recommendation explicitly labeled ANALYTICAL RECOMMENDATION — NOT APPROVAL
        rec = {
            "id": f"arec_{uuid.uuid4().hex[:8]}",
            "plan_id": plan_id,
            "label": "ANALYTICAL RECOMMENDATION — NOT APPROVAL",
            "recommendation_text": f"Analytical recommendation for plan '{plan['objective']}'. Requires human governance approval.",
            "confidence": 0.94
        }
        _in_memory_assurance_recommendations[rec["id"]] = rec

        TransformationResilienceKnowledgeAssurancePlanningService.emit_event(
            "transformation.resilience.knowledge.assurance_plan.created", plan
        )
        return plan

    @staticmethod
    async def submit_assurance_plan_for_approval(session: Optional[AsyncSession], plan_id: str) -> dict:
        _initialize_seed_resilience_planning_data()
        plan = _in_memory_assurance_plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found."}

        plan["status"] = "pending_approval"
        TransformationResilienceKnowledgeAssurancePlanningService.emit_event(
            "transformation.resilience.knowledge.assurance_plan.submitted", plan
        )
        return {"plan_id": plan_id, "status": "pending_approval", "approval_routed": True}

    @staticmethod
    async def process_natural_language_assurance_planning_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_planning_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking employee productivity scoring, individual remediation performance, or employee rankings)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee productivity score", "employee ranking", "individual remediation performance",
            "rank personnel", "rank employee", "surveillance"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee productivity scoring, individual remediation performance, or employee rankings."},
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
                    "weakest_assurance": "Knowledge assurance is weakest in Secondary Cloud SLA Telemetry across Wave 4 Cloud Transformation.",
                    "systemic_risks": "Systemic Risk: Telemetry deficit affects 5 decisions across 2 major transformations (Dependency Centrality: 92%).",
                    "root_causes": "Root Cause: Lack of direct synthetic monitoring integration with vendor interconnect telemetry.",
                    "remediation_levers": "Highest Coverage Lever: Deploy Third-Party Independent Synthetic Telemetry Mesh (Coverage: 85%).",
                    "capacity_constraints": "Capacity Constraint: 15.0% Specialist Capacity Deficit in Q3 (Cloud SLA verification bandwidth limited).",
                    "assurance_plan": "Recommended Plan 'aplan_01' (Parallel Synthetic Telemetry) achieves 92% risk coverage (Residual risk: 8%).",
                    "recommendation_notice": "ANALYTICAL RECOMMENDATION — NOT APPROVAL. Requires human governance approval prior to execution."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Knowledge Assurance Planning & Portfolio Optimization 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
