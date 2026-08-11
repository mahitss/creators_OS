import pytest
import asyncio
from app.services.foresight_intelligence_service import ForesightIntelligenceService

def test_get_foresight_overview():
    async def _test():
        res = await ForesightIntelligenceService.get_foresight_overview(None)
        assert res["programsCount"] >= 1
        assert res["driversCount"] >= 1
        assert res["trendsCount"] >= 1
        assert res["fragileAssumptionsCount"] >= 1
        assert res["scenariosCount"] >= 1
        assert res["indicatorsCount"] >= 1
        assert res["optionsCount"] >= 1
        assert res["betsCount"] >= 1
        assert res["exposuresCount"] >= 1
        assert res["redTeamScenariosCount"] >= 1
        assert res["robustnessScore"] == 0.94
    asyncio.run(_test())

def test_complete_foresight_review():
    async def _test():
        program_id = "fprog_5yr_01"
        res = await ForesightIntelligenceService.complete_foresight_review(None, program_id, {})
        assert res["status"] == "completed"
        assert res["programId"] == program_id
        assert "completed and logged" in res["message"]
    asyncio.run(_test())

def test_natural_language_foresight_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "What could change our business in five years?"
        res = await ForesightIntelligenceService.process_natural_language_foresight_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 96.0

        # Anti-Surveillance boundary breach (employee future-value ranking request) -> blocked
        surveil_q = "Rank employee career potential and predict future value score for Alice"
        blocked_surveil = await ForesightIntelligenceService.process_natural_language_foresight_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee future-value ranking" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What could change our business? vpr_88888888888"
        blocked_dlp = await ForesightIntelligenceService.process_natural_language_foresight_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
