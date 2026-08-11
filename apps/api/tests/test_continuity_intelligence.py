import pytest
import asyncio
from app.services.continuity_intelligence_service import ContinuityIntelligenceService

def test_get_resilience_overview():
    async def _test():
        res = await ContinuityIntelligenceService.get_resilience_overview(None)
        assert res["capabilitiesCount"] >= 1
        assert res["spofCount"] >= 1
        assert res["gapsCount"] >= 1
        assert res["scenariosCount"] >= 1
        assert res["plansCount"] >= 1
        assert res["testsCount"] >= 1
        assert res["overallReadinessScore"] == 0.94
    asyncio.run(_test())

def test_create_critical_capability():
    async def _test():
        cap_data = {
            "name": "Payments & Billing Settlement Engine",
            "description": "Critical capability handling transaction processing and partner revenue settlement.",
            "owner": "usr_fin_tech_lead",
            "criticality": "critical",
            "workspaceId": "ws_fintech"
        }
        res = await ContinuityIntelligenceService.create_critical_capability(None, cap_data)
        assert res["id"] is not None
        assert res["name"] == cap_data["name"]
        assert res["criticality"] == "critical"
        assert res["status"] == "active"
    asyncio.run(_test())

def test_validate_continuity_plan():
    async def _test():
        plan_id = "cplan_01"
        res = await ContinuityIntelligenceService.validate_continuity_plan(None, plan_id, actor_id="usr_resilience_lead")
        assert res["status"] == "validated"
        assert res["newVersion"] >= 2
        assert res["validatedBy"] == "usr_resilience_lead"
    asyncio.run(_test())

def test_natural_language_resilience_query_dlp():
    async def _test():
        # Valid query
        valid_q = "What happens if our primary vendor fails?"
        res = await ContinuityIntelligenceService.process_natural_language_resilience_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] > 0.0

        # Secret query -> blocked by DLP
        secret_q = "What happens if our primary vendor fails? vpr_98765432101"
        blocked = await ContinuityIntelligenceService.process_natural_language_resilience_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())
