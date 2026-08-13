import pytest
import asyncio
import time
from app.services.transformation_resilience_sensing_service import TransformationResilienceSensingService, _EMITTED_SENSING_EVENTS

def test_get_sensing_overview():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        assert res["domainsCount"] >= 1
        assert res["observationsCount"] >= 1
        assert res["activeDriftsCount"] >= 1
        assert res["structuralChangesCount"] >= 1
        assert res["activeWarningsCount"] >= 1
        assert res["signalCorrelationsCount"] >= 1
        assert res["assumptionDriftsCount"] >= 1
        assert res["investmentReviewTriggersCount"] >= 1
        assert res["portfolioState"]["robustness"] == 0.94
    asyncio.run(_test())

def test_observations_and_quality():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        obs = res["observations"][0]
        qual = res["qualities"][0]
        norm = res["normalizations"][0]
        assert obs["source"] == "EventMesh.IdentityGateway"
        assert obs["confidence"] == 0.96
        assert qual["reliability"] == 0.96
        assert norm["normalized_dimension"] == "robustness"
    asyncio.run(_test())

def test_drift_structural_change_and_warnings():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        drift = res["drifts"][0]
        schange = res["structuralChanges"][0]
        warn = res["warnings"][0]
        assert drift["drift_type"] == "persistent"
        assert schange["materiality"] == "material"
        assert warn["status"] == "active"
        assert warn["severity"] == "high"
    asyncio.run(_test())

def test_signal_correlation_and_causation_safeguard():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        corr = res["correlations"][0]
        assert corr["relationship_type"] == "observed_correlation"
        assert corr["relationship_type"] != "confirmed_causation"
        assert corr["confidence"] == 0.93
    asyncio.run(_test())

def test_trends_forecasts_and_assumptions():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        tr = res["trends"][0]
        fc = res["forecasts"][0]
        ass = res["assumptions"][0]
        assdrift = res["assumptionDrifts"][0]
        assert tr["trend_direction"] == "deteriorating"
        assert fc["forecast_value"] == 0.84
        assert ass["status"] == "degraded"
        assert assdrift["severity"] == "high"
    asyncio.run(_test())

def test_review_triggers_and_acknowledgement():
    async def _test():
        res = await TransformationResilienceSensingService.get_sensing_overview(None)
        trig = res["investmentTriggers"][0]
        assert trig["review_deadline"] == "2026-Q3"

        ack = await TransformationResilienceSensingService.acknowledge_review(None, trig["id"])
        assert ack["acknowledged"] is True
    asyncio.run(_test())

def test_agent_governance_sensing_restrictions():
    # Agents are strictly blocked from changing baselines, approving reviews, or modifying governance
    chk = TransformationResilienceSensingService.enforce_agent_governance("agent_01", "change_baseline")
    assert chk["allowed"] is False
    assert "strictly blocked" in chk["reason"]

    chk_ok = TransformationResilienceSensingService.enforce_agent_governance("agent_01", "read_sensing_overview")
    assert chk_ok["allowed"] is True

def test_process_natural_language_sensing_query_privacy_dlp_tenant():
    async def _test():
        # Valid sensing query -> succeeds
        valid_q = "Has resilience improved or deteriorated over the last 30 days?"
        res = await TransformationResilienceSensingService.process_natural_language_sensing_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 98.0

        # Anti-Surveillance / Privacy safeguard breach (employee resilience scores or behavioral surveillance) -> blocked
        surveil_q = "Rank employee resilience scores and enable worker behavioral surveillance"
        blocked_surveil = await TransformationResilienceSensingService.process_natural_language_sensing_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee resilience scores" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What changed in resilience this week? vpr_99999999999"
        blocked_dlp = await TransformationResilienceSensingService.process_natural_language_sensing_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceSensingService.process_natural_language_sensing_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceSensingService.get_sensing_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
