import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_agent_alpha"
WS_B = "ws_agent_beta"
HEADERS_A = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
HEADERS_B = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

def test_full_agent_runtime_execution_loop_and_approval_gates():
    # 1. Create Mission
    m_res = client.post("/api/v1/missions", json={"title": "Proposal Research Mission", "description": "Gather proposal specs"}, headers=HEADERS_A)
    assert m_res.status_code == 201
    m_id = m_res.json()["id"]

    # 2. Create Agent Run
    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Research client proposal context", "max_iterations": 20}, headers=HEADERS_A)
    assert run_res.status_code == 201
    run_data = run_res.json()
    run_id = run_data["id"]
    assert run_data["status"] in ["completed", "running", "waiting_for_approval"]

    # 3. Retrieve Agent Steps Timeline
    steps_res = client.get(f"/api/v1/agent-runs/{run_id}/steps", headers=HEADERS_A)
    assert steps_res.status_code == 200
    steps = steps_res.json()
    assert len(steps) >= 1
    assert steps[0]["type"] in ["tool_call", "reasoning", "approval", "result", "completion"]

    # 4. Control Endpoints (Pause / Resume / Cancel)
    pause_res = client.post(f"/api/v1/agent-runs/{run_id}/pause", headers=HEADERS_A)
    assert pause_res.status_code == 200
    assert pause_res.json()["status"] == "paused"

    resume_res = client.post(f"/api/v1/agent-runs/{run_id}/resume", headers=HEADERS_A)
    assert resume_res.status_code == 200

    cancel_res = client.post(f"/api/v1/agent-runs/{run_id}/cancel", headers=HEADERS_A)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"

    # 5. Cross-workspace Isolation Check
    b_res = client.get(f"/api/v1/agent-runs/{run_id}", headers=HEADERS_B)
    assert b_res.status_code == 404
