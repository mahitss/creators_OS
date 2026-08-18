from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentGenerateRequest,
    ContentResponse,
    ContentListResponse,
)
from app.services import content_service

router = APIRouter()

@router.get("/content", response_model=ContentListResponse)
async def list_content(
    type: Optional[str] = Query(None, description="Filter by content type"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    mission_id: Optional[str] = Query(None, description="Filter by mission ID"),
    search: Optional[str] = Query(None, description="Text search in title or content"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentListResponse:
    items, total = await content_service.list_content(
        db, ws_ctx.workspace_id, type_filter=type, status_filter=status_filter, mission_id_filter=mission_id, search_query=search
    )
    return ContentListResponse(
        content_items=[ContentResponse(**c) for c in items],
        total=total
    )

@router.post("/content", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    payload: ContentCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.create_content(db, ws_ctx.workspace_id, ws_ctx.user_id, payload)
    return ContentResponse(**c)

@router.get("/content/{id}", response_model=ContentResponse)
async def get_content(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.get_content_by_id(db, ws_ctx.workspace_id, id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.patch("/content/{id}", response_model=ContentResponse)
async def update_content(
    id: str,
    payload: ContentUpdate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.update_content(db, ws_ctx.workspace_id, id, payload)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.post("/content/{id}/archive", response_model=ContentResponse)
async def archive_content(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.archive_content(db, ws_ctx.workspace_id, id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.post("/content/{id}/approve", response_model=ContentResponse)
async def approve_content(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.approve_content(db, ws_ctx.workspace_id, id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.post("/content/{id}/generate", response_model=ContentResponse)
async def generate_content_ai(
    id: str,
    payload: ContentGenerateRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.generate_content_ai(db, ws_ctx.workspace_id, id, payload)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)
