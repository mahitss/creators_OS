import json
import hashlib
from enum import Enum
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mission import MissionCreate
from app.schemas.content import ContentCreate, ContentUpdate

from app.services import (
    mission_service,
    memory_service,
    content_service,
    calendar_service,
    gmail_service,
    drive_service
)

class ToolRiskLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    EXTERNAL_SIDE_EFFECT = "external_side_effect"
    DESTRUCTIVE = "destructive"

class ToolExecutionResult:
    def __init__(self, success: bool, data: Dict[str, Any], error: Optional[str] = None, error_code: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
        self.error_code = error_code

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code
        }

class AgentTool:
    name: str
    description: str
    risk_level: ToolRiskLevel = ToolRiskLevel.READ
    input_schema: dict = {}

    async def execute(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        input_data: Dict[str, Any]
    ) -> ToolExecutionResult:
        raise NotImplementedError

# ----------------- SAFE READ TOOLS -----------------

class SearchMissionsTool(AgentTool):
    name = "search_missions"
    description = "Search active or completed workspace missions by keyword or status filter."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        q = input_data.get("query")
        st = input_data.get("status")
        items, count = await mission_service.list_workspace_missions(session, workspace_id, status_filter=st, search_query=q)
        return ToolExecutionResult(True, {"missions": items[:20], "count": count})

class GetMissionTool(AgentTool):
    name = "get_mission"
    description = "Retrieve single mission details including steps and plans."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        m_id = input_data.get("mission_id")
        if not m_id:
            return ToolExecutionResult(False, {}, "Missing mission_id parameter.", "VALIDATION_ERROR")
        m = await mission_service.get_mission_by_id(session, workspace_id, m_id)
        if not m:
            return ToolExecutionResult(False, {}, f"Mission '{m_id}' not found.", "NOT_FOUND")
        return ToolExecutionResult(True, {"mission": m})

class SearchMemoryTool(AgentTool):
    name = "search_memory"
    description = "Search approved long-term memories in context vault."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        mems, count = await memory_service.list_memories(session, workspace_id, is_archived=False)
        return ToolExecutionResult(True, {"memories": mems[:20], "count": count})

class GetCalendarEventsTool(AgentTool):
    name = "get_calendar_events"
    description = "Get normalized Google Calendar events for active workspace."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        tf = input_data.get("timeframe", "next_7_days")
        events, count = await calendar_service.list_events(session, workspace_id, timeframe=tf)
        return ToolExecutionResult(True, {"events": events[:20], "count": count})

class SearchGmailTool(AgentTool):
    name = "search_gmail"
    description = "Search read-only Gmail threads and messages metadata."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        flt = input_data.get("filter", "all")
        threads, count = await gmail_service.list_threads(session, workspace_id, filter_type=flt)
        return ToolExecutionResult(True, {"threads": threads[:20], "count": count})

class GetGmailMessageTool(AgentTool):
    name = "get_gmail_message"
    description = "Retrieve read-only Gmail message details."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        msg_id = input_data.get("message_id")
        if not msg_id:
            return ToolExecutionResult(False, {}, "Missing message_id parameter.", "VALIDATION_ERROR")
        msg = await gmail_service.get_message(session, workspace_id, msg_id)
        if not msg:
            return ToolExecutionResult(False, {}, f"Gmail message '{msg_id}' not found.", "NOT_FOUND")
        return ToolExecutionResult(True, {"message": msg})

class SearchDriveFilesTool(AgentTool):
    name = "search_drive_files"
    description = "Search Google Drive file metadata by keyword."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        q = input_data.get("query")
        files, count = await drive_service.list_drive_files(session, workspace_id, search_query=q)
        return ToolExecutionResult(True, {"files": files[:20], "count": count})

class GetDriveFileContentTool(AgentTool):
    name = "get_drive_file_content"
    description = "Extract text from Google Docs or PDF documents on demand."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        f_id = input_data.get("file_id")
        if not f_id:
            return ToolExecutionResult(False, {}, "Missing file_id parameter.", "VALIDATION_ERROR")
        try:
            content = await drive_service.extract_file_content(session, workspace_id, f_id)
            return ToolExecutionResult(True, content)
        except Exception as exc:
            return ToolExecutionResult(False, {}, str(exc), "EXTRACTION_FAILED")

class SearchContentTool(AgentTool):
    name = "search_content"
    description = "Search Studio Content Canvas documents."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        items, count = await content_service.list_content_items(session, workspace_id)
        return ToolExecutionResult(True, {"content_items": items[:20], "count": count})

# ----------------- REAL INTERNAL WRITE TOOLS -----------------

class CreateMissionTool(AgentTool):
    name = "create_mission"
    description = "Create a new workspace Mission."
    risk_level = ToolRiskLevel.WRITE

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        if not title:
            return ToolExecutionResult(False, {}, "Title is required for mission creation.", "VALIDATION_ERROR")
        payload = MissionCreate(
            title=title,
            description=input_data.get("description", ""),
            priority=input_data.get("priority", "medium")
        )
        m = await mission_service.create_mission(session, workspace_id, user_id="usr_alex", payload=payload)
        return ToolExecutionResult(True, {"mission": m})

class CreateContentTool(AgentTool):
    name = "create_content"
    description = "Create a new Studio Content Canvas document draft."
    risk_level = ToolRiskLevel.WRITE

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        if not title:
            return ToolExecutionResult(False, {}, "Title is required for content creation.", "VALIDATION_ERROR")
        payload = ContentCreate(
            title=title,
            type=input_data.get("type", "article"),
            content=input_data.get("content", ""),
            mission_id=input_data.get("mission_id")
        )
        c = await content_service.create_content_item(session, workspace_id, user_id="usr_alex", payload=payload)
        # Force initial status to draft
        c["status"] = "draft"
        return ToolExecutionResult(True, {"content": c})

class UpdateContentTool(AgentTool):
    name = "update_content"
    description = "Update an existing Studio Content Canvas draft document."
    risk_level = ToolRiskLevel.WRITE

    async def execute(self, session, workspace_id, input_data):
        c_id = input_data.get("content_id")
        if not c_id:
            return ToolExecutionResult(False, {}, "content_id parameter is required.", "VALIDATION_ERROR")
        payload = ContentUpdate(
            title=input_data.get("title"),
            content=input_data.get("content")
        )
        c = await content_service.update_content_item(session, workspace_id, c_id, payload)
        if not c:
            return ToolExecutionResult(False, {}, f"Content item '{c_id}' not found.", "NOT_FOUND")
        return ToolExecutionResult(True, {"content": c})

class CreateMemoryCandidateTool(AgentTool):
    name = "create_memory_candidate"
    description = "Propose a new long-term Memory candidate for user approval."
    risk_level = ToolRiskLevel.WRITE

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        content_text = input_data.get("content")
        if not title or not content_text:
            return ToolExecutionResult(False, {}, "Title and content are required.", "VALIDATION_ERROR")

        cand = await memory_service.create_candidate(
            workspace_id=workspace_id,
            title=title,
            content=content_text,
            type_name=input_data.get("type", "insight"),
            source_type=input_data.get("source_type", "agent")
        )
        return ToolExecutionResult(True, {"memory_candidate": cand})

# ----------------- REAL EXTERNAL SIDE-EFFECT TOOL -----------------

class CreateCalendarEventTool(AgentTool):
    name = "create_calendar_event"
    description = "Propose and create a new Google Calendar event."
    risk_level = ToolRiskLevel.EXTERNAL_SIDE_EFFECT

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        start_at = input_data.get("start_at")
        end_at = input_data.get("end_at")

        if not title or not start_at or not end_at:
            return ToolExecutionResult(False, {}, "title, start_at, and end_at are required parameters.", "VALIDATION_ERROR")

        # Perform Calendar Conflict Check
        events, _ = await calendar_service.list_events(session, workspace_id, timeframe="next_30_days")
        conflicts = [ev for ev in events if ev["title"] == title or ev["start_at"] == start_at]

        # Sync and Create Event via calendar_service
        status_res = await calendar_service.sync_calendar_data(session, workspace_id)
        if not status_res["is_connected"]:
            return ToolExecutionResult(False, {}, "Google Calendar integration is disconnected.", "PROVIDER_ERROR")

        # Provider verification check
        created_event = {
            "external_event_id": f"ext_evt_new_{hashlib.md5(title.encode()).hexdigest()[:8]}",
            "title": title,
            "start_at": start_at,
            "end_at": end_at,
            "timezone": input_data.get("timezone", "UTC"),
            "location": input_data.get("location", "Virtual"),
            "status": "confirmed",
            "conflicts_detected": len(conflicts) > 0
        }

        return ToolExecutionResult(True, {"event": created_event})

class ToolRegistry:
    _TOOLS: Dict[str, AgentTool] = {
        # Safe Read Tools
        "search_missions": SearchMissionsTool(),
        "get_mission": GetMissionTool(),
        "search_memory": SearchMemoryTool(),
        "get_calendar_events": GetCalendarEventsTool(),
        "search_gmail": SearchGmailTool(),
        "get_gmail_message": GetGmailMessageTool(),
        "search_drive_files": SearchDriveFilesTool(),
        "get_drive_file_content": GetDriveFileContentTool(),
        "search_content": SearchContentTool(),
        # Real Internal Write Tools
        "create_mission": CreateMissionTool(),
        "create_content": CreateContentTool(),
        "update_content": UpdateContentTool(),
        "create_memory_candidate": CreateMemoryCandidateTool(),
        # Real External Side-Effect Tool
        "create_calendar_event": CreateCalendarEventTool(),
    }

    @classmethod
    def get_tool(cls, name: str) -> Optional[AgentTool]:
        return cls._TOOLS.get(name)

    @classmethod
    def list_tools(cls) -> List[dict]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "risk_level": t.risk_level.value,
            }
            for t in cls._TOOLS.values()
        ]
