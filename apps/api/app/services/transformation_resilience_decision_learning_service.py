import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_learning_domains: Dict[str, dict] = {}
_in_memory_expected_outcomes: Dict[str, dict] = {}
_in_memory_observed_outcomes: Dict[str, dict] = {}
_in_memory_outcome_comparisons: Dict[str, dict] = {}
_in_memory_attributions: Dict[str, dict] = {}
_in_memory_external_factors: Dict[str, dict] = {}
_in_memory_failure_analyses: Dict[str, dict] = {}
_in_memory_success_patterns: Dict[str, dict] = {}
_in_memory_failure_patterns: Dict[str, dict] = {}
_in_memory_decision_patterns: Dict[str, dict] = {}
_in_memory_lessons: Dict[str, dict] = {}
_in_memory_lesson_applications: Dict[str, dict] = {}
_in_memory_lesson_conflicts: Dict[str, dict] = {}
_in_memory_quality_assessments: Dict[str, dict] = {}
_in_memory_calibrations: Dict[str, dict] = {}
_in_memory_model_performances: Dict[str, dict] = {}
_in_memory_delay_analyses: Dict[str, dict] = {}
_in_memory_counterfactuals: Dict[str, dict] = {}

_EMITTED_LEARNING_EVENTS: List[dict] = []

EMITTED_LEARNING_EVENT_TYPES = [
    "transformation.resilience.learning.domain.created",
    "transformation.resilience.decision.expected_outcome.created",
    "transformation.resilience.decision.observed_outcome.created",
    "transformation.resilience.decision.outcome.compared",
    "transformation.resilience.decision.attribution.created",
    "transformation.resilience.decision.external_factor.detected",
    "transformation.resilience.decision.failure.analyzed",
    "transformation.resilience.decision.success_pattern.detected",
    "transformation.resilience.decision.failure_pattern.detected",
    "transformation.resilience.decision.pattern.detected",
    "transformation.resilience.decision.precedent.updated",
    "transformation.resilience.decision.lesson.created",
    "transformation.resilience.decision.lesson.conflict.detected",
    "transformation.resilience.decision.lesson.application.updated",
    "transformation.resilience.decision.quality.assessed",
    "transformation.resilience.decision.calibration.updated",
    "transformation.resilience.decision.scenario.learning.created",
    "transformation.resilience.decision.simulation.learning.created",
    "transformation.resilience.decision.model.performance.updated",
    "transformation.resilience.decision.recommendation.quality.updated",
    "transformation.resilience.decision.delay.analyzed",
    "transformation.resilience.decision.counterfactual.created"
]

def _initialize_seed_resilience_learning_data():
    if _in_memory_learning_domains:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Learning Domain
    ldom1 = {
        "id": "learn_dom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Continuous Resilience Decision Quality & Outcome Intelligence 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Decision Learning Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_learning_domains[ldom1["id"]] = ldom1

    dec_id = "dec_res_01"

    # Expected vs Observed Outcomes & Comparison
    exp1 = {
        "id": "exp_out_01",
        "decision_id": dec_id,
        "objective": "Restore Primary OAuth Gateway Latency and SLA Stability",
        "metric": "OAuth Gateway P99 Latency ms",
        "target_value": 45.0,
        "expected_time": "2026-Q3",
        "confidence": 0.95,
        "source": "DigitalTwin_Simulation_v2.0"
    }
    _in_memory_expected_outcomes[exp1["id"]] = exp1

    obs1 = {
        "id": "obs_out_01",
        "decision_id": dec_id,
        "metric": "OAuth Gateway P99 Latency ms",
        "observed_value": 42.0,
        "timestamp": now_iso,
        "source": "EventMesh.IdentityGateway",
        "confidence": 0.96,
        "freshness": 1.0
    }
    _in_memory_observed_outcomes[obs1["id"]] = obs1

    comp1 = {
        "id": "comp_01",
        "decision_id": dec_id,
        "expected_value": 45.0,
        "observed_value": 42.0,
        "variance_pct": -6.67,
        "variance_type": "better_than_expected",
        "confidence": 0.96,
        "materiality": "high"
    }
    _in_memory_outcome_comparisons[comp1["id"]] = comp1

    # Attribution & External Factors
    attr1 = {
        "id": "attr_01",
        "decision_id": dec_id,
        "attribution_level": "likely_related",
        "rationale": "Multi-region token cache pre-warming reduced cold-start latency spikes by 18ms.",
        "confidence": 0.88
    }
    _in_memory_attributions[attr1["id"]] = attr1

    ext1 = {
        "id": "ext_01",
        "decision_id": dec_id,
        "factor_type": "vendor_disruption",
        "description": "Secondary Cloud Region network provider performed unscheduled fiber maintenance.",
        "impact_level": "medium"
    }
    _in_memory_external_factors[ext1["id"]] = ext1

    # Failure & Success Patterns
    fail_an1 = {
        "id": "fail_an_01",
        "decision_id": dec_id,
        "failure_type": "bad_assumption",
        "root_cause_summary": "Secondary region network latency exceeded assumed 35ms threshold by 12ms during initial stress test.",
        "lessons_learned_ref": "less_01"
    }
    _in_memory_failure_analyses[fail_an1["id"]] = fail_an1

    spat1 = {
        "id": "succ_pat_01",
        "domain_id": ldom1["id"],
        "pattern_title": "Multi-Region Token Cache Pre-Warming Pattern",
        "conditions_json": {"active_active": True, "token_cache": "pre_warmed"},
        "supporting_cases_count": 6,
        "confidence": 0.94,
        "limitations": "Requires dedicated interconnect bandwidth >= 10Gbps."
    }
    _in_memory_success_patterns[spat1["id"]] = spat1

    fpat1 = {
        "id": "fail_pat_01",
        "domain_id": ldom1["id"],
        "pattern_title": "Single-Region Auth Bottleneck Pattern",
        "frequency": 4,
        "scope_json": ["wave_02_finops", "wave_04_hr_cloud"],
        "confidence": 0.92
    }
    _in_memory_failure_patterns[fpat1["id"]] = fpat1

    dpat1 = {
        "id": "dec_pat_01",
        "domain_id": ldom1["id"],
        "context_type": "high_concurrency_auth_expansion",
        "typical_outcome": "85% risk reduction when paired with Active-Active failover",
        "confidence": 0.91
    }
    _in_memory_decision_patterns[dpat1["id"]] = dpat1

    # Lessons & Lesson Conflicts & Applications
    less1 = {
        "id": "less_01",
        "domain_id": ldom1["id"],
        "lesson_type": "assumption",
        "lesson": "Secondary Cloud Region latency assumptions must include a +15ms vendor SLA buffer.",
        "evidence_json": {"decision_id": dec_id, "observed_variance_pct": -6.67},
        "confidence": "validated",
        "scope_json": ["enterprise_cloud_infrastructure"]
    }
    less2 = {
        "id": "less_02",
        "domain_id": ldom1["id"],
        "lesson_type": "capacity",
        "lesson": "Token cache replication should rely on eventual consistency to save inter-region bandwidth.",
        "evidence_json": {"source": "Sprint 70 Post-Mortem"},
        "confidence": "medium",
        "scope_json": ["wave_03_sso"]
    }
    _in_memory_lessons[less1["id"]] = less1
    _in_memory_lessons[less2["id"]] = less2

    lapp1 = {
        "id": "lapp_01",
        "lesson_id": less1["id"],
        "affected_transformation_id": "wave_04_hr_cloud",
        "status": "applied",
        "notes": "Buffer added to Wave 4 HR Cloud deployment architecture."
    }
    _in_memory_lesson_applications[lapp1["id"]] = lapp1

    lconf1 = {
        "id": "lconf_01",
        "lesson_a_id": less1["id"],
        "lesson_b_id": less2["id"],
        "conflict_description": "Lesson 1 recommends strict SLA buffering for cache latency while Lesson 2 recommends relaxed eventual consistency.",
        "context_differences_json": {"lesson_a_context": "Real-time OAuth Auth", "lesson_b_context": "Non-critical SSO Sessions"},
        "created_at": now_iso
    }
    _in_memory_lesson_conflicts[lconf1["id"]] = lconf1

    # Multi-Dimensional Decision Quality Assessment (8 Dimensions)
    qual1 = {
        "id": "qual_01",
        "decision_id": dec_id,
        "evidence_completeness": 0.95,
        "assumption_quality": 0.92,
        "scenario_coverage": 0.96,
        "option_diversity": 0.90,
        "tradeoff_completeness": 0.94,
        "decision_timeliness": 0.88,
        "execution_quality": 0.95,
        "verification_quality": 0.96,
        "created_at": now_iso
    }
    _in_memory_quality_assessments[qual1["id"]] = qual1

    # Calibration & Model Performance
    cal1 = {
        "id": "cal_01",
        "decision_id": dec_id,
        "prediction_value": 45.0,
        "actual_value": 42.0,
        "error_pct": 6.67,
        "bias_direction": "conservative",
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_calibrations[cal1["id"]] = cal1

    mperf1 = {
        "id": "mperf_01",
        "model_version": "DigitalTwin_v2.0",
        "outcome_accuracy_pct": 94.5,
        "evaluated_cases_count": 42,
        "created_at": now_iso
    }
    _in_memory_model_performances[mperf1["id"]] = mperf1

    # Delay Analysis & Counterfactuals
    delay1 = {
        "id": "delay_01",
        "decision_id": dec_id,
        "deadline": "2026-Q3",
        "actual_decision_time": "2026-Q3",
        "delay_days": 2.5,
        "consequence_summary": "$12,500/day risk burn during 2.5-day executive alignment delay."
    }
    _in_memory_delay_analyses[delay1["id"]] = delay1

    count1 = {
        "id": "count_01",
        "decision_id": dec_id,
        "simulated_alternative": "Option C: Do Nothing",
        "simulated_outcome": "Cascading OAuth outage affecting 3 transformation waves.",
        "label": "SIMULATED - COUNTERFACTUAL"
    }
    _in_memory_counterfactuals[count1["id"]] = count1

_initialize_seed_resilience_learning_data()


class TransformationResilienceDecisionLearningService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_LEARNING_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents are strictly blocked from modifying governance, changing decision rights, approving decisions, executing investments, or rewriting historical outcomes
        forbidden_actions = [
            "modify_governance", "change_decision_rights", "approve_decision",
            "execute_investment", "rewrite_history", "alter_historical_outcomes"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing learning governance action '{action}'. Historical outcomes and governance rights are immutable."
            }
        return {"allowed": True, "reason": "Action permitted."}

    @staticmethod
    async def get_decision_learning_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_learning_data()
        domains = list(_in_memory_learning_domains.values())
        expected = list(_in_memory_expected_outcomes.values())
        observed = list(_in_memory_observed_outcomes.values())
        comparisons = list(_in_memory_outcome_comparisons.values())
        attributions = list(_in_memory_attributions.values())
        ext_factors = list(_in_memory_external_factors.values())
        failures = list(_in_memory_failure_analyses.values())
        succ_patterns = list(_in_memory_success_patterns.values())
        fail_patterns = list(_in_memory_failure_patterns.values())
        dec_patterns = list(_in_memory_decision_patterns.values())
        lessons = list(_in_memory_lessons.values())
        lapps = list(_in_memory_lesson_applications.values())
        conflicts = list(_in_memory_lesson_conflicts.values())
        qualities = list(_in_memory_quality_assessments.values())
        calibrations = list(_in_memory_calibrations.values())
        mperfs = list(_in_memory_model_performances.values())
        delays = list(_in_memory_delay_analyses.values())
        counterfactuals = list(_in_memory_counterfactuals.values())

        return {
            "domainsCount": len(domains),
            "expectedOutcomesCount": len(expected),
            "observedOutcomesCount": len(observed),
            "comparisonsCount": len(comparisons),
            "lessonsCount": len(lessons),
            "validatedLessonsCount": sum(1 for l in lessons if l.get("confidence") == "validated"),
            "conflictsCount": len(conflicts),
            "successPatternsCount": len(succ_patterns),
            "failurePatternsCount": len(fail_patterns),
            "domains": domains,
            "expectedOutcomes": expected,
            "observedOutcomes": observed,
            "comparisons": comparisons,
            "attributions": attributions,
            "externalFactors": ext_factors,
            "failures": failures,
            "successPatterns": succ_patterns,
            "failurePatterns": fail_patterns,
            "decisionPatterns": dec_patterns,
            "lessons": lessons,
            "lessonApplications": lapps,
            "lessonConflicts": conflicts,
            "qualityAssessments": qualities,
            "calibrations": calibrations,
            "modelPerformances": mperfs,
            "delayAnalyses": delays,
            "counterfactuals": counterfactuals
        }

    @staticmethod
    async def create_lesson(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_resilience_learning_data()
        less_id = f"less_{uuid.uuid4().hex[:8]}"
        less = {
            "id": less_id,
            "domain_id": data.get("domain_id", "learn_dom_01"),
            "lesson_type": data.get("lesson_type", "assumption"),
            "lesson": data.get("lesson", "New Resilience Lesson"),
            "evidence_json": data.get("evidence_json", {}),
            "confidence": data.get("confidence", "validated"),
            "scope_json": data.get("scope_json", ["enterprise"])
        }
        _in_memory_lessons[less_id] = less
        TransformationResilienceDecisionLearningService.emit_event("transformation.resilience.decision.lesson.created", less)
        return less

    @staticmethod
    async def process_natural_language_learning_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_learning_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking worker decision rankings or behavioral profiles)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee decision-quality", "employee decision quality", "individual decision quality",
            "worker performance", "surveillance", "rank personnel", "rank employee",
            "behavioral profiles", "decision-quality ranking", "decision quality ranking"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual worker decision-quality rankings or behavioral profiles."},
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
                    "outcome_comparison": "OAuth Gateway Latency observed 42.0ms vs 45.0ms target (Variance: -6.67%, Better Than Expected).",
                    "attribution": "Likely Related (Multi-region token cache pre-warming reduced cold-start latency spikes by 18ms).",
                    "failure_analysis": "Root cause for initial stress test failure: Secondary region network latency exceeded assumed 35ms threshold by 12ms.",
                    "success_pattern": "Multi-Region Token Cache Pre-Warming Pattern (Supported by 6 cases, Confidence: 94%).",
                    "validated_lesson": "Secondary Cloud Region latency assumptions must include a +15ms vendor SLA buffer (Validated).",
                    "lesson_conflict": "Conflict detected between Lesson 1 (strict buffer) and Lesson 2 (eventual consistency) due to workload difference.",
                    "decision_quality": "Evidence Completeness: 95%, Scenario Coverage: 96%, Tradeoff Completeness: 94%, Timeliness: 88%",
                    "calibration_error": "6.67% error with conservative bias; DigitalTwin_v2.0 accuracy: 94.5%",
                    "counterfactual_analysis": "Option C: Do Nothing would have caused cascading OAuth outage affecting 3 transformation waves (Label: SIMULATED - COUNTERFACTUAL)"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Decision Learning 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
