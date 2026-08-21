"""Centralized Tool Fabric V1 for KINETIQ.
Provides standardized Tool Contracts, Capability-Aware Discovery, Multi-Level Authorization,
High-Risk Approval Gates, Bounded Timeouts, Idempotency Caching, Output Limits, and Audit Logging.
"""

import json
import hashlib
import re
import asyncio
import uuid
import time
import logging
from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.agent_lifecycle import ToolRiskLevel
from app.schemas.mission import MissionCreate
from app.schemas.content import ContentCreate, ContentUpdate

logger = logging.getLogger("kinetiq.agent.tool_fabric")

# Limits
MAX_OUTPUT_BYTES = 64 * 1024  # 64 KB
MAX_ITEMS_LIMIT = 50
MAX_OUTPUT_TOKENS = 4000
ESTIMATED_CHARS_PER_TOKEN = 4

# In-memory idempotency cache: idempotency_key -> ToolExecutionResult dict
_idempotency_cache: Dict[str, Dict[str, Any]] = {}
# In-memory tool audit logs: list of audit dicts
_in_memory_tool_audit_logs: List[Dict[str, Any]] = []


class ToolCategory(str, Enum):
    READ = "READ"
    SEARCH = "SEARCH"
    DATA = "DATA"
    CONTENT = "CONTENT"
    COMMUNICATION = "COMMUNICATION"
    WORKFLOW = "WORKFLOW"
    SYSTEM = "SYSTEM"
    ADMIN = "ADMIN"


class ToolExecutionContext:
    def __init__(
        self,
        user_id: str,
        workspace_id: str,
        tenant_id: Optional[str] = None,
        user_role: str = "member",
        agent_id: Optional[str] = None,
        agent_version_id: Optional[str] = None,
        agent_run_id: Optional[str] = None,
        mission_id: Optional[str] = None,
        request_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        approval_status: Optional[str] = None,
        idempotency_key: Optional[str] = None
    ):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.tenant_id = tenant_id or workspace_id
        self.user_role = user_role
        self.agent_id = agent_id
        self.agent_version_id = agent_version_id
        self.agent_run_id = agent_run_id
        self.mission_id = mission_id
        self.request_id = request_id or str(uuid.uuid4())
        self.trace_id = trace_id or str(uuid.uuid4())
        self.approval_status = approval_status
        self.idempotency_key = idempotency_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "workspaceId": self.workspace_id,
            "tenantId": self.tenant_id,
            "userRole": self.user_role,
            "agentId": self.agent_id,
            "agentVersionId": self.agent_version_id,
            "agentRunId": self.agent_run_id,
            "missionId": self.mission_id,
            "requestId": self.request_id,
            "traceId": self.trace_id,
            "approvalStatus": self.approval_status,
            "idempotencyKey": self.idempotency_key
        }


class ToolExecutionResult:
    def __init__(
        self,
        success: bool,
        data: Dict[str, Any],
        error: Optional[str] = None,
        error_code: Optional[str] = None,
        tool_name: Optional[str] = None,
        risk_level: str = "LOW",
        truncated: bool = False,
        citations: Optional[List[Dict[str, Any]]] = None
    ):
        self.success = success
        self.data = data or {}
        self.error = error
        self.error_code = error_code
        self.tool_name = tool_name
        self.risk_level = risk_level
        self.truncated = truncated
        self.citations = citations or []

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
            "tool_name": self.tool_name,
            "risk_level": self.risk_level,
            "truncated": self.truncated,
            "citations": self.citations
        }


class AgentTool:
    id: str
    name: str
    description: str
    version: int = 1
    category: ToolCategory = ToolCategory.READ
    risk_level: ToolRiskLevel = ToolRiskLevel.LOW
    required_permissions: List[str] = ["read"]
    timeout_ms: int = 30000
    timeout_seconds: int = 30
    enabled: bool = True
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}

    def validate(self, input_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validates input payload against tool schema and required properties."""
        if not isinstance(input_data, dict):
            return False, "Input data must be a JSON object/dictionary."

        required_fields = self.input_schema.get("required", [])
        for req in required_fields:
            if req not in input_data or input_data[req] is None:
                return False, f"Missing required parameter '{req}' for tool '{self.name}'."

        return True, None

    async def authorize(
        self,
        session: Optional[AsyncSession],
        context: ToolExecutionContext,
        agent: Optional[Dict[str, Any]] = None,
        agent_version: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """Authorizes tool execution against Agent policy, Workspace policy, User role, and PolicyEngine."""
        # 1. Check Tool Enablement
        if not self.enabled:
            return False, f"Tool '{self.name}' is currently disabled in system registry.", "TOOL_DISABLED"

        # 2. Check Agent Allowed Tools Whitelist
        if agent:
            allowed = agent.get("allowed_tools", [])
            if self.name not in allowed and self.id not in allowed:
                return False, f"Agent '{agent.get('name', 'agent')}' is not authorized to execute tool '{self.name}'.", "POLICY_DENIED"

        if agent_version:
            vp = agent_version.get("tool_policy", {})
            v_allowed = vp.get("allowed_tools", [])
            if v_allowed and self.name not in v_allowed and self.id not in v_allowed:
                return False, f"Agent version tool policy prohibits '{self.name}'.", "POLICY_DENIED"

        # 3. Check User Role & Required Permissions
        if self.category == ToolCategory.ADMIN and context.user_role != "admin" and context.user_role != "owner":
            return False, f"Tool '{self.name}' requires administrator privileges.", "UNAUTHORIZED"

        if self.category in [ToolCategory.DATA, ToolCategory.CONTENT, ToolCategory.COMMUNICATION, ToolCategory.WORKFLOW]:
            if context.user_role not in ["owner", "admin", "member"]:
                return False, f"Tool '{self.name}' requires write permissions.", "UNAUTHORIZED"

        # 4. Check PolicyEngine
        try:
            from app.services import policy_engine
            p_action = "admin" if self.risk_level == ToolRiskLevel.CRITICAL else "execute"
            eval_res = await policy_engine.evaluate_policy(
                session=session,
                workspace_id=context.workspace_id,
                user_id=context.user_id,
                user_role=context.user_role,
                action=p_action,
                resource_type=f"tool:{self.name}",
                resource_id=self.id,
                metadata={"risk_level": self.risk_level.value, "category": self.category.value}
            )
            if not eval_res.get("allowed", True):
                return False, f"Policy Engine denied execution: {eval_res.get('reason', 'Policy violation')}", "POLICY_DENIED"
        except Exception as exc:
            logger.debug(f"PolicyEngine evaluation skipped/fallback: {exc}")

        # 5. Check High-Risk Approval Gate
        if self.risk_level in [ToolRiskLevel.HIGH, ToolRiskLevel.CRITICAL]:
            if context.approval_status != "APPROVED":
                # Explicit approval required for high risk actions
                return False, f"HIGH_RISK_APPROVAL_REQUIRED: Tool '{self.name}' has risk level '{self.risk_level.value}' and requires explicit approval.", "APPROVAL_REQUIRED"

        return True, None, None

    def normalize(self, raw_output: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """Sanitizes credentials, neutralizes delimiters, and applies output size and item limits."""
        if not raw_output:
            return {}, False

        is_truncated = False
        sanitized = self._sanitize_data(raw_output)

        # Enforce maxItems on array results
        for k, v in list(sanitized.items()):
            if isinstance(v, list) and len(v) > MAX_ITEMS_LIMIT:
                sanitized[k] = v[:MAX_ITEMS_LIMIT]
                is_truncated = True

        # Enforce maxBytes limit on overall string representation
        serialized = json.dumps(sanitized)
        if len(serialized) > MAX_OUTPUT_BYTES:
            is_truncated = True
            # Safely truncate large string values within the dict
            for k, v in list(sanitized.items()):
                if isinstance(v, str) and len(v) > 2000:
                    sanitized[k] = v[:2000] + "... [TRUNCATED DUE TO SIZE LIMIT]"

        return sanitized, is_truncated

    def _sanitize_data(self, data: Any) -> Any:
        if isinstance(data, dict):
            clean_dict = {}
            for k, v in data.items():
                if str(k).lower() in ["password", "secret", "api_key", "token", "auth_token", "oauth_token", "access_token", "client_secret"]:
                    clean_dict[k] = "[REDACTED]"
                else:
                    clean_dict[k] = self._sanitize_data(v)
            return clean_dict
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, str):
            # Neutralize delimiter forgery in output strings
            return re.sub(r"=== (UNTRUSTED_RETRIEVED_DATA|END_UNTRUSTED_RETRIEVED_DATA)", r"== [DATA_TOKEN]", data)
        return data

    async def execute_impl(
        self,
        session: Optional[AsyncSession],
        context: ToolExecutionContext,
        input_data: Dict[str, Any]
    ) -> ToolExecutionResult:
        raise NotImplementedError


# ----------------- TOOL IMPLEMENTATIONS (REAL SERVICES) -----------------

class SearchDocumentsTool(AgentTool):
    id = "tool_search_documents"
    name = "search_documents"
    description = "Search authorized workspace files and documents by keyword or file type."
    category = ToolCategory.SEARCH
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Keyword search query to match against document names and descriptions"},
            "mime_type": {"type": "string", "description": "Optional MIME type filter e.g. application/pdf"}
        }
    }
    output_schema = {
        "type": "object",
        "properties": {
            "files": {"type": "array"},
            "count": {"type": "integer"}
        }
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import drive_service
        q = input_data.get("query")
        mt = input_data.get("mime_type")
        files, count = await drive_service.list_drive_files(session, context.workspace_id, search_query=q, mime_type=mt)
        citations = [{"source_type": "document", "source_id": f.get("id"), "title": f.get("name"), "workspace_id": context.workspace_id} for f in files[:5]]
        return ToolExecutionResult(True, {"files": files, "count": count}, tool_name=self.name, risk_level=self.risk_level.value, citations=citations)


class ReadDocumentTool(AgentTool):
    id = "tool_read_document"
    name = "read_document"
    description = "Extract and read text content from an authorized workspace document or Google Doc."
    category = ToolCategory.READ
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "Unique identifier of the target document"}
        },
        "required": ["file_id"]
    }
    output_schema = {
        "type": "object",
        "properties": {
            "file_id": {"type": "string"},
            "name": {"type": "string"},
            "text": {"type": "string"},
            "pages": {"type": "integer"}
        }
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import drive_service
        f_id = input_data.get("file_id")
        try:
            extracted = await drive_service.extract_file_content(session, context.workspace_id, f_id)
            citations = [{"source_type": "document", "source_id": f_id, "title": extracted.get("name", "Document"), "snippet": extracted.get("text", "")[:200], "workspace_id": context.workspace_id}]
            return ToolExecutionResult(True, extracted, tool_name=self.name, risk_level=self.risk_level.value, citations=citations)
        except Exception as exc:
            return ToolExecutionResult(False, {}, str(exc), "DOCUMENT_NOT_FOUND", tool_name=self.name)


class SearchKnowledgeTool(AgentTool):
    id = "tool_search_knowledge"
    name = "search_knowledge"
    description = "Search semantic knowledge base chunks and entity graphs across authorized workspace documents."
    category = ToolCategory.SEARCH
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Natural language query to search knowledge nodes"}
        },
        "required": ["query"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import knowledge_service
        q = input_data.get("query")
        chunks = []
        citations = []
        for chk in knowledge_service._in_memory_chunks.values():
            if q.lower() in chk.get("content", "").lower():
                chunks.append(chk)
                citations.append({
                    "source_type": "knowledge",
                    "source_id": chk.get("document_id", "kb_doc"),
                    "title": f"Knowledge Chunk {chk.get('id', '')[:8]}",
                    "snippet": chk.get("content", "")[:200],
                    "workspace_id": context.workspace_id
                })

        return ToolExecutionResult(True, {"chunks": chunks[:10], "count": len(chunks)}, tool_name=self.name, risk_level=self.risk_level.value, citations=citations)


class SearchMemoryTool(AgentTool):
    id = "tool_search_memory"
    name = "search_memory"
    description = "Search approved long-term memories and episodic experiences for active workspace."
    category = ToolCategory.SEARCH
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Semantic keyword query to search memories"},
            "type": {"type": "string", "description": "Optional filter by memory category: EPISODIC, SEMANTIC, PROCEDURAL, WORKING"}
        },
        "required": ["query"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import memory_service
        q = input_data.get("query")
        tf = input_data.get("type")
        mems = await memory_service.retrieve_relevant_memories(session, context.workspace_id, query_context=q, limit=10, type_filter=tf)
        citations = [{
            "source_type": "memory",
            "source_id": m.get("id"),
            "title": m.get("title", "Memory Record"),
            "snippet": m.get("content", "")[:200],
            "workspace_id": context.workspace_id
        } for m in mems]
        return ToolExecutionResult(True, {"memories": mems, "count": len(mems)}, tool_name=self.name, risk_level=self.risk_level.value, citations=citations)


class GetMissionTool(AgentTool):
    id = "tool_get_mission"
    name = "get_mission"
    description = "Retrieve details, goal, steps, and progress of a workspace Mission."
    category = ToolCategory.READ
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "mission_id": {"type": "string", "description": "Unique ID of the mission"}
        },
        "required": ["mission_id"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import mission_service
        m_id = input_data.get("mission_id")
        m = await mission_service.get_mission_by_id(session, context.workspace_id, m_id)
        if not m:
            return ToolExecutionResult(False, {}, f"Mission '{m_id}' not found in active workspace.", "NOT_FOUND", tool_name=self.name)
        citations = [{
            "source_type": "mission_step",
            "source_id": m_id,
            "title": m.get("title") or m.get("name") or "Mission",
            "workspace_id": context.workspace_id
        }]
        return ToolExecutionResult(True, {"mission": m}, tool_name=self.name, risk_level=self.risk_level.value, citations=citations)


class GetWorkspaceContextTool(AgentTool):
    id = "tool_get_workspace_context"
    name = "get_workspace_context"
    description = "Retrieve summary context, active member count, and settings for current workspace."
    category = ToolCategory.READ
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {}
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import workspace_service
        members = await workspace_service.list_workspace_members(session, context.workspace_id)
        return ToolExecutionResult(
            True,
            {
                "workspace_id": context.workspace_id,
                "tenant_id": context.tenant_id,
                "members_count": len(members),
                "active_members": [{"user_id": m.get("user_id"), "role": m.get("role")} for m in members[:10]]
            },
            tool_name=self.name,
            risk_level=self.risk_level.value
        )


class CreateContentTool(AgentTool):
    id = "tool_create_content"
    name = "create_content"
    description = "Create a new draft content document in Content Studio."
    category = ToolCategory.CONTENT
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the content item"},
            "content": {"type": "string", "description": "Text body or markdown content"},
            "type": {"type": "string", "description": "Content type: article, social_post, brief, script", "default": "article"}
        },
        "required": ["title", "content"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import content_service
        payload = ContentCreate(
            title=input_data.get("title"),
            content=input_data.get("content"),
            type=input_data.get("type", "article"),
            status="draft"
        )
        item = await content_service.create_content(session, context.workspace_id, context.user_id, payload)
        return ToolExecutionResult(True, {"content_item": item}, tool_name=self.name, risk_level=self.risk_level.value)


class TriggerWorkflowTool(AgentTool):
    id = "tool_trigger_workflow"
    name = "trigger_workflow"
    description = "Trigger a configured automated workflow in active workspace."
    category = ToolCategory.WORKFLOW
    risk_level = ToolRiskLevel.HIGH
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "workflow_id": {"type": "string", "description": "Identifier of the workflow to execute"},
            "inputs": {"type": "object", "description": "Input parameters for workflow run"}
        },
        "required": ["workflow_id"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import workflow_engine
        wf_id = input_data.get("workflow_id")
        wf_inputs = input_data.get("inputs", {})
        run_id = f"wf_run_{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        run_dict = {
            "id": run_id,
            "workflow_id": wf_id,
            "workspace_id": context.workspace_id,
            "status": "QUEUED",
            "inputs": wf_inputs,
            "created_at": now_iso
        }
        workflow_engine._in_memory_runs[run_id] = run_dict
        return ToolExecutionResult(True, {"run_id": run_id, "status": "QUEUED", "workflow_id": wf_id}, tool_name=self.name, risk_level=self.risk_level.value)


class SearchMissionsTool(AgentTool):
    id = "tool_search_missions"
    name = "search_missions"
    description = "Search active or completed workspace missions by keyword or status filter."
    category = ToolCategory.SEARCH
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search keyword query"},
            "status": {"type": "string", "description": "Filter by mission status (DRAFT, QUEUED, RUNNING, COMPLETED)"}
        }
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import mission_service
        q = input_data.get("query")
        st = input_data.get("status")
        items, count = await mission_service.list_workspace_missions(session, context.workspace_id, status_filter=st, search_query=q)
        return ToolExecutionResult(True, {"missions": items, "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class CreateMissionTool(AgentTool):
    id = "tool_create_mission"
    name = "create_mission"
    description = "Create a new workspace Mission in DRAFT status."
    category = ToolCategory.DATA
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title of the new mission"},
            "goal": {"type": "string", "description": "Primary objective of the mission"},
            "description": {"type": "string", "description": "Optional contextual description"}
        },
        "required": ["title", "goal"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import mission_service
        payload = MissionCreate(
            title=input_data.get("title"),
            goal=input_data.get("goal"),
            description=input_data.get("description", "")
        )
        m = await mission_service.create_mission(session, context.workspace_id, payload)
        return ToolExecutionResult(True, {"mission": m}, tool_name=self.name, risk_level=self.risk_level.value)


class CreateMemoryCandidateTool(AgentTool):
    id = "tool_create_memory_candidate"
    name = "create_memory_candidate"
    description = "Propose a structured memory candidate with provenance for user review."
    category = ToolCategory.DATA
    risk_level = ToolRiskLevel.MEDIUM
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Memory summary title"},
            "content": {"type": "string", "description": "Detailed memory knowledge content"},
            "type": {"type": "string", "description": "Memory tier: EPISODIC, SEMANTIC, PROCEDURAL, WORKING", "default": "SEMANTIC"}
        },
        "required": ["title", "content"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import memory_service
        cand = await memory_service.create_candidate(
            workspace_id=context.workspace_id,
            title=input_data.get("title"),
            content=input_data.get("content"),
            type_name=input_data.get("type", "SEMANTIC"),
            source_type="agent_run",
            source_id=context.agent_run_id,
            created_by=context.agent_id or "agent"
        )
        return ToolExecutionResult(True, {"candidate": cand}, tool_name=self.name, risk_level=self.risk_level.value)


class GetCalendarEventsTool(AgentTool):
    id = "tool_get_calendar_events"
    name = "get_calendar_events"
    description = "Get normalized Google Calendar events for active workspace."
    category = ToolCategory.READ
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "timeframe": {"type": "string", "description": "Timeframe filter e.g. next_7_days, next_30_days"}
        }
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import calendar_service
        tf = input_data.get("timeframe", "next_7_days")
        events, count = await calendar_service.list_events(session, context.workspace_id, timeframe=tf)
        return ToolExecutionResult(True, {"events": events, "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


class CreateCalendarEventTool(AgentTool):
    id = "tool_create_calendar_event"
    name = "create_calendar_event"
    description = "Schedule a new event on workspace calendar (External side-effect, requires approval)."
    category = ToolCategory.COMMUNICATION
    risk_level = ToolRiskLevel.HIGH
    required_permissions = ["write"]
    input_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "Event title or summary"},
            "start_time": {"type": "string", "description": "ISO format start timestamp"},
            "end_time": {"type": "string", "description": "ISO format end timestamp"},
            "description": {"type": "string", "description": "Optional event details"}
        },
        "required": ["summary", "start_time", "end_time"]
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import calendar_service
        from app.schemas.calendar import CalendarEventCreate
        payload = CalendarEventCreate(
            summary=input_data.get("summary"),
            start_time=input_data.get("start_time"),
            end_time=input_data.get("end_time"),
            description=input_data.get("description")
        )
        evt = await calendar_service.create_event(session, context.workspace_id, payload)
        return ToolExecutionResult(True, {"event": evt}, tool_name=self.name, risk_level=self.risk_level.value)


class SearchGmailTool(AgentTool):
    id = "tool_search_gmail"
    name = "search_gmail"
    description = "Search read-only Gmail threads and messages metadata."
    category = ToolCategory.SEARCH
    risk_level = ToolRiskLevel.LOW
    required_permissions = ["read"]
    input_schema = {
        "type": "object",
        "properties": {
            "filter": {"type": "string", "description": "Filter type e.g. unread, starred, all"}
        }
    }

    async def execute_impl(self, session, context, input_data):
        from app.services import gmail_service
        flt = input_data.get("filter", "all")
        threads, count = await gmail_service.list_threads(session, context.workspace_id, filter_type=flt)
        return ToolExecutionResult(True, {"threads": threads, "count": count}, tool_name=self.name, risk_level=self.risk_level.value)


# ----------------- CENTRALIZED TOOL REGISTRY -----------------

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, AgentTool] = {}
        self._register_default_tools()

    def register_tool(self, tool: AgentTool) -> None:
        self._tools[tool.name] = tool
        self._tools[tool.id] = tool

    def get_tool(self, name_or_id: str) -> Optional[AgentTool]:
        return self._tools.get(name_or_id)

    def list_all_tools(self) -> List[AgentTool]:
        """Returns unique registered tools."""
        seen = set()
        unique = []
        for t in self._tools.values():
            if t.id not in seen:
                seen.add(t.id)
                unique.append(t)
        return unique

    def _register_default_tools(self):
        # 1. search_documents / search_drive_files
        search_docs = SearchDocumentsTool()
        self.register_tool(search_docs)
        self._tools["search_drive_files"] = search_docs

        # 2. read_document / get_drive_file_content
        read_doc = ReadDocumentTool()
        self.register_tool(read_doc)
        self._tools["get_drive_file_content"] = read_doc

        # 3. search_knowledge
        self.register_tool(SearchKnowledgeTool())

        # 4. search_memory
        self.register_tool(SearchMemoryTool())

        # 5. get_mission
        self.register_tool(GetMissionTool())

        # 6. get_workspace_context
        self.register_tool(GetWorkspaceContextTool())

        # 7. create_content
        self.register_tool(CreateContentTool())

        # 8. trigger_workflow
        self.register_tool(TriggerWorkflowTool())

        # Additional tools
        self.register_tool(SearchMissionsTool())
        self.register_tool(CreateMissionTool())
        self.register_tool(CreateMemoryCandidateTool())
        self.register_tool(GetCalendarEventsTool())
        self.register_tool(CreateCalendarEventTool())
        self.register_tool(SearchGmailTool())

    def discover_tools_for_agent(
        self,
        workspace_id: str,
        agent: Optional[Dict[str, Any]] = None,
        agent_version: Optional[Dict[str, Any]] = None,
        user_role: str = "member"
    ) -> Tuple[List[AgentTool], List[Dict[str, Any]]]:
        """Capability-aware discovery: returns authorized tools and denied tools with rationale."""
        authorized: List[AgentTool] = []
        denied: List[Dict[str, Any]] = []

        all_tools = self.list_all_tools()
        for t in all_tools:
            if not t.enabled:
                denied.append({"id": t.id, "name": t.name, "reason": "TOOL_DISABLED"})
                continue

            if agent:
                allowed = agent.get("allowed_tools", [])
                if allowed and (t.name not in allowed and t.id not in allowed):
                    denied.append({"id": t.id, "name": t.name, "reason": "AGENT_POLICY_DISALLOWED"})
                    continue

            if agent_version:
                vp = agent_version.get("tool_policy", {})
                v_allowed = vp.get("allowed_tools", [])
                if v_allowed and (t.name not in v_allowed and t.id not in v_allowed):
                    denied.append({"id": t.id, "name": t.name, "reason": "AGENT_VERSION_POLICY_DISALLOWED"})
                    continue

            if t.category == ToolCategory.ADMIN and user_role not in ["admin", "owner"]:
                denied.append({"id": t.id, "name": t.name, "reason": "ADMIN_ROLE_REQUIRED"})
                continue

            authorized.append(t)

        return authorized, denied

    async def execute_tool_call(
        self,
        session: Optional[AsyncSession],
        tool_name: str,
        input_data: Dict[str, Any],
        context: ToolExecutionContext,
        agent: Optional[Dict[str, Any]] = None,
        agent_version: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None
    ) -> ToolExecutionResult:
        """Full governed tool execution pipeline with authorization, idempotency, timeouts, output limits, and audit."""
        start_time = time.time()
        tool = self.get_tool(tool_name)
        if not tool:
            res = ToolExecutionResult(False, {}, f"Tool '{tool_name}' is not registered in system catalog.", "TOOL_NOT_FOUND", tool_name=tool_name)
            self._record_audit_log(session, context, tool_name, "tool_unknown", "NOT_FOUND", False, int((time.time() - start_time) * 1000), "TOOL_NOT_FOUND", input_data, {})
            return res

        # 1. Check Idempotency Cache
        eff_idempotency_key = idempotency_key or context.idempotency_key
        if eff_idempotency_key and eff_idempotency_key in _idempotency_cache:
            cached = _idempotency_cache[eff_idempotency_key]
            logger.info(f"Returning cached idempotent tool result for key: {eff_idempotency_key}")
            return ToolExecutionResult(
                success=cached.get("success", True),
                data=cached.get("data", {}),
                error=cached.get("error"),
                error_code=cached.get("error_code"),
                tool_name=tool.name,
                risk_level=tool.risk_level.value,
                truncated=cached.get("truncated", False)
            )

        # 2. Multi-Level Authorization Check
        is_auth, auth_err, auth_code = await tool.authorize(session, context, agent=agent, agent_version=agent_version)
        if not is_auth:
            res = ToolExecutionResult(False, {}, auth_err, auth_code or "POLICY_DENIED", tool_name=tool.name, risk_level=tool.risk_level.value)
            self._record_audit_log(session, context, tool.name, tool.id, auth_code or "DENIED", False, int((time.time() - start_time) * 1000), auth_code, input_data, {})
            return res

        # 3. Input Validation
        is_valid, val_err = tool.validate(input_data)
        if not is_valid:
            res = ToolExecutionResult(False, {}, val_err, "VALIDATION_ERROR", tool_name=tool.name, risk_level=tool.risk_level.value)
            self._record_audit_log(session, context, tool.name, tool.id, "VALIDATION_ERROR", False, int((time.time() - start_time) * 1000), "VALIDATION_ERROR", input_data, {})
            return res

        # 4. Bounded Execution with Timeout
        timeout_sec = tool.timeout_seconds or (tool.timeout_ms // 1000) or 30
        try:
            raw_res = await asyncio.wait_for(
                tool.execute_impl(session, context, input_data),
                timeout=float(timeout_sec)
            )
        except asyncio.TimeoutError:
            duration_ms = int((time.time() - start_time) * 1000)
            res = ToolExecutionResult(False, {}, f"Tool '{tool.name}' execution timed out after {timeout_sec}s.", "TOOL_TIMEOUT", tool_name=tool.name, risk_level=tool.risk_level.value)
            self._record_audit_log(session, context, tool.name, tool.id, "AUTHORIZED", False, duration_ms, "TOOL_TIMEOUT", input_data, {})
            return res
        except Exception as exc:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Error executing tool '{tool.name}': {exc}", exc_info=True)
            res = ToolExecutionResult(False, {}, str(exc), "EXECUTION_ERROR", tool_name=tool.name, risk_level=tool.risk_level.value)
            self._record_audit_log(session, context, tool.name, tool.id, "AUTHORIZED", False, duration_ms, "EXECUTION_ERROR", input_data, {})
            return res

        # 5. Output Normalization & Limits
        norm_data, is_truncated = tool.normalize(raw_res.data)
        duration_ms = int((time.time() - start_time) * 1000)

        final_res = ToolExecutionResult(
            success=raw_res.success,
            data=norm_data,
            error=raw_res.error,
            error_code=raw_res.error_code,
            tool_name=tool.name,
            risk_level=tool.risk_level.value,
            truncated=is_truncated or raw_res.truncated,
            citations=raw_res.citations
        )

        # 6. Cache Idempotent Side-Effects
        if eff_idempotency_key and raw_res.success:
            _idempotency_cache[eff_idempotency_key] = final_res.to_dict()

        # 7. Record Tool Call Audit Log
        self._record_audit_log(
            session, context, tool.name, tool.id, "AUTHORIZED", raw_res.success,
            duration_ms, raw_res.error_code, input_data, norm_data, eff_idempotency_key, is_truncated
        )

        return final_res

    def _record_audit_log(
        self,
        session: Optional[AsyncSession],
        context: ToolExecutionContext,
        tool_name: str,
        tool_id: str,
        auth_res: str,
        success: bool,
        duration_ms: int,
        error_code: Optional[str],
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        idempotency_key: Optional[str] = None,
        truncated: bool = False
    ):
        now_iso = datetime.now(timezone.utc).isoformat()
        audit_id = str(uuid.uuid4())
        audit_entry = {
            "id": audit_id,
            "tool_id": tool_id,
            "tool_name": tool_name,
            "agent_run_id": context.agent_run_id,
            "mission_id": context.mission_id,
            "workspace_id": context.workspace_id,
            "user_id": context.user_id,
            "timestamp": now_iso,
            "authorization_result": auth_res,
            "policy_result": {"status": auth_res},
            "duration_ms": duration_ms,
            "status": "SUCCESS" if success else "FAILED",
            "error_code": error_code,
            "idempotency_key": idempotency_key,
            "truncated": truncated,
            "input_sanitized": AgentTool()._sanitize_data(input_data),
            "output_sanitized": AgentTool()._sanitize_data(output_data)
        }
        _in_memory_tool_audit_logs.append(audit_entry)


    @classmethod
    def list_tools(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "risk_level": t.risk_level.value,
                "required_permissions": t.required_permissions,
                "input_schema": t.input_schema,
                "output_schema": t.output_schema,
                "category": t.category.value,
                "timeout_seconds": t.timeout_seconds,
                "enabled": t.enabled
            }
            for t in global_tool_registry.list_all_tools()
        ]


# Singleton Registry
global_tool_registry = ToolRegistry()


def get_tool_registry() -> ToolRegistry:
    return global_tool_registry


async def authorize_and_execute_tool(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    user_role: str,
    agent: Optional[Dict[str, Any]],
    agent_version: Optional[Dict[str, Any]],
    tool_name: str,
    input_data: Dict[str, Any],
    idempotency_key: Optional[str] = None,
    approval_status: Optional[str] = None,
    mission_id: Optional[str] = None,
    agent_run_id: Optional[str] = None
) -> ToolExecutionResult:
    context = ToolExecutionContext(
        user_id=user_id,
        workspace_id=workspace_id,
        user_role=user_role,
        agent_id=agent.get("id") if agent else None,
        agent_version_id=agent_version.get("id") if agent_version else None,
        agent_run_id=agent_run_id,
        mission_id=mission_id,
        approval_status=approval_status,
        idempotency_key=idempotency_key
    )
    registry = get_tool_registry()
    return await registry.execute_tool_call(
        session=session,
        tool_name=tool_name,
        input_data=input_data,
        context=context,
        agent=agent,
        agent_version=agent_version,
        idempotency_key=idempotency_key
    )
