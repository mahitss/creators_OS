import pytest
import asyncio
from app.services.transformation_service import TransformationService

def test_get_transformation_overview():
    async def _test():
        res = await TransformationService.get_transformation_overview(None)
        assert res["programsCount"] >= 1
        assert res["driversCount"] >= 1
        assert res["deltasCount"] >= 1
        assert res["futureModelsCount"] >= 1
        assert res["designOptionsCount"] >= 1
        assert res["scenariosCount"] >= 1
        assert res["roadmapsCount"] >= 1
        assert res["decisionGatesCount"] >= 1
        assert res["pilotsCount"] >= 1
        assert res["proposedChangeProposalsCount"] >= 1
        assert res["overallTransformationReadinessPct"] == 92.5
    asyncio.run(_test())

def test_approve_and_execute_transformation_change_proposal():
    async def _test():
        prop_id = "transprop_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await TransformationService.execute_change_proposal(None, prop_id)
        assert "error" in blocked_exec
        assert "must be approved by leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await TransformationService.approve_change_proposal(None, prop_id, "usr_chief_transformation_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_transformation_officer"

        # Execution post-approval -> succeeds via ActionGateway & Execution Governance
        exec_res = await TransformationService.execute_change_proposal(None, prop_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_process_natural_language_transformation_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "Why does our operating model need to change?"
        res = await TransformationService.process_natural_language_transformation_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 96.0

        # Anti-Surveillance / Privacy boundary breach (fire employee/restructure individual request) -> blocked
        surveil_q = "Fire employee Bob and restructure individual role"
        blocked_surveil = await TransformationService.process_natural_language_transformation_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Why does our operating model need to change? vpr_99999999999"
        blocked_dlp = await TransformationService.process_natural_language_transformation_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
