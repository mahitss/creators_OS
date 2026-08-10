import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.automations import (
    SystemEventCreate,
    AgentTriggerCreate,
    AgentTriggerUpdate,
    DryRunTestRequest
)
from app.services import proactive_service, policy_engine

client = TestClient(app)

def test_event_ingestion_and_deduplication():
    async def _test():
        ev_data = SystemEventCreate(
            workspace_id="ws_test_events",
            source="calendar",
            event_type="calendar.event_updated",
            resource_type="calendar_event",
            resource_id="evt_1001",
            metadata_dict={"is_deadline_change": True, "summary": "Delivery moved to Monday."}
        )
        event, is_dup = await proactive_service.ingest_event(None, ev_data)
        assert event["workspace_id"] == "ws_test_events"
        assert event["source"] == "calendar"
        assert is_dup is False

        event_dup, is_dup2 = await proactive_service.ingest_event(None, ev_data)
        assert is_dup2 is True
        assert event_dup["status"] == "ignored"

    asyncio.run(_test())

def test_signal_extraction_and_truthful_insight():
    async def _test():
        ev_data = SystemEventCreate(
            workspace_id="ws_test_events",
            source="calendar",
            event_type="calendar.event_updated",
            resource_type="calendar_event",
            resource_id="evt_1002",
            metadata_dict={"has_conflict": True, "summary": "Conflict detected with client review."}
        )
        event, _ = await proactive_service.ingest_event(None, ev_data)
        
        insights = await proactive_service.list_workspace_insights(None, "ws_test_events")
        assert len(insights) >= 1
        latest = insights[0]
        assert "Potential Schedule Conflict" in latest["title"] or "Schedule Updated" in latest["title"]

    asyncio.run(_test())

def test_trigger_creation_and_structured_conditions():
    async def _test():
        tr_in = AgentTriggerCreate(
            workspace_id="ws_test_triggers",
            name="High Priority Deadline Trigger",
            description="Fires when calendar deadline changes",
            event_type="calendar.event_updated",
            conditions={"is_deadline_change": True},
            action_type="create_attention",
            scope="workspace",
            cooldown_seconds=3600
        )
        tr = await proactive_service.create_trigger(None, tr_in, created_by="user_owner")
        assert tr["name"] == "High Priority Deadline Trigger"
        assert tr["enabled"] is True
        assert tr["conditions"]["is_deadline_change"] is True

        met = proactive_service.evaluate_structured_condition("is_deadline_change", True, {"is_deadline_change": True})
        assert met is True
        not_met = proactive_service.evaluate_structured_condition("is_deadline_change", True, {"is_deadline_change": False})
        assert not_met is False

    asyncio.run(_test())

def test_dry_run_simulation():
    async def _test():
        tr_in = AgentTriggerCreate(
            workspace_id="ws_test_dryrun",
            name="Simulation Trigger",
            event_type="gmail.thread_updated",
            conditions={"priority": "urgent"},
            action_type="create_insight",
            scope="workspace"
        )
        tr = await proactive_service.create_trigger(None, tr_in, created_by="user_owner")
        
        test_payload = {
            "metadata_dict": {"priority": "urgent"}
        }
        dry_run = await proactive_service.dry_run_trigger(None, tr["id"], test_payload)
        assert dry_run.matched is True
        assert dry_run.proposed_action == "create_insight"
        assert dry_run.policy_decision == "ALLOW"

    asyncio.run(_test())

def test_loop_prevention_max_chain_depth():
    async def _test():
        event_dict = {
            "id": "evt_loop_test",
            "workspace_id": "ws_test_loop",
            "source": "system",
            "event_type": "agent.failed",
            "resource_type": "agent_run",
            "resource_id": "run_loop_999",
            "metadata_dict": {"error": "Loop test"}
        }
        res = await proactive_service.process_system_event(None, event_dict, chain_id="chain_loop_1", chain_depth=5)
        assert res["id"] == "evt_loop_test"

    asyncio.run(_test())

def test_automations_router_endpoints():
    # 1. Create trigger via API
    payload = {
        "workspace_id": "ws_api_test",
        "name": "API Webhook Trigger",
        "description": "Trigger created via REST API",
        "event_type": "drive.file_updated",
        "conditions": {"file_type": "pdf"},
        "action_type": "create_attention",
        "scope": "workspace",
        "cooldown_seconds": 600
    }
    response = client.post("/api/v1/automations", json=payload)
    assert response.status_code == 201
    tr_data = response.json()
    tr_id = tr_data["id"]

    # 2. List triggers via API
    list_res = client.get("/api/v1/automations?workspaceId=ws_api_test")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Dry-run test via API
    test_req = {
        "event_type": "drive.file_updated",
        "resource_type": "drive_file",
        "resource_id": "file_123",
        "metadata_dict": {"file_type": "pdf"}
    }
    test_res = client.post(f"/api/v1/automations/{tr_id}/test?workspaceId=ws_api_test", json=test_req)
    assert test_res.status_code == 200
    assert test_res.json()["matched"] is True

    # 4. Pause trigger via API
    pause_res = client.post(f"/api/v1/automations/{tr_id}/pause")
    assert pause_res.status_code == 200
    assert pause_res.json()["enabled"] is False

    # 5. Ingest webhook event via API
    wh_payload = {
        "workspace_id": "ws_api_test",
        "source": "drive",
        "event_type": "drive.file_updated",
        "resource_type": "drive_file",
        "resource_id": "file_999",
        "metadata_dict": {"file_type": "pdf"}
    }
    wh_res = client.post("/api/v1/automations/events/webhooks/drive", json=wh_payload)
    assert wh_res.status_code == 202
    assert wh_res.json()["status"] == "received"
