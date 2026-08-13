import pytest
import asyncio
from app.services.transformation_resilience_optimization_service import TransformationResilienceOptimizationService

def test_baseline():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        prob = res["problems"][0]
        assert prob["baseline_strategy"] == "continue_current_state"
    asyncio.run(_test())

def test_constraint():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        cnstr = res["constraints"][0]
        assert cnstr["constraint_type"] == "capacity"
        assert cnstr["remaining_capacity"] == 15.0
    asyncio.run(_test())

def test_candidates():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        cimps = res["candidateImpacts"]
        assert len(cimps) >= 2
        for c in cimps:
            assert "cost_usd" in c
            assert "effort_days" in c
            assert "risk_reduction_score" in c
    asyncio.run(_test())

def test_pareto():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        ppoint = res["paretoPoints"][0]
        assert ppoint["is_non_dominated"] is True
        assert len(ppoint["candidate_set_json"]) >= 1
    asyncio.run(_test())

def test_tradeoff():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        trade = res["tradeoffs"][0]
        assert trade["cost_difference_usd"] == 23000.0
        assert "Option A" in trade["tradeoff_summary"]
    asyncio.run(_test())

def test_resource():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        rreq = res["resourceRequirements"][0]
        assert rreq["shortfall"] == 15.0
    asyncio.run(_test())

def test_investment():
    async def _test():
        inv = await TransformationResilienceOptimizationService.create_investment_case(None, "cand_01")
        assert inv["label"] == "ANALYTICAL INVESTMENT CASE — NOT APPROVED BUDGET"
        assert inv["cost_usd"] == 35000.0
    asyncio.run(_test())

def test_sensitivity():
    async def _test():
        sens = await TransformationResilienceOptimizationService.run_sensitivity_analysis(None, "prob_01", "cost")
        assert sens["varied_parameter"] == "cost"
        assert sens["recommendation_changed"] is False
    asyncio.run(_test())

def test_robustness():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        rob = res["robustnesses"][0]
        assert rob["stability_score"] == 0.94
    asyncio.run(_test())

def test_regression():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        reg = res["regressions"][0]
        assert reg["status"] == "stable"
    asyncio.run(_test())

def test_drift():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        drift = res["drifts"][0]
        assert drift["drift_type"] == "cost_drift"
    asyncio.run(_test())

def test_outcome():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        out = res["outcomes"][0]
        assert "under budget" in out["variance_summary"]
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceOptimizationService.enforce_agent_governance("agent_opt_01", "run_optimization_problem")
    assert res1["allowed"] is True

    res2 = TransformationResilienceOptimizationService.enforce_agent_governance("agent_opt_01", "allocate_budgets")
    assert res2["allowed"] is False

    res3 = TransformationResilienceOptimizationService.enforce_agent_governance("agent_opt_01", "approve_investments")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy check: employee optimization
        p_res = await TransformationResilienceOptimizationService.process_natural_language_optimization_query(
            None, "Optimize employee productivity and individual worker allocation across project teams"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP check: secret leak
        dlp_res = await TransformationResilienceOptimizationService.process_natural_language_optimization_query(
            None, "Run optimization using secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceOptimizationService.process_natural_language_optimization_query(
            None, "Where should we improve resilience first?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())

def test_recommendation_label():
    async def _test():
        res = await TransformationResilienceOptimizationService.get_optimization_overview(None)
        rec = res["recommendations"][0]
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT DECISION"
    asyncio.run(_test())
