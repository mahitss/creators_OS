import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_mem_alpha"
WS_B = "ws_mem_beta"

def test_full_memory_lifecycle_and_candidate_approval():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Create Memory in Workspace A
    create_res = client.post("/api/v1/memories", json={
        "type": "preference",
        "title": "User Docker Explanation Preference",
        "content": "User prefers beginner-friendly Docker explanations with practical code examples.",
        "importance": "high"
    }, headers=headers_a)
    assert create_res.status_code == 201
    mem = create_res.json()
    mem_id = mem["id"]
    assert mem["type"] == "preference"
    assert mem["importance"] == "high"

    # 2. Cross-workspace security check: Workspace B cannot access Workspace A's memory
    res_b = client.get(f"/api/v1/memories/{mem_id}", headers=headers_b)
    assert res_b.status_code == 404

    # 3. List & Filter Memories
    list_res = client.get("/api/v1/memories?type=preference&search=Docker", headers=headers_a)
    assert list_res.status_code == 200
    assert list_res.json()["total"] == 1

    # 4. Update Memory
    upd_res = client.patch(f"/api/v1/memories/{mem_id}", json={
        "title": "Updated Docker Preference",
        "importance": "critical"
    }, headers=headers_a)
    assert upd_res.status_code == 200
    assert upd_res.json()["importance"] == "critical"

    # 5. Archive & Restore
    arch_res = client.post(f"/api/v1/memories/{mem_id}/archive", headers=headers_a)
    assert arch_res.status_code == 200
    assert arch_res.json()["is_archived"] is True

    rest_res = client.post(f"/api/v1/memories/{mem_id}/restore", headers=headers_a)
    assert rest_res.status_code == 200
    assert rest_res.json()["is_archived"] is False

    # 6. Test Candidate Extraction on Mission Completion
    m_res = client.post("/api/v1/missions", json={
        "title": "Build Docker Microservice",
        "description": "Deploy containerized FastAPI service.",
        "priority": "medium"
    }, headers=headers_a)
    m_id = m_res.json()["id"]

    client.post(f"/api/v1/missions/{m_id}/complete", headers=headers_a)

    # 7. Verify Candidate Memory Created
    cand_res = client.get("/api/v1/memory-candidates", headers=headers_a)
    assert cand_res.status_code == 200
    candidates = cand_res.json()["candidates"]
    assert len(candidates) > 0
    cand_id = candidates[0]["id"]

    # 8. Approve Candidate Memory -> Converts to Permanent Memory
    appr_res = client.post(f"/api/v1/memory-candidates/{cand_id}/approve", headers=headers_a)
    assert appr_res.status_code == 200
    approved_mem = appr_res.json()
    assert approved_mem["source_type"] == "mission"

    # 9. Verify Context Memory Enriched in Mission Planning
    m2_res = client.post("/api/v1/missions", json={
        "title": "Create Docker Tutorial",
        "description": "Tutorial for Docker beginners.",
        "priority": "high"
    }, headers=headers_a)
    m2_id = m2_res.json()["id"]

    plan_res = client.post(f"/api/v1/missions/{m2_id}/plan", headers=headers_a)
    assert plan_res.status_code == 200

    # 10. Delete Memory
    del_res = client.delete(f"/api/v1/memories/{mem_id}", headers=headers_a)
    assert del_res.status_code == 204
