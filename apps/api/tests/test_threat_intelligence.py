import pytest
import asyncio
from app.services.threat_intelligence_service import ThreatIntelligenceService

def test_get_threat_overview():
    async def _test():
        res = await ThreatIntelligenceService.get_threat_overview(None)
        assert res["signalsCount"] >= 1
        assert res["weakSignalsCount"] >= 1
        assert res["correlationsCount"] >= 1
        assert res["patternsCount"] >= 1
        assert res["threatsCount"] >= 1
        assert res["warningsCount"] >= 1
        assert res["mitigationsCount"] >= 1
        assert res["blindSpotsCount"] >= 1
        assert res["precisionScore"] == 0.94
        assert res["monitoringCoveragePct"] == 0.96
    asyncio.run(_test())

def test_suppress_early_warning_audited():
    async def _test():
        warning_id = "ewarn_01"

        # Missing reason -> blocked
        blocked = await ThreatIntelligenceService.suppress_early_warning(None, warning_id, {"reason": "", "actor": "usr_anon"})
        assert "error" in blocked
        assert "requires an explicit reason" in blocked["error"]

        # Valid suppression -> logged in audit history
        res = await ThreatIntelligenceService.suppress_early_warning(
            None,
            warning_id,
            {"reason": "Signal confirmed as planned maintenance activity", "actor": "usr_threat_architect"}
        )
        assert res["status"] == "false_positive"
        assert res["actor"] == "usr_threat_architect"
        assert "suppressed and logged" in res["message"]
    asyncio.run(_test())

def test_action_gateway_mitigation_execution():
    async def _test():
        mitigation_id = "tmit_01"
        res = await ThreatIntelligenceService.execute_mitigation(None, mitigation_id)
        assert res["status"] == "completed"
        assert res["actualRiskReductionPct"] == 0.88
        assert "Universal Action Gateway" in res["executionGatewayPath"]
    asyncio.run(_test())

def test_natural_language_threat_query_privacy_and_dlp():
    async def _test():
        # Valid query -> succeeds
        valid_q = "What risks are emerging right now?"
        res = await ThreatIntelligenceService.process_natural_language_threat_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 94.0

        # Anti-Surveillance boundary breach (employee profiling request) -> blocked
        surveil_q = "Profile employee performance and predict individual threat level for John"
        blocked_surveil = await ThreatIntelligenceService.process_natural_language_threat_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee surveillance" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "What risks are emerging? vpr_99999999999"
        blocked_dlp = await ThreatIntelligenceService.process_natural_language_threat_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")
    asyncio.run(_test())
