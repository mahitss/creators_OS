import pytest
import asyncio
from app.services.transformation_war_room_service import TransformationWarRoomService

def test_get_war_room_overview():
    async def _test():
        res = await TransformationWarRoomService.get_war_room_overview(None)
        assert res["activeWarRoomsCount"] >= 1
        assert res["detectedDeviationsCount"] >= 1
        assert res["activeEarlyWarningsCount"] >= 1
        assert res["proposedInterventionsCount"] >= 1
        assert res["activeResponsePlansCount"] >= 1
        assert res["liveStateFreshnessMinutes"] == 2.5
    asyncio.run(_test())

def test_process_natural_language_situation_query_privacy_and_dlp():
    async def _test():
        # Valid situation briefing query -> succeeds
        valid_q = "What changed in the transformation portfolio?"
        res = await TransformationWarRoomService.process_natural_language_situation_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 96.5

        # Anti-Surveillance / Privacy boundary breach (employee surveillance request) -> blocked
        surveil_q = "Enable employee surveillance and track worker behavioral score"
        blocked_surveil = await TransformationWarRoomService.process_natural_language_situation_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee surveillance" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What changed in the transformation portfolio? vpr_99999999999"
        blocked_dlp = await TransformationWarRoomService.process_natural_language_situation_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
