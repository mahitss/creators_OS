import pytest
import asyncio
import time
from app.services.transformation_resilience_engineering_service import TransformationResilienceEngineeringService, _EMITTED_EVENTS

def test_get_resilience_overview():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        assert res["activeResilienceDomainsCount"] >= 1
        assert res["detectedFailureModesCount"] >= 1
        assert res["systemicWeaknessesCount"] >= 1
        assert res["singlePointsOfFailureCount"] >= 1
        assert res["investmentCandidatesCount"] >= 1
        assert res["resilienceRobustnessScore"] == 0.91
    asyncio.run(_test())

def test_resilience_baseline_and_dimensions():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        base = res["baselines"][0]
        assert base["robustness_score"] == 0.91
        assert base["redundancy_score"] == 0.86
        assert base["recoverability_score"] == 0.94
        assert base["adaptability_score"] == 0.89
        assert base["optionality_score"] == 0.88
        assert base["observability_score"] == 0.95
        assert base["governability_score"] == 0.92
    asyncio.run(_test())

def test_failure_modes_and_systemic_weaknesses():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        fm = res["failureModes"][0]
        fma = res["failureAnalyses"][0]
        weak = res["weaknesses"][0]
        spof = res["spofs"][0]
        assert fm["failure_type"] == "single_dependency"
        assert fm["severity"] == "high"
        assert fma["trigger_description"] != ""
        assert len(weak["affected_transformations_json"]) >= 2
        assert spof["criticality_score"] == 0.95
    asyncio.run(_test())

def test_redundancy_substitution_capacity_buffer_optionality():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        red = res["redundancies"][0]
        sub = res["substitutions"][0]
        buf = res["buffers"][0]
        opt = res["optionalities"][0]
        assert red["redundancy_type"] == "dependency"
        assert sub["substitution_type"] == "technology"
        assert buf["required_buffer_fte"] == 15.0
        assert opt["path_count"] == 3
    asyncio.run(_test())

def test_investment_creation_and_simulation():
    async def _test():
        inv = await TransformationResilienceEngineeringService.create_investment_candidate(None, {
            "improvement_title": "Multi-Region Gateway Redundancy",
            "investment_amount": 250000.0,
            "risk_reduction_pct": 45.0
        })
        assert inv["investment_amount"] == 250000.0
        assert inv["risk_reduction_pct"] == 45.0

        sim = await TransformationResilienceEngineeringService.simulate_investment(None, inv["id"])
        assert sim["simulationCompleted"] is True
        assert sim["simulatedRobustness"] == 0.98
        assert sim["crossTransformationProtectionCount"] == 3
    asyncio.run(_test())

def test_cascading_failure_fragility_and_roadmaps():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        casc = res["cascades"][0]
        road = res["roadmaps"][0]
        comp = res["comparisons"][0]
        assert casc["uncertainty_label"] == "estimated"
        assert road["investment_total"] == 430000.0
        assert comp["improved_scores_json"]["robustness"] == 0.98
    asyncio.run(_test())

def test_resilience_drill_and_learning():
    async def _test():
        drill = await TransformationResilienceEngineeringService.run_resilience_drill(None, "red_01", "Simulated Gateway Failover Drill")
        assert drill["no_production_mutation"] is True
        assert drill["status"] == "completed"
    asyncio.run(_test())

def test_resilience_warning_lesson_pattern():
    async def _test():
        res = await TransformationResilienceEngineeringService.get_resilience_overview(None)
        les = res["lessons"][0]
        pat = res["patterns"][0]
        warn = res["warnings"][0]
        assert les["confidence"] == 0.94
        assert pat["confidence"] == 0.95
        assert warn["severity"] == "high"
    asyncio.run(_test())

def test_agent_governance_restrictions():
    # Agents are strictly blocked from executing autonomous structural modifications or funding allocations
    chk = TransformationResilienceEngineeringService.enforce_agent_governance("agent_01", "allocate_investment")
    assert chk["allowed"] is False
    assert "strictly blocked" in chk["reason"]

    chk_ok = TransformationResilienceEngineeringService.enforce_agent_governance("agent_01", "read_resilience_overview")
    assert chk_ok["allowed"] is True

def test_process_natural_language_resilience_query_privacy_dlp_tenant():
    async def _test():
        # Valid resilience query -> succeeds
        valid_q = "Where are our biggest resilience weaknesses across Wave 2 and Wave 3?"
        res = await TransformationResilienceEngineeringService.process_natural_language_resilience_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 96.2

        # Anti-Surveillance / Privacy safeguard breach (employee resilience ranking) -> blocked
        surveil_q = "Rank employee resilience scores and enable worker performance surveillance"
        blocked_surveil = await TransformationResilienceEngineeringService.process_natural_language_resilience_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee resilience rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Where are our biggest resilience weaknesses? vpr_99999999999"
        blocked_dlp = await TransformationResilienceEngineeringService.process_natural_language_resilience_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceEngineeringService.process_natural_language_resilience_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceEngineeringService.get_resilience_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())

