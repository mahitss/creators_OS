import pytest
import asyncio
from app.services.transformation_recovery_service import TransformationRecoveryService

def test_get_recovery_overview():
    async def _test():
        res = await TransformationRecoveryService.get_recovery_overview(None)
        assert res["activeRecoveryDomainsCount"] >= 1
        assert res["confirmedDisruptionsCount"] >= 1
        assert res["recommendedRecoveryPathsCount"] >= 1
        assert res["simulatedOptionsCount"] >= 1
        assert res["activeReturnToNormalPlansCount"] >= 1
        assert res["recoveryReadinessScore"] == 0.92
    asyncio.run(_test())

def test_process_natural_language_recovery_query_privacy_and_dlp():
    async def _test():
        # Valid recovery query -> succeeds
        valid_q = "What recovery options exist for the IAM dependency disruption?"
        res = await TransformationRecoveryService.process_natural_language_recovery_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 95.8

        # Anti-Surveillance / Privacy safeguard breach (individual employee recovery scoring) -> blocked
        surveil_q = "Calculate individual employee recovery score and monitor worker performance"
        blocked_surveil = await TransformationRecoveryService.process_natural_language_recovery_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual employee recovery scoring" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What recovery options exist? vpr_99999999999"
        blocked_dlp = await TransformationRecoveryService.process_natural_language_recovery_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
