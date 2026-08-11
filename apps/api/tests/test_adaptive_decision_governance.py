import pytest
import asyncio
from app.services.adaptive_decision_governance_service import AdaptiveDecisionGovernanceService

def test_get_control_overview():
    async def _test():
        res = await AdaptiveDecisionGovernanceService.get_control_overview(None)
        assert res["loopsCount"] >= 1
        assert res["signalsCount"] >= 1
        assert res["guardrailsCount"] >= 1
        assert res["reassessmentsCount"] >= 1
        assert res["responsesCount"] >= 1
        assert res["observationsCount"] >= 1
        assert res["loopHealthScore"] == 0.98
    asyncio.run(_test())

def test_create_control_loop_default_mode():
    async def _test():
        loop_data = {
            "name": "Cloud FinOps & GPU Cluster Control Loop",
            "description": "Closed-loop monitoring of GPU compute cost and node availability.",
            "targetEntityType": "infrastructure",
            "targetEntityId": "infra_gpu_pool_01",
            "owner": "usr_finops_lead",
            "workspaceId": "ws_finops"
        }
        res = await AdaptiveDecisionGovernanceService.create_control_loop(None, loop_data)
        assert res["id"] is not None
        assert res["name"] == loop_data["name"]
        assert res["mode"] == "monitor_only" # Default mode
        assert res["status"] == "active"
    asyncio.run(_test())

def test_pause_and_resume_control_loop():
    async def _test():
        loop_id = "loop_ctrl_01"
        paused = await AdaptiveDecisionGovernanceService.pause_control_loop(None, loop_id, actor_id="usr_admin")
        assert paused["status"] == "paused"
        assert paused["pausedBy"] == "usr_admin"

        resumed = await AdaptiveDecisionGovernanceService.resume_control_loop(None, loop_id, actor_id="usr_admin")
        assert resumed["status"] == "active"
        assert resumed["resumedBy"] == "usr_admin"
    asyncio.run(_test())

def test_natural_language_control_query_dlp_and_privacy():
    async def _test():
        # Valid query -> returns control loop state
        valid_q = "Which decisions are no longer valid?"
        res = await AdaptiveDecisionGovernanceService.process_natural_language_control_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] > 0.0

        # Secret query -> blocked by DLP
        secret_q = "Which decisions are no longer valid? vpr_12345678901"
        blocked = await AdaptiveDecisionGovernanceService.process_natural_language_control_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

        # Privacy query -> denied due to employee profiling/surveillance scoring prohibition
        privacy_q = "Calculate worker score and track employee surveillance ranking"
        denied = await AdaptiveDecisionGovernanceService.process_natural_language_control_query(None, privacy_q)
        assert denied["confidencePct"] == 0.0
        assert "Employee surveillance" in denied["evidenceJson"].get("error", "")
    asyncio.run(_test())
