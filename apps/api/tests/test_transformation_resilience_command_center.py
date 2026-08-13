import pytest
import asyncio
import time
from app.services.transformation_resilience_command_center_service import TransformationResilienceCommandCenterService, _EMITTED_COMMAND_CENTER_EVENTS

def test_get_command_center_overview():
    async def _test():
        res = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
        assert res["commandCentersCount"] >= 1
        assert res["executiveDimensionsCount"] == 7
        assert res["priorityItemsCount"] >= 1
        assert res["situationsCount"] >= 1
        assert res["snapshotsCount"] >= 1
        assert res["exposureMapsCount"] >= 1
        assert res["unappliedLessonsCount"] >= 1
        assert res["decisionPacketsCount"] >= 1
    asyncio.run(_test())

def test_executive_state_7_dimensions():
    async def _test():
        res = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
        states = res["executiveStates"]
        dims = {es["dimension"]: es for es in states}
        assert "robustness" in dims
        assert "redundancy" in dims
        assert "recoverability" in dims
        assert "adaptability" in dims
        assert "optionality" in dims
        assert "observability" in dims
        assert "governability" in dims
        assert dims["robustness"]["confidence"] == 0.94
        assert dims["observability"]["state"] == "degraded"
    asyncio.run(_test())

def test_priority_items_and_situations():
    async def _test():
        res = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
        pitem = res["priorities"][0]
        sit = res["situations"][0]
        snap = res["snapshots"][0]
        assert pitem["priority"] == "critical"
        assert pitem["impact_score"] == 0.94
        assert "Primary OAuth Auth Gateway SLA drifted" in sit["summary"]
        assert snap["freshness"] == 1.0
    asyncio.run(_test())

def test_evidence_summary_and_conflict_resolution():
    async def _test():
        res = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
        evsum = res["evidenceSummary"]
        assert evsum["quality_score"] == 0.95
        assert evsum["has_conflicts"] is True
        assert len(evsum["conflicts_json"]) >= 1
        conflict = evsum["conflicts_json"][0]
        assert conflict["source_a"] == "EventMesh.IdentityGateway"
        assert conflict["source_b"] == "KPI.OAuthMonitor"
    asyncio.run(_test())

def test_unapplied_lessons_and_simulation_triggering():
    async def _test():
        res = await TransformationResilienceCommandCenterService.get_command_center_overview(None)
        uless = res["unappliedLessons"][0]
        assert uless["status"] == "unapplied"

        sim = await TransformationResilienceCommandCenterService.trigger_simulation(None, "cc_res_01", {
            "trigger": "Executive What-If: OAuth Latency Spike",
            "requested_question": "What if latency increases by 50ms?"
        })
        assert sim["status"] == "completed"
        assert sim["simulated_robustness"] == 0.91
    asyncio.run(_test())

def test_create_decision_packet():
    async def _test():
        dp = await TransformationResilienceCommandCenterService.create_decision_packet(None, "cc_res_01", {
            "title": "Cross-Portfolio IAM Active-Active Deployment Packet",
            "recommendation": "Fund pinv_01 ($350k)."
        })
        assert dp["title"] == "Cross-Portfolio IAM Active-Active Deployment Packet"
        assert dp["required_approval"] == "PolicyEngine + Enterprise Executive Board"
    asyncio.run(_test())

def test_agent_governance_command_center_restrictions():
    # Agents are strictly blocked from approving, funding, executing, changing strategy, or changing governance
    chk = TransformationResilienceCommandCenterService.enforce_agent_governance("agent_01", "approve")
    assert chk["allowed"] is False
    assert "strictly blocked" in chk["reason"]

    chk_fund = TransformationResilienceCommandCenterService.enforce_agent_governance("agent_01", "fund")
    assert chk_fund["allowed"] is False

    chk_ok = TransformationResilienceCommandCenterService.enforce_agent_governance("agent_01", "read_overview")
    assert chk_ok["allowed"] is True

def test_process_natural_language_command_center_query_privacy_dlp_tenant():
    async def _test():
        # Valid command center query -> succeeds
        valid_q = "What is the current portfolio resilience state and top priority item?"
        res = await TransformationResilienceCommandCenterService.process_natural_language_command_center_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 98.5

        # Anti-Surveillance / Privacy safeguard breach (employee resilience scores or worker performance predictions) -> blocked
        surveil_q = "Rank employee resilience scores and enable worker behavioral surveillance"
        blocked_surveil = await TransformationResilienceCommandCenterService.process_natural_language_command_center_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual worker resilience scores" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What is the current resilience state? vpr_99999999999"
        blocked_dlp = await TransformationResilienceCommandCenterService.process_natural_language_command_center_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceCommandCenterService.process_natural_language_command_center_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceCommandCenterService.get_command_center_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
