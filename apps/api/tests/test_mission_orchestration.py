import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
api_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import mission_orchestration_service
from app.schemas.mission_orchestration import (
    MissionObjectiveCreate,
    MissionReplanRequest,
    MissionValidateRequest
)

def test_clear_vs_ambiguous_objective_classification():
    async def _test():
        req_clear = MissionObjectiveCreate(
            title="Clear Mission",
            goal="Execute data backup and verify checksums",
            priority="normal"
        )
        m1, plan1 = await mission_orchestration_service.create_mission_orchestration(
            None, workspace_id="ws_test_orch", user_id="usr_01", req=req_clear
        )
        assert plan1["version"] == 1
        assert len(plan1["steps"]) >= 1

        req_amb = MissionObjectiveCreate(
            title="Ambiguous Mission",
            goal="Do something vague and ambiguous with unspecified parameters",
            priority="low"
        )
        m2, plan2 = await mission_orchestration_service.create_mission_orchestration(
            None, workspace_id="ws_test_orch", user_id="usr_01", req=req_amb
        )
        assert plan2["version"] == 1
    asyncio.run(_test())

def test_versioned_replanning_and_replan_limit():
    async def _test():
        req = MissionObjectiveCreate(
            title="Replan Test Mission",
            goal="Audit system logs and export summary report",
            priority="high"
        )
        m, plan = await mission_orchestration_service.create_mission_orchestration(
            None, workspace_id="ws_test_replan", user_id="usr_01", req=req
        )
        m_id = m["id"]

        replan_req = MissionReplanRequest(triggerReason="Dependency latency spike detected")
        updated_plan = await mission_orchestration_service.replan_mission(
            None, workspace_id="ws_test_replan", mission_id=m_id, req=replan_req
        )
        assert updated_plan["version"] == 2
        assert updated_plan["replan_count"] == 1

        versions = await mission_orchestration_service.get_plan_versions(None, mission_id=m_id)
        assert len(versions) == 2
        assert versions[1]["version"] == 2

        # Enforce max replan limit
        updated_plan["replan_count"] = updated_plan["max_replans"]
        with pytest.raises(ValueError, match="Max replan limit"):
            await mission_orchestration_service.replan_mission(
                None, workspace_id="ws_test_replan", mission_id=m_id, req=replan_req
            )
    asyncio.run(_test())

def test_deliverable_validation():
    async def _test():
        req = MissionObjectiveCreate(
            title="Validator Test Mission",
            goal="Scan repository for secrets",
            priority="high"
        )
        m, plan = await mission_orchestration_service.create_mission_orchestration(
            None, workspace_id="ws_test_val", user_id="usr_01", req=req
        )
        m_id = m["id"]
        step_id = plan["steps"][0]["id"]

        val_req = MissionValidateRequest(stepId=step_id, verifierType="action_gateway")
        res = await mission_orchestration_service.validate_deliverable(
            None, mission_id=m_id, req=val_req
        )
        assert res["passed"] is True
        assert res["step_id"] == step_id

        updated_plan = await mission_orchestration_service.get_plan(None, mission_id=m_id)
        target = next(s for s in updated_plan["steps"] if s["id"] == step_id)
        assert target["status"] == "completed"
    asyncio.run(_test())

def test_mission_costs_and_risks():
    async def _test():
        m_id = "m_demo_orchestrator_01"
        costs = await mission_orchestration_service.get_costs(None, mission_id=m_id)
        assert costs is not None
        assert costs["remaining_budget_usd"] > 0

        risks = await mission_orchestration_service.get_risks(None, mission_id=m_id)
        assert risks is not None
        assert "data_risk" in risks
        assert "action_risk" in risks
    asyncio.run(_test())
