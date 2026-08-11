import pytest
import asyncio
from app.services.transformation_simulation_service import TransformationSimulationService

def test_get_simulation_overview():
    async def _test():
        res = await TransformationSimulationService.get_simulation_overview(None)
        assert res["activeTwinsCount"] >= 1
        assert res["totalSnapshotsCount"] >= 1
        assert res["completedRunsCount"] >= 1
        assert res["modelsValidatedCount"] >= 1
        assert res["multiScenarioRobustnessScore"] == 0.92
        assert res["simulationAccuracyCalibrationPct"] == 95.8
    asyncio.run(_test())

def test_process_natural_language_what_if_query_privacy_and_dlp():
    async def _test():
        # Valid what-if simulation query -> succeeds
        valid_q = "What if we delay Wave 2 by 3 months?"
        res = await TransformationSimulationService.process_natural_language_what_if_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 94.0

        # Anti-Surveillance / Privacy boundary breach (individual employee digital twin request) -> blocked
        surveil_q = "Create an employee digital twin to simulate worker behavior and performance"
        blocked_surveil = await TransformationSimulationService.process_natural_language_what_if_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee digital twins" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What if we delay Wave 2 by 3 months? vpr_99999999999"
        blocked_dlp = await TransformationSimulationService.process_natural_language_what_if_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
