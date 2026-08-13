import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_decision_domains: Dict[str, dict] = {}
_in_memory_decision_questions: Dict[str, dict] = {}
_in_memory_decision_contexts: Dict[str, dict] = {}
_in_memory_evidence_packs: Dict[str, dict] = {}
_in_memory_decision_assumptions: Dict[str, dict] = {}
_in_memory_decision_options: Dict[str, dict] = {}
_in_memory_scenario_sets: Dict[str, dict] = {}
_in_memory_tradeoffs: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_decisions: Dict[str, dict] = {}
_in_memory_consequences: Dict[str, dict] = {}
_in_memory_execution_plans: Dict[str, dict] = {}
_in_memory_verifications: Dict[str, dict] = {}
_in_memory_effectivenesses: Dict[str, dict] = {}
_in_memory_failures: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_precedents: Dict[str, dict] = {}

_EMITTED_DECISION_EVENTS: List[dict] = []

EMITTED_DECISION_EVENT_TYPES = [
    "transformation.resilience.decision.domain.created",
    "transformation.resilience.decision.detected",
    "transformation.resilience.decision.context.snapshot.created",
    "transformation.resilience.decision.evidence.created",
    "transformation.resilience.decision.assumption.created",
    "transformation.resilience.decision.option.created",
    "transformation.resilience.decision.scenario.created",
    "transformation.resilience.decision.tradeoff.created",
    "transformation.resilience.decision.recommendation.created",
    "transformation.resilience.decision.approval.requested",
    "transformation.resilience.decision.approved",
    "transformation.resilience.decision.rejected",
    "transformation.resilience.decision.deferred",
    "transformation.resilience.decision.created",
    "transformation.resilience.decision.execution.started",
    "transformation.resilience.decision.execution.completed",
    "transformation.resilience.decision.verification.completed",
    "transformation.resilience.decision.effectiveness.updated",
    "transformation.resilience.decision.failure.detected",
    "transformation.resilience.decision.review.requested",
    "transformation.resilience.decision.reopened",
    "transformation.resilience.decision.precedent.created",
    "transformation.resilience.decision.learning.created"
]

def _initialize_seed_resilience_decision_data():
    if _in_memory_decision_domains:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Decision Domain
    dom1 = {
        "id": "dec_dom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Governed Resilience Decision OS 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Decision Governance Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_decision_domains[dom1["id"]] = dom1

    # Decision Record & Question
    dec1 = {
        "id": "dec_res_01",
        "domain_id": dom1["id"],
        "decision_title": "Active-Active Multi-Region Identity Gateway Architecture & Funding Decision",
        "owner": "Chief Resilience Officer & VP Enterprise Infrastructure",
        "status": "pending_decision",
        "selected_option_id": None,
        "rationale_summary": "Mitigate primary OAuth Auth Gateway SLA drift (99.91%) and single-region vendor lock-in.",
        "approval_state": "submitted",
        "deadline": "2026-Q3",
        "created_at": now_iso
    }
    _in_memory_decisions[dec1["id"]] = dec1

    q1 = {
        "id": "dec_q_01",
        "domain_id": dom1["id"],
        "question": "Should Enterprise Board approve $350,000 funding for pinv_01 Active-Active IAM Gateway deployment?",
        "context_description": "OAuth Gateway P99 latency reached 142.5ms causing downstream FinOps & HR cloud wave contention.",
        "trigger": "warning",
        "scope": "portfolio",
        "deadline": "2026-Q3",
        "decision_owner": dec1["owner"],
        "required_approvers_json": ["PolicyEngine", "Enterprise Executive Board", "Chief Security Officer"]
    }
    _in_memory_decision_questions[q1["id"]] = q1

    # Decision Context Snapshot (Versioned)
    ctx1 = {
        "id": "dec_ctx_01",
        "decision_id": dec1["id"],
        "portfolio_state_json": {"robustness": 0.94, "redundancy": 0.91, "observability": 0.96},
        "resilience_state_json": {"recoverability": 0.95, "optionality": 0.93},
        "dependencies_json": ["Central IAM OAuth Gateway API v2", "Wave 02 FinOps", "Wave 04 HR Cloud"],
        "capacity_json": {"resource": "Senior IAM Engineers", "margin": "-15.0 FTE"},
        "recovery_json": {"paths": 4, "readiness": 0.95},
        "risk_json": {"primary_risk": "OAuth Gateway Bottleneck"},
        "assumptions_json": ["Primary Auth Gateway SLA >= 99.99%"],
        "scenario_versions_json": {"DigitalTwin": "v2.0"},
        "created_at": now_iso
    }
    _in_memory_decision_contexts[ctx1["id"]] = ctx1

    # Evidence Pack
    evpack1 = {
        "id": "dec_ev_01",
        "decision_id": dec1["id"],
        "evidence_items_json": [
            {"metric": "Primary Gateway SLA", "observed_value": 99.91, "target": 99.99},
            {"metric": "Gateway Latency P99", "observed_value": "142.5ms", "target": "<100ms"}
        ],
        "source": "EventMesh.IdentityGateway + ResilienceSensingEngine",
        "freshness": 1.0,
        "quality": 0.95,
        "confidence": 0.94,
        "conflicts_json": [
            {"source_a": "EventMesh.IdentityGateway", "source_b": "KPI.OAuthMonitor", "description": "142.5ms vs 118ms due to sampling window difference."}
        ]
    }
    _in_memory_evidence_packs[evpack1["id"]] = evpack1

    # Assumptions & Sensitivity
    assm1 = {
        "id": "dec_assm_01",
        "decision_id": dec1["id"],
        "assumption": "Secondary Multi-Cloud region latency remains under 35ms overhead.",
        "source": "ForesightScenarioEngine",
        "confidence": 0.92,
        "sensitivity": "critical",
        "status": "valid"
    }
    _in_memory_decision_assumptions[assm1["id"]] = assm1

    # Options Analysis (3 Options)
    opt1 = {
        "id": "opt_01",
        "decision_id": dec1["id"],
        "option_type": "add_redundancy",
        "title": "Option A: Full Active-Active Multi-Region IAM Deployment (Recommended)",
        "benefits_json": ["SLA restored to 99.99%", "Eliminates single cloud failure point"],
        "risks_json": ["$350k capital expenditure", "2-week maintenance window"],
        "cost": 350000.0,
        "capacity_impact_json": {"required_fte": 4.5},
        "dependencies_json": ["Cloud Provider Region B"],
        "reversibility": "high",
        "optionality_score": 0.96
    }
    opt2 = {
        "id": "opt_02",
        "decision_id": dec1["id"],
        "option_type": "invest",
        "title": "Option B: Rate Limiting Cluster Only",
        "benefits_json": ["$150k cost", "Fast 3-day rollout"],
        "risks_json": ["Does not fix single cloud vendor outage risk"],
        "cost": 150000.0,
        "capacity_impact_json": {"required_fte": 1.5},
        "dependencies_json": [],
        "reversibility": "high",
        "optionality_score": 0.72
    }
    opt3 = {
        "id": "opt_03",
        "decision_id": dec1["id"],
        "option_type": "maintain_current",
        "title": "Option C: Do Nothing (Maintain Baseline)",
        "benefits_json": ["$0 immediate spend"],
        "risks_json": ["Cascading SLA breach on Wave 2 FinOps and Wave 4 HR Cloud"],
        "cost": 0.0,
        "capacity_impact_json": {"required_fte": 0.0},
        "dependencies_json": [],
        "reversibility": "instant",
        "optionality_score": 0.40
    }
    _in_memory_decision_options[opt1["id"]] = opt1
    _in_memory_decision_options[opt2["id"]] = opt2
    _in_memory_decision_options[opt3["id"]] = opt3

    # Scenario Set & Trade-off Matrix
    scenset1 = {
        "id": "dec_scen_01",
        "decision_id": dec1["id"],
        "evaluated_scenarios_json": ["baseline", "stress", "severe", "multi-failure", "capacity-constrained"],
        "scenario_comparisons_json": {
            "opt_01": {"robustness_under_severe": 0.96, "payback": "Q3 2026"},
            "opt_02": {"robustness_under_severe": 0.81, "payback": "Q4 2026"},
            "opt_03": {"robustness_under_severe": 0.54, "payback": "N/A"}
        },
        "created_at": now_iso
    }
    _in_memory_scenario_sets[scenset1["id"]] = scenset1

    tradeoff1 = {
        "id": "dec_to_01",
        "decision_id": dec1["id"],
        "tradeoff_matrix_json": {
            "comparison": [
                {"option": "Option A", "cost": 350000, "risk_reduction": "65%", "optionality": 0.96},
                {"option": "Option B", "cost": 150000, "risk_reduction": "25%", "optionality": 0.72},
                {"option": "Option C", "cost": 0, "risk_reduction": "0%", "optionality": 0.40}
            ]
        },
        "created_at": now_iso
    }
    _in_memory_tradeoffs[tradeoff1["id"]] = tradeoff1

    # Recommendation (Explicit Labeling as "RECOMMENDATION - NOT DECISION")
    rec1 = {
        "id": "dec_rec_01",
        "decision_id": dec1["id"],
        "recommended_option_id": opt1["id"],
        "supporting_evidence_json": {"evidence_pack_id": evpack1["id"], "confidence": 0.94},
        "confidence": 0.95,
        "alternatives_json": ["Option B: Rate Limiting Cluster Only ($150k)", "Option C: Do Nothing"],
        "limitations": "Requires 2-week scheduled maintenance window in Region B.",
        "required_approval": "PolicyEngine + Enterprise Executive Board",
        "label": "RECOMMENDATION - NOT DECISION"
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    # Consequence & Execution Plan
    consq1 = {
        "id": "dec_consq_01",
        "decision_id": dec1["id"],
        "expected_impact_json": {"robustness_boost": "+5.0%", "sla_restoration": 99.99},
        "affected_transformations_json": ["wave_02_finops", "wave_03_sso", "wave_04_hr_cloud"],
        "delay_consequence_json": {"daily_burn_rate_risk": "$12,500/day", "cascading_delay_weeks": 3.5}
    }
    _in_memory_consequences[consq1["id"]] = consq1

    execplan1 = {
        "id": "dec_exec_01",
        "decision_id": dec1["id"],
        "actions_json": [
            {"step": 1, "action": "Provision Active-Active Region B Gateway", "gateway_target": "ActionGateway"},
            {"step": 2, "action": "Sync Multi-Region OAuth Token Caches", "gateway_target": "ActionGateway"}
        ],
        "milestones_json": ["Region B Provisioned", "Traffic Cutover Completed"],
        "owner": "Lead Cloud Infrastructure Engineer",
        "rollback_strategy": "Automated traffic drain back to Region A within 30 seconds."
    }
    _in_memory_execution_plans[execplan1["id"]] = execplan1

    # Verification & Effectiveness & Failures & Reviews & Precedents
    verif1 = {
        "id": "dec_verif_01",
        "decision_id": dec1["id"],
        "expected_json": {"sla": 99.99, "latency_p99_ms": 45.0},
        "observed_json": {"sla": 99.99, "latency_p99_ms": 42.0},
        "variance_pct": 2.1,
        "confidence": 0.96
    }
    _in_memory_verifications[verif1["id"]] = verif1

    eff1 = {
        "id": "dec_eff_01",
        "decision_id": dec1["id"],
        "objective_achievement": 0.95,
        "resilience_improvement": 0.05,
        "risk_reduction_pct": 65.0
    }
    _in_memory_effectivenesses[eff1["id"]] = eff1

    fail1 = {
        "id": "dec_fail_01",
        "decision_id": dec1["id"],
        "failure_classification": "bad_assumption",
        "details": "Secondary vendor latency exceeded assumed 35ms threshold by 12ms during initial stress test."
    }
    _in_memory_failures[fail1["id"]] = fail1

    rev1 = {
        "id": "dec_rev_01",
        "decision_id": dec1["id"],
        "trigger_reason": "Assumption drift flagged on secondary region network latency.",
        "status": "review_requested",
        "created_at": now_iso
    }
    _in_memory_reviews[rev1["id"]] = rev1

    prec1 = {
        "id": "dec_prec_01",
        "prior_decision_id": "dec_hist_2025_04",
        "context_description": "2025 SSO Cluster Multi-Region Expansion",
        "outcome": "completed_successfully",
        "applicability": 0.92,
        "limitations": "Context differed in token cache sync protocol."
    }
    _in_memory_precedents[prec1["id"]] = prec1

_initialize_seed_resilience_decision_data()


class TransformationResilienceDecisionLifecycleService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_DECISION_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from approving, rejecting, funding, executing material changes, overriding owners, or changing decision rights
        forbidden_actions = [
            "approve", "reject", "fund", "execute_material_change",
            "override_owner", "change_decision_rights", "change_governance"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing decision governance action '{action}'. Decision authority belongs exclusively to human owners."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_decision_lifecycle_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_decision_data()
        domains = list(_in_memory_decision_domains.values())
        questions = list(_in_memory_decision_questions.values())
        contexts = list(_in_memory_decision_contexts.values())
        evpacks = list(_in_memory_evidence_packs.values())
        assumptions = list(_in_memory_decision_assumptions.values())
        options = list(_in_memory_decision_options.values())
        scenarios = list(_in_memory_scenario_sets.values())
        tradeoffs = list(_in_memory_tradeoffs.values())
        recs = list(_in_memory_recommendations.values())
        decisions = list(_in_memory_decisions.values())
        consequences = list(_in_memory_consequences.values())
        exec_plans = list(_in_memory_execution_plans.values())
        verifications = list(_in_memory_verifications.values())
        effectivenesses = list(_in_memory_effectivenesses.values())
        failures = list(_in_memory_failures.values())
        reviews = list(_in_memory_reviews.values())
        precedents = list(_in_memory_precedents.values())

        return {
            "domainsCount": len(domains),
            "questionsCount": len(questions),
            "decisionsCount": len(decisions),
            "optionsCount": len(options),
            "evidencePacksCount": len(evpacks),
            "precedentsCount": len(precedents),
            "domains": domains,
            "questions": questions,
            "contexts": contexts,
            "evidencePacks": evpacks,
            "assumptions": assumptions,
            "options": options,
            "scenarios": scenarios,
            "tradeoffs": tradeoffs,
            "recommendations": recs,
            "decisions": decisions,
            "consequences": consequences,
            "executionPlans": exec_plans,
            "verifications": verifications,
            "effectivenesses": effectivenesses,
            "failures": failures,
            "reviews": reviews,
            "precedents": precedents
        }

    @staticmethod
    async def make_decision(session: Optional[AsyncSession], dec_id: str, selected_option_id: str, rationale: str, decider_id: str) -> dict:
        _initialize_seed_resilience_decision_data()
        if dec_id in _in_memory_decisions:
            dec = _in_memory_decisions[dec_id]
            dec["selected_option_id"] = selected_option_id
            dec["rationale_summary"] = rationale
            dec["status"] = "approved"
            dec["approval_state"] = "approved_by_owner"
            dec["updated_at"] = datetime.now(timezone.utc).isoformat()
            TransformationResilienceDecisionLifecycleService.emit_event("transformation.resilience.decision.approved", dec)
            return dec

        res = {
            "id": dec_id,
            "selected_option_id": selected_option_id,
            "rationale_summary": rationale,
            "status": "approved",
            "owner": decider_id
        }
        TransformationResilienceDecisionLifecycleService.emit_event("transformation.resilience.decision.created", res)
        return res

    @staticmethod
    async def execute_decision(session: Optional[AsyncSession], dec_id: str, payload: dict) -> dict:
        _initialize_seed_resilience_decision_data()
        exec_id = f"exec_{uuid.uuid4().hex[:8]}"
        res = {
            "id": exec_id,
            "decision_id": dec_id,
            "action_gateway_route": "/api/v1/action-gateway/dispatch",
            "status": "executing",
            "initiated_by": payload.get("initiated_by", "Authorized Human Decision Owner"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        TransformationResilienceDecisionLifecycleService.emit_event("transformation.resilience.decision.execution.started", res)
        return res

    @staticmethod
    async def process_natural_language_decision_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_decision_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking employee decision rankings or behavioral profiles)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee decision ranking", "individual decision profile", "worker behavioral profile", "surveillance", "rank personnel"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual personnel decision profiling or behavioral surveillance."},
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
                    "decision_question": "Should Enterprise Board approve $350,000 funding for pinv_01 Active-Active IAM Gateway deployment?",
                    "trigger": "Warning (OAuth Gateway SLA Drift: 99.91%)",
                    "decision_owner": "Chief Resilience Officer & VP Enterprise Infrastructure",
                    "evidence_summary": "High evidence quality (95% score) with 1 surface conflict between EventMesh (142.5ms) and KPI Monitor (118ms).",
                    "sensitive_assumption": "Secondary Multi-Cloud region latency remains under 35ms overhead (Critical Sensitivity).",
                    "options_evaluated": "Option A: Full Active-Active ($350k), Option B: Rate Limiter ($150k), Option C: Do Nothing ($0)",
                    "recommendation": "Option A: Full Active-Active Multi-Region IAM Deployment (Label: RECOMMENDATION - NOT DECISION)",
                    "delay_consequence": "$12,500/day daily burn rate risk with 3.5 weeks cascading delay across Wave 2 & Wave 4.",
                    "required_approval": "PolicyEngine + Enterprise Executive Board",
                    "precedent_lookup": "2025 SSO Cluster Multi-Region Expansion (Applicability: 92%)"
                }
            ],
            "evidenceJson": {
                "data_source": "Governed Resilience Decision Operating System 2.0",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.0
        }
