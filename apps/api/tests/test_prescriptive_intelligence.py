import pytest
import asyncio
from app.services.prescriptive_intelligence_service import PrescriptiveIntelligenceService

def test_get_optimization_overview():
    async def _test():
        res = await PrescriptiveIntelligenceService.get_optimization_overview(None)
        assert res["problemsCount"] >= 1
        assert res["optionsCount"] >= 2
        assert res["recommendationsCount"] >= 1
        assert res["actionPlansCount"] >= 1
        assert res["paretoOptionsCount"] >= 1
        assert res["optimizationHealthScore"] == 0.96
    asyncio.run(_test())

def test_create_optimization_problem():
    async def _test():
        prob_data = {
            "name": "Q4 Cloud Infrastructure Cost & SLA Optimization",
            "description": "Optimize cloud instances to reduce spending while keeping p99 latency < 200ms.",
            "objectiveType": "minimize_cost",
            "owner": "usr_cloud_architect",
            "workspaceId": "ws_infra"
        }
        res = await PrescriptiveIntelligenceService.create_problem(None, prob_data)
        assert res["id"] is not None
        assert res["name"] == prob_data["name"]
        assert res["objective_type"] == "minimize_cost"
        assert res["status"] == "configured"
    asyncio.run(_test())

def test_action_plan_execution_and_rollback():
    async def _test():
        plan_id = "act_plan_01"
        res = await PrescriptiveIntelligenceService.execute_action_plan(None, plan_id, actor_id="usr_admin")
        assert res["actionPlanId"] == plan_id
        assert res["status"] == "executing"
        assert res["authorizedBy"] == "usr_admin"
        assert "rollbackPlan" in res
    asyncio.run(_test())

def test_natural_language_prescriptive_query_dlp_and_privacy():
    async def _test():
        # Valid query -> returns advisory options
        valid_q = "How should we allocate this capacity?"
        res = await PrescriptiveIntelligenceService.process_natural_language_prescriptive_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] > 0.0

        # Secret query -> blocked by DLP
        secret_q = "How should we allocate this capacity? vpr_12345678901"
        blocked = await PrescriptiveIntelligenceService.process_natural_language_prescriptive_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

        # Privacy query -> denied due to employee surveillance/termination prohibition
        privacy_q = "Optimize worker termination and fire worker next month"
        denied = await PrescriptiveIntelligenceService.process_natural_language_prescriptive_query(None, privacy_q)
        assert denied["confidencePct"] == 0.0
        assert "Employee surveillance" in denied["evidenceJson"].get("error", "")
    asyncio.run(_test())
