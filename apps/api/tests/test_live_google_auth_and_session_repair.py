import pytest
import asyncio
import json
import base64
import jwt
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.config import settings
from app.services import identity_service

def generate_mock_google_id_token(
    sub: str = "google_sub_1092837465",
    email: str = "alex.creator@example.com",
    name: str = "Alex Creator",
    picture: str = "https://lh3.googleusercontent.com/a/mock",
    aud: str = "381940932694-o2q57f2bhp8sjbt9r6fgm240q4jknmfa.apps.googleusercontent.com",
    iss: str = "https://accounts.google.com",
    exp_delta_seconds: int = 3600
) -> str:
    header = {"alg": "RS256", "typ": "JWT", "kid": "mock_google_kid"}
    now = int(datetime.now(timezone.utc).timestamp())
    payload = {
        "iss": iss,
        "sub": sub,
        "aud": aud,
        "email": email,
        "email_verified": True,
        "name": name,
        "picture": picture,
        "iat": now,
        "exp": now + exp_delta_seconds
    }
    
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    fake_sig = base64.urlsafe_b64encode(b"mock_google_signature_bytes_12345").decode().rstrip("=")
    return f"{header_b64}.{payload_b64}.{fake_sig}"

def generate_vapor_session_token(user_id: str, email: str, role: str = "member", workspace_id: str = "ws_test_01") -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "name": "Test User",
        "role": role,
        "workspace_id": workspace_id,
        "exp": int((now + timedelta(hours=24)).timestamp()),
        "iat": int(now.timestamp())
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def test_auth_me_without_session_returns_401():
    """Unauthenticated GET /api/v1/auth/me MUST return 401 without fabricating a user."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.get("/api/v1/auth/me")
            assert resp.status_code == 401
            data = resp.json()
            assert "detail" in data
    asyncio.run(_test())

def test_auth_me_with_valid_session_returns_200():
    """GET /api/v1/auth/me with valid session cookie/token returns 200 and authorized user info."""
    async def _test():
        transport = ASGITransport(app=app)
        user_id = "usr_live_test_user_01"
        ws_id = "ws_live_test_ws_01"
        
        identity_service._in_memory_identities[user_id] = {
            "id": user_id,
            "email": "alex.test@vapor.os",
            "name": "Alex Live Test",
            "avatar_url": "https://avatar.example.com/alex.png",
            "role": "member",
            "organization_id": "org_default_creator"
        }
        identity_service._in_memory_workspaces[ws_id] = {
            "id": ws_id,
            "name": "Alex's Studio",
            "organization_id": "org_default_creator"
        }
        identity_service._in_memory_workspace_memberships[f"{user_id}:{ws_id}"] = {
            "id": "mem_01",
            "user_id": user_id,
            "workspace_id": ws_id,
            "role": "owner",
            "status": "active"
        }

        token = generate_vapor_session_token(user_id, "alex.test@vapor.os", role="owner", workspace_id=ws_id)

        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            # Via Cookie
            client.cookies.set("vapor_session_token", token)
            resp = await client.get("/api/v1/auth/me")
            assert resp.status_code == 200
            data = resp.json()
            assert data["user_id"] == user_id
            assert data["email"] == "alex.test@vapor.os"
            assert data["workspace_id"] == ws_id
            assert data["authenticated"] is True
            assert len(data["workspaces"]) >= 1

            # Via Authorization Bearer Header
            resp2 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
            assert resp2.status_code == 200
            assert resp2.json()["user_id"] == user_id
    asyncio.run(_test())

def test_google_invalid_token_returns_401():
    """POST /api/v1/auth/google/verify with malformed or invalid token returns 401."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post("/api/v1/auth/google/verify", json={"credential": "invalid.malformed.token"})
            assert resp.status_code == 401
    asyncio.run(_test())

def test_google_wrong_audience_returns_401():
    """Google ID token with untrusted/foreign client ID audience is rejected with 401."""
    async def _test():
        token = generate_mock_google_id_token(aud="untrusted-attacker-app.apps.googleusercontent.com")
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post("/api/v1/auth/google/verify", json={"credential": token})
            assert resp.status_code == 401
            assert "audience" in resp.json()["detail"].lower()
    asyncio.run(_test())

def test_google_wrong_issuer_returns_401():
    """Google ID token with invalid issuer is rejected with 401."""
    async def _test():
        token = generate_mock_google_id_token(iss="https://evil-issuer.example.com")
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post("/api/v1/auth/google/verify", json={"credential": token})
            assert resp.status_code == 401
            assert "issuer" in resp.json()["detail"].lower()
    asyncio.run(_test())

def test_google_valid_identity_creates_session():
    """Valid Google ID token provisions user/workspace and issues HttpOnly session cookie."""
    async def _test():
        sub_id = "google_sub_unique_998877"
        email = "sarah.connor@cyberdyne.org"
        token = generate_mock_google_id_token(sub=sub_id, email=email, name="Sarah Connor")
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post("/api/v1/auth/google/verify", json={"credential": token})
            assert resp.status_code == 200
            data = resp.json()
            assert data["email"] == email
            assert data["name"] == "Sarah Connor"
            assert "vapor_session_token" in resp.cookies

            # Test session immediately against /auth/me
            session_cookie = resp.cookies.get("vapor_session_token")
            client.cookies.set("vapor_session_token", session_cookie)
            me_resp = await client.get("/api/v1/auth/me")
            assert me_resp.status_code == 200
            me_data = me_resp.json()
            assert me_data["email"] == email
            assert me_data["authenticated"] is True
    asyncio.run(_test())

def test_google_same_sub_does_not_duplicate_user():
    """Subsequent logins with the same Google sub maintain the same user identity and workspace."""
    async def _test():
        sub_id = "google_sub_idempotent_123"
        email = "john.reese@machine.ai"
        token1 = generate_mock_google_id_token(sub=sub_id, email=email, name="John Reese")
        token2 = generate_mock_google_id_token(sub=sub_id, email=email, name="John Reese Updated")

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp1 = await client.post("/api/v1/auth/google/verify", json={"credential": token1})
            assert resp1.status_code == 200
            user1_id = resp1.json()["user_id"]
            ws1_id = resp1.json()["workspace_id"]

            resp2 = await client.post("/api/v1/auth/google/verify", json={"credential": token2})
            assert resp2.status_code == 200
            user2_id = resp2.json()["user_id"]
            ws2_id = resp2.json()["workspace_id"]

            assert user1_id == user2_id, "Duplicate user created for the same Google subject!"
            assert ws1_id == ws2_id, "New workspace created instead of reusing existing workspace!"
    asyncio.run(_test())

def test_logout_revokes_session():
    """POST /api/v1/auth/logout clears session cookies."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            token = generate_vapor_session_token("usr_temp_01", "temp@vapor.os")
            client.cookies.set("vapor_session_token", token)

            logout_resp = await client.post("/api/v1/auth/logout")
            assert logout_resp.status_code == 200
            assert logout_resp.json()["status"] == "logged_out"
    asyncio.run(_test())

def test_spoofed_identity_headers_do_not_authenticate():
    """Headers such as X-User-Id / X-Workspace-Id alone without JWT never establish authentication."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            headers = {"X-User-Id": "usr_admin_01", "X-Workspace-Id": "ws_admin_01"}
            resp = await client.get("/api/v1/missions", headers=headers)
            assert resp.status_code == 401

            resp_me = await client.get("/api/v1/auth/me", headers=headers)
            assert resp_me.status_code == 401
    asyncio.run(_test())

def test_spoofed_workspace_header_does_not_change_tenant():
    """Supplying an unauthorized X-Workspace-Id header does not allow accessing another tenant."""
    async def _test():
        transport = ASGITransport(app=app)
        user_a = "usr_alice_victim_guard"
        ws_a = "ws_alice_private"
        identity_service._in_memory_workspace_memberships[f"{user_a}:{ws_a}"] = {
            "user_id": user_a,
            "workspace_id": ws_a,
            "role": "member",
            "status": "active"
        }
        token_a = generate_vapor_session_token(user_a, "alice@guard.org", role="member", workspace_id=ws_a)

        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.get("/api/v1/missions", headers={
                "Authorization": f"Bearer {token_a}",
                "X-Workspace-Id": "ws_target_other_tenant"
            })
            assert resp.status_code == 403
    asyncio.run(_test())

def test_telemetry_failure_does_not_break_authentication():
    """POST /api/v1/telemetry/web-vitals responds cleanly even with empty/malformed data."""
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post("/api/v1/telemetry/web-vitals", json={})
            assert resp.status_code == 202

            resp_str = await client.post(
                "/api/v1/telemetry/web-vitals",
                content="not a json",
                headers={"Content-Type": "text/plain"}
            )
            assert resp_str.status_code == 202
    asyncio.run(_test())

def test_attacker_origin_rejected():
    """State-changing mutations from attacker origins are rejected by CSRF middleware."""
    async def _test():
        transport = ASGITransport(app=app)
        token = generate_vapor_session_token("usr_origin_test", "test@origin.org")
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post(
                "/api/v1/missions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Origin": "https://attacker.evil.com"
                },
                json={"title": "CSRF Attack"}
            )
            assert resp.status_code == 403
    asyncio.run(_test())

def test_trusted_origin_allowed():
    """Requests with trusted CORS origins are processed normally."""
    async def _test():
        transport = ASGITransport(app=app)
        user_id = "usr_trusted_origin_user"
        ws_id = "ws_trusted_origin_ws"
        identity_service._in_memory_workspace_memberships[f"{user_id}:{ws_id}"] = {
            "user_id": user_id,
            "workspace_id": ws_id,
            "role": "owner",
            "status": "active"
        }
        token = generate_vapor_session_token(user_id, "trusted@test.com", role="owner", workspace_id=ws_id)
        
        async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as client:
            resp = await client.post(
                "/api/v1/missions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Origin": "http://localhost:3000"
                },
                json={"title": "Legitimate Mission", "description": "Mission created from localhost:3000"}
            )
            assert resp.status_code == 201
    asyncio.run(_test())
