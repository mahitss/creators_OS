import pytest
import asyncio
import time
from app.services.transformation_resilience_decision_learning_service import TransformationResilienceDecisionLearningService, _EMITTED_LEARNING_EVENTS

def test_get_decision_learning_overview():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        assert res["domainsCount"] >= 1
        assert res["expectedOutcomesCount"] >= 1
        assert res["observedOutcomesCount"] >= 1
        assert res["comparisonsCount"] >= 1
        assert res["lessonsCount"] >= 2
        assert res["validatedLessonsCount"] >= 1
        assert res["conflictsCount"] >= 1
        assert res["successPatternsCount"] >= 1
        assert res["failurePatternsCount"] >= 1
    asyncio.run(_test())

def test_expected_vs_observed_outcomes_and_comparison():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        exp = res["expectedOutcomes"][0]
        obs = res["observedOutcomes"][0]
        comp = res["comparisons"][0]
        assert exp["target_value"] == 45.0
        assert obs["observed_value"] == 42.0
        assert comp["variance_pct"] == -6.67
        assert comp["variance_type"] == "better_than_expected"
    asyncio.run(_test())

def test_attribution_external_factors_and_failure_analysis():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        attr = res["attributions"][0]
        ext = res["externalFactors"][0]
        fail = res["failures"][0]
        assert attr["attribution_level"] == "likely_related"
        assert ext["factor_type"] == "vendor_disruption"
        assert fail["failure_type"] == "bad_assumption"
    asyncio.run(_test())

def test_success_and_failure_patterns():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        spat = res["successPatterns"][0]
        fpat = res["failurePatterns"][0]
        dpat = res["decisionPatterns"][0]
        assert spat["supporting_cases_count"] == 6
        assert spat["confidence"] == 0.94
        assert fpat["frequency"] == 4
        assert "85% risk reduction" in dpat["typical_outcome"]
    asyncio.run(_test())

def test_lessons_lesson_applications_and_conflicts():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        lessons = res["lessons"]
        lapps = res["lessonApplications"]
        conflicts = res["lessonConflicts"]
        assert len(lessons) >= 2
        assert lessons[0]["confidence"] == "validated"
        assert lapps[0]["status"] == "applied"
        assert len(conflicts) >= 1
        assert "Lesson 1 recommends strict SLA buffering" in conflicts[0]["conflict_description"]
    asyncio.run(_test())

def test_multi_dimensional_quality_calibration_and_counterfactuals():
    async def _test():
        res = await TransformationResilienceDecisionLearningService.get_decision_learning_overview(None)
        qual = res["qualityAssessments"][0]
        cal = res["calibrations"][0]
        mperf = res["modelPerformances"][0]
        delay = res["delayAnalyses"][0]
        count = res["counterfactuals"][0]
        assert qual["evidence_completeness"] == 0.95
        assert qual["scenario_coverage"] == 0.96
        assert cal["error_pct"] == 6.67
        assert cal["bias_direction"] == "conservative"
        assert mperf["outcome_accuracy_pct"] == 94.5
        assert delay["delay_days"] == 2.5
        assert count["label"] == "SIMULATED - COUNTERFACTUAL"
    asyncio.run(_test())

def test_create_lesson_and_event_mesh():
    async def _test():
        less = await TransformationResilienceDecisionLearningService.create_lesson(None, {
            "lesson_type": "dependency",
            "lesson": "Token cache replication inter-region bandwidth must be pre-allocated.",
            "confidence": "validated"
        })
        assert less["confidence"] == "validated"
        assert less["lesson_type"] == "dependency"
    asyncio.run(_test())

def test_agent_governance_decision_learning_restrictions():
    # Agents are strictly blocked from modifying governance, changing decision rights, approving decisions, executing investments, or rewriting historical outcomes
    chk_gov = TransformationResilienceDecisionLearningService.enforce_agent_governance("agent_01", "modify_governance")
    assert chk_gov["allowed"] is False
    assert "strictly blocked" in chk_gov["reason"]

    chk_hist = TransformationResilienceDecisionLearningService.enforce_agent_governance("agent_01", "rewrite_history")
    assert chk_hist["allowed"] is False

    chk_appr = TransformationResilienceDecisionLearningService.enforce_agent_governance("agent_01", "approve_decision")
    assert chk_appr["allowed"] is False

    chk_read = TransformationResilienceDecisionLearningService.enforce_agent_governance("agent_01", "analyze_outcomes")
    assert chk_read["allowed"] is True

def test_process_natural_language_learning_query_privacy_dlp_tenant():
    async def _test():
        # Valid learning query -> succeeds
        valid_q = "Which resilience decisions worked best and what lessons have been validated?"
        res = await TransformationResilienceDecisionLearningService.process_natural_language_learning_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee decision-quality rankings or behavioral profiles) -> blocked
        surveil_q = "Rank employee decision quality and generate worker behavioral profiles"
        blocked_surveil = await TransformationResilienceDecisionLearningService.process_natural_language_learning_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual worker decision-quality rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show decision learning outcomes. vpr_99999999999"
        blocked_dlp = await TransformationResilienceDecisionLearningService.process_natural_language_learning_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceDecisionLearningService.process_natural_language_learning_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceDecisionLearningService.get_decision_learning_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
