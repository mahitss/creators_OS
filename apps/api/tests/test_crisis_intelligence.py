import pytest
import asyncio
from app.services.crisis_intelligence_service import CrisisIntelligenceService

def test_get_crisis_overview():
    async def _test():
        res = await CrisisIntelligenceService.get_crisis_overview(None)
        assert res["crisesCount"] >= 1
        assert res["signalsCount"] >= 1
        assert res["impactsCount"] >= 1
        assert res["commandsCount"] >= 1
        assert res["optionsCount"] >= 1
        assert res["commsCount"] >= 1
        assert res["timelineEventsCount"] >= 1
        assert res["readinessScore"] == 0.96
    asyncio.run(_test())

def test_create_major_crisis_declaration_governance():
    async def _test():
        # Major crisis (SEV1) with authorized actor -> succeeds
        valid_crisis = {
            "name": "Database Cluster Split-Brain Incident",
            "description": "Primary database cluster experiencing split-brain condition and replication lag.",
            "severity": "SEV1",
            "declaredBy": "usr_crisis_commander_lead",
            "commanderId": "usr_crisis_commander_lead",
            "workspaceId": "ws_infra"
        }
        res = await CrisisIntelligenceService.create_crisis(None, valid_crisis)
        assert res["id"] is not None
        assert res["severity"] == "SEV1"
        assert res["declared_by"] == "usr_crisis_commander_lead"
        assert res["status"] == "declared"

        # Major crisis (SEV1) without authorized actor -> blocked
        invalid_crisis = {
            "name": "Database Cluster Split-Brain Incident",
            "description": "Primary database cluster experiencing split-brain condition and replication lag.",
            "severity": "SEV1",
            "declaredBy": "",
            "commanderId": "usr_anon",
            "workspaceId": "ws_infra"
        }
        blocked = await CrisisIntelligenceService.create_crisis(None, invalid_crisis)
        assert "error" in blocked
        assert "requires explicit authorized declaredBy actor" in blocked["error"]
    asyncio.run(_test())

def test_resolve_crisis_evidence_gating():
    async def _test():
        crisis_id = "crs_sev1_01"

        # Empty evidence -> blocked (premature resolution protection)
        blocked = await CrisisIntelligenceService.resolve_crisis(None, crisis_id, {"criteria": "alerts stopped", "evidence": ""})
        assert "error" in blocked
        assert "Premature resolution blocked" in blocked["error"]

        # Valid empirical evidence -> succeeds
        valid_res = await CrisisIntelligenceService.resolve_crisis(
            None,
            crisis_id,
            {
                "criteria": "P99 latency < 200ms & zero dropped tokens across 30 minutes",
                "evidence": "Verified via real-time telemetry mesh and 1,000 synthetic load test probes.",
                "authorizedResolver": "usr_crisis_commander_lead"
            }
        )
        assert valid_res["status"] == "resolved"
        assert "resolved cleanly" in valid_res["message"]
    asyncio.run(_test())

def test_natural_language_crisis_query_dlp():
    async def _test():
        # Valid query
        valid_q = "What is happening right now?"
        res = await CrisisIntelligenceService.process_natural_language_crisis_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] > 0.0

        # Secret query -> blocked by DLP
        secret_q = "What is happening right now? vpr_55555555555"
        blocked = await CrisisIntelligenceService.process_natural_language_crisis_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())
