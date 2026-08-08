import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_drv_alpha"
WS_B = "ws_drv_beta"

def test_full_google_drive_intelligence_sync_and_extraction():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Connect Google Integration
    conn_res = client.post("/api/v1/integrations/google/connect", headers=headers_a)
    state = conn_res.json()["state"]
    client.get(f"/api/v1/integrations/google/callback?code=mock_code&state={state}", headers=headers_a)

    # 2. Perform Read-Only Drive Metadata Sync
    sync_res = client.post("/api/v1/drive/sync", headers=headers_a)
    assert sync_res.status_code == 200
    sync_data = sync_res.json()
    assert sync_data["is_connected"] is True
    assert sync_data["file_count"] >= 2

    # 3. Search Drive Files Metadata
    f_res = client.get("/api/v1/drive/files?q=Proposal", headers=headers_a)
    assert f_res.status_code == 200
    files = f_res.json()["files"]
    assert len(files) >= 1
    file_id = files[0]["id"]
    assert "Proposal" in files[0]["name"]

    # 4. Extract Document Content (On-Demand & Bounded)
    cnt_res = client.get(f"/api/v1/drive/files/{file_id}/content", headers=headers_a)
    assert cnt_res.status_code == 200
    cnt_data = cnt_res.json()
    assert "Executive Summary" in cnt_data["text"]
    assert cnt_data["truncated"] is False

    # 5. Create Mission and Attach Document Reference
    m_payload = {"title": "Client Proposal Mission", "description": "Prepare client proposal", "priority": "high"}
    m_res = client.post("/api/v1/missions", json=m_payload, headers=headers_a)
    assert m_res.status_code == 201
    m_id = m_res.json()["id"]

    att_res = client.post(f"/api/v1/missions/{m_id}/documents/{file_id}", headers=headers_a)
    assert att_res.status_code == 200
    att_data = att_res.json()
    assert att_data["drive_file_id"] == file_id

    # 6. List Mission Documents with Citations
    docs_res = client.get(f"/api/v1/missions/{m_id}/documents", headers=headers_a)
    assert docs_res.status_code == 200
    docs = docs_res.json()
    assert len(docs) == 1
    assert "web_url" in docs[0]

    # 7. Cross-workspace Isolation Check
    files_b = client.get("/api/v1/drive/files", headers=headers_b)
    assert files_b.status_code == 200
    assert files_b.json()["total"] == 0
