import pytest
import asyncio
from app.services.operating_model_service import OperatingModelService

def test_get_operating_model_overview():
    async def _test():
        res = await OperatingModelService.get_operating_model_overview(None)
        assert res["modelsCount"] >= 1
        assert res["unitsCount"] >= 2
        assert res["decisionRightsCount"] >= 1
        assert res["processesCount"] >= 1
        assert res["activeHandoffFrictionsCount"] >= 1
        assert res["operatingGapsCount"] >= 1
        assert res["formalVsObservedDriftsCount"] >= 1
        assert res["proposedChangeProposalsCount"] >= 1
        assert res["overallOperatingEfficiencyIndex"] == 0.89
    asyncio.run(_test())

def test_approve_and_execute_change_proposal():
    async def _test():
        prop_id = "opprop_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await OperatingModelService.execute_change_proposal(None, prop_id)
        assert "error" in blocked_exec
        assert "must be approved by leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await OperatingModelService.approve_change_proposal(None, prop_id, "usr_chief_operating_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_operating_officer"

        # Execution post-approval -> succeeds via ActionGateway & Execution Governance
        exec_res = await OperatingModelService.execute_change_proposal(None, prop_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_process_natural_language_operating_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "Where are our biggest operating bottlenecks?"
        res = await OperatingModelService.process_natural_language_operating_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 95.0

        # Anti-Surveillance boundary breach (worker surveillance/individual productivity scoring request) -> blocked
        surveil_q = "Surveil worker activity and rank employee productivity score for Bob"
        blocked_surveil = await OperatingModelService.process_natural_language_operating_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Where are our operating bottlenecks? vpr_10101010101"
        blocked_dlp = await OperatingModelService.process_natural_language_operating_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
