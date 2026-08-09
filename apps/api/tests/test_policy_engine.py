import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.policy_engine import PolicyContext, PolicyDecision, evaluate_policy, create_policy_rule

client = TestClient(app)
HEADERS = {"X-User-Id": "usr_alex", "X-Workspace-Id": "ws_pol_test"}

def test_policy_read_allow_decision():
    async def _test():
        ctx = PolicyContext(
            workspace_id="ws_pol_test",
            user_id="usr_alex",
            tool_name="search_drive_files",
            risk_level="READ",
            user_role="member"
        )
        decision = await evaluate_policy(None, ctx)
        assert decision.decision == "ALLOW"
        assert decision.risk_level == "READ"

    asyncio.run(_test())

def test_policy_write_approval_required():
    async def _test():
        ctx = PolicyContext(
            workspace_id="ws_pol_test",
            user_id="usr_alex",
            tool_name="create_calendar_event",
            risk_level="WRITE",
            user_role="member"
        )
        decision = await evaluate_policy(None, ctx)
        assert decision.decision == "APPROVAL_REQUIRED"
        assert decision.required_approval_type == "USER_CONFIRMATION"

    asyncio.run(_test())

def test_policy_destructive_deny_shielding():
    async def _test():
        ctx = PolicyContext(
            workspace_id="ws_pol_test",
            user_id="usr_alex",
            tool_name="delete_file",
            risk_level="DESTRUCTIVE",
            user_role="owner"
        )
        decision = await evaluate_policy(None, ctx)
        assert decision.decision == "DENY"
        assert "strictly prohibited" in decision.reason

    asyncio.run(_test())

def test_policy_viewer_role_write_denial():
    async def _test():
        ctx = PolicyContext(
            workspace_id="ws_pol_test",
            user_id="usr_viewer_01",
            tool_name="create_content",
            risk_level="WRITE",
            user_role="viewer"
        )
        decision = await evaluate_policy(None, ctx)
        assert decision.decision == "DENY"
        assert "viewer" in decision.reason

    asyncio.run(_test())

def test_policy_custom_rule_priority():
    async def _test():
        await create_policy_rule(
            session=None,
            workspace_id="ws_pol_test",
            name="Block Search Tool",
            action="DENY",
            conditions={"tool_name": "search_drive_files"},
            priority=100
        )
        ctx = PolicyContext(
            workspace_id="ws_pol_test",
            user_id="usr_alex",
            tool_name="search_drive_files",
            risk_level="READ",
            user_role="owner"
        )
        decision = await evaluate_policy(None, ctx)
        assert decision.decision == "DENY"
        assert "Block Search Tool" in decision.reason

    asyncio.run(_test())

def test_policies_rest_endpoints():
    # 1. Create Rule via REST API
    res = client.post("/api/v1/policies/rules", json={
        "name": "Rest API Rule",
        "action": "APPROVAL_REQUIRED",
        "conditions": {"tool_name": "create_content"},
        "priority": 50
    }, headers=HEADERS)
    assert res.status_code == 201

    # 2. Evaluate Dry-Run
    eval_res = client.post("/api/v1/policies/evaluate", json={
        "tool_name": "create_content",
        "risk_level": "WRITE",
        "user_role": "member"
    }, headers=HEADERS)
    assert eval_res.status_code == 200
    assert eval_res.json()["decision"] == "APPROVAL_REQUIRED"
