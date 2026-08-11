import pytest
import asyncio
from app.services.execution_intelligence_service import ExecutionIntelligenceService

def test_get_execution_intelligence_overview():
    async def _test():
        res = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
        assert res["objectivesCount"] >= 1
        assert res["alignmentsCount"] >= 1
        assert res["coveragesCount"] >= 1
        assert res["pathsCount"] >= 1
        assert res["driftsCount"] >= 1
        assert res["activeBlockersCount"] >= 1
        assert res["staleDecisionGapsCount"] >= 1
        assert res["outcomeGapsCount"] >= 1
        assert res["proposedRecommendationsCount"] >= 1
        assert res["executionVelocityIndex"] == 0.91
        assert res["overallExecutionCoveragePct"] == 0.88
    asyncio.run(_test())

def test_approve_and_execute_recommendation():
    async def _test():
        rec_id = "erec_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await ExecutionIntelligenceService.execute_recommendation(None, rec_id)
        assert "error" in blocked_exec
        assert "must be approved by leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await ExecutionIntelligenceService.approve_execution_recommendation(None, rec_id, "usr_chief_technology_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_technology_officer"

        # Execution post-approval -> succeeds via ActionGateway
        exec_res = await ExecutionIntelligenceService.execute_recommendation(None, rec_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_process_natural_language_execution_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "Are we executing our strategy?"
        res = await ExecutionIntelligenceService.process_natural_language_execution_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 96.0

        # Anti-Surveillance boundary breach (employee ranking/productivity scoring request) -> blocked
        surveil_q = "Rank employee execution productivity score for Alice"
        blocked_surveil = await ExecutionIntelligenceService.process_natural_language_execution_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Are we executing our strategy? vpr_99999999999"
        blocked_dlp = await ExecutionIntelligenceService.process_natural_language_execution_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
