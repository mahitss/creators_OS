import pytest
import asyncio
import time
from app.services.transformation_resilience_assurance_intelligence_service import (
    TransformationResilienceAssuranceIntelligenceService,
    _EMITTED_ASSURANCE_EVENTS
)

def test_get_assurance_intelligence_overview():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        assert res["domainsCount"] >= 1
        assert res["outcomesCount"] >= 1
        assert res["comparisonsCount"] >= 1
        assert res["variancesCount"] >= 1
        assert res["evidencesCount"] >= 1
        assert res["causalsCount"] >= 1
        assert res["recQualitiesCount"] >= 1
        assert res["decQualitiesCount"] >= 1
        assert res["patternsCount"] >= 1
        assert res["analoguesCount"] >= 1
        assert res["signalsCount"] >= 1
        assert res["proposalsCount"] >= 2
        assert res["versionsCount"] >= 1
        assert res["regressionsCount"] >= 1
        assert res["lessonsCount"] >= 1
    asyncio.run(_test())

def test_decision_outcomes_expected_vs_actual_and_variance():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        doc = res["outcomes"][0]
        eac = res["comparisons"][0]
        ovar = res["variances"][0]
        assert doc["outcome_status"] == "positive"
        assert doc["selected_option"] == "sequence"
        assert eac["expected_coverage"] == 0.92
        assert eac["actual_coverage"] == 0.94
        assert ovar["dimension"] == "coverage"
        assert ovar["delta"] == 0.02
    asyncio.run(_test())

def test_causal_analysis_and_provenance_evidence():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        oev = res["evidences"][0]
        causal = res["causals"][0]
        assert oev["source"] == "resilience_sensing"
        assert oev["evidence_type"] == "telemetry_verification"
        assert causal["causal_relationship"] == "contributed_to"
        assert "Sequencing simulation compute" in causal["description"]
    asyncio.run(_test())

def test_recommendation_quality_and_decision_quality():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        rq = res["recommendationQualities"][0]
        dq = res["decisionQualities"][0]
        assert rq["risk_calibration"] == 0.95
        assert rq["coverage_accuracy"] == 0.96
        assert dq["information_sufficiency"] == 0.95
        assert dq["governance_alignment"] == 0.98
    asyncio.run(_test())

def test_pattern_performance_and_historical_analogues():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        pp = res["patternPerformances"][0]
        analog = res["historicalAnalogues"][0]
        assert pp["usage_count"] == 12
        assert pp["success_count"] == 11
        assert analog["relevance_score"] == 0.90
        assert "Historical case involved legacy Oracle database" in analog["differences_description"]
    asyncio.run(_test())


def test_recommendation_calibration_learning_signals_and_proposals():
    async def _test():
        res = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        rcal = res["calibrations"][0]
        lsig = res["learningSignals"][0]
        kup = res["knowledgeUpdateProposals"][0]
        rup = res["recommendationUpdateProposals"][0]
        assert rcal["status"] == "well_calibrated"
        assert lsig["priority"] == "high"
        assert kup["status"] == "pending_review"
        assert rup["status"] == "pending_review"

        # Test requesting proposal approval
        req = await TransformationResilienceAssuranceIntelligenceService.request_proposal_approval(None, "kup_01")
        assert req["status"] == "awaiting_approval"
        assert req["approval_routed"] is True
    asyncio.run(_test())

def test_shadow_evaluation_regressions_and_drifts():
    async def _test():
        seval = await TransformationResilienceAssuranceIntelligenceService.run_shadow_evaluation(None, {
            "production_recommendation": "sequence",
            "shadow_recommendation": "sequence_with_capacity_buffer"
        })
        assert seval["status"] == "completed"
        assert seval["production_recommendation"] == "sequence"
        assert seval["shadow_recommendation"] == "sequence_with_capacity_buffer"

        overview = await TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None)
        reg = overview["regressions"][0]
        rdrift = overview["drifts"][0]
        assert reg["affected_dimension"] == "risk_calibration"
        assert rdrift["drift_type"] == "confidence_drift"
    asyncio.run(_test())

def test_agent_governance_learning_restrictions():
    # Agents may analyze outcomes, compare expected vs actual, identify learning signals, prepare lessons, identify analogues, prepare update proposals, run shadow evaluations, detect regressions
    # Agents may NOT approve learning, change production governance, deploy material recommendation changes, change decision rights, or bypass policy
    chk_approve = TransformationResilienceAssuranceIntelligenceService.enforce_agent_governance("agent_01", "approve_learning")
    assert chk_approve["allowed"] is False
    assert "strictly blocked" in chk_approve["reason"]

    chk_gov = TransformationResilienceAssuranceIntelligenceService.enforce_agent_governance("agent_01", "change_production_governance")
    assert chk_gov["allowed"] is False

    chk_deploy = TransformationResilienceAssuranceIntelligenceService.enforce_agent_governance("agent_01", "deploy_material_recommendation_change")
    assert chk_deploy["allowed"] is False

    chk_analyze = TransformationResilienceAssuranceIntelligenceService.enforce_agent_governance("agent_01", "run_shadow_evaluations")
    assert chk_analyze["allowed"] is True

def test_process_natural_language_assurance_intelligence_query_privacy_dlp_tenant():
    async def _test():
        # Valid query -> succeeds with 5 core distinctions & verified lessons
        valid_q = "Show expected vs actual outcomes and recommendation calibration."
        res = await TransformationResilienceAssuranceIntelligenceService.process_natural_language_assurance_intelligence_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5
        assert "WHAT WAS RECOMMENDED" in res["results"][0]["five_core_distinctions"]
        assert "Expected coverage 92% vs Actual coverage 94%" in res["results"][0]["expected_vs_actual_variance"]

        # Anti-Surveillance / Privacy safeguard breach (employee performance profile or worker behavioral learning score) -> blocked
        surveil_q = "Calculate employee performance profile and rank worker behavioral learning score"
        blocked_surveil = await TransformationResilienceAssuranceIntelligenceService.process_natural_language_assurance_intelligence_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "prohibits employee performance profiles" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked
        dlp_q = "Show decision outcome details. vpr_100000000000"
        blocked_dlp = await TransformationResilienceAssuranceIntelligenceService.process_natural_language_assurance_intelligence_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceAssuranceIntelligenceService.process_natural_language_assurance_intelligence_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceAssuranceIntelligenceService.get_assurance_intelligence_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
