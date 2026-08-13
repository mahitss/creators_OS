import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_portfolios: Dict[str, dict] = {}
_in_memory_exposures: Dict[str, dict] = {}
_in_memory_shared_deps: Dict[str, dict] = {}
_in_memory_capacity_exposures: Dict[str, dict] = {}
_in_memory_capacity_conflicts: Dict[str, dict] = {}
_in_memory_failure_patterns: Dict[str, dict] = {}
_in_memory_systemic_risks: Dict[str, dict] = {}
_in_memory_multi_failures: Dict[str, dict] = {}
_in_memory_portfolio_investments: Dict[str, dict] = {}
_in_memory_overlaps: Dict[str, dict] = {}
_in_memory_gaps: Dict[str, dict] = {}
_in_memory_tradeoffs: Dict[str, dict] = {}
_in_memory_sequences: Dict[str, dict] = {}
_in_memory_option_values: Dict[str, dict] = {}
_in_memory_diversifications: Dict[str, dict] = {}
_in_memory_portfolio_roadmaps: Dict[str, dict] = {}
_in_memory_portfolio_reviews: Dict[str, dict] = {}

_EMITTED_PORTFOLIO_EVENTS: List[dict] = []

EMITTED_PORTFOLIO_EVENT_TYPES = [
    "transformation.resilience.portfolio.created",
    "transformation.resilience.portfolio.exposure.updated",
    "transformation.resilience.shared_dependency.detected",
    "transformation.resilience.capacity_exposure.detected",
    "transformation.resilience.capacity_conflict.detected",
    "transformation.resilience.failure_pattern.detected",
    "transformation.resilience.systemic_risk.detected",
    "transformation.resilience.multi_failure.created",
    "transformation.resilience.portfolio.simulation.started",
    "transformation.resilience.portfolio.simulation.completed",
    "transformation.resilience.investment.created",
    "transformation.resilience.investment.overlap",
    "transformation.resilience.investment.gap",
    "transformation.resilience.portfolio.tradeoff.created",
    "transformation.resilience.investment.sequence.created",
    "transformation.resilience.option_value.updated",
    "transformation.resilience.diversification.created",
    "transformation.resilience.portfolio.roadmap.created",
    "transformation.resilience.portfolio.review.created",
    "transformation.resilience.portfolio.verified",
    "transformation.resilience.portfolio.learning.created"
]

def _initialize_seed_resilience_portfolio_data():
    if _in_memory_portfolios:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Portfolio
    port1 = {
        "id": "port_res_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Resilience Portfolio 2.0",
        "scope": "enterprise",
        "owner": "Chief Enterprise Resilience Architect",
        "status": "baseline",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_portfolios[port1["id"]] = port1

    # Exposure & Shared Dependency
    exp1 = {
        "id": "exp_01",
        "portfolio_id": port1["id"],
        "transformation_id": "wave_02_finops",
        "exposure_type": "dependency",
        "severity": "high",
        "confidence": 0.94
    }
    _in_memory_exposures[exp1["id"]] = exp1

    dep1 = {
        "id": "sdep_01",
        "portfolio_id": port1["id"],
        "dependency_name": "Central IAM OAuth Federation Gateway v2",
        "affected_transformations_json": ["wave_02_finops", "wave_03_sso", "wave_04_hr_cloud"],
        "criticality": 0.96,
        "failure_impact_json": {"estimated_schedule_slip_days": 45, "at_risk_benefit_amount": 1800000.0},
        "substitution_options_json": ["Active-Active Multi-Region Gateway", "Mesh Rate-Limiter Cluster"]
    }
    _in_memory_shared_deps[dep1["id"]] = dep1

    # Capacity & Conflicts
    cap1 = {
        "id": "cap_01",
        "portfolio_id": port1["id"],
        "capacity_type": "engineering_fte",
        "affected_transformations_json": ["wave_02_finops", "wave_03_sso"],
        "required_capacity": 45.0,
        "available_capacity": 30.0,
        "contention_score": 0.88
    }
    _in_memory_capacity_exposures[cap1["id"]] = cap1

    conf1 = {
        "id": "conf_01",
        "portfolio_id": port1["id"],
        "conflicting_investments_json": ["pinv_01", "pinv_02"],
        "capacity_resource": "Senior IAM Security Engineers",
        "severity": "high"
    }
    _in_memory_capacity_conflicts[conf1["id"]] = conf1

    # Pattern, Systemic Risk, Multi-Failure Scenario
    pat1 = {
        "id": "fpat_01",
        "portfolio_id": port1["id"],
        "pattern_name": "Shared Identity Dependency Bottleneck Pattern",
        "recurring_failure_type": "single_dependency",
        "affected_transformations_count": 4,
        "confidence": 0.95
    }
    _in_memory_failure_patterns[pat1["id"]] = pat1

    srisk1 = {
        "id": "srisk_01",
        "portfolio_id": port1["id"],
        "source_dependency": "Central OAuth Gateway API",
        "affected_scope_json": ["Wave 2 FinOps", "Wave 3 SSO", "Wave 4 HR Migration"],
        "severity": "critical",
        "confidence": 0.97
    }
    _in_memory_systemic_risks[srisk1["id"]] = srisk1

    mfail1 = {
        "id": "mfail_01",
        "portfolio_id": port1["id"],
        "scenario_title": "Simultaneous IAM Gateway Failure & Regional Cloud Quota Exhaustion",
        "simultaneous_failures_json": ["IAM OAuth Outage", "AWS East Quota Slip"],
        "correlated_propagation_json": {"stage_1": "Auth Stalled", "stage_2": "FinOps Data Pipeline Stalled"},
        "created_at": now_iso
    }
    _in_memory_multi_failures[mfail1["id"]] = mfail1

    # Investment, Overlap, Gap
    pinv1 = {
        "id": "pinv_01",
        "portfolio_id": port1["id"],
        "investment_title": "Cross-Portfolio Active-Active IAM Gateway & 15 FTE Resilience Reserve",
        "cost": 350000.0,
        "protected_transformations_json": ["wave_02_finops", "wave_03_sso", "wave_04_hr_cloud"],
        "risk_reduction_pct": 65.0,
        "priority": "high"
    }
    _in_memory_portfolio_investments[pinv1["id"]] = pinv1

    over1 = {
        "id": "over_01",
        "portfolio_id": port1["id"],
        "overlapping_investments_json": ["pinv_01", "wave_02_local_failover"],
        "duplicated_coverage_description": "Wave 2 local failover investment is redundant given portfolio-wide active-active IAM deployment.",
        "potential_savings": 120000.0,
        "created_at": now_iso
    }
    _in_memory_overlaps[over1["id"]] = over1

    gap1 = {
        "id": "gap_01",
        "portfolio_id": port1["id"],
        "unprotected_systemic_exposure": "Wave 4 HR Cloud Migration lacks fallback vendor SLA coverage.",
        "affected_transformations_json": ["wave_04_hr_cloud"],
        "severity": "high"
    }
    _in_memory_gaps[gap1["id"]] = gap1

    # Trade-off, Sequence, Option Value, Diversification, Roadmap, Review
    trade1 = {
        "id": "trade_01",
        "portfolio_id": port1["id"],
        "option_a_json": {"title": "Active-Active IAM Gateway", "cost": 350000.0, "risk_reduction": 65.0},
        "option_b_json": {"title": "Distributed Rate Limiter Only", "cost": 150000.0, "risk_reduction": 35.0},
        "tradeoff_comparison_json": {"recommended": "option_a", "rationale": "Option A protects 3 parallel waves versus 1."},
        "created_at": now_iso
    }
    _in_memory_tradeoffs[trade1["id"]] = trade1

    seq1 = {
        "id": "seq_01",
        "portfolio_id": port1["id"],
        "sequence_order": 1,
        "investment_id": pinv1["id"],
        "prerequisites_json": []
    }
    _in_memory_sequences[seq1["id"]] = seq1

    optv1 = {
        "id": "optv_01",
        "portfolio_id": port1["id"],
        "option_name": "Multi-Cloud IAM Federation Option",
        "flexibility_score": 0.93,
        "preserved_future_paths_count": 4,
        "created_at": now_iso
    }
    _in_memory_option_values[optv1["id"]] = optv1

    div1 = {
        "id": "div_01",
        "portfolio_id": port1["id"],
        "concentration_target": "Single Primary Cloud Auth Provider",
        "proposed_diversification": "Deploy secondary cloud provider fallback route for non-sensitive workloads.",
        "recommendation_only": True
    }
    _in_memory_diversifications[div1["id"]] = div1

    road1 = {
        "id": "proad_01",
        "portfolio_id": port1["id"],
        "roadmap_title": "Enterprise Portfolio Resilience Protection Roadmap 2.0",
        "milestones_json": ["Q3 Active-Active Deploy", "Q4 Multi-Cloud Fallback", "Q1 Capacity Balancing"],
        "total_budget": 750000.0,
        "status": "draft"
    }
    _in_memory_portfolio_roadmaps[road1["id"]] = road1

    rev1 = {
        "id": "prev_01",
        "portfolio_id": port1["id"],
        "review_trigger": "Shared Dependency Concentration Exceeded 90%",
        "summary_findings_json": {"status": "action_required", "recommended_action": "Fund pinv_01"},
        "status": "open",
        "created_at": now_iso
    }
    _in_memory_portfolio_reviews[rev1["id"]] = rev1

_initialize_seed_resilience_portfolio_data()


class TransformationResiliencePortfolioService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_PORTFOLIO_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from autonomous budget allocations, investment approvals, or priority changes
        forbidden_actions = [
            "allocate_budget", "approve_investment", "change_portfolio_priority",
            "cancel_transformation", "restructure_organization", "change_governance",
            "execute_resilience_investment"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing non-read-only portfolio action '{action}'. Action requires PolicyEngine authorization + human approval."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_portfolio_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_portfolio_data()
        portfolios = list(_in_memory_portfolios.values())
        exposures = list(_in_memory_exposures.values())
        shared_deps = list(_in_memory_shared_deps.values())
        capacity_exposures = list(_in_memory_capacity_exposures.values())
        capacity_conflicts = list(_in_memory_capacity_conflicts.values())
        failure_patterns = list(_in_memory_failure_patterns.values())
        systemic_risks = list(_in_memory_systemic_risks.values())
        multi_failures = list(_in_memory_multi_failures.values())
        investments = list(_in_memory_portfolio_investments.values())
        overlaps = list(_in_memory_overlaps.values())
        gaps = list(_in_memory_gaps.values())
        tradeoffs = list(_in_memory_tradeoffs.values())
        sequences = list(_in_memory_sequences.values())
        option_values = list(_in_memory_option_values.values())
        diversifications = list(_in_memory_diversifications.values())
        roadmaps = list(_in_memory_portfolio_roadmaps.values())
        reviews = list(_in_memory_portfolio_reviews.values())

        return {
            "activePortfoliosCount": len(portfolios),
            "systemicExposuresCount": len(exposures),
            "sharedDependenciesCount": len(shared_deps),
            "capacityConflictsCount": len(capacity_conflicts),
            "systemicRisksCount": len(systemic_risks),
            "investmentCandidatesCount": len(investments),
            "investmentOverlapsCount": len(overlaps),
            "investmentGapsCount": len(gaps),
            "portfolioRobustnessScore": 0.94,
            "portfolios": portfolios,
            "exposures": exposures,
            "sharedDependencies": shared_deps,
            "capacityExposures": capacity_exposures,
            "capacityConflicts": capacity_conflicts,
            "failurePatterns": failure_patterns,
            "systemicRisks": systemic_risks,
            "multiFailures": multi_failures,
            "investments": investments,
            "overlaps": overlaps,
            "gaps": gaps,
            "tradeoffs": tradeoffs,
            "sequences": sequences,
            "optionValues": option_values,
            "diversifications": diversifications,
            "roadmaps": roadmaps,
            "reviews": reviews
        }

    @staticmethod
    async def create_portfolio_resilience_investment(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_resilience_portfolio_data()
        inv_id = data.get("id", f"pinv_{uuid.uuid4().hex[:8]}")
        item = {
            "id": inv_id,
            "portfolio_id": data.get("portfolio_id", "port_res_01"),
            "investment_title": data.get("investment_title", data.get("investmentTitle", "Portfolio Resilience Investment")),
            "cost": float(data.get("cost", 350000.0)),
            "protected_transformations_json": data.get("protected_transformations_json", ["wave_02_finops", "wave_03_sso"]),
            "risk_reduction_pct": float(data.get("risk_reduction_pct", data.get("riskReductionPct", 60.0))),
            "priority": data.get("priority", "high")
        }
        _in_memory_portfolio_investments[inv_id] = item
        TransformationResiliencePortfolioService.emit_event("transformation.resilience.investment.created", item)
        return item

    @staticmethod
    async def simulate_investment(session: Optional[AsyncSession], port_id: str, inv_id: str) -> dict:
        _initialize_seed_resilience_portfolio_data()
        TransformationResiliencePortfolioService.emit_event("transformation.resilience.portfolio.simulation.started", {"portfolio_id": port_id, "investment_id": inv_id})
        res = {
            "portfolioId": port_id,
            "investmentId": inv_id,
            "simulationCompleted": True,
            "baselinePortfolioRobustness": 0.94,
            "simulatedPortfolioRobustness": 0.99,
            "riskReductionPct": 65.0,
            "protectedTransformationsCount": 3,
            "paybackHorizon": "Q3 2026"
        }
        TransformationResiliencePortfolioService.emit_event("transformation.resilience.portfolio.simulation.completed", res)
        return res

    @staticmethod
    async def create_multi_failure_scenario(session: Optional[AsyncSession], port_id: str, data: dict) -> dict:
        _initialize_seed_resilience_portfolio_data()
        scen_id = f"mfail_{uuid.uuid4().hex[:8]}"
        scen = {
            "id": scen_id,
            "portfolio_id": port_id,
            "scenario_title": data.get("scenario_title", data.get("scenarioTitle", "Simultaneous Failure Scenario")),
            "simultaneous_failures_json": data.get("simultaneous_failures_json", ["IAM Failure", "Quota Breach"]),
            "correlated_propagation_json": data.get("correlated_propagation_json", {"impact": "high"}),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_multi_failures[scen_id] = scen
        TransformationResiliencePortfolioService.emit_event("transformation.resilience.multi_failure.created", scen)
        return scen

    @staticmethod
    async def complete_portfolio_review(session: Optional[AsyncSession], review_id: str) -> dict:
        _initialize_seed_resilience_portfolio_data()
        rev = _in_memory_portfolio_reviews.get(review_id)
        if not rev:
            rev = {"id": review_id, "portfolio_id": "port_res_01", "status": "open"}
        rev["status"] = "completed"
        _in_memory_portfolio_reviews[review_id] = rev
        TransformationResiliencePortfolioService.emit_event("transformation.resilience.portfolio.review.created", rev)
        return rev

    @staticmethod
    async def process_natural_language_portfolio_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_portfolio_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking individual employee or investment performance rankings)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee resilience", "individual worker", "worker performance", "surveillance", "rank employee"]):
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
                    "portfolio": "Global Enterprise Transformation Resilience Portfolio (port_res_01 - Status: BASELINE)",
                    "shared_dependency": "Central IAM OAuth Federation Gateway v2 (Criticality: 96%)",
                    "systemic_risk": "Central OAuth Gateway API failure propagates to FinOps, SSO, and HR Migration waves.",
                    "capacity_conflict": "Senior IAM Security Engineers bottleneck between pinv_01 and pinv_02.",
                    "investment_overlap": "Overlap between pinv_01 and Wave 2 local failover ($120k potential savings).",
                    "recommended_investment": "Cross-Portfolio Active-Active IAM Gateway & 15 FTE Resilience Reserve ($350k investment, 65% risk reduction)",
                    "portfolio_roadmap": "Enterprise Portfolio Resilience Protection Roadmap 2.0 ($750k budget)"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Portfolio 2.0 Engine",
                "portfolio_robustness_score": 0.94
            },
            "confidencePct": 97.5
        }
