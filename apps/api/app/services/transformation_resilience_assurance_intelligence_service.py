import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_intelligence_domains: Dict[str, dict] = {}
_in_memory_decision_outcomes: Dict[str, dict] = {}
_in_memory_expected_actual_comparisons: Dict[str, dict] = {}
_in_memory_outcome_variances: Dict[str, dict] = {}
_in_memory_outcome_evidences: Dict[str, dict] = {}
_in_memory_causal_analyses: Dict[str, dict] = {}
_in_memory_recommendation_qualities: Dict[str, dict] = {}
_in_memory_decision_qualities: Dict[str, dict] = {}
_in_memory_decision_quality_trends: Dict[str, dict] = {}
_in_memory_pattern_performances: Dict[str, dict] = {}
_in_memory_context_similarities: Dict[str, dict] = {}
_in_memory_historical_analogues: Dict[str, dict] = {}
_in_memory_recommendation_calibrations: Dict[str, dict] = {}
_in_memory_learning_signals: Dict[str, dict] = {}
_in_memory_learning_priorities: Dict[str, dict] = {}
_in_memory_knowledge_update_proposals: Dict[str, dict] = {}
_in_memory_recommendation_update_proposals: Dict[str, dict] = {}
_in_memory_learning_versions: Dict[str, dict] = {}
_in_memory_recommendation_regressions: Dict[str, dict] = {}
_in_memory_recommendation_drifts: Dict[str, dict] = {}
_in_memory_lessons: Dict[str, dict] = {}
_in_memory_lesson_qualities: Dict[str, dict] = {}

_EMITTED_ASSURANCE_EVENTS: List[dict] = []

EMITTED_ASSURANCE_EVENT_TYPES = [
    "transformation.resilience.assurance.intelligence.domain.created",
    "transformation.resilience.assurance.decision.outcome.recorded",
    "transformation.resilience.assurance.expected_actual.compared",
    "transformation.resilience.assurance.outcome.variance.detected",
    "transformation.resilience.assurance.outcome.evidence.recorded",
    "transformation.resilience.assurance.causal.analysis.created",
    "transformation.resilience.assurance.recommendation.quality.updated",
    "transformation.resilience.assurance.decision.quality.updated",
    "transformation.resilience.assurance.pattern.performance.updated",
    "transformation.resilience.assurance.historical_analogue.detected",
    "transformation.resilience.assurance.recommendation.calibration.updated",
    "transformation.resilience.assurance.learning_signal.detected",
    "transformation.resilience.assurance.learning_priority.updated",
    "transformation.resilience.assurance.knowledge_update.proposed",
    "transformation.resilience.assurance.recommendation_update.proposed",
    "transformation.resilience.assurance.learning.review_requested",
    "transformation.resilience.assurance.learning.approved",
    "transformation.resilience.assurance.learning.version.created",
    "transformation.resilience.assurance.shadow_evaluation.completed",
    "transformation.resilience.assurance.recommendation.regression.detected",
    "transformation.resilience.assurance.recommendation.drift.detected",
    "transformation.resilience.assurance.lesson.created",
    "transformation.resilience.assurance.lesson.reuse.detected"
]

def _initialize_seed_assurance_intelligence_data():
    if _in_memory_intelligence_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Assurance Intelligence Domain
    dom1 = {
        "id": "adom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Assurance Decision Intelligence & Closed-Loop Resolution Learning 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Assurance Decision Intelligence Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_intelligence_domains[dom1["id"]] = dom1

    # Decision Outcome
    doc1 = {
        "id": "dout_01",
        "decision_id": "dec_seq_01",
        "conflict_id": "ccase_01",
        "plan_id": "aplan_01",
        "recommendation_id": "crec_01",
        "selected_option": "sequence",
        "execution_status": "completed",
        "verification_status": "verified",
        "outcome_status": "positive",
        "observed_at": now_iso
    }
    _in_memory_decision_outcomes[doc1["id"]] = doc1

    # Expected vs Actual Comparison & Variance
    eac1 = {
        "id": "eac_01",
        "decision_outcome_id": doc1["id"],
        "expected_risk": 0.08,
        "actual_risk": 0.07,
        "expected_coverage": 0.92,
        "actual_coverage": 0.94,
        "expected_effort": "medium",
        "actual_effort": "medium",
        "expected_timeline_days": 14,
        "actual_timeline_days": 13,
        "expected_capacity_pct": 80.0,
        "actual_capacity_pct": 78.0,
        "expected_residual_risk": 0.08,
        "actual_residual_risk": 0.06,
        "created_at": now_iso
    }
    _in_memory_expected_actual_comparisons[eac1["id"]] = eac1

    ovar1 = {
        "id": "ovar_01",
        "comparison_id": eac1["id"],
        "dimension": "coverage",
        "expected_val": 0.92,
        "actual_val": 0.94,
        "delta": 0.02,
        "confidence": 0.95,
        "explanation_status": "explained"
    }
    _in_memory_outcome_variances[ovar1["id"]] = ovar1

    # Outcome Evidence & Causal Analysis
    oev1 = {
        "id": "oev_01",
        "decision_outcome_id": doc1["id"],
        "source": "resilience_sensing",
        "evidence_type": "telemetry_verification",
        "quality": 0.95,
        "relationship": "verified_telemetry",
        "confidence": 0.96,
        "created_at": now_iso
    }
    _in_memory_outcome_evidences[oev1["id"]] = oev1

    causal1 = {
        "id": "causal_01",
        "decision_outcome_id": doc1["id"],
        "causal_relationship": "contributed_to",
        "description": "Sequencing simulation compute directly relieved 20% over-subscription without delaying critical deployment milestones.",
        "confidence": 0.92,
        "created_at": now_iso
    }
    _in_memory_causal_analyses[causal1["id"]] = causal1

    # Recommendation Quality & Decision Quality
    rq1 = {
        "id": "rq_01",
        "recommendation_id": "crec_01",
        "evidence_quality": 0.94,
        "scenario_quality": 0.92,
        "risk_calibration": 0.95,
        "coverage_accuracy": 0.96,
        "timeline_accuracy": 0.90,
        "capacity_accuracy": 0.92,
        "uncertainty_calibration": 0.94,
        "created_at": now_iso
    }
    _in_memory_recommendation_qualities[rq1["id"]] = rq1

    dq1 = {
        "id": "dq_01",
        "decision_id": "dec_seq_01",
        "information_sufficiency": 0.95,
        "option_completeness": 0.92,
        "tradeoff_visibility": 0.94,
        "uncertainty_visibility": 0.90,
        "governance_alignment": 0.98,
        "outcome_alignment": 0.94,
        "created_at": now_iso
    }
    _in_memory_decision_qualities[dq1["id"]] = dq1

    dqtrend1 = {
        "id": "dqtrend_01",
        "domain_id": dom1["id"],
        "average_quality": 0.94,
        "trend_direction": "improving",
        "created_at": now_iso
    }
    _in_memory_decision_quality_trends[dqtrend1["id"]] = dqtrend1

    # Pattern Performance & Context Similarity & Historical Analogue
    ppperf1 = {
        "id": "ppperf_01",
        "pattern_id": "rpatt_01",
        "usage_count": 12,
        "success_count": 11,
        "failure_count": 1,
        "risk_reduction_avg": 0.90,
        "coverage_preservation_avg": 0.92,
        "deadline_recovery_avg": 0.88,
        "capacity_relief_avg": 0.85,
        "uncertainty_reduction_avg": 0.94,
        "created_at": now_iso
    }
    _in_memory_pattern_performances[ppperf1["id"]] = ppperf1

    csim1 = {
        "id": "csim_01",
        "case_a_id": "ccase_01",
        "case_b_id": "ccase_hist_99",
        "similarity_score": 0.88,
        "matching_dimensions_json": ["risk_type", "resource_constraints", "knowledge_conditions"]
    }
    _in_memory_context_similarities[csim1["id"]] = csim1

    analog1 = {
        "id": "analog_01",
        "current_case_id": "ccase_01",
        "historical_case_id": "ccase_hist_99",
        "similarities_description": "Both cases involved simulation cluster compute bottlenecks in Q3 rollout waves.",
        "differences_description": "Historical case involved legacy Oracle database while current case involves cloud-native Postgres.",
        "historical_outcome": "positive",
        "relevance_score": 0.90,
        "confidence": 0.92
    }
    _in_memory_historical_analogues[analog1["id"]] = analog1

    # Recommendation Calibration
    rcal1 = {
        "id": "rcal_01",
        "domain_id": dom1["id"],
        "predicted_confidence_avg": 0.95,
        "observed_accuracy_avg": 0.94,
        "calibration_error": 0.01,
        "status": "well_calibrated",
        "created_at": now_iso
    }
    _in_memory_recommendation_calibrations[rcal1["id"]] = rcal1

    # Learning Signal & Priority
    lsig1 = {
        "id": "lsig_01",
        "signal_type": "recurring_pattern",
        "source": "resolution_learning",
        "description": "Sequencing simulation compute workloads across adjacent weeks consistently preserves >90% coverage.",
        "priority": "high",
        "confidence": 0.95,
        "created_at": now_iso
    }
    _in_memory_learning_signals[lsig1["id"]] = lsig1

    lprio1 = {
        "id": "lprio_01",
        "learning_signal_id": lsig1["id"],
        "priority_score": 0.92,
        "decision_impact": "high",
        "recurrence_frequency": 4,
        "severity": "high"
    }
    _in_memory_learning_priorities[lprio1["id"]] = lprio1

    # Update Proposals
    kup1 = {
        "id": "kup_01",
        "learning_signal_id": lsig1["id"],
        "proposal_type": "new_validation_requirement",
        "description": "Require simulation cluster capacity validation prior to final Q3 wave authorization.",
        "status": "pending_review",
        "created_at": now_iso
    }
    _in_memory_knowledge_update_proposals[kup1["id"]] = kup1

    rup1 = {
        "id": "rup_01",
        "learning_signal_id": lsig1["id"],
        "current_behavior": "Default to parallel execution until compute failure detected.",
        "observed_weakness": "Causes 20% compute over-subscription during peak validation windows.",
        "proposed_improvement": "Proactively recommend sequenced execution when cluster utilization exceeds 85%.",
        "status": "pending_review",
        "created_at": now_iso
    }
    _in_memory_recommendation_update_proposals[rup1["id"]] = rup1

    # Learning Version & Regressions & Drift
    lver1 = {
        "id": "lver_01",
        "version_number": "v2.0",
        "parent_version": "v1.0",
        "changes_summary": "Integrated closed-loop resolution learning and recommendation optimization 2.0.",
        "reason": "Elevates recommendation accuracy and eliminates simulation compute over-subscription.",
        "approval_state": "approved",
        "created_at": now_iso
    }
    _in_memory_learning_versions[lver1["id"]] = lver1

    reg1 = {
        "id": "reg_01",
        "previous_version": "v1.0",
        "new_version": "v2.0",
        "affected_dimension": "risk_calibration",
        "severity": "low",
        "description": "Minor 0.5% variance increase in secondary timeline prediction window."
    }
    _in_memory_recommendation_regressions[reg1["id"]] = reg1

    rdrift1 = {
        "id": "rdrift_01",
        "drift_type": "confidence_drift",
        "description": "Confidence drift detected: vendor operations plans show higher variance in timeline predictions.",
        "created_at": now_iso
    }
    _in_memory_recommendation_drifts[rdrift1["id"]] = rdrift1

    # Lessons & Quality
    less1 = {
        "id": "less_01",
        "lesson_type": "success",
        "title": "Sequenced Simulation Workload Optimization Lesson",
        "description": "Staggering compute-intensive simulation workloads by 7 days resolves capacity shortages without compromising risk coverage.",
        "created_at": now_iso
    }
    _in_memory_lessons[less1["id"]] = less1

    lqual1 = {
        "id": "lqual_01",
        "lesson_id": less1["id"],
        "evidence_quality": 0.95,
        "recurrence_count": 5,
        "confidence": 0.96
    }
    _in_memory_lesson_qualities[lqual1["id"]] = lqual1

_initialize_seed_assurance_intelligence_data()


class TransformationResilienceAssuranceIntelligenceService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_ASSURANCE_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may analyze outcomes, compare expected vs actual, identify learning signals, prepare lessons, identify analogues, prepare update proposals, run shadow evaluations, detect regressions
        # Agents may NOT approve learning, change production governance, deploy material recommendation changes, change decision rights, or bypass policy
        forbidden_actions = [
            "approve_learning", "change_production_governance", "deploy_material_recommendation_change",
            "change_decision_rights", "bypass_policy"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing learning governance action '{action}'. Approval belongs strictly to human governance."
            }
        return {"allowed": True, "reason": "Action permitted for assurance decision intelligence agent."}

    @staticmethod
    async def get_assurance_intelligence_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_assurance_intelligence_data()
        domains = list(_in_memory_intelligence_domains.values())
        outcomes = list(_in_memory_decision_outcomes.values())
        comparisons = list(_in_memory_expected_actual_comparisons.values())
        variances = list(_in_memory_outcome_variances.values())
        evidences = list(_in_memory_outcome_evidences.values())
        causals = list(_in_memory_causal_analyses.values())
        rec_qualities = list(_in_memory_recommendation_qualities.values())
        dec_qualities = list(_in_memory_decision_qualities.values())
        trends = list(_in_memory_decision_quality_trends.values())
        patterns = list(_in_memory_pattern_performances.values())
        similarities = list(_in_memory_context_similarities.values())
        analogues = list(_in_memory_historical_analogues.values())
        calibrations = list(_in_memory_recommendation_calibrations.values())
        signals = list(_in_memory_learning_signals.values())
        priorities = list(_in_memory_learning_priorities.values())
        ku_proposals = list(_in_memory_knowledge_update_proposals.values())
        ru_proposals = list(_in_memory_recommendation_update_proposals.values())
        versions = list(_in_memory_learning_versions.values())
        regressions = list(_in_memory_recommendation_regressions.values())
        drifts = list(_in_memory_recommendation_drifts.values())
        lessons = list(_in_memory_lessons.values())
        lesson_qualities = list(_in_memory_lesson_qualities.values())

        return {
            "domainsCount": len(domains),
            "outcomesCount": len(outcomes),
            "comparisonsCount": len(comparisons),
            "variancesCount": len(variances),
            "evidencesCount": len(evidences),
            "causalsCount": len(causals),
            "recQualitiesCount": len(rec_qualities),
            "decQualitiesCount": len(dec_qualities),
            "patternsCount": len(patterns),
            "analoguesCount": len(analogues),
            "signalsCount": len(signals),
            "proposalsCount": len(ku_proposals) + len(ru_proposals),
            "versionsCount": len(versions),
            "regressionsCount": len(regressions),
            "lessonsCount": len(lessons),
            "domains": domains,
            "outcomes": outcomes,
            "comparisons": comparisons,
            "variances": variances,
            "evidences": evidences,
            "causals": causals,
            "recommendationQualities": rec_qualities,
            "decisionQualities": dec_qualities,
            "decisionQualityTrends": trends,
            "patternPerformances": patterns,
            "contextSimilarities": similarities,
            "historicalAnalogues": analogues,
            "calibrations": calibrations,
            "learningSignals": signals,
            "learningPriorities": priorities,
            "knowledgeUpdateProposals": ku_proposals,
            "recommendationUpdateProposals": ru_proposals,
            "learningVersions": versions,
            "regressions": regressions,
            "drifts": drifts,
            "lessons": lessons,
            "lessonQualities": lesson_qualities
        }

    @staticmethod
    async def run_shadow_evaluation(session: Optional[AsyncSession], data: dict) -> dict:
        _initialize_seed_assurance_intelligence_data()
        seval_id = f"seval_{uuid.uuid4().hex[:8]}"
        res = {
            "id": seval_id,
            "production_recommendation": data.get("production_recommendation", "sequence"),
            "shadow_recommendation": data.get("shadow_recommendation", "sequence_with_capacity_buffer"),
            "production_coverage_predicted": 0.92,
            "shadow_coverage_predicted": 0.95,
            "production_risk_predicted": 0.08,
            "shadow_risk_predicted": 0.05,
            "status": "completed",
            "production_impact": "none",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        TransformationResilienceAssuranceIntelligenceService.emit_event(
            "transformation.resilience.assurance.shadow_evaluation.completed", res
        )
        return res

    @staticmethod
    async def request_proposal_approval(session: Optional[AsyncSession], proposal_id: str) -> dict:
        _initialize_seed_assurance_intelligence_data()
        prop = _in_memory_knowledge_update_proposals.get(proposal_id) or _in_memory_recommendation_update_proposals.get(proposal_id)
        if not prop:
            return {"error": "Proposal not found."}

        prop["status"] = "awaiting_approval"
        TransformationResilienceAssuranceIntelligenceService.emit_event(
            "transformation.resilience.assurance.learning.review_requested",
            {"proposal_id": proposal_id, "status": "awaiting_approval"}
        )
        return {
            "proposal_id": proposal_id,
            "status": "awaiting_approval",
            "approval_routed": True
        }

    @staticmethod
    async def process_natural_language_assurance_intelligence_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_assurance_intelligence_data()

        # Anti-Surveillance / Privacy check (blocking employee performance profiles, individual behavioral learning scores, or worker rankings)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee performance profile", "worker behavioral learning score", "employee ranking",
            "individual behavioral profile", "rank worker learning", "surveil worker learning"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee performance profiles, worker behavioral learning scores, or employee rankings."},
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
                    "five_core_distinctions": "WHAT WAS RECOMMENDED ('sequence') vs WHAT WAS DECIDED ('sequence') vs WHAT WAS EXECUTED ('sequence week 1 & 2') vs WHAT ACTUALLY HAPPENED ('positive outcome, 94% coverage, 0.07 risk') vs WHAT WAS LEARNED ('sequencing compute workloads staggering by 7 days resolves capacity bottlenecks').",
                    "expected_vs_actual_variance": "Expected coverage 92% vs Actual coverage 94% (+2% variance, explained by verified telemetry).",
                    "causal_analysis": "Causal relationship: 'contributed_to' (verified via telemetry; temporal correlation alone is never treated as automatic causation).",
                    "recommendation_quality": "Recommendation Quality: 94% overall (risk calibration 95%, coverage accuracy 96%, timeline accuracy 90%).",
                    "pattern_performance": "Pattern 'Sequenced Simulation Workload Resolution Pattern' (Usage: 12, Success: 11, Failure: 1, 92% coverage preservation).",
                    "calibration": "Recommendation Calibration: Well Calibrated (predicted confidence 95% vs observed accuracy 94%, calibration error 1%).",
                    "lessons": "Lesson: Staggering compute-intensive simulation workloads by 7 days resolves capacity shortages without compromising risk coverage.",
                    "learning_proposal": "Knowledge Update Proposal 'kup_01' (Require simulation cluster capacity validation prior to final Q3 wave authorization) pending human approval."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Assurance Decision Intelligence & Closed-Loop Resolution Learning 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
