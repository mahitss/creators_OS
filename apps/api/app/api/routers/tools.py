from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.tools import (
    ToolDefinitionRead,
    ToolListResponse,
    AgentToolDiscoveryResponse,
    ToolAuditLogListResponse,
    ToolCallAuditLogRead
)
from app.services.tool_registry import get_tool_registry, _in_memory_tool_audit_logs
from app.services.agent_service import get_agent_by_id as get_agent

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("", response_model=ToolListResponse)
async def list_tools(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    category: Optional[str] = None
):
    """List all registered tools in system registry."""
    registry = get_tool_registry()
    tools = registry.list_all_tools()

    if category:
        tools = [t for t in tools if t.category.value.upper() == category.upper()]

    tool_reads = [
        ToolDefinitionRead(
            id=t.id,
            name=t.name,
            description=t.description,
            version=t.version,
            category=t.category.value,
            input_schema=t.input_schema,
            output_schema=t.output_schema,
            required_permissions=t.required_permissions,
            risk_level=t.risk_level.value,
            timeout_ms=t.timeout_ms,
            timeout_seconds=t.timeout_seconds,
            enabled=t.enabled
        )
        for t in tools
    ]

    return ToolListResponse(tools=tool_reads, total=len(tool_reads))


@router.get("/audit-logs", response_model=ToolAuditLogListResponse)
async def list_tool_audit_logs(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    tool_id: Optional[str] = None,
    agent_run_id: Optional[str] = None,
    limit: int = 50
):
    """Retrieve governed tool execution audit logs for active workspace."""
    workspace_id = ws_ctx.workspace_id
    logs = [
        l for l in _in_memory_tool_audit_logs
        if l.get("workspace_id") == workspace_id
    ]

    if tool_id:
        logs = [l for l in logs if l.get("tool_id") == tool_id or l.get("tool_name") == tool_id]
    if agent_run_id:
        logs = [l for l in logs if l.get("agent_run_id") == agent_run_id]

    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    selected = logs[:limit]

    return ToolAuditLogListResponse(
        logs=[ToolCallAuditLogRead(**l) for l in selected],
        total=len(logs)
    )


@router.get("/{tool_id}", response_model=ToolDefinitionRead)
async def get_tool_details(
    tool_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace)
):
    """Retrieve detailed schema and risk level for a single tool."""
    registry = get_tool_registry()
    tool = registry.get_tool(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_id}' not found in registry.")

    return ToolDefinitionRead(
        id=tool.id,
        name=tool.name,
        description=tool.description,
        version=tool.version,
        category=tool.category.value,
        input_schema=tool.input_schema,
        output_schema=tool.output_schema,
        required_permissions=tool.required_permissions,
        risk_level=tool.risk_level.value,
        timeout_ms=tool.timeout_ms,
        timeout_seconds=tool.timeout_seconds,
        enabled=tool.enabled
    )


@router.get("/agents/{agent_id}/tools", response_model=AgentToolDiscoveryResponse)
async def discover_agent_tools(
    agent_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    """Capability-aware discovery: returns permitted tools and denied tools for an agent."""
    workspace_id = ws_ctx.workspace_id
    agent_data = await get_agent(db, workspace_id, agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found in active workspace.")

    registry = get_tool_registry()
    authorized, denied = registry.discover_tools_for_agent(
        workspace_id=workspace_id,
        agent=agent_data,
        user_role=ws_ctx.role or "member"
    )

    auth_reads = [
        ToolDefinitionRead(
            id=t.id,
            name=t.name,
            description=t.description,
            version=t.version,
            category=t.category.value,
            input_schema=t.input_schema,
            output_schema=t.output_schema,
            required_permissions=t.required_permissions,
            risk_level=t.risk_level.value,
            timeout_ms=t.timeout_ms,
            timeout_seconds=t.timeout_seconds,
            enabled=t.enabled
        )
        for t in authorized
    ]

    return AgentToolDiscoveryResponse(
        agent_id=agent_id,
        workspace_id=workspace_id,
        authorized_tools=auth_reads,
        denied_tools=denied,
        total_authorized=len(auth_reads),
        total_denied=len(denied)
    )
