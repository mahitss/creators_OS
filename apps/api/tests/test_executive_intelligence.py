import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_intel_alpha"
WS_B = "ws_intel_beta"

def test_executive_intelligence_brief_rules():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Initially Empty / Quiet Workspace
    res1 = client.get("/api/v1/home/brief?user_name=Alex", headers=headers_a)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["is_quiet_state"] is True
    assert len(data1["needs_attention"]) == 0
    assert data1["primary_recommendation"] is None

    # 2. Create Mission & Plan & Steps
    m_res = client.post("/api/v1/missions", json={
        "title": "Deploy Production K8s Cluster",
        "description": "Configure terraform and helm charts.",
        "priority": "urgent"
    }, headers=headers_a)
    m_id = m_res.json()["id"]

    client.post(f"/api/v1/missions/{m_id}/plan", headers=headers_a)
    client.post(f"/api/v1/missions/{m_id}/steps", headers=headers_a)
    client.post(f"/api/v1/missions/{m_id}/start", headers=headers_a)

    # 3. Pause Execution
    client.post(f"/api/v1/missions/{m_id}/pause", headers=headers_a)

    # 4. Verify Executive Intelligence surfaces Paused Attention & Recommendation
    res2 = client.get("/api/v1/home/brief?user_name=Alex", headers=headers_a)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["is_quiet_state"] is False
    assert len(data2["needs_attention"]) > 0
    assert "Execution Paused" in data2["needs_attention"][0]["title"]
    assert data2["primary_recommendation"] is not None
    assert "Execution Paused" in data2["primary_recommendation"]["title"]
    assert "Resume" in data2["primary_recommendation"]["action_label"]

    # 5. Cross-workspace Isolation: Workspace B should remain Quiet
    res_b = client.get("/api/v1/home/brief?user_name=Bob", headers=headers_b)
    assert res_b.status_code == 200
    assert res_b.json()["is_quiet_state"] is True
