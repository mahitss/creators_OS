import pytest
import asyncio
import time
from app.services.transformation_resilience_portfolio_service import TransformationResiliencePortfolioService, _EMITTED_PORTFOLIO_EVENTS

def test_get_portfolio_overview():
    async def _test():
        res = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
        assert res["activePortfoliosCount"] >= 1
        assert res["systemicExposuresCount"] >= 1
        assert res["sharedDependenciesCount"] >= 1
        assert res["capacityConflictsCount"] >= 1
        assert res["systemicRisksCount"] >= 1
        assert res["investmentCandidatesCount"] >= 1
        assert res["investmentOverlapsCount"] >= 1
        assert res["investmentGapsCount"] >= 1
        assert res["portfolioRobustnessScore"] == 0.94
    asyncio.run(_test())

def test_shared_dependencies_and_exposures():
    async def _test():
        res = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
        exp = res["exposures"][0]
        dep = res["sharedDependencies"][0]
        srisk = res["systemicRisks"][0]
        assert exp["exposure_type"] == "dependency"
        assert dep["criticality"] == 0.96
        assert len(dep["affected_transformations_json"]) >= 3
        assert srisk["severity"] == "critical"
    asyncio.run(_test())

def test_shared_capacity_and_conflicts():
    async def _test():
        res = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
        cap = res["capacityExposures"][0]
        conf = res["capacityConflicts"][0]
        assert cap["capacity_type"] == "engineering_fte"
        assert cap["required_capacity"] == 45.0
        assert conf["severity"] == "high"
    asyncio.run(_test())

def test_investment_creation_simulation_and_multi_failure():
    async def _test():
        inv = await TransformationResiliencePortfolioService.create_portfolio_resilience_investment(None, {
            "investment_title": "Multi-Region Core Auth Failover",
            "cost": 350000.0,
            "risk_reduction_pct": 65.0
        })
        assert inv["cost"] == 350000.0
        assert inv["risk_reduction_pct"] == 65.0

        sim = await TransformationResiliencePortfolioService.simulate_investment(None, "port_res_01", inv["id"])
        assert sim["simulationCompleted"] is True
        assert sim["simulatedPortfolioRobustness"] == 0.99

        scen = await TransformationResiliencePortfolioService.create_multi_failure_scenario(None, "port_res_01", {
            "scenario_title": "Compound Cloud Outage Scenario",
            "simultaneous_failures_json": ["Auth Outage", "Database Lag"]
        })
        assert scen["scenario_title"] == "Compound Cloud Outage Scenario"
    asyncio.run(_test())

def test_overlaps_gaps_tradeoffs_and_option_value():
    async def _test():
        res = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
        over = res["overlaps"][0]
        gap = res["gaps"][0]
        trade = res["tradeoffs"][0]
        optv = res["optionValues"][0]
        assert over["potential_savings"] == 120000.0
        assert gap["severity"] == "high"
        assert trade["option_a_json"]["cost"] == 350000.0
        assert optv["flexibility_score"] == 0.93
    asyncio.run(_test())

def test_portfolio_roadmap_and_review():
    async def _test():
        res = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
        road = res["roadmaps"][0]
        rev = res["reviews"][0]
        assert road["total_budget"] == 750000.0
        assert rev["status"] == "open"

        completed_rev = await TransformationResiliencePortfolioService.complete_portfolio_review(None, rev["id"])
        assert completed_rev["status"] == "completed"
    asyncio.run(_test())

def test_agent_governance_portfolio_restrictions():
    # Agents are strictly blocked from budget allocations, investment approvals, or priority changes
    chk = TransformationResiliencePortfolioService.enforce_agent_governance("agent_01", "allocate_budget")
    assert chk["allowed"] is False
    assert "strictly blocked" in chk["reason"]

    chk_ok = TransformationResiliencePortfolioService.enforce_agent_governance("agent_01", "read_portfolio_overview")
    assert chk_ok["allowed"] is True

def test_process_natural_language_portfolio_query_privacy_dlp_tenant():
    async def _test():
        # Valid portfolio query -> succeeds
        valid_q = "Which transformations share critical dependencies across Wave 2 and Wave 3?"
        res = await TransformationResiliencePortfolioService.process_natural_language_portfolio_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 97.5

        # Anti-Surveillance / Privacy safeguard breach (employee or investment performance ranking) -> blocked
        surveil_q = "Rank employee resilience scores and enable investment performance surveillance"
        blocked_surveil = await TransformationResiliencePortfolioService.process_natural_language_portfolio_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee resilience rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Which transformations share critical dependencies? vpr_99999999999"
        blocked_dlp = await TransformationResiliencePortfolioService.process_natural_language_portfolio_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResiliencePortfolioService.process_natural_language_portfolio_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResiliencePortfolioService.get_portfolio_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
