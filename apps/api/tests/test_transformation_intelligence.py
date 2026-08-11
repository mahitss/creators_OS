import pytest
import asyncio
from app.services.transformation_intelligence_service import TransformationIntelligenceService

def test_get_fabric_overview():
    async def _test():
        res = await TransformationIntelligenceService.get_fabric_overview(None)
        assert res["graphNodesCount"] >= 3
        assert res["graphEdgesCount"] >= 2
        assert res["provenanceRecordsCount"] >= 1
        assert res["crossTransformationImpactsCount"] >= 1
        assert res["capabilityOverlapsCount"] >= 1
        assert res["sharedAssumptionClustersCount"] >= 1
        assert res["scenarioExposuresCount"] >= 1
        assert res["benefitGraphsCount"] >= 1
        assert res["conflictGraphsCount"] >= 1
        assert res["patternsDetectedCount"] >= 1
        assert res["analogiesIdentifiedCount"] >= 1
        assert res["complexityHotspotsCount"] >= 1
        assert res["graphSnapshotsCount"] >= 1
        assert res["overallFabricDensityScore"] == 0.88
    asyncio.run(_test())

def test_query_multi_hop_paths():
    async def _test():
        res = await TransformationIntelligenceService.query_multi_hop_paths(None, "cand_01", "cand_02")
        assert res["fromEntity"] == "cand_01"
        assert res["toEntity"] == "cand_02"
        assert len(res["multiHopPath"]) >= 3
        assert len(res["relationships"]) >= 2
        assert res["confidencePct"] == 96.0
        assert "Observed dependency matrix" in res["evidence"]
    asyncio.run(_test())

def test_process_natural_language_intelligence_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "What depends on this transformation?"
        res = await TransformationIntelligenceService.process_natural_language_intelligence_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 97.0

        # Anti-Surveillance / Privacy boundary breach (individual employee relationship graph request) -> blocked
        surveil_q = "Show individual employee graph and surveil worker relationship matrix"
        blocked_surveil = await TransformationIntelligenceService.process_natural_language_intelligence_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee relationship graphs" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What depends on this transformation? vpr_99999999999"
        blocked_dlp = await TransformationIntelligenceService.process_natural_language_intelligence_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
