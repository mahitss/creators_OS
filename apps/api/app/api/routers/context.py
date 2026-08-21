from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.context import (
    ContextPreviewRequest,
    ContextPreviewResponse,
    ContextSectionRead,
    CitationItemRead,
    ContextSnapshotRead
)
from app.services.agent_context import ContextAssembler, get_context_snapshot
from app.services.agent_service import get_agent_by_id as get_agent, list_agent_versions

router = APIRouter(prefix="/context", tags=["Context Fabric"])


@router.post("/preview", response_model=ContextPreviewResponse)
async def preview_context(
    payload: ContextPreviewRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
):
    """Preview assembled model context, citations, and token budget without executing model inference."""
    workspace_id = ws_ctx.workspace_id
    agent_data = await get_agent(db, workspace_id, payload.agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found in active workspace.")

    # Fetch version if specified
    agent_version = {}
    if payload.agent_version_id:
        versions = await list_agent_versions(db, workspace_id, payload.agent_id)
        for v in versions:
            if v.get("id") == payload.agent_version_id:
                agent_version = v
                break

    assembler = ContextAssembler(workspace_id=workspace_id)
    res = await assembler.assemble_context(
        session=db,
        agent=agent_data,
        agent_version=agent_version,
        mission_id=payload.mission_id,
        goal=payload.goal or "",
        user_context=payload.user_context,
        max_context_tokens=payload.max_context_tokens or 16384
    )

    sections_read = [
        ContextSectionRead(
            name=s["name"],
            content=s["content"],
            estimated_tokens=s["estimated_tokens"],
            is_untrusted=s.get("is_untrusted", False)
        )
        for s in res["sections"]
    ]

    citations_read = [
        CitationItemRead(
            source_type=c["source_type"],
            source_id=c["source_id"],
            title=c["title"],
            snippet=c.get("snippet"),
            workspace_id=c["workspace_id"],
            confidence=c.get("confidence", 1.0)
        )
        for c in res["citations"]
    ]

    return ContextPreviewResponse(
        sections=sections_read,
        total_estimated_tokens=res["total_estimated_tokens"],
        token_ceiling=res["token_ceiling"],
        is_budget_exceeded=res["is_budget_exceeded"],
        citations=citations_read,
        sources=res["sources_used"]
    )


@router.get("/snapshots/{agent_run_id}", response_model=ContextSnapshotRead)
async def retrieve_context_snapshot(
    agent_run_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace)
):
    """Retrieve exact context snapshot for reproducible execution replay."""
    workspace_id = ws_ctx.workspace_id
    snapshot = await get_context_snapshot(agent_run_id)
    if not snapshot or snapshot.get("workspace_id") != workspace_id:
        raise HTTPException(status_code=404, detail=f"Context snapshot for run '{agent_run_id}' not found.")

    return ContextSnapshotRead(
        id=snapshot["id"],
        agent_run_id=snapshot["agent_run_id"],
        workspace_id=snapshot["workspace_id"],
        sources=snapshot.get("sources", []),
        memory_ids=snapshot.get("memory_ids", []),
        knowledge_ids=snapshot.get("knowledge_ids", []),
        document_ids=snapshot.get("document_ids", []),
        policy_version=str(snapshot.get("policy_version", "v1")),
        agent_version_id=snapshot.get("agent_version_id"),
        token_budget=snapshot.get("token_budget", 16384),
        estimated_tokens=snapshot.get("estimated_tokens", 0),
        created_at=snapshot.get("created_at", "")
    )
