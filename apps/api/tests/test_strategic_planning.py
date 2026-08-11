import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.strategic_planning_service import StrategicPlanningService

def test_strategy_overview_telemetry():
    async def _test():
        ov = await StrategicPlanningService.get_strategy_overview(None)
        assert ov is not None
        assert "objectivesCount" in ov
        assert "initiativesCount" in ov
        assert "assumptionsCount" in ov
        assert "strategyDriftCount" in ov
        assert ov["strategyHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_plan_in_draft_status():
    async def _test():
        plan_data = {
            "name": "Q4 AI Infrastructure Scaling Plan",
            "description": "Expand multi-region compute capacity for enterprise agent workloads.",
            "owner": "usr_exec_01",
            "startDate": "2026-10-01",
            "endDate": "2026-12-31",
            "workspaceId": "ws_default"
        }
        plan = await StrategicPlanningService.create_plan(None, plan_data)
        assert plan["id"] is not None
        assert plan["status"] == "draft"
        assert plan["version"] == 1

    asyncio.run(_test())

def test_verify_assumption_and_invalidation_governance():
    async def _test():
        ov = await StrategicPlanningService.get_strategy_overview(None)
        ass_id = ov["assumptions"][0]["id"]
        v_ass = await StrategicPlanningService.verify_assumption(None, ass_id)
        assert v_ass["validity"] == "valid"
        assert v_ass["verified_at"] is not None

    asyncio.run(_test())

def test_multi_option_recommendations_and_reversibility():
    async def _test():
        ov = await StrategicPlanningService.get_strategy_overview(None)
        recs = ov["recommendations"]
        assert len(recs) > 0
        rec = recs[0]
        assert len(rec["alternatives_json"]) >= 3
        # Check explicit reversibility ratings
        for alt in rec["alternatives_json"]:
            assert "reversibility" in alt

    asyncio.run(_test())

def test_natural_language_strategy_query_and_dlp():
    async def _test():
        # Valid strategy query
        res = await StrategicPlanningService.process_natural_language_strategy_query(None, "Which objectives are most at risk?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Secret query -> blocked by DLP
        secret_q = "Which objectives are at risk? sk_live_999988887777"
        blocked = await StrategicPlanningService.process_natural_language_strategy_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

    asyncio.run(_test())
