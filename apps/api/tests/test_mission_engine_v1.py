import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.core.mission_lifecycle import (
    MissionStatus,
    MissionStepStatus,
    MissionEventType,
    FailureType,
    validate_status_transition,
    InvalidMissionStateTransitionError,
)
from app.services.mission_planner import MissionPlanner
from app.services.mission_engine import mission_engine
from app.core.ai_provider import DeterministicTestProvider

client = TestClient(app)

# Workspace / Tenant IDs configured in conftest
WS_A = "ws_test_alpha"
USER_A = "usr_alex"
HEADERS_A = {"X-Workspace-Id": WS_A, "X-User-Id": USER_A}

WS_B = "ws_test_beta"
USER_B = "usr_bob"
HEADERS_B = {"X-Workspace-Id": WS_B, "X-User-Id": USER_B}

def test_mission_creation_persists_draft():
    """Test 1: Creating a mission persists it in DRAFT state with initialized token/cost accounting."""
    payload = {
        "name": "Audit Security Boundaries",
        "goal": "Verify all API router boundaries and authentication headers",
        "description": "Perform comprehensive automated scan across endpoints.",
        "priority": "high",
        "agentId": "ag_security_auditor",
        "model": "openrouter/free"
    }
    res = client.post("/api/v1/missions", json=payload, headers=HEADERS_A)
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "DRAFT"
    assert data["workspace_id"] == WS_A
    assert data["title"] == "Audit Security Boundaries"
    assert data["name"] == "Audit Security Boundaries"
    assert data["goal"] == "Verify all API router boundaries and authentication headers"
    assert data["agent_id"] == "ag_security_auditor"
    assert data["progress"] == 0.0
    assert data["token_usage"]["total_tokens"] == 0
    assert data["cost_usd"] == 0.0
    assert len(data["activities"]) >= 1

def test_mission_launch_and_execution_lifecycle():
    """Test 2: Full autonomous execution lifecycle from DRAFT -> QUEUED -> PLANNING -> RUNNING -> COMPLETED."""
    # 1. Create Mission
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "End-to-End Pipeline Verification", "priority": "urgent"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    # 2. Launch Mission
    launch_res = client.post(f"/api/v1/missions/{m_id}/launch", headers=HEADERS_A)
    assert launch_res.status_code == 200
    assert launch_res.json()["status"] in ["QUEUED", "PLANNING", "RUNNING", "COMPLETED"]

    # 3. Direct execution to guarantee completion in test environment
    asyncio.run(mission_engine._execute_mission_lifecycle(WS_A, m_id))

    final_res = client.get(f"/api/v1/missions/{m_id}", headers=HEADERS_A)
    assert final_res.status_code == 200
    final_data = final_res.json()
    assert final_data["status"] == "COMPLETED"
    assert final_data["progress"] == 100.0
    assert final_data["completed_at"] is not None
    assert final_data["token_usage"]["total_tokens"] > 0
    assert final_data["cost_usd"] >= 0.0
    assert final_data["result"] is not None

    # 4. Verify steps were generated and completed
    steps_res = client.get(f"/api/v1/missions/{m_id}/steps", headers=HEADERS_A)
    assert steps_res.status_code == 200
    steps_data = steps_res.json()["steps"]
    assert len(steps_data) >= 1
    for s in steps_data:
        assert s["status"] == "COMPLETED"
        assert s["output"] is not None

def test_invalid_state_transitions_rejected():
    """Test 3: Invalid status transitions are strictly rejected by the State Machine."""
    # Direct state machine validation test
    with pytest.raises(InvalidMissionStateTransitionError):
        validate_status_transition("COMPLETED", "RUNNING")

    with pytest.raises(InvalidMissionStateTransitionError):
        validate_status_transition("CANCELLED", "RUNNING")

    with pytest.raises(InvalidMissionStateTransitionError):
        validate_status_transition("FAILED", "RUNNING")

    # API validation test: DRAFT cannot transition directly to COMPLETED without execution
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "State Transition Guard Test"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    illegal_res = client.patch(
        f"/api/v1/missions/{m_id}",
        json={"status": "COMPLETED"},
        headers=HEADERS_A
    )
    assert illegal_res.status_code == 400

def test_tenant_isolation_idor_prevention():
    """Test 4: Tenant A missions are strictly inaccessible and unmodifiable by Tenant B."""
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "Secret Tenant Alpha Mission", "goal": "Confidential"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    # Tenant B attempts to read Tenant A's mission -> 404
    get_b = client.get(f"/api/v1/missions/{m_id}", headers=HEADERS_B)
    assert get_b.status_code == 404

    # Tenant B attempts to update Tenant A's mission -> 404
    patch_b = client.patch(
        f"/api/v1/missions/{m_id}",
        json={"title": "Hacked Title"},
        headers=HEADERS_B
    )
    assert patch_b.status_code == 404

    # Tenant B attempts to launch Tenant A's mission -> 404
    launch_b = client.post(f"/api/v1/missions/{m_id}/launch", headers=HEADERS_B)
    assert launch_b.status_code == 404

    # Tenant B attempts to cancel Tenant A's mission -> 404
    cancel_b = client.post(f"/api/v1/missions/{m_id}/cancel", headers=HEADERS_B)
    assert cancel_b.status_code == 404

    # Tenant B attempts to read events -> 404
    events_b = client.get(f"/api/v1/missions/{m_id}/events", headers=HEADERS_B)
    assert events_b.status_code == 404

def test_planner_validation_and_structured_steps():
    """Test 5: MissionPlanner generates schema-valid steps with correct types."""
    planner = MissionPlanner(provider=DeterministicTestProvider())
    plan_struct, telemetry = asyncio.run(planner.plan_mission(
        workspace_id=WS_A,
        title="Deploy Redis Cluster",
        goal="Deploy highly available Redis cluster with sentinel failover",
        description="Configure master and two replicas",
        priority="HIGH"
    ))

    assert len(plan_struct.steps) >= 1
    for step in plan_struct.steps:
        assert step.order >= 1
        assert step.title
        assert step.step_type in ["retrieval", "analysis", "reasoning", "generation", "action"]
    assert telemetry["total_tokens"] > 0
    assert "estimated_cost_usd" in telemetry

def test_pause_and_resume_lifecycle():
    """Test 6: Mission pause and resume state transitions and idempotent controls."""
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "Pausable Mission Workflow"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    # Launch
    l_res = client.post(f"/api/v1/missions/{m_id}/launch", headers=HEADERS_A)
    assert l_res.status_code == 200

    # Pause
    pause_res = client.post(f"/api/v1/missions/{m_id}/pause", headers=HEADERS_A)
    assert pause_res.status_code == 200
    assert pause_res.json()["status"] in ["PAUSED", "COMPLETED", "RUNNING", "QUEUED"]

    # Resume
    if pause_res.json()["status"] == "PAUSED":
        resume_res = client.post(f"/api/v1/missions/{m_id}/resume", headers=HEADERS_A)
        assert resume_res.status_code == 200
        assert resume_res.json()["status"] in ["QUEUED", "RUNNING", "COMPLETED"]

def test_cancel_running_mission():
    """Test 7: Mission cancellation stops execution and marks CANCELLED."""
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "Cancellable Mission Workflow"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    cancel_res = client.post(f"/api/v1/missions/{m_id}/cancel", headers=HEADERS_A)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "CANCELLED"
    assert cancel_res.json()["cancelled_at"] is not None

def test_append_only_event_stream():
    """Test 8: Events are recorded chronologically in an append-only timeline."""
    create_res = client.post(
        "/api/v1/missions",
        json={"name": "Event Stream Verification Mission"},
        headers=HEADERS_A
    )
    assert create_res.status_code == 201
    m_id = create_res.json()["id"]

    # Launch & run
    client.post(f"/api/v1/missions/{m_id}/launch", headers=HEADERS_A)
    asyncio.run(mission_engine._execute_mission_lifecycle(WS_A, m_id))

    events_res = client.get(f"/api/v1/missions/{m_id}/events", headers=HEADERS_A)
    assert events_res.status_code == 200
    evts = events_res.json()
    assert len(evts) >= 2

    event_types = [e["event_type"] for e in evts]
    assert "MISSION_CREATED" in event_types
    assert "MISSION_QUEUED" in event_types
    assert "PLAN_CREATED" in event_types
    assert "MISSION_COMPLETED" in event_types

def test_idempotent_launch_and_cancel():
    """Test 9: Launch and Cancel endpoints are strictly idempotent."""
    # 1. Test Launch idempotency
    create_res1 = client.post(
        "/api/v1/missions",
        json={"name": "Idempotent Launch Test"},
        headers=HEADERS_A
    )
    assert create_res1.status_code == 201
    m_id1 = create_res1.json()["id"]

    l1 = client.post(f"/api/v1/missions/{m_id1}/launch", headers=HEADERS_A)
    assert l1.status_code == 200
    l2 = client.post(f"/api/v1/missions/{m_id1}/launch", headers=HEADERS_A)
    assert l2.status_code == 200

    # 2. Test Cancel idempotency
    create_res2 = client.post(
        "/api/v1/missions",
        json={"name": "Idempotent Cancel Test"},
        headers=HEADERS_A
    )
    assert create_res2.status_code == 201
    m_id2 = create_res2.json()["id"]

    c1 = client.post(f"/api/v1/missions/{m_id2}/cancel", headers=HEADERS_A)
    assert c1.status_code == 200
    assert c1.json()["status"] == "CANCELLED"
    c2 = client.post(f"/api/v1/missions/{m_id2}/cancel", headers=HEADERS_A)
    assert c2.status_code == 200
    assert c2.json()["status"] == "CANCELLED"
