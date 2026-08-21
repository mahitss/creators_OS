import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_test_alpha"
WS_B = "ws_test_beta"

def test_mission_lifecycle_and_workspace_isolation():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. List initially empty
    res = client.get("/api/v1/missions", headers=headers_a)
    assert res.status_code == 200
    assert res.json()["total"] == 0

    # 2. Create mission in Workspace A
    create_payload = {
        "title": "Prepare Docker Video Tutorial",
        "description": "Outline key topics: images, containers, volumes, docker-compose.",
        "priority": "high"
    }
    res = client.post("/api/v1/missions", json=create_payload, headers=headers_a)
    assert res.status_code == 201
    mission_a = res.json()
    assert mission_a["title"] == create_payload["title"]
    assert mission_a["status"] in ["DRAFT", "active"]
    assert mission_a["priority"].lower() == "high"
    mission_id = mission_a["id"]

    # 3. Cross-workspace isolation check: Workspace B cannot see or access Workspace A's mission
    res_b = client.get(f"/api/v1/missions/{mission_id}", headers=headers_b)
    assert res_b.status_code == 404

    res_b_list = client.get("/api/v1/missions", headers=headers_b)
    assert res_b_list.json()["total"] == 0

    # 4. Get Mission in Workspace A
    res = client.get(f"/api/v1/missions/{mission_id}", headers=headers_a)
    assert res.status_code == 200
    assert res.json()["id"] == mission_id
    assert len(res.json()["activities"]) > 0

    # 5. Update Mission
    update_payload = {"description": "Updated outline: added multi-stage build section."}
    res = client.patch(f"/api/v1/missions/{mission_id}", json=update_payload, headers=headers_a)
    assert res.status_code == 200
    assert res.json()["description"] == update_payload["description"]

    # 6. Complete Mission
    res = client.post(f"/api/v1/missions/{mission_id}/complete", headers=headers_a)
    assert res.status_code == 200
    assert res.json()["status"] in ["COMPLETED", "completed"]
    assert res.json()["completed_at"] is not None

    # 7. Search & Filter
    res_filtered = client.get("/api/v1/missions?status=completed&search=Docker", headers=headers_a)
    assert res_filtered.status_code == 200
    assert res_filtered.json()["total"] == 1

    # 8. Archive Mission
    res = client.post(f"/api/v1/missions/{mission_id}/archive", headers=headers_a)
    assert res.status_code == 200
    assert res.json()["status"] == "archived"

    res_active = client.get("/api/v1/missions?status=active", headers=headers_a)
    assert res_active.json()["total"] == 0
