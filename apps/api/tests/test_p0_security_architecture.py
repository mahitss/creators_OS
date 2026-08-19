import pytest
import asyncio
import jwt
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.config import settings, Settings, validate_production_secrets
from app.services import identity_service, mission_service

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

def test_every_protected_router_requires_auth():
    """Every protected endpoint under /api/v1 must fail closed with 401 when unauthenticated."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            protected_endpoints = [
                ("GET", "/api/v1/missions"),
                ("GET", "/api/v1/memories"),
                ("GET", "/api/v1/content"),
                ("GET", "/api/v1/deliverables"),
                ("GET", "/api/v1/workflows"),
                ("GET", "/api/v1/automations"),
                ("GET", "/api/v1/finops"),
                ("GET", "/api/v1/intelligence/signals"),
                ("GET", "/api/v1/knowledge"),
                ("GET", "/api/v1/search?q=test"),
                ("GET", "/api/v1/admin/agents/overview"),
                ("GET", "/api/v1/admin/identity/providers"),
                ("POST", "/api/v1/missions"),
                ("POST", "/api/v1/workflows"),
                ("POST", "/api/v1/automations"),
            ]
            for method, ep in protected_endpoints:
                if method == "GET":
                    resp = await client.get(ep)
                else:
                    resp = await client.post(ep, json={"test": "payload"})
                assert resp.status_code == 401, f"Endpoint {ep} allowed unauthenticated access!"
    asyncio.run(_test())

def test_user_headers_never_authenticate():
    """Client-supplied identity headers without valid JWT/cookie must be rejected with 401."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            headers = {
                "X-User-Id": "usr_admin_01",
                "X-User-Role": "admin",
                "X-Workspace-Id": "ws_default_01"
            }
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 401

            resp = await client.get("/api/v1/missions", headers=headers)
            assert resp.status_code == 401

            resp = await client.post("/api/v1/missions", headers=headers, json={"title": "Hacked"})
            assert resp.status_code == 401
    asyncio.run(_test())

def test_workspace_headers_never_authorize():
    """Supplying an unauthorized X-Workspace-Id header must be rejected with 403."""
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_user_a:ws_tenant_a"] = {
            "user_id": "usr_user_a",
            "workspace_id": "ws_tenant_a",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        token_a = generate_test_token("usr_user_a", "user_a@tenant-a.com", role="member", workspace_id="ws_tenant_a")
        
        # User A trying to switch to Workspace B via header
        headers = {
            "Authorization": f"Bearer {token_a}",
            "X-Workspace-Id": "ws_tenant_b"
        }

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/api/v1/missions", headers=headers)
            assert resp.status_code == 403
            assert "not an authorized member" in resp.json()["detail"]
    asyncio.run(_test())

def test_cross_tenant_read_denied():
    """Tenant A cannot read Tenant B missions or resources (IDOR prevention)."""
    async def _test():
        transport = ASGITransport(app=app)
        # Seed Tenant A and B memberships
        identity_service._in_memory_workspace_memberships["usr_tenant_a:ws_tenant_a"] = {
            "user_id": "usr_tenant_a",
            "workspace_id": "ws_tenant_a",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        identity_service._in_memory_workspace_memberships["usr_tenant_b:ws_tenant_b"] = {
            "user_id": "usr_tenant_b",
            "workspace_id": "ws_tenant_b",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }

        # Create mission in Tenant B
        token_b = generate_test_token("usr_tenant_b", "user_b@tenant-b.com", role="member", workspace_id="ws_tenant_b")
        headers_b = {"Authorization": f"Bearer {token_b}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res_b = await client.post(
                "/api/v1/missions",
                headers=headers_b,
                json={"title": "Confidential Tenant B Mission", "description": "Secret strategy"}
            )
            assert res_b.status_code == 201
            mission_b_id = res_b.json()["id"]

            # Tenant A attempts to read Tenant B's mission
            token_a = generate_test_token("usr_tenant_a", "user_a@tenant-a.com", role="member", workspace_id="ws_tenant_a")
            headers_a = {"Authorization": f"Bearer {token_a}"}

            res_a = await client.get(f"/api/v1/missions/{mission_b_id}", headers=headers_a)
            assert res_a.status_code in [403, 404]
    asyncio.run(_test())

def test_cross_tenant_write_and_delete_denied():
    """Tenant A cannot mutate or delete Tenant B resources."""
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_tenant_a:ws_tenant_a"] = {
            "user_id": "usr_tenant_a",
            "workspace_id": "ws_tenant_a",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        identity_service._in_memory_workspace_memberships["usr_tenant_b:ws_tenant_b"] = {
            "user_id": "usr_tenant_b",
            "workspace_id": "ws_tenant_b",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }

        token_b = generate_test_token("usr_tenant_b", "user_b@tenant-b.com", role="member", workspace_id="ws_tenant_b")
        headers_b = {"Authorization": f"Bearer {token_b}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res_b = await client.post(
                "/api/v1/missions",
                headers=headers_b,
                json={"title": "Mission B", "description": "Original"}
            )
            mission_b_id = res_b.json()["id"]

            token_a = generate_test_token("usr_tenant_a", "user_a@tenant-a.com", role="member", workspace_id="ws_tenant_a")
            headers_a = {"Authorization": f"Bearer {token_a}"}

            # Tenant A attempts to update Tenant B mission
            patch_res = await client.patch(
                f"/api/v1/missions/{mission_b_id}",
                headers=headers_a,
                json={"description": "Tampered description"}
            )
            assert patch_res.status_code in [403, 404]

            # Tenant A attempts to delete Tenant B mission / automation
            del_res = await client.delete(f"/api/v1/missions/{mission_b_id}", headers=headers_a)
            assert del_res.status_code in [403, 404, 405]
    asyncio.run(_test())

def test_member_and_viewer_admin_denied():
    """Members and Viewers are strictly denied access to administrative control planes."""
    async def _test():
        transport = ASGITransport(app=app)
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
            # Member trying admin overview
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 403

            # Member trying member invitations
            resp = await client.post(
                "/api/v1/workspaces/ws_tenant_a/invitations",
                headers=headers,
                json={"email": "new@tenant-a.com", "role": "admin"}
            )
            assert resp.status_code == 403

            # Member trying IdP management
            resp = await client.get("/api/v1/admin/identity/providers", headers=headers)
            assert resp.status_code == 403
    asyncio.run(_test())

def test_agent_cross_workspace_denied():
    """Agent run execution cannot target victim workspaces."""
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_attacker:ws_attacker"] = {
            "user_id": "usr_attacker",
            "workspace_id": "ws_attacker",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        token = generate_test_token("usr_attacker", "attacker@evil.com", role="member", workspace_id="ws_attacker")
        headers = {"Authorization": f"Bearer {token}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Attempt to launch agent run on a victim's mission
            resp = await client.post(
                "/api/v1/missions/msn_victim_01/agent-runs",
                headers=headers,
                json={"goal": "Exfiltrate data"}
            )
            assert resp.status_code in [400, 403, 404]
    asyncio.run(_test())

def test_mass_assignment_neutralized():
    """Client cannot spoof workspace_id or created_by via body payload."""
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
            resp = await client.post(
                "/api/v1/missions",
                headers=headers,
                json={
                    "title": "Legitimate Mission",
                    "description": "Description",
                    "workspace_id": "ws_victim_tenant",
                    "created_by": "usr_admin_victim"
                }
            )
            assert resp.status_code == 201
            data = resp.json()
            assert data["workspace_id"] == "ws_tenant_a"
            assert data["created_by"] == "usr_member_01"
    asyncio.run(_test())

def test_csrf_protection_blocks_unauthorized_origin():
    """State-changing requests with untrusted Origin header receive 403 Forbidden."""
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
        
        headers = {
            "Authorization": f"Bearer {admin_token}",
            "Origin": "https://attacker.example.com"
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

def test_legitimate_authenticated_member_workflow():
    """Legitimate authenticated member can successfully create, list, and read resources."""
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_legit_01:ws_legit_01"] = {
            "user_id": "usr_legit_01",
            "workspace_id": "ws_legit_01",
            "role": "member",
            "status": "active",
            "permissions": ["read", "write"]
        }
        token = generate_test_token("usr_legit_01", "legit@vapor.os", role="member", workspace_id="ws_legit_01")
        headers = {"Authorization": f"Bearer {token}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Create Mission
            res = await client.post(
                "/api/v1/missions",
                headers=headers,
                json={"title": "Legitimate Q3 Planning", "description": "Roadmap deliverables", "priority": "high"}
            )
            assert res.status_code == 201
            m = res.json()
            assert m["workspace_id"] == "ws_legit_01"
            m_id = m["id"]

            # 2. Get Mission
            get_res = await client.get(f"/api/v1/missions/{m_id}", headers=headers)
            assert get_res.status_code == 200
            assert get_res.json()["id"] == m_id

            # 3. List Missions
            list_res = await client.get("/api/v1/missions", headers=headers)
            assert list_res.status_code == 200
            assert list_res.json()["total"] >= 1
    asyncio.run(_test())

def test_legitimate_admin_workflow():
    """Legitimate workspace admin can access administrative endpoints."""
    async def _test():
        transport = ASGITransport(app=app)
        identity_service._in_memory_workspace_memberships["usr_admin_01:ws_admin_01"] = {
            "user_id": "usr_admin_01",
            "workspace_id": "ws_admin_01",
            "role": "admin",
            "status": "active",
            "permissions": ["admin", "read", "write"]
        }
        admin_token = generate_test_token("usr_admin_01", "admin@vapor.os", role="admin", workspace_id="ws_admin_01")
        headers = {"Authorization": f"Bearer {admin_token}"}

        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 200
            assert "active_agents" in resp.json()
    asyncio.run(_test())
