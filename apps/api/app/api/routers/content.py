from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentGenerateRequest,
    ContentResponse,
    ContentListResponse,
)
from app.services import content_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"
DEFAULT_USER_ID = "usr_creator_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> str:
    return x_user_id or DEFAULT_USER_ID

@router.get("/content", response_model=ContentListResponse)
async def list_content(
    type: Optional[str] = Query(None, description="Filter by content type"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    mission_id: Optional[str] = Query(None, description="Filter by mission ID"),
    search: Optional[str] = Query(None, description="Text search in title or content"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentListResponse:
    items, total = await content_service.list_content(
        db, workspace_id, type_filter=type, status_filter=status_filter, mission_id_filter=mission_id, search_query=search
    )
    return ContentListResponse(
        content_items=[ContentResponse(**c) for c in items],
        total=total
    )

@router.post("/content", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    payload: ContentCreate,
    workspace_id: str = Depends(get_current_workspace_id),
    user_id: str = Depends(get_current_user_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.create_content(db, workspace_id, user_id, payload)
    return ContentResponse(**c)

@router.get("/content/{id}", response_model=ContentResponse)
async def get_content(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.get_content_by_id(db, workspace_id, id)
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
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.update_content(db, workspace_id, id, payload)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.post("/content/{id}/archive", response_model=ContentResponse)
async def archive_content(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.archive_content(db, workspace_id, id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)

@router.post("/content/{id}/approve", response_model=ContentResponse)
async def approve_content(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.approve_content(db, workspace_id, id)
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
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    c = await content_service.generate_content_ai(db, workspace_id, id, payload)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content deliverable not found in active workspace."
        )
    return ContentResponse(**c)
