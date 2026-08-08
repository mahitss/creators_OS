import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_exec_alpha"
WS_B = "ws_exec_beta"

def test_full_mission_execution_engine_flow():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Create Mission
    m_res = client.post("/api/v1/missions", json={
        "title": "Setup Production Monitoring Dashboard",
        "description": "Configure Prometheus metrics and Grafana alerts.",
        "priority": "urgent"
    }, headers=headers_a)
    assert m_res.status_code == 201
    mission_id = m_res.json()["id"]

    # 2. Generate Plan
    plan_res = client.post(f"/api/v1/missions/{mission_id}/plan", headers=headers_a)
    assert plan_res.status_code == 200

    # 3. Convert Plan to Executable Steps
    conv_res = client.post(f"/api/v1/missions/{mission_id}/steps", headers=headers_a)
    assert conv_res.status_code == 200
    data = conv_res.json()
    assert data["execution"]["status"] == "idle"
    assert len(data["steps"]) == 3
    assert data["steps"][0]["status"] == "ready"
    assert data["steps"][1]["status"] == "pending"

    # 4. Cross-workspace isolation check
    res_b = client.get(f"/api/v1/missions/{mission_id}/steps", headers=headers_b)
    assert res_b.json()["execution"] is None

    # 5. Start Execution
    start_res = client.post(f"/api/v1/missions/{mission_id}/start", headers=headers_a)
    assert start_res.status_code == 200
    start_data = start_res.json()
    assert start_data["execution"]["status"] == "running"
    assert start_data["steps"][0]["status"] == "in_progress"

    # 6. Complete Step 1
    step1_id = start_data["steps"][0]["id"]
    step1_res = client.post(f"/api/v1/mission-steps/{step1_id}/complete", headers=headers_a)
    assert step1_res.status_code == 200
    step1_data = step1_res.json()
    assert step1_data["execution"]["completed_steps_count"] == 1
    assert step1_data["steps"][0]["status"] == "completed"
    assert step1_data["steps"][1]["status"] == "in_progress" # Next step unlocked & started!

    # 7. Pause & Resume Execution
    pause_res = client.post(f"/api/v1/missions/{mission_id}/pause", headers=headers_a)
    assert pause_res.status_code == 200
    assert pause_res.json()["execution"]["status"] == "paused"

    resume_res = client.post(f"/api/v1/missions/{mission_id}/start", headers=headers_a)
    assert resume_res.status_code == 200
    assert resume_res.json()["execution"]["status"] == "running"

    # 8. Complete Step 2 & Step 3
    step2_id = start_data["steps"][1]["id"]
    step3_id = start_data["steps"][2]["id"]

    client.post(f"/api/v1/mission-steps/{step2_id}/complete", headers=headers_a)
    final_res = client.post(f"/api/v1/mission-steps/{step3_id}/complete", headers=headers_a)
    assert final_res.status_code == 200
    final_data = final_res.json()

    assert final_data["execution"]["status"] == "completed"
    assert final_data["execution"]["completed_steps_count"] == 3

    # 9. Verify Mission status updated to completed
    m_final = client.get(f"/api/v1/missions/{mission_id}", headers=headers_a).json()
    assert m_final["status"] == "completed"
