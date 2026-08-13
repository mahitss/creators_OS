import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_assurance_control_service import TransformationResilienceKnowledgeAssuranceControlService, _EMITTED_CONTROL_EVENTS

def test_get_knowledge_assurance_control_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
        assert res["domainsCount"] >= 1
        assert res["baselinesCount"] >= 1
        assert res["signalsCount"] >= 1
        assert res["stalePlansCount"] >= 1
        assert res["replanTriggersCount"] >= 1
        assert res["planVersionsCount"] >= 2
        assert res["emergencyReplansCount"] >= 1
        assert res["crossPlanImpactsCount"] >= 1
    asyncio.run(_test())

def test_baselines_change_signals_and_detections():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
        base = res["baselines"][0]
        sig = res["signals"][0]
        cdet = res["detections"][0]
        assert base["plan_version"] == "v1.0"
        assert base["approval_state"] == "approved"
        assert sig["change_type"] == "dependency_change"
        assert sig["significance"] == "material"
        assert cdet["confidence"] == 0.94
    asyncio.run(_test())

def test_assumption_impacts_plan_impacts_and_health():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
        aimp = res["assumptionImpacts"][0]
        pimp = res["planImpacts"][0]
        health = res["healths"][0]
        assert "Synthetic telemetry packets require 2x retry buffer" in aimp["impact"]
        assert pimp["severity"] == "material"
        assert health["risk_alignment"] == 0.92
        assert health["evidence_alignment"] == 0.88
    asyncio.run(_test())

def test_staleness_replan_triggers_and_recommendations():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
        stale = res["stalenesses"][0]
        trig = res["triggers"][0]
        rec = res["recommendations"][0]
        assert stale["status"] == "materially_stale"
        assert trig["status"] == "open"
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT APPROVAL"
        assert rec["recommended_option"] == "resequence"
    asyncio.run(_test())

def test_plan_versioning_diffing_and_parent_preservation():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceControlService.create_plan_version(None, "aplan_01", {
            "version_number": "v2.0",
            "parent_version": "v1.0",
            "change_summary": "Resequence synthetic telemetry execution"
        })
        ver = res["version"]
        diff = res["diff"]
        assert ver["version_number"] == "v2.0"
        assert ver["parent_version"] == "v1.0"
        assert diff["from_version"] == "v1.0"
        assert diff["to_version"] == "v2.0"
    asyncio.run(_test())

def test_execute_plan_version_and_stale_execution_protection():
    async def _test():
        # Executing materially stale plan -> Stale Execution Protection triggers pause
        res = await TransformationResilienceKnowledgeAssuranceControlService.execute_plan_version(None, "aplan_01", "v2.0")
        assert res["execution_status"] == "paused"
        assert "Stale Execution Protection" in res["reason"]
    asyncio.run(_test())

def test_cross_plan_impacts_drift_and_emergencies():
    async def _test():
        overview = await TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None)
        cpimp = overview["crossImpacts"][0]
        drift = overview["drifts"][0]
        emg = overview["emergencies"][0]
        assert cpimp["source_plan_id"] == "aplan_01"
        assert drift["risk_drift"] == 0.12
        assert emg["status"] == "active"
        assert emg["war_room_session_id"] == "war_room_resilience_01"
    asyncio.run(_test())

def test_agent_governance_assurance_control_restrictions():
    # Agents may NOT approve replans, modify approved plans directly, or accept material risk
    chk_replan = TransformationResilienceKnowledgeAssuranceControlService.enforce_agent_governance("agent_01", "approve_replan")
    assert chk_replan["allowed"] is False
    assert "strictly blocked" in chk_replan["reason"]

    chk_modify = TransformationResilienceKnowledgeAssuranceControlService.enforce_agent_governance("agent_01", "modify_approved_plan_directly")
    assert chk_modify["allowed"] is False

    chk_monitor = TransformationResilienceKnowledgeAssuranceControlService.enforce_agent_governance("agent_01", "monitor_signals")
    assert chk_monitor["allowed"] is True

def test_process_natural_language_assurance_control_query_privacy_dlp_tenant():
    async def _test():
        # Valid control query -> succeeds
        valid_q = "Which plans are stale and what changed since approval?"
        res = await TransformationResilienceKnowledgeAssuranceControlService.process_natural_language_assurance_control_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee adaptive performance scores or worker rankings) -> blocked
        surveil_q = "Calculate employee adaptive-performance score and rank worker surveillance metrics"
        blocked_surveil = await TransformationResilienceKnowledgeAssuranceControlService.process_natural_language_assurance_control_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee adaptive-performance scores" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show adaptive plan diffs. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeAssuranceControlService.process_natural_language_assurance_control_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeAssuranceControlService.process_natural_language_assurance_control_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeAssuranceControlService.get_knowledge_assurance_control_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
