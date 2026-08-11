import pytest
import asyncio
from app.services.adaptive_strategy_service import AdaptiveStrategyService

def test_get_adaptive_strategy_overview():
    async def _test():
        res = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
        assert res["strategiesCount"] >= 1
        assert res["thesesCount"] >= 1
        assert res["indicatorsCount"] >= 1
        assert res["driftsCount"] >= 1
        assert res["proposedReconfigurationsCount"] >= 1
        assert res["bottlenecksCount"] >= 1
        assert res["runningExperimentsCount"] >= 1
        assert res["healthDimensions"]["intentAlignment"] == 0.94
        assert res["healthDimensions"]["assumptionValidity"] == 0.82
    asyncio.run(_test())

def test_approve_and_execute_reconfiguration():
    async def _test():
        reconfig_id = "prconf_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await AdaptiveStrategyService.execute_reconfiguration(None, reconfig_id)
        assert "error" in blocked_exec
        assert "must be approved by leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await AdaptiveStrategyService.approve_reconfiguration(None, reconfig_id, "usr_chief_strategy_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_strategy_officer"

        # Execution post-approval -> succeeds
        exec_res = await AdaptiveStrategyService.execute_reconfiguration(None, reconfig_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_natural_language_adaptive_strategy_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "Is our current strategy still working?"
        res = await AdaptiveStrategyService.process_natural_language_adaptive_strategy_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 95.0

        # Anti-Surveillance boundary breach (employee workforce scoring request) -> blocked
        surveil_q = "Rank employee strategic performance and predict workforce scoring for Bob"
        blocked_surveil = await AdaptiveStrategyService.process_natural_language_adaptive_strategy_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee strategic ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Is our strategy working? vpr_77777777777"
        blocked_dlp = await AdaptiveStrategyService.process_natural_language_adaptive_strategy_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
