import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.workspace_service import (
    invite_workspace_member,
    accept_workspace_invitation,
    update_member_role,
    suspend_workspace_member,
    remove_workspace_member
)

client = TestClient(app)
HEADERS_OWNER = {"X-User-Id": "usr_alex", "X-Workspace-Id": "ws_team_test"}
HEADERS_MEMBER = {"X-User-Id": "usr_member_01", "X-Workspace-Id": "ws_team_test"}

def test_workspace_invitation_flow():
    async def _test():
        inv = await invite_workspace_member(None, workspace_id="ws_team_test", email="colleague@vapor.internal", role="member", invited_by="usr_alex")
        assert inv["status"] == "pending"
        token = inv["raw_token_preview"]

        member = await accept_workspace_invitation(None, workspace_id="ws_team_test", token=token, user_id="usr_member_01")
        assert member["status"] == "active"
        assert member["role"] == "member"

    asyncio.run(_test())

def test_last_owner_protection():
    async def _test():
        # Setup workspace with 1 owner
        await accept_workspace_invitation(None, workspace_id="ws_single_owner", token=(await invite_workspace_member(None, "ws_single_owner", "owner@v.in", "owner", "usr_alex"))["raw_token_preview"], user_id="usr_sole_owner")

        # Attempt to demote sole owner -> Expect ValueError
        try:
            await update_member_role(None, workspace_id="ws_single_owner", member_user_id="usr_sole_owner", new_role="member", actor_id="usr_sole_owner")
            assert False, "Should have raised ValueError for last owner demotion"
        except ValueError as exc:
            assert "last owner" in str(exc).lower()

        # Attempt to suspend sole owner -> Expect ValueError
        try:
            await suspend_workspace_member(None, workspace_id="ws_single_owner", member_user_id="usr_sole_owner", actor_id="usr_sole_owner")
            assert False, "Should have raised ValueError for last owner suspension"
        except ValueError as exc:
            assert "last owner" in str(exc).lower()

    asyncio.run(_test())

def test_workspace_member_api_endpoints():
    # 1. Invite Member
    res = client.post("/api/v1/workspaces/ws_team_test/invitations", json={
        "email": "dev@vapor.internal",
        "role": "member"
    }, headers=HEADERS_OWNER)
    assert res.status_code == 201
    inv_data = res.json()

    # 2. Accept Invitation
    token = inv_data["raw_token_preview"]
    acc_res = client.post("/api/v1/workspaces/ws_team_test/invitations/accept", json={"token": token}, headers=HEADERS_MEMBER)
    assert acc_res.status_code == 200

    # 3. Member List
    list_res = client.get("/api/v1/workspaces/ws_team_test/members", headers=HEADERS_OWNER)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
