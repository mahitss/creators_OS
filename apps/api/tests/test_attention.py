import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_att_alpha"
WS_B = "ws_att_beta"

def test_full_attention_lifecycle_and_reconciliation():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Initially Clear Workspace -> Open Count 0
    cnt1 = client.get("/api/v1/attention/count", headers=headers_a)
    assert cnt1.status_code == 200
    assert cnt1.json()["open_count"] == 0

    # 2. Create Mission & Pause Execution -> Generates Paused Attention Item
    m_res = client.post("/api/v1/missions", json={
        "title": "Deploy AWS Infrastructure",
        "description": "Terraform execution.",
        "priority": "urgent"
    }, headers=headers_a)
    m_id = m_res.json()["id"]
    client.post(f"/api/v1/missions/{m_id}/plan", headers=headers_a)
    client.post(f"/api/v1/missions/{m_id}/steps", headers=headers_a)
    client.post(f"/api/v1/missions/{m_id}/start", headers=headers_a)
    client.post(f"/api/v1/missions/{m_id}/pause", headers=headers_a)

    # 3. Check Attention List & Count
    list1 = client.get("/api/v1/attention", headers=headers_a)
    assert list1.status_code == 200
    data1 = list1.json()
    assert data1["open_count"] == 1
    att_item = data1["items"][0]
    att_id = att_item["id"]
    assert "Execution Paused" in att_item["title"]

    # 4. Idempotency Check: Reconcile does not create duplicate item
    rec_res = client.post("/api/v1/attention/reconcile", headers=headers_a)
    assert rec_res.status_code == 200
    assert rec_res.json()["open_count"] == 1

    # 5. Cross-workspace Isolation: Workspace B cannot see Workspace A's attention item
    list_b = client.get("/api/v1/attention", headers=headers_b)
    assert list_b.status_code == 200
    assert list_b.json()["open_count"] == 0

    # 6. Snooze Attention Item
    snz_res = client.post(f"/api/v1/attention/{att_id}/snooze?minutes=60", headers=headers_a)
    assert snz_res.status_code == 200
    assert snz_res.json()["status"] == "snoozed"

    # Count decreases when item is snoozed
    cnt2 = client.get("/api/v1/attention/count", headers=headers_a)
    assert cnt2.json()["open_count"] == 0

    # 7. Resolve Attention Item
    res_res = client.post(f"/api/v1/attention/{att_id}/resolve", headers=headers_a)
    assert res_res.status_code == 200
    assert res_res.json()["status"] == "resolved"
