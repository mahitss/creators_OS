import pytest
import asyncio
from app.services.transformation_governance_service import TransformationGovernanceService

def test_get_governance_overview():
    async def _test():
        res = await TransformationGovernanceService.get_governance_overview(None)
        assert res["activeProfilesCount"] >= 1
        assert res["decisionRightsCount"] >= 1
        assert res["activeControlsCount"] >= 1
        assert res["surfacedConflictsCount"] >= 1
        assert res["detectedFrictionsCount"] >= 1
        assert res["delegationCandidatesCount"] >= 1
        assert res["activeExceptionsCount"] >= 1
        assert res["governanceEfficiencyScorePct"] == 94.5
    asyncio.run(_test())

def test_process_natural_language_governance_query_privacy_and_dlp():
    async def _test():
        # Valid governance query -> succeeds
        valid_q = "Where is governance slowing us down?"
        res = await TransformationGovernanceService.process_natural_language_governance_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 98.1

        # Anti-Surveillance / Privacy boundary breach (individual employee compliance ranking request) -> blocked
        surveil_q = "Rank employee compliance and show who is violating policy worker"
        blocked_surveil = await TransformationGovernanceService.process_natural_language_governance_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee compliance rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Where is governance slowing us down? vpr_99999999999"
        blocked_dlp = await TransformationGovernanceService.process_natural_language_governance_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
