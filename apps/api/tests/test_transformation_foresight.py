import pytest
import asyncio
from app.services.transformation_foresight_service import TransformationForesightService

def test_get_foresight_overview():
    async def _test():
        res = await TransformationForesightService.get_foresight_overview(None)
        assert res["activeDomainsCount"] >= 1
        assert res["futureDriversCount"] >= 2
        assert res["weakSignalsCount"] >= 1
        assert res["emergingPatternsCount"] >= 1
        assert res["futureStatesCount"] >= 2
        assert res["scenarioImpactsCount"] >= 1
        assert res["secondOrderEffectsCount"] >= 1
        assert res["vulnerabilitiesCount"] >= 1
        assert res["opportunitiesCount"] >= 1
        assert res["noRegretActionsCount"] >= 1
        assert res["triggersCount"] >= 1
        assert res["forecastVersionsCount"] >= 1
        assert res["calibrationAccuracyPct"] == 96.0
    asyncio.run(_test())

def test_process_natural_language_foresight_query_privacy_and_dlp():
    async def _test():
        # Valid foresight query -> succeeds
        valid_q = "What future risks should we watch?"
        res = await TransformationForesightService.process_natural_language_foresight_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 95.0

        # Anti-Surveillance / Privacy boundary breach (individual employee performance forecast request) -> blocked
        surveil_q = "Predict employee performance forecast and individual worker behavior"
        blocked_surveil = await TransformationForesightService.process_natural_language_foresight_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee performance forecasting" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What future risks should we watch? vpr_88888888888"
        blocked_dlp = await TransformationForesightService.process_natural_language_foresight_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
