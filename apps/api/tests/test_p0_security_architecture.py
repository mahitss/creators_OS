import pytest
import asyncio
import jwt
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.config import settings
from app.services import identity_service

def generate_test_token(user_id: str, email: str, role: str = "member", workspace_id: str = "ws_default_01") -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "workspace_id": workspace_id,
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "iat": int(now.timestamp())
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def test_p0_unauthenticated_request_rejected():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Protected missions endpoint without auth
            resp = await client.get("/api/v1/missions")
            assert resp.status_code == 401

            # Protected workspace members endpoint without auth
            resp = await client.get("/api/v1/workspaces/ws_default_01/members")
            assert resp.status_code == 401

            # Protected admin endpoint without auth
            resp = await client.get("/api/v1/admin/agents/overview")
            assert resp.status_code == 401
    asyncio.run(_test())

def test_p0_header_spoofing_neutralized():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Attempting header-based admin spoofing without JWT
            headers = {
                "X-User-Id": "usr_admin_01",
                "X-User-Role": "admin",
                "X-Workspace-Id": "ws_default_01"
            }
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 401

            resp = await client.get("/api/v1/missions", headers=headers)
            assert resp.status_code == 401
    asyncio.run(_test())

def test_p0_member_cannot_access_admin_endpoints():
    async def _test():
        transport = ASGITransport(app=app)
        # Seed membership for standard member
        identity_service._in_memory_workspace_memberships["usr_member_01:ws_tenant_a"] = {
            "user_id": "usr_member_01",
            "workspace_id": "ws_tenant_a",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }

        member_token = generate_test_token("usr_member_01", "member@tenant-a.com", role="member", workspace_id="ws_tenant_a")
        headers = {"Authorization": f"Bearer {member_token}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Member trying to access admin agent control
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 403

            # Member trying to invite a member (requires admin)
            resp = await client.post(
                "/api/v1/workspaces/ws_tenant_a/invitations",
                headers=headers,
                json={"email": "new@tenant-a.com", "role": "admin"}
            )
            assert resp.status_code == 403

            # Member trying to access admin identity providers
            resp = await client.get("/api/v1/admin/identity/providers", headers=headers)
            assert resp.status_code == 403
    asyncio.run(_test())

def test_p0_cross_workspace_tenant_isolation():
    async def _test():
        transport = ASGITransport(app=app)
        # User A in Workspace A
        identity_service._in_memory_workspace_memberships["usr_tenant_a:ws_tenant_a"] = {
            "user_id": "usr_tenant_a",
            "workspace_id": "ws_tenant_a",
            "role": "owner",
            "status": "active",
            "permissions": ["admin", "read", "write"]
        }
        # User B in Workspace B
        identity_service._in_memory_workspace_memberships["usr_tenant_b:ws_tenant_b"] = {
            "user_id": "usr_tenant_b",
            "workspace_id": "ws_tenant_b",
            "role": "owner",
            "status": "active",
            "permissions": ["admin", "read", "write"]
        }

        token_a = generate_test_token("usr_tenant_a", "owner@tenant-a.com", role="owner", workspace_id="ws_tenant_a")
        headers_a = {"Authorization": f"Bearer {token_a}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # User A trying to access Workspace B members
            resp = await client.get("/api/v1/workspaces/ws_tenant_b/members", headers=headers_a)
            assert resp.status_code == 403

            # User A trying to invite into Workspace B
            resp = await client.post(
                "/api/v1/workspaces/ws_tenant_b/invitations",
                headers=headers_a,
                json={"email": "attacker@external.com", "role": "admin"}
            )
            assert resp.status_code == 403
    asyncio.run(_test())

def test_p0_csrf_protection_blocks_unauthorized_origin():
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_admin_01:ws_default_01"] = {
            "user_id": "usr_admin_01",
            "workspace_id": "ws_default_01",
            "role": "admin",
            "status": "active",
            "permissions": ["admin", "read", "write"]
        }
        admin_token = generate_test_token("usr_admin_01", "admin@vapor.test", role="admin", workspace_id="ws_default_01")
        
        # State changing request from malicious origin
        headers = {
            "Authorization": f"Bearer {admin_token}",
            "Origin": "https://malicious-evil-site.com"
        }

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/missions",
                headers=headers,
                json={"title": "CSRF Attack Mission", "description": "Attempt to create mission via CSRF"}
            )
            assert resp.status_code == 403
            assert "rejected" in resp.json()["detail"].lower()
    asyncio.run(_test())

def test_p0_mass_assignment_neutralization():
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_member_01:ws_tenant_a"] = {
            "user_id": "usr_member_01",
            "workspace_id": "ws_tenant_a",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        token = generate_test_token("usr_member_01", "member@tenant-a.com", role="member", workspace_id="ws_tenant_a")
        headers = {"Authorization": f"Bearer {token}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Attempting to assign mission to ws_tenant_b via body payload
            resp = await client.post(
                "/api/v1/missions",
                headers=headers,
                json={
                    "title": "Legitimate Title",
                    "description": "Legitimate Description",
                    "workspace_id": "ws_tenant_b"  # Mass assignment attempt
                }
            )
            assert resp.status_code == 201
            data = resp.json()
            # Created mission must belong to ws_tenant_a, NOT ws_tenant_b
            assert data["workspace_id"] == "ws_tenant_a"
            assert data["created_by"] == "usr_member_01"
    asyncio.run(_test())
