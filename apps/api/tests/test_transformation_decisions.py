import pytest
import asyncio
from app.services.transformation_decisions_service import TransformationDecisionsService

def test_get_decisions_overview():
    async def _test():
        res = await TransformationDecisionsService.get_decisions_overview(None)
        assert res["activeDecisionCasesCount"] >= 1
        assert res["readyForReviewCount"] >= 1
        assert res["evidenceConflictsCount"] >= 1
        assert res["decisionOptionsCount"] >= 2
        assert res["decisionPacketsCount"] >= 1
        assert res["decisionCalibrationAccuracyPct"] == 97.5
    asyncio.run(_test())

def test_process_natural_language_decision_query_privacy_and_dlp():
    async def _test():
        # Valid decision query -> succeeds
        valid_q = "What decisions are waiting for leadership?"
        res = await TransformationDecisionsService.process_natural_language_decision_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 98.0

        # Anti-Surveillance / Privacy boundary breach (individual employee decision score request) -> blocked
        surveil_q = "Give employee decision score and rank worker for layoff"
        blocked_surveil = await TransformationDecisionsService.process_natural_language_decision_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee decision scoring" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What decisions are waiting for leadership? vpr_77777777777"
        blocked_dlp = await TransformationDecisionsService.process_natural_language_decision_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
