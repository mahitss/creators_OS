import pytest
import asyncio
from app.services.transformation_control_service import TransformationControlService

def test_get_control_overview():
    async def _test():
        res = await TransformationControlService.get_control_overview(None)
        assert res["controlTowersCount"] >= 1
        assert res["liveStatesCount"] >= 1
        assert res["signalsCount"] >= 2
        assert res["situationsCount"] >= 1
        assert res["rootCausesCount"] >= 1
        assert res["earlyWarningsCount"] >= 1
        assert res["waveReadinessesCount"] >= 1
        assert res["proposedChangeRequestsCount"] >= 1
        assert res["activeIncidentsCount"] >= 1
        assert res["activeEscalationsCount"] >= 1
        assert res["weeklyReviewsCount"] >= 1
        assert res["learningsCount"] >= 1
        assert res["controlTowerStatus"] == "healthy"
        assert res["overallWaveReadinessPct"] == 92.0
    asyncio.run(_test())

def test_approve_and_execute_change_request():
    async def _test():
        req_id = "cr_sequence_adjust_01"

        # Attempt execution before approval -> blocked
        blocked_exec = await TransformationControlService.execute_change_request(None, req_id)
        assert "error" in blocked_exec
        assert "must be approved by human leadership" in blocked_exec["error"]

        # Leadership Approval
        appr_res = await TransformationControlService.approve_change_request(None, req_id, "usr_chief_transformation_officer")
        assert appr_res["status"] == "approved"
        assert appr_res["approvedBy"] == "usr_chief_transformation_officer"

        # Execution post-approval -> succeeds via ActionGateway & Execution Governance
        exec_res = await TransformationControlService.execute_change_request(None, req_id)
        assert exec_res["status"] == "executed"
        assert "Universal Action Gateway" in exec_res["executionPath"]
    asyncio.run(_test())

def test_process_natural_language_control_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "What changed in the transformation portfolio?"
        res = await TransformationControlService.process_natural_language_control_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 98.0

        # Anti-Surveillance / Privacy boundary breach (rank employee/worker score request) -> blocked
        surveil_q = "Show individual worker score and rank employee adoption rate"
        blocked_surveil = await TransformationControlService.process_natural_language_control_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What changed in the transformation portfolio? vpr_88888888888"
        blocked_dlp = await TransformationControlService.process_natural_language_control_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
