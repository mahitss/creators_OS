import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_lifecycles: Dict[str, dict] = {}
_in_memory_transitions: Dict[str, dict] = {}
_in_memory_baselines: Dict[str, dict] = {}
_in_memory_expected_outcomes: Dict[str, dict] = {}
_in_memory_actual_outcomes: Dict[str, dict] = {}
_in_memory_variances: Dict[str, dict] = {}
_in_memory_assumption_outcomes: Dict[str, dict] = {}
_in_memory_rec_outcomes: Dict[str, dict] = {}
_in_memory_lessons: Dict[str, dict] = {}
_in_memory_patterns: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_counterfactuals: Dict[str, dict] = {}
_in_memory_regrets: Dict[str, dict] = {}
_in_memory_success_conditions: Dict[str, dict] = {}
_in_memory_failure_analyses: Dict[str, dict] = {}
_in_memory_quality_reviews: Dict[str, dict] = {}

def _initialize_seed_learning_data():
    if _in_memory_lifecycles:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    case_id = "case_scale_finops_01"

    # Lifecycle & Transitions
    lc1 = {
        "id": "lc_01",
        "decision_case_id": case_id,
        "current_stage": "learning",
        "started_at": now_iso,
        "completed_at": None,
        "last_transition_at": now_iso,
        "status": "active"
    }
    _in_memory_lifecycles[lc1["id"]] = lc1

    tr1 = {
        "id": "tr_01",
        "lifecycle_id": lc1["id"],
        "from_stage": "verification",
        "to_stage": "learning",
        "actor": "Transformation Learning Engine",
        "timestamp": now_iso,
        "reason": "Verified Wave 2 scale performance against baseline expected outcome",
        "evidence_version": "v1.2",
        "decision_packet_version": "v1.0"
    }
    _in_memory_transitions[tr1["id"]] = tr1

    # Baseline & Outcomes
    base1 = {
        "id": "base_01",
        "decision_case_id": case_id,
        "expected_benefits_json": {"annual_opex_savings": "$4.2M", "cloud_cost_reduction_pct": 30.0},
        "expected_risks_json": {"capacity_friction": "low"},
        "expected_timing_json": {"target_horizon": "90 days"},
        "expected_capacity_json": {"required_ftes": "4.5 FTEs"},
        "expected_dependencies_json": ["cand_01"],
        "expected_scenario": "baseline",
        "expected_outcome": "Sub-100ms policy validation with 30.0% Q2 OpEx reduction"
    }
    _in_memory_baselines[base1["id"]] = base1

    exp1 = {
        "id": "exp_01",
        "decision_case_id": case_id,
        "metric": "Cloud OpEx Reduction",
        "target": "30.0%",
        "range_str": "30-35%",
        "time_horizon": "90 days",
        "confidence": 0.95,
        "source": "Foresight Model v2026.3"
    }
    act1 = {
        "id": "act_01",
        "decision_case_id": case_id,
        "metric": "Cloud OpEx Reduction",
        "value": "31.2%",
        "timestamp": now_iso,
        "source": "Verified Cloud Infrastructure Accounting Connector",
        "confidence": 0.98
    }
    _in_memory_expected_outcomes[exp1["id"]] = exp1
    _in_memory_actual_outcomes[act1["id"]] = act1

    # Variance
    var1 = {
        "id": "var_01",
        "decision_case_id": case_id,
        "expected": "30.0%",
        "actual": "31.2%",
        "difference": "+1.2%",
        "direction": "favorable",
        "materiality": "minor",
        "variance_type": "benefit"
    }
    _in_memory_variances[var1["id"]] = var1

    # Assumption & Recommendation Outcomes
    ass_out1 = {
        "id": "ass_out_01",
        "decision_case_id": case_id,
        "assumption": "Multi-region Zero-Trust pre-signer API schema stability",
        "original_status": "valid",
        "actual_state": "stronger",
        "impact": "Pre-signer latency was 12.4ms vs 50.0ms threshold"
    }
    rec_out1 = {
        "id": "rec_out_01",
        "decision_case_id": case_id,
        "recommendation": "Full Wave 2 scale rollout across 4 regions",
        "decision": "Approved by Transformation Steering Committee",
        "result": "$4.2M OpEx reduction realized 5 days ahead of schedule",
        "alignment": "aligned"
    }
    _in_memory_assumption_outcomes[ass_out1["id"]] = ass_out1
    _in_memory_rec_outcomes[rec_out1["id"]] = rec_out1

    # Lesson, Pattern, Review
    les1 = {
        "id": "les_01",
        "lesson": "Pre-signer rule caching in Zero-Trust FinOps pipelines consistently delivers +1.2% higher cost reduction than baseline forecast model",
        "source_decision": case_id,
        "evidence": "Observed 31.2% actual vs 30.0% forecast across 4 region clusters",
        "confidence": "high",
        "scope": "enterprise_relevant",
        "created_at": now_iso
    }
    _in_memory_lessons[les1["id"]] = les1

    pat1 = {
        "id": "pat_01",
        "pattern": "Wave scale decisions backed by sub-20ms policy telemetry succeed with zero execution drift across 12 consecutive transformations",
        "sample_size": 12,
        "confidence": 0.96,
        "limitations": "Requires pre-signer telemetry integration"
    }
    _in_memory_patterns[pat1["id"]] = pat1

    rev1 = {
        "id": "rev_01",
        "lesson_id": les1["id"],
        "status": "approved",
        "reviewer": "Chief Architecture Officer",
        "feedback": "Approved for enterprise-wide propagation across future FinOps scale decisions"
    }
    _in_memory_reviews[rev1["id"]] = rev1

    # Counterfactual, Regret, Success, Failure, Quality
    cf1 = {
        "id": "cf_01",
        "decision_case_id": case_id,
        "actual_path": "Full Wave 2 scale rollout across 4 regions",
        "alternative_path": "Option 2: Staggered rollout across 2 regions",
        "assumptions": "Staggered path would have delayed $1.1M OpEx savings by 45 days",
        "uncertainty": "low"
    }
    reg1 = {
        "id": "reg_01",
        "decision_case_id": case_id,
        "missed_benefit": "$0 (Optimal option selected)",
        "avoidable_risk": "N/A",
        "timing_loss": "0 days",
        "optionality_loss": "Minimal temporary capacity lock-in",
        "uncertainty": "low"
    }
    sc1 = {
        "id": "sc_01",
        "decision_case_id": case_id,
        "condition_text": "Cloud OpEx reduction exceeds 30.0% within 90 days",
        "metric_target": ">= 30.0%",
        "status": "verified"
    }
    fa1 = {
        "id": "fa_01",
        "decision_case_id": case_id,
        "decision_effect": "No decision failure (Favorable outcome)",
        "execution_effect": "Zero execution drift",
        "assumption_effect": "Pre-signer latency assumption validated stronger than expected",
        "external_effect": "Cloud provider pricing remained stable"
    }
    qr1 = {
        "id": "qr_01",
        "decision_case_id": case_id,
        "cadence": "post_transformation",
        "evidence_quality": 0.95,
        "forecast_accuracy": 0.94,
        "outcome_variance": "favorable",
        "created_at": now_iso
    }
    _in_memory_counterfactuals[cf1["id"]] = cf1
    _in_memory_regrets[reg1["id"]] = reg1
    _in_memory_success_conditions[sc1["id"]] = sc1
    _in_memory_failure_analyses[fa1["id"]] = fa1
    _in_memory_quality_reviews[qr1["id"]] = qr1

_initialize_seed_learning_data()


class TransformationDecisionLearningService:

    @staticmethod
    async def get_learning_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_learning_data()
        lifecycles = list(_in_memory_lifecycles.values())
        transitions = list(_in_memory_transitions.values())
        baselines = list(_in_memory_baselines.values())
        expected_outcomes = list(_in_memory_expected_outcomes.values())
        actual_outcomes = list(_in_memory_actual_outcomes.values())
        variances = list(_in_memory_variances.values())
        assumption_outcomes = list(_in_memory_assumption_outcomes.values())
        rec_outcomes = list(_in_memory_rec_outcomes.values())
        lessons = list(_in_memory_lessons.values())
        patterns = list(_in_memory_patterns.values())
        reviews = list(_in_memory_reviews.values())
        counterfactuals = list(_in_memory_counterfactuals.values())
        regrets = list(_in_memory_regrets.values())
        success_conditions = list(_in_memory_success_conditions.values())
        failure_analyses = list(_in_memory_failure_analyses.values())
        quality_reviews = list(_in_memory_quality_reviews.values())

        return {
            "activeLifecyclesCount": len(lifecycles),
            "frozenBaselinesCount": len(baselines),
            "verifiedLessonsCount": len([l for l in lessons if l.get("confidence") == "high"]),
            "detectedPatternsCount": len(patterns),
            "approvedReviewsCount": len([r for r in reviews if r.get("status") == "approved"]),
            "forecastCalibrationAccuracyPct": 96.8,
            "lifecycles": lifecycles,
            "transitions": transitions,
            "baselines": baselines,
            "expectedOutcomes": expected_outcomes,
            "actualOutcomes": actual_outcomes,
            "variances": variances,
            "assumptionOutcomes": assumption_outcomes,
            "recOutcomes": rec_outcomes,
            "lessons": lessons,
            "patterns": patterns,
            "reviews": reviews,
            "counterfactuals": counterfactuals,
            "regrets": regrets,
            "successConditions": success_conditions,
            "failureAnalyses": failure_analyses,
            "qualityReviews": quality_reviews
        }

    @staticmethod
    async def process_natural_language_learning_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_learning_data()

        # Enforce Privacy Safeguard (blocking individual employee decision quality ranking or employee blame attribution)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["rank employee decision quality", "who was right employee", "employee blame", "judge leadership worker", "individual worker ranking"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual decision-quality rankings, employee blame attribution, or individual worker evaluation."},
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
                    "historical_case": "Wave 2 Scale Authorization: Autonomous FinOps Transformation (case_scale_finops_01)",
                    "expected_vs_actual": "Expected 30.0% OpEx reduction vs Actual 31.2% (+1.2% favorable variance)",
                    "assumption_validation": "Pre-signer latency schema stability validated stronger than expected (12.4ms)",
                    "lesson_learned": "Pre-signer rule caching consistently delivers +1.2% higher cost reduction than baseline forecast model",
                    "counterfactual_analysis": "Staggered rollout path would have delayed $1.1M OpEx savings by 45 days",
                    "detected_pattern": "Sub-20ms policy telemetry backing yields zero execution drift (Sample size: 12 transformations)",
                    "no_blame_systemic_analysis": "Zero systemic failure; process and assumptions validated favorably"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Decision Lifecycle + Closed-Loop Learning 2.0 Engine",
                "baselines_evaluated": len(_in_memory_baselines)
            },
            "confidencePct": 97.2
        }
