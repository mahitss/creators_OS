import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.operating_graph_service import OperatingGraphService

def test_organization_overview_telemetry():
    async def _test():
        ov = await OperatingGraphService.get_organization_overview(None)
        assert ov is not None
        assert "activeOutcomesCount" in ov
        assert "dependenciesMonitoredCount" in ov
        assert "systemBottlenecksCount" in ov
        assert "capabilityGapsCount" in ov
        assert "concentrationRisksCount" in ov
        assert ov["graphHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_outcome_and_traceability():
    async def _test():
        out_data = {
            "name": "ISO 27001 Certification",
            "description": "Achieve international security standard compliance.",
            "owner": "team_security",
            "target": "100% Policy Controls Verified",
            "currentState": "70% Controls Verified",
            "workspaceId": "ws_default"
        }
        out = await OperatingGraphService.create_outcome(None, out_data)
        assert out["id"] is not None
        assert out["status"] == "active"
        assert out["owner"] == "team_security"

    asyncio.run(_test())

def test_production_safe_scenario_simulation():
    async def _test():
        sim_data = {
            "name": "Simulated Integration Failure",
            "assumptionsJson": {"failed_node": "integration_sf_01"}
        }
        sc = await OperatingGraphService.simulate_scenario(None, sim_data)
        assert sc["id"] is not None
        assert sc["expected_impact_json"]["production_modified"] is False
        assert sc["confidence_pct"] > 80.0

    asyncio.run(_test())

def test_natural_language_graph_query_and_dlp_enforcement():
    async def _test():
        # Valid query
        res = await OperatingGraphService.process_natural_language_query(None, "Which missions depend on Salesforce?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Query with secret pattern -> blocked by DLP
        secret_query = "What is blocking Project X? sk_live_1234567890abcdef"
        blocked_res = await OperatingGraphService.process_natural_language_query(None, secret_query)
        assert blocked_res["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_res["evidenceJson"].get("error", "")

    asyncio.run(_test())

def test_no_sensitive_employee_profiling_safeguards():
    async def _test():
        ov = await OperatingGraphService.get_organization_overview(None)
        # Verify focus is strictly on work, systems, capabilities, and outcomes
        for r in ov["risks"]:
            assert "employee_ranking" not in r
            assert "personality" not in r
            assert "surveillance" not in r

    asyncio.run(_test())
