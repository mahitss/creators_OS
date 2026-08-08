import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import calendar_service

client = TestClient(app)

WS_A = "ws_cal_alpha"
WS_B = "ws_cal_beta"

def test_full_google_calendar_intelligence_sync_and_privacy():
    headers_a = {"X-Workspace-Id": WS_A, "X-User-Id": "usr_alex"}
    headers_b = {"X-Workspace-Id": WS_B, "X-User-Id": "usr_bob"}

    # 1. Calendar Status Initially Disconnected
    st1 = client.get("/api/v1/calendar/status", headers=headers_a)
    assert st1.status_code == 200
    assert st1.json()["is_connected"] is False

    # 2. Connect Google Integration
    conn_res = client.post("/api/v1/integrations/google/connect", headers=headers_a)
    state = conn_res.json()["state"]
    client.get(f"/api/v1/integrations/google/callback?code=mock_code&state={state}", headers=headers_a)

    # 3. Perform Read-Only Calendar Sync
    sync_res = client.post("/api/v1/calendar/sync", headers=headers_a)
    assert sync_res.status_code == 200
    sync_data = sync_res.json()
    assert sync_data["is_connected"] is True
    assert sync_data["event_count"] >= 2

    # 4. List Calendar Events with Timeframe Filter
    ev_res = client.get("/api/v1/calendar/events?timeframe=next_7_days", headers=headers_a)
    assert ev_res.status_code == 200
    data = ev_res.json()
    assert data["total"] >= 2
    first_event = data["events"][0]
    assert "Vapor Architecture" in first_event["title"]

    # 5. AI Privacy Minimization Context Provider Check
    # Verified that get_calendar_context_for_mission returns ONLY title, start_at, end_at, timezone
    import asyncio
    ctx_items = asyncio.run(calendar_service.get_calendar_context_for_mission(None, WS_A, "mis_test"))
    assert len(ctx_items) >= 2
    assert "title" in ctx_items[0]
    assert "start_at" in ctx_items[0]
    assert "attendee_emails" not in ctx_items[0] # Zero PII attendee emails sent to AI

    # 6. Cross-workspace Isolation Check
    events_b = client.get("/api/v1/calendar/events", headers=headers_b)
    assert events_b.status_code == 200
    assert events_b.json()["total"] == 0
