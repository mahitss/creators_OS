import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.finops_v2_service import FinOpsV2Service

def test_finops_overview_dashboard():
    async def _test():
        dash = await FinOpsV2Service.get_overview_dashboard(None)
        assert dash is not None
        assert "totalSpend" in dash
        assert "activeBudgetsCount" in dash
        assert "recommendationsCount" in dash

    asyncio.run(_test())

def test_record_usage_event_and_cost_calculation():
    async def _test():
        usage_data = {
            "organizationId": "org_default_creator",
            "workspaceId": "ws_default",
            "modelId": "gpt-4o",
            "providerId": "openai",
            "usageType": "model_input",
            "tokensInput": 1000,
            "tokensOutput": 500
        }
        evt = await FinOpsV2Service.record_usage_event(None, usage_data)
        assert evt["id"] is not None
        assert evt["tokens_input"] == 1000

        dash = await FinOpsV2Service.get_overview_dashboard(None)
        assert dash["totalSpend"] > 0

    asyncio.run(_test())

def test_attributed_costs_hierarchical():
    async def _test():
        by_model = await FinOpsV2Service.get_attributed_costs(None, "model")
        assert len(by_model) > 0
        assert by_model[0]["model"] is not None

        by_agent = await FinOpsV2Service.get_attributed_costs(None, "agent")
        assert len(by_agent) > 0

        by_mission = await FinOpsV2Service.get_attributed_costs(None, "mission")
        assert len(by_mission) > 0

    asyncio.run(_test())

def test_optimization_recommendations_approval_and_apply():
    async def _test():
        rec_id = "rec_model_switch_01"
        app = await FinOpsV2Service.approve_recommendation(None, rec_id)
        assert app["approval_status"] == "approved"

        applied = await FinOpsV2Service.apply_recommendation(None, rec_id)
        assert applied["approval_status"] == "applied"

        reverted = await FinOpsV2Service.revert_recommendation(None, rec_id)
        assert reverted["approval_status"] == "reverted"

    asyncio.run(_test())

def test_audited_cost_adjustment():
    async def _test():
        adj_data = {
            "costCalculationId": "calc_demo_01",
            "originalAmount": 10.0,
            "adjustedAmount": 7.5,
            "reason": "Audited billing correction"
        }
        adj = await FinOpsV2Service.create_cost_adjustment(None, adj_data, "usr_sec_admin_01")
        assert adj["id"] is not None
        assert adj["adjusted_amount"] == 7.5

    asyncio.run(_test())
