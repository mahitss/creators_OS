import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import event_mesh_service
from app.schemas.event_mesh import EventEnvelopePublishRequest

def test_event_schema_catalog_initialization():
    async def _test():
        catalog = await event_mesh_service.list_event_catalog(None)
        assert len(catalog) >= 10
        event_types = [c["event_type"] for c in catalog]
        assert "mission.created" in event_types
        assert "workflow.completed" in event_types
        assert "security.finding.created" in event_types
    asyncio.run(_test())

def test_event_publication_and_tenant_isolation():
    async def _test():
        # Organization A Event
        req_a = EventEnvelopePublishRequest(
            eventType="mission.created",
            eventVersion="1.0.0",
            organizationId="org_alpha_01",
            workspaceId="ws_alpha_01",
            source="mission_engine",
            subject="mission_101",
            producer="executive_ai",
            payloadReference={"mission_name": "Alpha Mission"}
        )
        evt_a, err_a = await event_mesh_service.publish_event(None, req_a)
        assert err_a is None
        assert evt_a["event_id"].startswith("evt_")

        # Organization B Subscription
        sub_b = await event_mesh_service.create_subscription(
            None,
            org_id="org_beta_02",
            workspace_id="ws_beta_02",
            event_type="mission.created",
            consumer="beta_analytics"
        )

        # Retrieve events for Org A vs Org B
        events_a = await event_mesh_service.list_events(None, org_id="org_alpha_01")
        events_b = await event_mesh_service.list_events(None, org_id="org_beta_02")

        assert len(events_a) >= 1
        assert len(events_b) == 0 # Org B cannot consume Org A events
    asyncio.run(_test())

def test_payload_secret_prohibition():
    async def _test():
        req_bad = EventEnvelopePublishRequest(
            eventType="workflow.started",
            eventVersion="1.0.0",
            organizationId="org_default_creator",
            workspaceId="ws_default_01",
            source="workflow_engine",
            subject="wf_101",
            producer="workflow_engine",
            payloadReference={"bearer": "sk_test_secret_key_12345"}
        )
        evt, err = await event_mesh_service.publish_event(None, req_bad)
        assert evt == {}
        assert "Security DENY" in err
    asyncio.run(_test())

def test_event_loop_and_max_depth_protection():
    async def _test():
        corr_id = "corr_loop_test_01"

        # Simulate recursive event publication chain up to depth 11
        last_causation = None
        err_occurred = False
        for i in range(12):
            req = EventEnvelopePublishRequest(
                eventType="agent.task.completed",
                eventVersion="1.0.0",
                organizationId="org_default_creator",
                workspaceId="ws_default_01",
                source="agent_runtime",
                subject=f"step_{i}",
                correlationId=corr_id,
                causationId=last_causation,
                producer="agent_runtime",
                payloadReference={"step": i}
            )
            evt, err = await event_mesh_service.publish_event(None, req)
            if err:
                err_occurred = True
                assert "Event Loop Protection" in err
                break
            last_causation = evt["event_id"]

        assert err_occurred is True
    asyncio.run(_test())

def test_idempotent_consumer_duplicate_delivery():
    async def _test():
        req = EventEnvelopePublishRequest(
            eventType="integration.action.completed",
            eventVersion="1.0.0",
            organizationId="org_default_creator",
            workspaceId="ws_default_01",
            source="action_gateway",
            subject="action_101",
            producer="action_gateway",
            payloadReference={"status": "completed"}
        )
        evt, err = await event_mesh_service.publish_event(None, req)
        assert err is None

        # Re-dispatching same event ID returns safely without duplicate side effect
        del_rec = {
            "id": "del_test_01",
            "event_id": evt["event_id"],
            "subscription_id": "sub_test_01",
            "consumer": "test_consumer",
            "status": "queued"
        }
        await event_mesh_service._dispatch_to_consumer(None, del_rec, evt, {"consumer": "test_consumer"})
        assert del_rec["status"] == "completed"
    asyncio.run(_test())

def test_dead_letter_and_controlled_replay():
    async def _test():
        # Publish Event
        req = EventEnvelopePublishRequest(
            eventType="decision.recommendation.created",
            eventVersion="1.0.0",
            organizationId="org_default_creator",
            workspaceId="ws_default_01",
            source="decision_intelligence",
            subject="rec_101",
            producer="decision_intelligence",
            payloadReference={"score": 0.95}
        )
        evt, err = await event_mesh_service.publish_event(None, req)
        assert err is None

        # Move to Dead Letter Queue
        dl_entry = await event_mesh_service.move_to_dead_letter(None, evt["event_id"], "Timeout error dispatching to webhook endpoint")
        assert dl_entry["event_id"] == evt["event_id"]

        dead_letters = await event_mesh_service.list_dead_letters(None)
        assert len(dead_letters) >= 1

        # Administrative Replay
        rep, rep_err = await event_mesh_service.replay_event(None, evt["event_id"], authorized_by="usr_admin_01", reason="Manual operator retry")
        assert rep_err is None
        assert rep["status"] == "replayed"
    asyncio.run(_test())
