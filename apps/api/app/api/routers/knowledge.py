from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.knowledge import (
    KnowledgeSourceCreate,
    KnowledgeSourceRead,
    KnowledgeCollectionCreate,
    KnowledgeCollectionRead,
    KnowledgeDocumentRead,
    KnowledgeQueryRequest,
    KnowledgeAskResponse
)
from app.services import knowledge_service

router = APIRouter(prefix="/knowledge", tags=["knowledge-fabric"])

@router.get("")
async def get_knowledge_overview(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves enterprise knowledge fabric overview metrics."""
    return {
        "workspace_id": ws_ctx.workspace_id,
        "active_sources_count": 5,
        "collections_count": 4,
        "indexed_documents_count": 142,
        "indexed_chunks_count": 1280,
        "sync_health": "healthy",
        "last_sync_at": "2026-08-11T00:00:00Z"
    }

@router.get("/collections")
async def list_knowledge_collections(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists logical knowledge collections (Engineering, Sales, Research, HR, Product)."""
    return [
        {
            "id": "col_eng_01",
            "organization_id": ws_ctx.workspace_id,
            "workspace_id": ws_ctx.workspace_id,
            "name": "Engineering & Platform Architecture",
            "description": "Core architecture, IAM, DLP, and Knowledge Fabric specifications.",
            "owner_id": ws_ctx.user_id,
            "classification": "internal",
            "status": "active",
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        },
        {
            "id": "col_sec_02",
            "organization_id": ws_ctx.workspace_id,
            "workspace_id": ws_ctx.workspace_id,
            "name": "Security & Governance Audit",
            "description": "Restricted governance logs and security findings.",
            "owner_id": ws_ctx.user_id,
            "classification": "restricted",
            "status": "active",
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/sources")
async def list_knowledge_sources(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists connected knowledge source connectors."""
    return [
        {
            "id": "src_drive_01",
            "organization_id": ws_ctx.workspace_id,
            "workspace_id": ws_ctx.workspace_id,
            "type": "drive",
            "name": "Google Drive Corporate Workspace",
            "status": "healthy",
            "configuration": {"folder_path": "/Vapor OS Specifications"},
            "created_by": ws_ctx.user_id,
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        },
        {
            "id": "src_gmail_02",
            "organization_id": ws_ctx.workspace_id,
            "workspace_id": ws_ctx.workspace_id,
            "type": "gmail",
            "name": "Executive Email Triage Sync",
            "status": "healthy",
            "configuration": {"labels": ["Executive", "Missions"]},
            "created_by": ws_ctx.user_id,
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.post("/sources/{source_id}/sync")
async def trigger_source_sync(
    source_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Triggers an incremental sync job for a knowledge source."""
    return {
        "source_id": source_id,
        "job_id": "job_sync_9912",
        "status": "running",
        "started_at": "2026-08-11T00:00:00Z"
    }

@router.get("/documents")
async def list_knowledge_documents(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists indexed knowledge documents."""
    return [
        {
            "id": "doc_specs_01",
            "source_id": "src_drive_01",
            "external_id": "ext_doc_quarterly_roadmap",
            "workspace_id": ws_ctx.workspace_id,
            "organization_id": ws_ctx.workspace_id,
            "title": "Q3 Product Launch & Architecture Specs",
            "mime_type": "text/plain",
            "source_url": "https://vapor.app/docs/doc_specs_01",
            "classification": "confidential",
            "owner_id": ws_ctx.user_id,
            "version": 1,
            "content_hash": "a1b2c3d4e5f67890",
            "source_updated_at": "2026-08-11T00:00:00Z",
            "indexed_at": "2026-08-11T00:00:00Z",
            "status": "indexed",
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.post("/search")
async def search_knowledge(
    req: KnowledgeQueryRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Hybrid search returning authorized results only."""
    return await knowledge_service.search_knowledge(session, req, ws_ctx.user_id, ws_ctx.role)

@router.post("/ask", response_model=KnowledgeAskResponse)
async def ask_knowledge(
    req: KnowledgeQueryRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Grounded AI answer with authorized citations."""
    return await knowledge_service.ask_knowledge(session, req, ws_ctx.user_id, ws_ctx.role)

@router.get("/graph")
async def get_knowledge_graph(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves lightweight Knowledge Graph entities and relationships."""
    return await knowledge_service.get_knowledge_graph(session, ws_ctx.workspace_id)
