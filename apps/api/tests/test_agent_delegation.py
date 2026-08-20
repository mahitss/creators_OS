import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.agent_delegation_service import (
    create_agent_definition,
    create_delegation,
    revoke_delegation,
    create_agent_handoff
)
from app.services.workspace_service import _in_memory_members
from app.services.policy_engine import PolicyContext, evaluate_policy

client = TestClient(app)
HEADERS_OWNER = {"X-User-Id": "usr_alex", "X-Workspace-Id": "ws_del_test"}

_in_memory_members["ws_del_test_usr_alex"] = {
    "id": "mem_del_01",
    "workspace_id": "ws_del_test",
    "user_id": "usr_alex",
    "email": "alex@vapor.internal",
    "role": "owner",
    "status": "active"
}

def test_delegation_creation_and_tool_whitelisting():
    async def _test():
        # 1. Create Agent Definition
        agent_def = await create_agent_definition(None, workspace_id="ws_del_test", name="Research Agent", description="Read-only research", created_by="usr_alex")
        def_id = agent_def["id"]

        # 2. Create Scoped Delegation with Tool Whitelist [search_drive_files]
        delegation = await create_delegation(
            None, workspace_id="ws_del_test", delegated_by="usr_alex", agent_id=def_id,
            scope="mission", allowed_tools=["search_drive_files"]
        )
        del_id = delegation["id"]

        # 3. Evaluate Policy for Whitelisted Tool -> Expected ALLOW
        ctx_ok = PolicyContext(
            workspace_id="ws_del_test",
            user_id="usr_alex",
            tool_name="search_drive_files",
            risk_level="READ",
            delegation_id=del_id
        )
        dec_ok = await evaluate_policy(None, ctx_ok)
        assert dec_ok.decision == "ALLOW"

        # 4. Evaluate Policy for Un-whitelisted Tool -> Expected DENY
        ctx_denied = PolicyContext(
            workspace_id="ws_del_test",
            user_id="usr_alex",
            tool_name="create_calendar_event",
            risk_level="WRITE",
            delegation_id=del_id
        )
        dec_denied = await evaluate_policy(None, ctx_denied)
        assert dec_denied.decision == "DENY"
        assert "not in delegation allowed tools" in dec_denied.reason

    asyncio.run(_test())

def test_privilege_escalation_prevention():
    async def _test():
        # Explicitly register usr_viewer_01 as viewer in ws_del_test
        _in_memory_members["ws_del_test_usr_viewer_01"] = {
            "id": "mem_v01",
            "workspace_id": "ws_del_test",
            "user_id": "usr_viewer_01",
            "email": "viewer@vapor.internal",
            "role": "viewer",
            "status": "active"
        }

        # Viewer attempting to delegate write permissions -> Expected ValueError
        try:
            await create_delegation(
                None, workspace_id="ws_del_test", delegated_by="usr_viewer_01", agent_id="def_research_01",
                permissions=["create_draft", "schedule_event"]
            )
            assert False, "Should have blocked viewer from delegating write permissions"
        except ValueError as exc:
            assert "cannot delegate" in str(exc).lower()

    asyncio.run(_test())

def test_delegation_revocation_denial():
    async def _test():
        agent_def = await create_agent_definition(None, workspace_id="ws_del_test", name="Drafting Agent", description="Drafting", created_by="usr_alex")
        del_obj = await create_delegation(None, workspace_id="ws_del_test", delegated_by="usr_alex", agent_id=agent_def["id"])
        del_id = del_obj["id"]

        # Revoke Delegation
        await revoke_delegation(None, workspace_id="ws_del_test", del_id=del_id, actor_id="usr_alex")

        # Evaluate Policy -> Expected DENY
        ctx = PolicyContext(workspace_id="ws_del_test", user_id="usr_alex", tool_name="search_drive_files", delegation_id=del_id)
        dec = await evaluate_policy(None, ctx)
        assert dec.decision == "DENY"
        assert "revoked" in dec.reason

    asyncio.run(_test())

def test_max_handoff_depth_limit():
    async def _test():
        # Attempt handoff at depth = 4 -> Expected ValueError
        try:
            await create_agent_handoff(
                None, workspace_id="ws_del_test", source_agent_run_id="run_01",
                target_agent_definition_id="def_research_01", mission_id="m_01", current_depth=4
            )
            assert False, "Should have blocked depth > 3"
        except ValueError as exc:
            assert "exceeded" in str(exc).lower()

    asyncio.run(_test())

def test_delegation_rest_api_endpoints():
    # 1. Create Agent Definition
    a_res = client.post("/api/v1/agents", json={
        "name": "Scheduling Assistant",
        "description": "Calendar scheduling agent",
        "visibility": "workspace"
    }, headers=HEADERS_OWNER)
    assert a_res.status_code == 201
    ag_id = a_res.json()["id"]

    # 2. Create Delegation
    d_res = client.post(f"/api/v1/agents/{ag_id}/delegations", json={
        "scope": "mission",
        "allowed_tools": ["get_calendar_events", "create_calendar_event"]
    }, headers=HEADERS_OWNER)
    assert d_res.status_code == 201
    del_id = d_res.json()["id"]

    # 3. Revoke Delegation via REST
    rev_res = client.post(f"/api/v1/delegations/{del_id}/revoke", headers=HEADERS_OWNER)
    assert rev_res.status_code == 200
    assert rev_res.json()["status"] == "revoked"
