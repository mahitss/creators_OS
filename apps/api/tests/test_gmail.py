import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_gm_alpha"
WS_B = "ws_gm_beta"

def test_full_gmail_intelligence_triage_and_mission_creation():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Connect Google Integration
    conn_res = client.post("/api/v1/integrations/google/connect", headers=headers_a)
    state = conn_res.json()["state"]
    client.get(f"/api/v1/integrations/google/callback?code=mock_code&state={state}", headers=headers_a)

    # 2. Perform Read-Only Gmail Sync
    sync_res = client.post("/api/v1/gmail/sync", headers=headers_a)
    assert sync_res.status_code == 200
    sync_data = sync_res.json()
    assert sync_data["is_connected"] is True
    assert sync_data["thread_count"] >= 2

    # 3. List Threads with Filter (Needs Response)
    th_res = client.get("/api/v1/gmail/threads?filter=needs_response", headers=headers_a)
    assert th_res.status_code == 200
    threads = th_res.json()["threads"]
    assert len(threads) >= 1
    assert "Proposal" in threads[0]["subject"]

    # 4. Message Detail & AI Summarization
    msg_id = f"msg_01_{WS_A}"
    sum_res = client.post(f"/api/v1/gmail/messages/{msg_id}/summarize", headers=headers_a)
    assert sum_res.status_code == 200
    sum_data = sum_res.json()
    assert sum_data["classification"] == "needs_response"
    assert "Elena" in sum_data["summary"]

    # 5. Create Mission from Email Workflow
    cm_res = client.post(f"/api/v1/gmail/messages/{msg_id}/create-mission", headers=headers_a)
    assert cm_res.status_code == 200
    cm_data = cm_res.json()
    assert "Email Action:" in cm_data["title"]
    m_id = cm_data["mission_id"]

    # Verify Mission created in database
    get_m = client.get(f"/api/v1/missions/{m_id}", headers=headers_a)
    assert get_m.status_code == 200

    # 6. Cross-workspace Security Isolation Check
    th_b = client.get("/api/v1/gmail/threads", headers=headers_b)
    assert th_b.status_code == 200
    assert th_b.json()["total"] == 0
