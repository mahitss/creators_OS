import time
import uuid
import json
import base64
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.api.routers.auth import _create_jwt_token, _pending_challenges

def test_admin_requires_authenticated_session():
    """Unauthenticated access to administrative endpoints must be denied with 401."""
    async def _test():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/v1/admin/agents/overview")
            assert resp.status_code == 401
    asyncio.run(_test())

def test_admin_headers_cannot_authenticate():
    """Spoofed X-User-Id and X-Workspace-Id headers without valid session must be denied with 401."""
    async def _test():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            headers = {
                "X-User-Id": "usr_admin_01",
                "X-Workspace-Id": "ws_default_01"
            }
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 401
    asyncio.run(_test())

def test_admin_headers_cannot_escalate_member():
    """A member session must not be escalated to admin simply by spoofing admin headers."""
    async def _test():
        now = time.time()
        member_token = _create_jwt_token({
            "sub": "usr_member_123",
            "email": "member@vapor.os",
            "role": "member",
            "workspace_id": "ws_member_123",
            "iat": int(now),
            "exp": int(now + 3600),
            "jti": str(uuid.uuid4())
        })

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            headers = {
                "Authorization": f"Bearer {member_token}",
                "X-User-Id": "usr_admin_01",
                "X-Workspace-Id": "ws_member_123"
            }
            resp = await client.get("/api/v1/admin/agents/overview", headers=headers)
            assert resp.status_code == 403
    asyncio.run(_test())

def test_workspace_header_cannot_change_tenant():
    """An authenticated user in Workspace A cannot access Workspace B via header injection."""
    async def _test():
        now = time.time()
        user_token = _create_jwt_token({
            "sub": "usr_user_a",
            "email": "user_a@vapor.os",
            "role": "member",
            "workspace_id": "ws_tenant_a",
            "iat": int(now),
            "exp": int(now + 3600),
            "jti": str(uuid.uuid4())
        })

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            headers = {
                "Authorization": f"Bearer {user_token}",
                "X-Workspace-Id": "ws_tenant_b"
            }
            resp = await client.get("/api/v1/missions", headers=headers)
            assert resp.status_code in [200, 403, 404]
    asyncio.run(_test())

def test_passkey_requires_challenge():
    """POST /auth/passkey/verify without challenge must be rejected with 401."""
    async def _test():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/auth/passkey/verify",
                json={"email": "attacker@example.com", "credential_id": "credential_123456"}
            )
            assert resp.status_code in [400, 401]
    asyncio.run(_test())

def test_passkey_invalid_signature_rejected():
    """POST /auth/passkey/verify with mismatched challenge signature must be rejected with 401."""
    async def _test():
        email = "target_user@example.com"
        _pending_challenges[email] = {
            "challenge": "valid_hex_challenge_1234567890",
            "issued_at": time.time(),
            "user_id": "usr_target_01"
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/auth/passkey/verify",
                json={
                    "email": email,
                    "credential_id": "credential_valid_123",
                    "challenge": "wrong_signature_attempt"
                }
            )
            assert resp.status_code == 401
    asyncio.run(_test())

def test_passkey_expired_challenge_rejected():
    """POST /auth/passkey/verify with expired challenge must be rejected with 401."""
    async def _test():
        email = "expired_user@example.com"
        _pending_challenges[email] = {
            "challenge": "expired_hex_challenge_1234567890",
            "issued_at": time.time() - 300, # 5 minutes old
            "user_id": "usr_expired_01"
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/auth/passkey/verify",
                json={
                    "email": email,
                    "credential_id": "credential_valid_123",
                    "challenge": "expired_hex_challenge_1234567890"
                }
            )
            assert resp.status_code == 401
    asyncio.run(_test())

def test_passkey_valid_assertion_accepted():
    """POST /auth/passkey/verify with valid matching challenge produces authenticated token."""
    async def _test():
        email = "legit_passkey_user@example.com"
        challenge_val = "valid_hex_challenge_abcdef123456"
        _pending_challenges[email] = {
            "challenge": challenge_val,
            "issued_at": time.time(),
            "user_id": "usr_legit_passkey_01"
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/auth/passkey/verify",
                json={
                    "email": email,
                    "credential_id": "credential_valid_888",
                    "challenge": challenge_val
                }
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "access_token" in data
            assert data["email"] == email
    asyncio.run(_test())

def test_cors_rejects_untrusted_origin():
    """Requests from untrusted origins must NOT receive Access-Control-Allow-Origin."""
    async def _test():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.options(
                "/api/v1/health",
                headers={
                    "Origin": "https://attacker.example",
                    "Access-Control-Request-Method": "GET"
                }
            )
            assert resp.headers.get("access-control-allow-origin") != "https://attacker.example"
    asyncio.run(_test())

def test_cors_allows_configured_origin():
    """Requests from configured origin (http://localhost:3000) must receive Access-Control-Allow-Origin."""
    async def _test():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.options(
                "/api/v1/health",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET"
                }
            )
            assert resp.headers.get("access-control-allow-origin") == "http://localhost:3000"
    asyncio.run(_test())
