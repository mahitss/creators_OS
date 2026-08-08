import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import agent_runtime, agent_recovery

client = TestClient(app)

WS_A = "ws_rec_alpha"
HEADERS_A = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}

def test_agent_checkpointing_and_worker_lease_recovery():
    # 1. Create Mission & Agent Run
    m_res = client.post("/api/v1/missions", json={"title": "Recovery Test Mission", "description": "Survive worker crash"}, headers=HEADERS_A)
    assert m_res.status_code == 201
    m_id = m_res.json()["id"]

    run_res = client.post(f"/api/v1/missions/{m_id}/agent-runs", json={"goal": "Survive crashes and resume"}, headers=HEADERS_A)
    assert run_res.status_code == 201
    run_id = run_res.json()["id"]

    # 2. Check Checkpoints Endpoint
    cp_res = client.get(f"/api/v1/agent-runs/{run_id}/checkpoints", headers=HEADERS_A)
    assert cp_res.status_code == 200
    checkpoints = cp_res.json()
    assert len(checkpoints) >= 1
    assert "budget_state" in checkpoints[0]["state"]

    # 3. Simulate Worker Crash & Lease Expiration
    run_dict = asyncio.run(agent_runtime.get_agent_run(None, WS_A, run_id))
    assert run_dict is not None

    # Force lease expiration
    run_dict["lease_expires_at"] = "2020-01-01T00:00:00+00:00"

    # Claim lease with Recovery Worker "worker_02"
    claimed = asyncio.run(agent_recovery.claim_run_lease(run_dict, worker_id="worker_02"))
    assert claimed is True
    assert run_dict["lease_worker_id"] == "worker_02"
    assert run_dict["version"] >= 2

    # 4. Tool Execution Recovery Resolution
    texec = asyncio.run(agent_recovery.record_tool_execution(run_id, "step_1", "create_calendar_event", "idemp_100", "hash_abc", status="unknown"))
    assert texec["status"] == "unknown"

    resolved = asyncio.run(agent_recovery.resolve_unknown_tool_execution(texec["id"], {"verified": True}))
    assert resolved["status"] == "completed"
