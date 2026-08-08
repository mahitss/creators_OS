from enum import Enum
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

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
    def __init__(self, success: bool, data: Dict[str, Any], error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }

class AgentTool:
    name: str
    description: str
    risk_level: ToolRiskLevel = ToolRiskLevel.READ
    input_schema: dict = {}
    output_schema: dict = {}

    async def execute(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        input_data: Dict[str, Any]
    ) -> ToolExecutionResult:
        raise NotImplementedError

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
            return ToolExecutionResult(False, {}, "Missing mission_id parameter.")
        m = await mission_service.get_mission_by_id(session, workspace_id, m_id)
        if not m:
            return ToolExecutionResult(False, {}, f"Mission '{m_id}' not found.")
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
            return ToolExecutionResult(False, {}, "Missing message_id parameter.")
        msg = await gmail_service.get_message(session, workspace_id, msg_id)
        if not msg:
            return ToolExecutionResult(False, {}, f"Gmail message '{msg_id}' not found.")
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
            return ToolExecutionResult(False, {}, "Missing file_id parameter.")
        try:
            content = await drive_service.extract_file_content(session, workspace_id, f_id)
            return ToolExecutionResult(True, content)
        except Exception as exc:
            return ToolExecutionResult(False, {}, str(exc))

class SearchContentTool(AgentTool):
    name = "search_content"
    description = "Search Studio Content Canvas documents."
    risk_level = ToolRiskLevel.READ

    async def execute(self, session, workspace_id, input_data):
        items, count = await content_service.list_content_items(session, workspace_id)
        return ToolExecutionResult(True, {"content_items": items[:20], "count": count})

class ToolRegistry:
    _TOOLS: Dict[str, AgentTool] = {
        "search_missions": SearchMissionsTool(),
        "get_mission": GetMissionTool(),
        "search_memory": SearchMemoryTool(),
        "get_calendar_events": GetCalendarEventsTool(),
        "search_gmail": SearchGmailTool(),
        "get_gmail_message": GetGmailMessageTool(),
        "search_drive_files": SearchDriveFilesTool(),
        "get_drive_file_content": GetDriveFileContentTool(),
        "search_content": SearchContentTool(),
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
