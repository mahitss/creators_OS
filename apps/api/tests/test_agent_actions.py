import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WS_A = "ws_act_alpha"
HEADERS_A = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}

def test_full_real_agent_actions_approval_gates_and_verification():
    # 1. Connect Google Integration for Calendar tool
    conn_res = client.post("/api/v1/integrations/google/connect", headers=HEADERS_A)
    state = conn_res.json()["state"]
    client.get(f"/api/v1/integrations/google/callback?code=mock_code&state={state}", headers=HEADERS_A)

    # 2. Create Mission
    m_res = client.post("/api/v1/missions", json={"title": "Proposal Action Mission", "description": "Execute proposal actions"}, headers=HEADERS_A)
    assert m_res.status_code == 201
    m_id = m_res.json()["id"]

    # 3. Create Agent Run
    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Schedule project review", "max_iterations": 20}, headers=HEADERS_A)
    assert run_res.status_code == 201
    run_id = run_res.json()["id"]

    # 4. Trigger External Action Tool requiring Approval Gate (create_calendar_event)
    import asyncio
    from app.services import agent_runtime
    run_app = asyncio.run(
        agent_runtime.step_agent_run(
            None, WS_A, run_id,
            requested_tool="create_calendar_event",
            tool_input={"title": "Client Review Meeting", "start_at": "2026-08-10T14:00:00Z", "end_at": "2026-08-10T15:00:00Z"}
        )
    )
    assert run_app["status"] == "waiting_for_approval"

    # Find Approval ID
    app_id = None
    for app in agent_runtime._in_memory_approvals.values():
        if app["agent_run_id"] == run_id:
            app_id = app["id"]
            break
    assert app_id is not None

    # 5. Approve Request
    app_res = client.post(f"/api/v1/agent-runs/{run_id}/approvals/{app_id}/approve", headers=HEADERS_A)
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "approved"

    # Double approval idempotency check
    app_res_dup = client.post(f"/api/v1/agent-runs/{run_id}/approvals/{app_id}/approve", headers=HEADERS_A)
    assert app_res_dup.status_code == 200

    # Verify Agent Run is completed
    run_final = client.get(f"/api/v1/agent-runs/{run_id}", headers=HEADERS_A).json()
    assert run_final["status"] == "completed"

def test_real_agent_action_rejection_flow():
    m_res = client.post("/api/v1/missions", json={"title": "Rejection Test Mission", "description": "Test rejection flow"}, headers=HEADERS_A)
    m_id = m_res.json()["id"]

    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Create draft content"}, headers=HEADERS_A)
    run_id = run_res.json()["id"]

    import asyncio
    from app.services import agent_runtime
    asyncio.run(
        agent_runtime.step_agent_run(
            None, WS_A, run_id,
            requested_tool="create_content",
            tool_input={"title": "Draft Proposal Document", "content": "Sample content"}
        )
    )

    app_id = None
    for app in agent_runtime._in_memory_approvals.values():
        if app["agent_run_id"] == run_id:
            app_id = app["id"]
            break

    # Reject Approval Request
    rej_res = client.post(f"/api/v1/agent-runs/{run_id}/approvals/{app_id}/reject", headers=HEADERS_A)
    assert rej_res.status_code == 200
    assert rej_res.json()["status"] == "rejected"

    run_final = client.get(f"/api/v1/agent-runs/{run_id}", headers=HEADERS_A).json()
    assert run_final["status"] == "cancelled"
