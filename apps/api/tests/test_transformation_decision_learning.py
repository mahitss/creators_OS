import pytest
import asyncio
from app.services.transformation_decision_learning_service import TransformationDecisionLearningService

def test_get_learning_overview():
    async def _test():
        res = await TransformationDecisionLearningService.get_learning_overview(None)
        assert res["activeLifecyclesCount"] >= 1
        assert res["frozenBaselinesCount"] >= 1
        assert res["verifiedLessonsCount"] >= 1
        assert res["detectedPatternsCount"] >= 1
        assert res["approvedReviewsCount"] >= 1
        assert res["forecastCalibrationAccuracyPct"] == 96.8
    asyncio.run(_test())

def test_process_natural_language_learning_query_privacy_and_dlp():
    async def _test():
        # Valid learning query -> succeeds
        valid_q = "What did we learn from similar transformations?"
        res = await TransformationDecisionLearningService.process_natural_language_learning_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 97.2

        # Anti-Surveillance / Privacy boundary breach (individual employee blame / decision quality ranking request) -> blocked
        surveil_q = "Rank employee decision quality and show who was right employee"
        blocked_surveil = await TransformationDecisionLearningService.process_natural_language_learning_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual decision-quality rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What did we learn from similar transformations? vpr_88888888888"
        blocked_dlp = await TransformationDecisionLearningService.process_natural_language_learning_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
