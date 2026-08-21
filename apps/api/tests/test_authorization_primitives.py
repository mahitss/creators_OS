import pytest
import asyncio
import jwt
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, Depends

from app.core.config import settings
from app.dependencies.auth import (
    AuthenticatedContext,
    get_authenticated_context,
    require_role,
    authorize,
    require_admin,
    require_owner
)

# Test FastAPI App with authorization dependencies
auth_test_app = FastAPI()

@auth_test_app.get("/test/context")
async def context_route(ctx: AuthenticatedContext = Depends(get_authenticated_context)):
    return {"user_id": ctx.user_id, "workspace_id": ctx.workspace_id, "role": ctx.role}

@auth_test_app.get("/test/admin-only")
async def admin_route(ctx: AuthenticatedContext = Depends(require_admin)):
    return {"status": "authorized_admin"}

@auth_test_app.get("/test/owner-only")
async def owner_route(ctx: AuthenticatedContext = Depends(require_owner)):
    return {"status": "authorized_owner"}

@auth_test_app.get("/test/operator-or-above")
async def operator_route(ctx: AuthenticatedContext = Depends(require_role(["owner", "admin", "operator"]))):
    return {"status": "authorized_operator"}

@auth_test_app.post("/test/execute-action")
async def execute_route(ctx: AuthenticatedContext = Depends(authorize("EXECUTE", "mission_engine"))):
    return {"status": "executed"}

@auth_test_app.post("/test/administer-action")
async def administer_route(ctx: AuthenticatedContext = Depends(authorize("ADMINISTER", "security_policy"))):
    return {"status": "administered"}


def create_token(user_id: str, role: str, workspace_id: str = "ws_tenant_alpha") -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": f"{user_id}@domain.com",
        "role": role,
        "workspace_id": workspace_id,
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "iat": int(now.timestamp())
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def test_rbac_require_role_hierarchy():
    """Verify require_role permits authorized roles and blocks unauthorized roles."""
    async def _test():
        transport = ASGITransport(app=auth_test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            viewer_token = create_token("usr_viewer", "viewer")
            operator_token = create_token("usr_operator", "operator")
            admin_token = create_token("usr_admin", "admin")
            owner_token = create_token("usr_owner", "owner")

            # 1. Operator endpoint
            # Viewer -> 403
            resp = await client.get("/test/operator-or-above", headers={"Authorization": f"Bearer {viewer_token}"})
            assert resp.status_code == 403
            assert "Access denied" in resp.json()["detail"]

            # Operator -> 200
            resp = await client.get("/test/operator-or-above", headers={"Authorization": f"Bearer {operator_token}"})
            assert resp.status_code == 200

            # Admin -> 200
            resp = await client.get("/test/operator-or-above", headers={"Authorization": f"Bearer {admin_token}"})
            assert resp.status_code == 200

            # Owner -> 200
            resp = await client.get("/test/operator-or-above", headers={"Authorization": f"Bearer {owner_token}"})
            assert resp.status_code == 200
    asyncio.run(_test())


def test_fine_grained_authorize_action_matrix():
    """Verify authorize(action, resource) evaluates the role-action matrix correctly."""
    async def _test():
        transport = ASGITransport(app=auth_test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            viewer_token = create_token("usr_viewer", "viewer")
            analyst_token = create_token("usr_analyst", "analyst")
            operator_token = create_token("usr_operator", "operator")
            admin_token = create_token("usr_admin", "admin")

            # Action: EXECUTE
            # Viewer cannot EXECUTE -> 403
            resp = await client.post("/test/execute-action", headers={"Authorization": f"Bearer {viewer_token}"})
            assert resp.status_code == 403

            # Analyst cannot EXECUTE -> 403
            resp = await client.post("/test/execute-action", headers={"Authorization": f"Bearer {analyst_token}"})
            assert resp.status_code == 403

            # Operator CAN EXECUTE -> 200
            resp = await client.post("/test/execute-action", headers={"Authorization": f"Bearer {operator_token}"})
            assert resp.status_code == 200

            # Action: ADMINISTER
            # Operator cannot ADMINISTER -> 403
            resp = await client.post("/test/administer-action", headers={"Authorization": f"Bearer {operator_token}"})
            assert resp.status_code == 403

            # Admin CAN ADMINISTER -> 200
            resp = await client.post("/test/administer-action", headers={"Authorization": f"Bearer {admin_token}"})
            assert resp.status_code == 200
    asyncio.run(_test())


def test_cross_tenant_isolation_boundary():
    """Verify attempting to switch to an unassigned workspace fails closed with 403 Forbidden."""
    async def _test():
        transport = ASGITransport(app=auth_test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = create_token("usr_alpha", "admin", workspace_id="ws_tenant_alpha")

            # Same workspace header -> 200
            resp = await client.get("/test/context", headers={
                "Authorization": f"Bearer {token}",
                "X-Workspace-Id": "ws_tenant_alpha"
            })
            assert resp.status_code == 200
            assert resp.json()["workspace_id"] == "ws_tenant_alpha"

            # Foreign workspace header without membership -> 403 Forbidden
            resp = await client.get("/test/context", headers={
                "Authorization": f"Bearer {token}",
                "X-Workspace-Id": "ws_tenant_beta_foreign"
            })
            assert resp.status_code == 403
            assert "is not an authorized member of workspace" in resp.json()["detail"]
    asyncio.run(_test())
