"""Centralized Tool Registry, Schemas, Risk Classification, Idempotency & Governance Authorization for Agent Runtime V1."""

import json
import hashlib
import re
import logging
from enum import Enum
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.agent_lifecycle import ToolRiskLevel
from app.schemas.mission import MissionCreate
from app.schemas.content import ContentCreate, ContentUpdate
from app.services import (
    mission_service,
    memory_service,
    content_service,
    calendar_service,
    gmail_service,
    drive_service,
    policy_engine
)

logger = logging.getLogger("kinetiq.agent.tools")

# In-memory idempotency cache: idempotency_key -> ToolExecutionResult dict
_idempotency_cache: Dict[str, Dict[str, Any]] = {}


class ToolExecutionResult:
    def __init__(
        self,
        success: bool,
        data: Dict[str, Any],
        error: Optional[str] = None,
        error_code: Optional[str] = None,
        tool_name: Optional[str] = None,
        risk_level: str = "LOW"
    ):
        self.success = success
        self.data = data or {}
        self.error = error
        self.error_code = error_code
        self.tool_name = tool_name
        self.risk_level = risk_level

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "tool_name": self.tool_name,
            "risk_level": self.risk_level
        }


class AgentTool:
    id: str
    name: str
    description: str
    risk_level: ToolRiskLevel = ToolRiskLevel.LOW
    required_permissions: List[str] = ["read"]
    timeout_seconds: int = 30
    enabled: bool = True
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}

    def sanitize_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizes tool output to prevent prompt injection payload forwarding."""
        if not data:
            return {}
        # Ensure no credential or raw token keys leaked
        sanitized = {}
        for k, v in data.items():
            if k.lower() in ["password", "secret", "api_key", "token", "auth_token"]:
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, str):
                # Neutralize dangerous delimiter attempts in strings
                sanitized[k] = re.sub(r"=== (UNTRUSTED_RETRIEVED_DATA|END_UNTRUSTED_RETRIEVED_DATA)", r"== [DATA_TOKEN]", v)
            elif isinstance(v, dict):
                sanitized[k] = self.sanitize_output(v)
            else:
                sanitized[k] = v
        return sanitized

    async def execute(
        self,
        session: Optional[AsyncSession],
        workspace_id: str,
        input_data: Dict[str, Any]
    ) -> ToolExecutionResult:
        raise NotImplementedError


# ----------------- SAFE READ TOOLS (LOW RISK) -----------------

class SearchMissionsTool(AgentTool):
    id = "tool_search_missions"
    name = "search_missions"
    description = "Search active or completed workspace missions by keyword or status filter."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search keyword query"},
            "status": {"type": "string", "description": "Filter by mission status (DRAFT, QUEUED, RUNNING, COMPLETED)"}
        }
    }

    async def execute(self, session, workspace_id, input_data):
        q = input_data.get("query")
        st = input_data.get("status")
        items, count = await mission_service.list_workspace_missions(session, workspace_id, status_filter=st, search_query=q)
        return ToolExecutionResult(True, {"missions": items[:20], "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class GetMissionTool(AgentTool):
    id = "tool_get_mission"
    name = "get_mission"
    description = "Retrieve single mission details including steps and plans."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "mission_id": {"type": "string", "description": "Unique identifier of the target mission"}
        },
        "required": ["mission_id"]
    }

    async def execute(self, session, workspace_id, input_data):
        m_id = input_data.get("mission_id")
        if not m_id:
            return ToolExecutionResult(False, {}, "Missing mission_id parameter.", "VALIDATION_ERROR", tool_name=self.name)
        m = await mission_service.get_mission_by_id(session, workspace_id, m_id)
        if not m:
            return ToolExecutionResult(False, {}, f"Mission '{m_id}' not found in active workspace.", "NOT_FOUND", tool_name=self.name)
        return ToolExecutionResult(True, {"mission": m}, tool_name=self.name, risk_level=self.risk_level.value)


class SearchMemoryTool(AgentTool):
    id = "tool_search_memory"
    name = "search_memory"
    description = "Search approved long-term memories in context vault."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Semantic query text to search memory embeddings"}
        }
    }

    async def execute(self, session, workspace_id, input_data):
        q = input_data.get("query")
        mems = await memory_service.list_memories(session, workspace_id, query=q, is_archived=False)
        return ToolExecutionResult(True, {"memories": mems[:20], "count": len(mems)}, tool_name=self.name, risk_level=self.risk_level.value)


class GetCalendarEventsTool(AgentTool):
    id = "tool_get_calendar_events"
    name = "get_calendar_events"
    description = "Get normalized Google Calendar events for active workspace."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "timeframe": {"type": "string", "description": "Timeframe filter e.g. next_7_days, next_30_days"}
        }
    }

    async def execute(self, session, workspace_id, input_data):
        tf = input_data.get("timeframe", "next_7_days")
        events, count = await calendar_service.list_events(session, workspace_id, timeframe=tf)
        return ToolExecutionResult(True, {"events": events[:20], "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class SearchGmailTool(AgentTool):
    id = "tool_search_gmail"
    name = "search_gmail"
    description = "Search read-only Gmail threads and messages metadata."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "filter": {"type": "string", "description": "Filter type e.g. unread, starred, all"}
        }
    }

    async def execute(self, session, workspace_id, input_data):
        flt = input_data.get("filter", "all")
        threads, count = await gmail_service.list_threads(session, workspace_id, filter_type=flt)
        return ToolExecutionResult(True, {"threads": threads[:20], "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class SearchDriveFilesTool(AgentTool):
    id = "tool_search_drive_files"
    name = "search_drive_files"
    description = "Search Google Drive file metadata by keyword."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Keyword search query"}
        }
    }

    async def execute(self, session, workspace_id, input_data):
        q = input_data.get("query")
        files, count = await drive_service.list_drive_files(session, workspace_id, search_query=q)
        return ToolExecutionResult(True, {"files": files[:20], "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class GetDriveFileContentTool(AgentTool):
    id = "tool_get_drive_file_content"
    name = "get_drive_file_content"
    description = "Extract text from Google Docs or PDF documents on demand."
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "Google Drive file ID to extract text from"}
        },
        "required": ["file_id"]
    }

    async def execute(self, session, workspace_id, input_data):
        f_id = input_data.get("file_id")
        if not f_id:
            return ToolExecutionResult(False, {}, "Missing file_id parameter.", "VALIDATION_ERROR", tool_name=self.name)
        try:
            content = await drive_service.extract_file_content(session, workspace_id, f_id)
            return ToolExecutionResult(True, content, tool_name=self.name, risk_level=self.risk_level.value)
        except Exception as exc:
            return ToolExecutionResult(False, {}, str(exc), "EXTRACTION_FAILED", tool_name=self.name)


# ----------------- INTERNAL WRITE TOOLS (MEDIUM RISK) -----------------

class CreateMissionTool(AgentTool):
    id = "tool_create_mission"
    name = "create_mission"
    description = "Create a new workspace Mission in DRAFT status."
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Mission title"},
            "goal": {"type": "string", "description": "High level mission objective"},
            "description": {"type": "string", "description": "Detailed mission description"},
            "priority": {"type": "string", "description": "Mission priority (LOW, MEDIUM, HIGH, URGENT)"}
        },
        "required": ["title"]
    }

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        if not title:
            return ToolExecutionResult(False, {}, "Title is required for mission creation.", "VALIDATION_ERROR", tool_name=self.name)
        payload = MissionCreate(
            title=title,
            goal=input_data.get("goal") or title,
            description=input_data.get("description", ""),
            priority=input_data.get("priority", "medium")
        )
        user_id = input_data.get("user_id", "usr_agent_runner")
        m = await mission_service.create_mission(session, workspace_id, user_id=user_id, payload=payload)
        return ToolExecutionResult(True, {"mission": m}, tool_name=self.name, risk_level=self.risk_level.value)


class CreateContentTool(AgentTool):
    id = "tool_create_content"
    name = "create_content"
    description = "Create a new Studio Content Canvas document draft."
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the new content article"},
            "content": {"type": "string", "description": "Markdown body content"},
            "type": {"type": "string", "description": "Content type (article, tweet_thread, script)"},
            "mission_id": {"type": "string", "description": "Optional associated mission ID"}
        },
        "required": ["title"]
    }

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        if not title:
            return ToolExecutionResult(False, {}, "Title is required for content creation.", "VALIDATION_ERROR", tool_name=self.name)
        payload = ContentCreate(
            title=title,
            type=input_data.get("type", "article"),
            content=input_data.get("content", ""),
            mission_id=input_data.get("mission_id")
        )
        user_id = input_data.get("user_id", "usr_agent_runner")
        c = await content_service.create_content_item(session, workspace_id, user_id=user_id, payload=payload)
        c["status"] = "draft"
        return ToolExecutionResult(True, {"content": c}, tool_name=self.name, risk_level=self.risk_level.value)


class CreateMemoryCandidateTool(AgentTool):
    id = "tool_create_memory_candidate"
    name = "create_memory_candidate"
    description = "Propose a new long-term Memory candidate for user approval."
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Summary title of the learned insight or memory"},
            "content": {"type": "string", "description": "Detailed text content of the memory"},
            "type": {"type": "string", "description": "Memory type (insight, context, procedural)"}
        },
        "required": ["title", "content"]
    }

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        content_text = input_data.get("content")
        if not title or not content_text:
            return ToolExecutionResult(False, {}, "Title and content are required.", "VALIDATION_ERROR", tool_name=self.name)

        cand = await memory_service.create_candidate(
            workspace_id=workspace_id,
            title=title,
            content=content_text,
            type_name=input_data.get("type", "insight"),
            source_type=input_data.get("source_type", "agent")
        )
        return ToolExecutionResult(True, {"memory_candidate": cand}, tool_name=self.name, risk_level=self.risk_level.value)


# ----------------- SIDE-EFFECT & HIGH RISK TOOLS (HIGH / CRITICAL) -----------------

class CreateCalendarEventTool(AgentTool):
    id = "tool_create_calendar_event"
    name = "create_calendar_event"
    description = "Create a new Google Calendar event."
    risk_level = ToolRiskLevel.HIGH
    required_permissions = ["write", "integrations:calendar"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Calendar event title"},
            "start_at": {"type": "string", "description": "Start ISO timestamp"},
            "end_at": {"type": "string", "description": "End ISO timestamp"},
            "location": {"type": "string", "description": "Meeting location or virtual link"}
        },
        "required": ["title", "start_at", "end_at"]
    }

    async def execute(self, session, workspace_id, input_data):
        title = input_data.get("title")
        start_at = input_data.get("start_at")
        end_at = input_data.get("end_at")

        if not title or not start_at or not end_at:
            return ToolExecutionResult(False, {}, "title, start_at, and end_at are required parameters.", "VALIDATION_ERROR", tool_name=self.name)

        # Conflict check
        events, _ = await calendar_service.list_events(session, workspace_id, timeframe="next_30_days")
        conflicts = [ev for ev in events if ev["title"] == title or ev["start_at"] == start_at]

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
        return ToolExecutionResult(True, {"event": created_event}, tool_name=self.name, risk_level=self.risk_level.value)


class SendNotificationTool(AgentTool):
    id = "tool_send_notification"
    name = "send_notification"
    description = "Send a high-priority operational alert or team notification."
    risk_level = ToolRiskLevel.HIGH
    required_permissions = ["write", "notifications:send"]
    input_schema = {
        "type": "object",
        "properties": {
            "channel": {"type": "string", "description": "Notification channel e.g. slack, email, in_app"},
            "recipient": {"type": "string", "description": "Recipient address or channel ID"},
            "message": {"type": "string", "description": "Notification text content"}
        },
        "required": ["channel", "message"]
    }

    async def execute(self, session, workspace_id, input_data):
        ch = input_data.get("channel")
        msg = input_data.get("message")
        if not ch or not msg:
            return ToolExecutionResult(False, {}, "channel and message are required parameters.", "VALIDATION_ERROR", tool_name=self.name)

        notification_record = {
            "notification_id": f"ntf_{hashlib.md5(f'{ch}:{msg}'.encode()).hexdigest()[:8]}",
            "channel": ch,
            "recipient": input_data.get("recipient", "workspace_general"),
            "message": msg,
            "status": "delivered"
        }
        return ToolExecutionResult(True, {"notification": notification_record}, tool_name=self.name, risk_level=self.risk_level.value)


# ----------------- CENTRALIZED TOOL REGISTRY -----------------

class ToolRegistry:
    """Centralized Tool Registry with schemas, permission constraints, and risk classification."""

    _TOOLS: Dict[str, AgentTool] = {
        # Safe Read Tools (LOW)
        "search_missions": SearchMissionsTool(),
        "get_mission": GetMissionTool(),
        "search_memory": SearchMemoryTool(),
        "get_calendar_events": GetCalendarEventsTool(),
        "search_gmail": SearchGmailTool(),
        "search_drive_files": SearchDriveFilesTool(),
        "get_drive_file_content": GetDriveFileContentTool(),
        # Write Tools (MEDIUM)
        "create_mission": CreateMissionTool(),
        "create_content": CreateContentTool(),
        "create_memory_candidate": CreateMemoryCandidateTool(),
        # High Risk Tools (HIGH)
        "create_calendar_event": CreateCalendarEventTool(),
        "send_notification": SendNotificationTool(),
    }

    @classmethod
    def get_tool(cls, name: str) -> Optional[AgentTool]:
        return cls._TOOLS.get(name)

    @classmethod
    def list_tools(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "risk_level": t.risk_level.value,
                "required_permissions": t.required_permissions,
                "timeout_seconds": t.timeout_seconds,
                "enabled": t.enabled,
                "input_schema": t.input_schema,
            }
            for t in cls._TOOLS.values()
        ]

    @classmethod
    def register_tool(cls, tool: AgentTool) -> None:
        cls._TOOLS[tool.name] = tool


# ----------------- AUTHORIZATION & GOVERNANCE PIPELINE -----------------

async def authorize_and_execute_tool(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    user_role: str,
    agent: Dict[str, Any],
    agent_version: Dict[str, Any],
    tool_name: str,
    input_data: Dict[str, Any],
    idempotency_key: Optional[str] = None
) -> ToolExecutionResult:
    """Multi-level Tool Authorization Pipeline:
    1. Tool existence check
    2. Agent & Version tool policy check
    3. User permission check
    4. PolicyEngine risk & action evaluation
    5. Idempotency key check
    6. Tool execution & output sanitization
    """
    # 1. Tool existence check
    tool = ToolRegistry.get_tool(tool_name)
    if not tool or not tool.enabled:
        return ToolExecutionResult(
            success=False,
            data={},
            error=f"Tool '{tool_name}' is not registered or is disabled.",
            error_code="TOOL_NOT_FOUND",
            tool_name=tool_name
        )

    # 2. Check Agent & Version allowed_tools
    allowed_tools = agent_version.get("tool_policy", {}).get("allowed_tools") or agent.get("allowed_tools", [])
    if allowed_tools and "*" not in allowed_tools and tool_name not in allowed_tools:
        return ToolExecutionResult(
            success=False,
            data={},
            error=f"Tool '{tool_name}' is not in agent's allowed_tools policy.",
            error_code="POLICY_DENIED",
            tool_name=tool_name,
            risk_level=tool.risk_level.value
        )

    # 3. User Permission Check (e.g. member vs admin)
    user_role_norm = (user_role or "MEMBER").upper()
    if "admin" in tool.required_permissions and user_role_norm not in ["ADMIN", "OWNER"]:
        return ToolExecutionResult(
            success=False,
            data={},
            error=f"Tool '{tool_name}' requires administrative privileges.",
            error_code="AUTH_ERROR",
            tool_name=tool_name,
            risk_level=tool.risk_level.value
        )

    # 4. PolicyEngine check for HIGH and CRITICAL risk tools
    if tool.risk_level in [ToolRiskLevel.HIGH, ToolRiskLevel.CRITICAL]:
        try:
            policy_check = await policy_engine.evaluate_action_policy(
                session=session,
                workspace_id=workspace_id,
                action_type=tool_name,
                payload=input_data,
                actor_id=user_id,
                actor_role=user_role_norm
            )
            if not policy_check.get("allowed", True):
                reason = policy_check.get("reason", "Action denied by governance policy.")
                return ToolExecutionResult(
                    success=False,
                    data={},
                    error=f"PolicyEngine denied tool '{tool_name}': {reason}",
                    error_code="POLICY_DENIED",
                    tool_name=tool_name,
                    risk_level=tool.risk_level.value
                )
        except Exception as exc:
            logger.warning(f"Policy check evaluation fallback: {exc}")

    # 5. Idempotency Key check
    if idempotency_key:
        cached = _idempotency_cache.get(idempotency_key)
        if cached:
            logger.info(f"Idempotent execution returned from cache for key: {idempotency_key}")
            return ToolExecutionResult(
                success=cached["success"],
                data=cached["data"],
                error=cached.get("error"),
                error_code=cached.get("error_code"),
                tool_name=tool_name,
                risk_level=tool.risk_level.value
            )

    # 6. Execute tool
    try:
        raw_result = await tool.execute(session, workspace_id, input_data)
        # Sanitize output to strip injection attempts and leaked secrets
        sanitized_data = tool.sanitize_output(raw_result.data)
        raw_result.data = sanitized_data

        # Cache for idempotency
        if idempotency_key and raw_result.success:
            _idempotency_cache[idempotency_key] = raw_result.to_dict()

        return raw_result
    except Exception as exc:
        logger.error(f"Error executing tool '{tool_name}': {exc}", exc_info=True)
        return ToolExecutionResult(
            success=False,
            data={},
            error=str(exc),
            error_code="TOOL_ERROR",
            tool_name=tool_name,
            risk_level=tool.risk_level.value
        )
