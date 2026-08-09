import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.eval_synthetic_providers import SyntheticWorkspaceFixture, FakeGoogleCalendarProvider, FakeGmailProvider, FakeDriveProvider, FakeAIProvider
from app.services.evaluation_runner import run_evaluation_suite, create_evaluation_run, list_suites

client = TestClient(app)
ADMIN_HEADERS = {"X-User-Id": "usr_admin_01"}

def test_synthetic_workspace_isolation():
    fixture1 = SyntheticWorkspaceFixture("case_01")
    fixture2 = SyntheticWorkspaceFixture("case_02")

    m1 = fixture1.seed_mission("Mission 1", "Alpha mission")
    m2 = fixture2.seed_mission("Mission 2", "Beta mission")

    assert m1["workspace_id"] != m2["workspace_id"]
    assert fixture1.workspace_id not in fixture2.missions

def test_fake_providers_deterministic_behavior():
    async def _test():
        cal = FakeGoogleCalendarProvider()
        evt = await cal.create_event("ws_synth", "Team Sync", "2026-08-10T10:00:00Z", "2026-08-10T10:30:00Z")
        assert evt["status"] == "confirmed"

        gmail = FakeGmailProvider()
        gmail.messages["msg_1"] = {"id": "msg_1", "workspace_id": "ws_synth", "subject": "Project Status", "body": "All systems operational."}
        msgs = await gmail.search_messages("ws_synth", "Status")
        assert len(msgs) == 1

        drive = FakeDriveProvider()
        drive.files["f_1"] = {"id": "f_1", "workspace_id": "ws_synth", "name": "Architecture.pdf", "content": "Vapor OS Core Specs"}
        files = await drive.search_files("ws_synth", "Architecture")
        assert len(files) == 1

    asyncio.run(_test())

def test_golden_suite_list_and_run_creation():
    res = client.get("/api/v1/evaluations/suites", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    suites = res.json()
    assert len(suites) > 0
    golden_suite_id = suites[0]["id"]

    run_res = client.post(f"/api/v1/evaluations/suites/{golden_suite_id}/run", headers=ADMIN_HEADERS)
    assert run_res.status_code == 201
    run_data = run_res.json()
    assert run_data["total_cases"] >= 30

def test_full_30_case_golden_evaluation_execution():
    async def _test():
        suites = await list_suites()
        suite_id = suites[0]["id"]

        run = await create_evaluation_run(suite_id)
        executed_run = await run_evaluation_suite(run["id"], "fake")

        assert executed_run["status"] == "completed"
        assert executed_run["total_cases"] >= 30
        assert executed_run["score"] > 0.80
        assert executed_run["release_blocked"] is False

    asyncio.run(_test())

def test_admin_authorization_enforcement():
    res = client.get("/api/v1/evaluations/suites")
    assert res.status_code == 200
