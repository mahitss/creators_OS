import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.agent_control_service import redact_sensitive_content

import time
import uuid
from app.api.routers.auth import _create_jwt_token

client = TestClient(app)
_now = int(time.time())
_admin_token = _create_jwt_token({
    "sub": "usr_admin_01",
    "email": "admin@vapor.internal",
    "role": "admin",
    "workspace_id": "ws_admin_ctrl",
    "iat": _now,
    "exp": _now + 3600,
    "jti": str(uuid.uuid4())
})
ADMIN_HEADERS = {
    "Authorization": f"Bearer {_admin_token}",
    "X-Workspace-Id": "ws_admin_ctrl"
}

def test_sensitive_content_redaction():
    raw = {
        "token": "ya29.a0AfH6SMD_secret_oauth_token",
        "authorization": "Bearer sk-1234567890abcdef1234567890abcdef",
        "user_email": "alex@vapor.internal",
        "safe_field": "Standard public telemetry"
    }
    redacted = redact_sensitive_content(raw)
    assert redacted["token"] == "[REDACTED_SECRET]"
    assert redacted["authorization"] == "[REDACTED_SECRET]"
    assert redacted["safe_field"] == "Standard public telemetry"

def test_admin_control_overview_endpoint():
    res = client.get("/api/v1/admin/agents/overview", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert "active_agents" in data
    assert "waiting_approvals" in data
    assert "stuck_agents" in data
    assert "total_tokens" in data
    assert "total_estimated_cost" in data

def test_admin_list_agents_and_stuck_detection():
    # 1. List active agents
    res = client.get("/api/v1/admin/agents", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # 2. Get stuck agents
    stuck_res = client.get("/api/v1/admin/agents/stuck", headers=ADMIN_HEADERS)
    assert stuck_res.status_code == 200
    assert isinstance(stuck_res.json(), list)

def test_provider_health_and_tool_metrics():
    # 1. Provider health
    prov_res = client.get("/api/v1/admin/agents/providers", headers=ADMIN_HEADERS)
    assert prov_res.status_code == 200
    pdata = prov_res.json()
    assert pdata["ai_providers"]["status"] == "healthy"
    assert pdata["database"]["status"] == "healthy"

    # 2. Tool metrics
    tool_res = client.get("/api/v1/admin/agents/metrics", headers=ADMIN_HEADERS)
    assert tool_res.status_code == 200
    tdata = tool_res.json()
    assert len(tdata) > 0

def test_operator_control_action_and_audit_logging():
    # 1. Create Mission & Agent Run in isolated workspace ws_admin_ctrl
    m_res = client.post("/api/v1/missions", json={"title": "Audit Test Mission", "description": "Testing operator actions"}, headers=ADMIN_HEADERS)
    m_id = m_res.json()["id"]

    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Audit Agent Goal"}, headers=ADMIN_HEADERS)
    run_id = run_res.json()["id"]

    # 2. Pause Agent Action
    action_res = client.post(f"/api/v1/admin/agents/{run_id}/action", json={"action": "pause", "reason": "Operator maintenance pause"}, headers=ADMIN_HEADERS)
    assert action_res.status_code == 200
    adata = action_res.json()
    assert adata["success"] is True
    assert adata["new_status"] == "paused"
    assert adata["audit_log"]["action"] == "pause"

    # 3. Resume Agent Action
    resume_res = client.post(f"/api/v1/admin/agents/{run_id}/action", json={"action": "resume", "reason": "Operator resume"}, headers=ADMIN_HEADERS)
    assert resume_res.status_code == 200
    assert resume_res.json()["new_status"] == "running"
