import sys
import asyncio
import pytest
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from app.services.eval_synthetic_providers import FakeGoogleCalendarProvider, FakeDriveProvider
from app.services.evaluation_runner import execute_evaluation_case

def test_chaos_provider_timeout_simulation():
    async def _test():
        cal = FakeGoogleCalendarProvider()
        cal.fail_rate = 1.0

        with pytest.raises(RuntimeError) as exc_info:
            await cal.create_event("ws_chaos", "Test Event", "2026-08-10T10:00:00Z", "2026-08-10T10:30:00Z")
        assert "Simulated API timeout/failure" in str(exc_info.value)

    asyncio.run(_test())

def test_chaos_revoked_permission_handling():
    async def _test():
        drive = FakeDriveProvider()
        drive.permission_revoked = True

        with pytest.raises(PermissionError) as exc_info:
            await drive.search_files("ws_chaos", "Proposal")
        assert "Drive OAuth scope revoked" in str(exc_info.value)

    asyncio.run(_test())

def test_chaos_evaluation_case_execution():
    async def _test():
        case = {
            "id": "case_chaos_01",
            "name": "Chaos Tool Selection Test",
            "category": "tool_selection",
            "input": {"prompt": "Find relevant proposal PDF documents in Google Drive."},
            "expected": {"selected_tool": "search_drive_files"},
            "constraints": {}
        }
        result = await execute_evaluation_case(case, "fake")
        assert result["status"] == "passed"
        assert result["score"] == 1.0

    asyncio.run(_test())
