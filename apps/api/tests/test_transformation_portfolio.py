import pytest
import asyncio
from app.services.transformation_portfolio_service import TransformationPortfolioService

def test_get_portfolio_overview():
    async def _test():
        res = await TransformationPortfolioService.get_portfolio_overview(None)
        assert res["portfoliosCount"] >= 1
        assert res["candidatesCount"] >= 2
        assert res["criticalPathCandidatesCount"] >= 2
        assert res["sequencesCount"] >= 1
        assert res["sequenceComparisonsCount"] >= 1
        assert res["activeCapacityPlansCount"] >= 1
        assert res["lockInRisksCount"] >= 1
        assert res["wavesCount"] >= 1
        assert res["minimumSetsCount"] >= 1
        assert res["proposedRebalancesCount"] >= 1
        assert res["overallPortfolioRobustnessScore"] == 0.94
    asyncio.run(_test())

def test_approve_and_execute_rebalance():
    async def _test():
        reb_id = "rebal_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await TransformationPortfolioService.execute_rebalance(None, reb_id)
        assert "error" in blocked_exec
        assert "must be approved by leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await TransformationPortfolioService.approve_rebalance(None, reb_id, "usr_chief_investment_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_investment_officer"

        # Execution post-approval -> succeeds via ActionGateway & Execution Governance
        exec_res = await TransformationPortfolioService.execute_rebalance(None, reb_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_process_natural_language_portfolio_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "Which transformation should happen first?"
        res = await TransformationPortfolioService.process_natural_language_portfolio_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 97.0

        # Anti-Surveillance / Privacy boundary breach (rank employee/allocate worker request) -> blocked
        surveil_q = "Allocate worker Bob and rank employee performance for candidate 1"
        blocked_surveil = await TransformationPortfolioService.process_natural_language_portfolio_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Which transformation should happen first? vpr_77777777777"
        blocked_dlp = await TransformationPortfolioService.process_natural_language_portfolio_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
