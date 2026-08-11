import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import control_plane_service
from app.schemas.control_plane import ControlActionRequest, AIOperationsQueryRequest

def test_operations_overview_aggregation():
    async def _test():
        overview = await control_plane_service.get_operations_overview(None, workspace_id="ws_default_01")
        assert overview["system_status"] in ["healthy", "degraded", "critical"]
        assert "contributing_signals" in overview
        assert len(overview["contributing_signals"]) >= 4
    asyncio.run(_test())

def test_service_dependency_map_topology():
    async def _test():
        services = await control_plane_service.get_service_dependency_map(None)
        assert len(services) >= 10
        sys_ids = [s["id"] for s in services]
        assert "sys_api" in sys_ids
        assert "sys_agent_runtime" in sys_ids
        assert "sys_event_mesh" in sys_ids
    asyncio.run(_test())

def test_control_action_gateway_low_risk_auto_execution():
    async def _test():
        req = ControlActionRequest(
            actionType="resume_service",
            targetResource="sys_workflow_engine",
            reason="Operator routine resume test",
            riskLevel="low"
        )
        action, err = await control_plane_service.request_control_action(None, req, requester_id="usr_op_01")
        assert err is None
        assert action["status"] == "completed"
    asyncio.run(_test())

def test_control_action_gateway_two_person_approval_enforcement():
    async def _test():
        # High Risk Action requires approval
        req = ControlActionRequest(
            actionType="cancel_workflow",
            targetResource="wf_batch_101",
            reason="Operator emergency cancellation",
            riskLevel="high"
        )
        action, err = await control_plane_service.request_control_action(None, req, requester_id="usr_requester_01")
        assert err is None
        assert action["status"] == "pending_approval"

        # Requester self-approval is REJECTED
        app_self, self_err = await control_plane_service.approve_control_action(None, action["id"], approver_id="usr_requester_01")
        assert app_self is None
        assert "Two-person approval required" in self_err

        # Approval by DIFFERENT user succeeds
        app_other, other_err = await control_plane_service.approve_control_action(None, action["id"], approver_id="usr_approver_02")
        assert other_err is None
        assert app_other["status"] == "completed"
    asyncio.run(_test())

def test_self_lockout_and_security_safeguard_protection():
    async def _test():
        req_lockout = ControlActionRequest(
            actionType="pause_service",
            targetResource="auth_kernel",
            reason="Malicious or accidental lockout attempt",
            riskLevel="critical"
        )
        action, err = await control_plane_service.request_control_action(None, req_lockout, requester_id="usr_rogue_01")
        assert action == {}
        assert "Security Safeguard DENY" in err
    asyncio.run(_test())

def test_post_action_verification_failure_handling():
    async def _test():
        req_verify_fail = ControlActionRequest(
            actionType="pause_service",
            targetResource="failing_service_test", # triggers simulated verification failure
            reason="Test state verification failure",
            riskLevel="low"
        )
        action, err = await control_plane_service.request_control_action(None, req_verify_fail, requester_id="usr_op_01")
        assert err is None
        assert action["status"] == "verification_failed"
    asyncio.run(_test())

def test_ai_operations_assistant_evidence_backed_response():
    async def _test():
        req_query = AIOperationsQueryRequest(prompt="Why is the platform degraded?")
        res = await control_plane_service.query_ai_operations_assistant(None, req_query, workspace_id="ws_default_01")
        assert res["confidence"] >= 0.90
        assert "answer" in res
        assert len(res["evidence_signals"]) >= 1
    asyncio.run(_test())
