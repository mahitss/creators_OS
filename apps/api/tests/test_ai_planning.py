import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_plan_alpha"
WS_B = "ws_plan_beta"

def test_executive_ai_mission_planning_flow():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Create Mission in Workspace A
    res = client.post("/api/v1/missions", json={
        "title": "Build SaaS Competitor Analysis Report",
        "description": "Analyze key market competitors, pricing models, and feature gaps.",
        "priority": "high"
    }, headers=headers_a)
    assert res.status_code == 201
    mission_id = res.json()["id"]

    # 2. Plan with Vapor (v1)
    plan_res = client.post(f"/api/v1/missions/{mission_id}/plan", headers=headers_a)
    assert plan_res.status_code == 200
    plan_v1 = plan_res.json()
    assert plan_v1["mission_id"] == mission_id
    assert plan_v1["version"] == 1
    assert "goal" in plan_v1
    assert "summary" in plan_v1
    assert len(plan_v1["steps"]) > 0
    assert len(plan_v1["deliverables"]) > 0
    assert len(plan_v1["open_questions"]) > 0
    assert len(plan_v1["recommendations"]) > 0

    # 3. Cross-Workspace isolation check on Plan
    res_b = client.get(f"/api/v1/missions/{mission_id}/plan", headers=headers_b)
    assert res_b.status_code == 404

    # 4. Fetch Mission Plan (v1)
    get_plan = client.get(f"/api/v1/missions/{mission_id}/plan", headers=headers_a)
    assert get_plan.status_code == 200
    assert get_plan.json()["version"] == 1

    # 5. Regenerate Mission Plan (v2)
    regen_res = client.post(f"/api/v1/missions/{mission_id}/plan/regenerate", headers=headers_a)
    assert regen_res.status_code == 200
    plan_v2 = regen_res.json()
    assert plan_v2["version"] == 2

    # 6. Verify Mission Activity Timeline includes PLAN_GENERATED & PLAN_REGENERATED
    m_detail = client.get(f"/api/v1/missions/{mission_id}", headers=headers_a).json()
    actions = [act["action"] for act in m_detail["activities"]]
    assert "PLAN_GENERATED" in actions
    assert "PLAN_REGENERATED" in actions
