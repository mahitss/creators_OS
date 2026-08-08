import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_integ_alpha"
WS_B = "ws_integ_beta"

def test_full_oauth_lifecycle_encryption_and_security():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Generate Connect URL for Google
    conn_res = client.post("/api/v1/integrations/google/connect", headers=headers_a)
    assert conn_res.status_code == 200
    conn_data = conn_res.json()
    assert "authorization_url" in conn_data
    state = conn_data["state"]

    # 2. Reject Invalid OAuth State Callback
    bad_cb = client.get(f"/api/v1/integrations/google/callback?code=mock_code&state=invalid_state", headers=headers_a)
    assert bad_cb.status_code == 400
    assert "Invalid or expired OAuth state" in bad_cb.json()["detail"]

    # 3. Successful OAuth Code Exchange Callback
    cb_res = client.get(f"/api/v1/integrations/google/callback?code=mock_code_123&state={state}", headers=headers_a)
    assert cb_res.status_code == 200
    data = cb_res.json()
    assert data["provider"] == "google"
    assert data["status"] == "connected"
    assert "encrypted_access_token" not in data # Zero token leakage in API responses
    assert "encrypted_refresh_token" not in data

    # 4. List Connections in Workspace A
    list_a = client.get("/api/v1/integrations", headers=headers_a)
    assert list_a.status_code == 200
    assert list_a.json()["total"] == 1

    # 5. Cross-workspace Security Isolation: Workspace B sees 0 connections
    list_b = client.get("/api/v1/integrations", headers=headers_b)
    assert list_b.status_code == 200
    assert list_b.json()["total"] == 0

    # 6. Disconnect Provider
    disc_res = client.post("/api/v1/integrations/google/disconnect", headers=headers_a)
    assert disc_res.status_code == 200
    assert disc_res.json()["status"] == "disconnected"
