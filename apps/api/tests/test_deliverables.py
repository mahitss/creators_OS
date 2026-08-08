import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_deliv_alpha"
WS_B = "ws_deliv_beta"

def test_full_deliverable_intelligence_lifecycle():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Create Mission
    m_res = client.post("/api/v1/missions", json={
        "title": "Research Competitor Docker Adoption",
        "description": "Deep analysis of developer container adoption.",
        "priority": "high"
    }, headers=headers_a)
    m_id = m_res.json()["id"]

    # 2. Insufficient Output Check: No steps executed yet -> No suggestions
    an1_res = client.post(f"/api/v1/missions/{m_id}/deliverable-suggestions/analyze", headers=headers_a)
    assert an1_res.status_code == 200
    assert an1_res.json() is None

    # 3. Create & Execute Steps
    client.post(f"/api/v1/missions/{m_id}/plan", headers=headers_a)
    steps_res = client.post(f"/api/v1/missions/{m_id}/steps", headers=headers_a)
    steps = steps_res.json()["steps"]
    step_1_id = steps[0]["id"]

    client.post(f"/api/v1/missions/{m_id}/start", headers=headers_a)
    # Complete Step 1
    client.post(f"/api/v1/mission-steps/{step_1_id}/complete", headers=headers_a)

    # 4. Trigger Analysis -> Generates Report Suggestion
    an2_res = client.post(f"/api/v1/missions/{m_id}/deliverable-suggestions/analyze", headers=headers_a)
    assert an2_res.status_code == 200
    sugg = an2_res.json()
    assert sugg is not None
    sugg_id = sugg["id"]
    assert sugg["type"] == "report"
    assert sugg["status"] == "pending"

    # 5. Duplicate Prevention Guard: Second analysis returns existing suggestion
    an3_res = client.post(f"/api/v1/missions/{m_id}/deliverable-suggestions/analyze", headers=headers_a)
    assert an3_res.status_code == 200
    assert an3_res.json()["id"] == sugg_id

    # 6. Cross-workspace Isolation: Workspace B cannot view or accept Workspace A's suggestion
    res_b = client.post(f"/api/v1/deliverable-suggestions/{sugg_id}/accept", headers=headers_b)
    assert res_b.status_code == 404

    # 7. Accept Suggestion -> Creates Draft Content Item
    acc_res = client.post(f"/api/v1/deliverable-suggestions/{sugg_id}/accept", headers=headers_a)
    assert acc_res.status_code == 200
    content_item = acc_res.json()
    assert content_item["type"] == "report"
    assert content_item["status"] == "draft"
    assert content_item["mission_id"] == m_id

    # 8. Dismiss Suggestion Test
    m2_res = client.post("/api/v1/missions", json={
        "title": "Create Video Script Tutorial",
        "description": "Video production.",
        "priority": "medium"
    }, headers=headers_a)
    m2_id = m2_res.json()["id"]
    client.post(f"/api/v1/missions/{m2_id}/plan", headers=headers_a)
    steps2_res = client.post(f"/api/v1/missions/{m2_id}/steps", headers=headers_a)
    step2_1_id = steps2_res.json()["steps"][0]["id"]
    client.post(f"/api/v1/missions/{m2_id}/start", headers=headers_a)
    client.post(f"/api/v1/mission-steps/{step2_1_id}/complete", headers=headers_a)

    an4_res = client.post(f"/api/v1/missions/{m2_id}/deliverable-suggestions/analyze", headers=headers_a)
    sugg2_id = an4_res.json()["id"]

    dism_res = client.post(f"/api/v1/deliverable-suggestions/{sugg2_id}/dismiss", headers=headers_a)
    assert dism_res.status_code == 200
    assert dism_res.json()["status"] == "dismissed"
