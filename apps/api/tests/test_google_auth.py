import time
import json
import base64
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

def make_test_google_id_token(
    sub: str = "google_sub_1092837465",
    email: str = "alex.creator@example.com",
    name: str = "Alex Creator",
    iss: str = "https://accounts.google.com",
    expired: bool = False
) -> str:
    header = {"alg": "RS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": iss,
        "sub": sub,
        "email": email,
        "name": name,
        "picture": "https://lh3.googleusercontent.com/a/avatar.jpg",
        "email_verified": True,
        "iat": now - 100,
        "exp": (now - 10) if expired else (now + 3600)
    }
    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"{h_b64}.{p_b64}.mock_signature_bytes"

def test_google_auth_success_and_provisioning():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            id_token = make_test_google_id_token(
                sub="google_sub_user_alpha",
                email="alpha@vapor.os",
                name="Alpha User"
            )
            res = await client.post("/api/v1/auth/google/verify", json={"id_token": id_token})
            assert res.status_code == 200
            data = res.json()
            assert "access_token" in data
            assert data["email"] == "alpha@vapor.os"
            assert data["name"] == "Alpha User"
            assert data["user_id"].startswith("usr_")
            assert data["workspace_id"].startswith("ws_")
            assert data["role"] == "owner"

            # Check session cookie
            assert "vapor_session_token" in res.cookies

            # Verify session with /auth/me using bearer token
            token = data["access_token"]
            me_res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
            assert me_res.status_code == 200
            me_data = me_res.json()
            assert me_data["user_id"] == data["user_id"]
            assert me_data["email"] == "alpha@vapor.os"
            assert len(me_data["workspaces"]) >= 1
    asyncio.run(_test())

def test_google_auth_existing_user_idempotence():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            id_token = make_test_google_id_token(
                sub="google_sub_user_idempotent",
                email="idempotent@vapor.os",
                name="Idempotent User"
            )
            # First login
            res1 = await client.post("/api/v1/auth/google/verify", json={"id_token": id_token})
            assert res1.status_code == 200
            user1 = res1.json()

            # Second login with same Google sub
            res2 = await client.post("/api/v1/auth/google/verify", json={"id_token": id_token})
            assert res2.status_code == 200
            user2 = res2.json()

            # Must resolve to exact same user ID and workspace ID
            assert user1["user_id"] == user2["user_id"]
            assert user1["workspace_id"] == user2["workspace_id"]
    asyncio.run(_test())

def test_google_auth_expired_token_rejected():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            expired_token = make_test_google_id_token(
                sub="google_sub_expired",
                email="expired@vapor.os",
                expired=True
            )
            res = await client.post("/api/v1/auth/google/verify", json={"id_token": expired_token})
            assert res.status_code == 401
            assert "expired" in res.json()["detail"].lower()
    asyncio.run(_test())

def test_google_auth_invalid_issuer_rejected():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            untrusted_token = make_test_google_id_token(
                sub="google_sub_fake",
                email="fake@attacker.com",
                iss="https://malicious-issuer.com"
            )
            res = await client.post("/api/v1/auth/google/verify", json={"id_token": untrusted_token})
            assert res.status_code == 401
            assert "untrusted" in res.json()["detail"].lower()
    asyncio.run(_test())

def test_logout_endpoint():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.post("/api/v1/auth/logout")
            assert res.status_code == 200
            assert res.json()["status"] == "logged_out"
    asyncio.run(_test())

def test_workspace_isolation_and_cross_tenant_denial():
    async def _test():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create User A
            token_a = make_test_google_id_token(sub="sub_user_tenant_a", email="user_a@corp.com")
            res_a = await client.post("/api/v1/auth/google/verify", json={"id_token": token_a})
            data_a = res_a.json()
            jwt_a = data_a["access_token"]
            ws_a = data_a["workspace_id"]

            # Create User B
            token_b = make_test_google_id_token(sub="sub_user_tenant_b", email="user_b@corp.com")
            res_b = await client.post("/api/v1/auth/google/verify", json={"id_token": token_b})
            data_b = res_b.json()
            jwt_b = data_b["access_token"]
            ws_b = data_b["workspace_id"]

            # User A attempting to select/access User B's workspace -> MUST BE 403 Forbidden
            select_res = await client.post(
                "/api/v1/auth/workspaces/select",
                headers={"Authorization": f"Bearer {jwt_a}"},
                json={"workspace_id": ws_b}
            )
            assert select_res.status_code == 403
            assert "access denied" in select_res.json()["detail"].lower()
    asyncio.run(_test())
