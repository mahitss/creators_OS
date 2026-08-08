import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_content_alpha"
WS_B = "ws_content_beta"

def test_full_content_lifecycle_and_ai_generation():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Create Mission in Workspace A
    m_res = client.post("/api/v1/missions", json={
        "title": "Prepare Docker Video Script",
        "description": "Video production mission.",
        "priority": "high"
    }, headers=headers_a)
    m_id = m_res.json()["id"]

    # 2. Create Content Linked to Mission
    create_res = client.post("/api/v1/content", json={
        "title": "Docker Beginner Tutorial Script",
        "type": "script",
        "content": "# Intro\nWelcome to Docker tutorial.",
        "mission_id": m_id
    }, headers=headers_a)
    assert create_res.status_code == 201
    cnt = create_res.json()
    cnt_id = cnt["id"]
    assert cnt["type"] == "script"
    assert cnt["status"] == "draft"
    assert cnt["mission_id"] == m_id

    # 3. Cross-workspace Security Check: Workspace B cannot access Workspace A's content
    res_b = client.get(f"/api/v1/content/{cnt_id}", headers=headers_b)
    assert res_b.status_code == 404

    # 4. List & Filter Content
    list_res = client.get("/api/v1/content?type=script&search=Docker", headers=headers_a)
    assert list_res.status_code == 200
    assert list_res.json()["total"] == 1

    # 5. AI Generation (Draft intent)
    gen_res = client.post(f"/api/v1/content/{cnt_id}/generate", json={
        "intent": "draft",
        "custom_prompt": "Focus on practical CLI commands."
    }, headers=headers_a)
    assert gen_res.status_code == 200
    updated_cnt = gen_res.json()
    assert "Docker" in updated_cnt["content"]

    # 6. Update Content manually
    upd_res = client.patch(f"/api/v1/content/{cnt_id}", json={
        "title": "Final Docker Beginner Script",
        "content": "# Final Script\nRevised text."
    }, headers=headers_a)
    assert upd_res.status_code == 200

    # 7. Approve Content
    appr_res = client.post(f"/api/v1/content/{cnt_id}/approve", headers=headers_a)
    assert appr_res.status_code == 200
    assert appr_res.json()["status"] == "approved"

    # 8. Archive Content
    arch_res = client.post(f"/api/v1/content/{cnt_id}/archive", headers=headers_a)
    assert arch_res.status_code == 200
    assert arch_res.json()["status"] == "archived"
