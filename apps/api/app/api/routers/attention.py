from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.attention import AttentionItemResponse, AttentionListResponse, AttentionCountResponse
from app.services import attention_service

router = APIRouter()

@router.get("/attention", response_model=AttentionListResponse)
async def list_attention_items(
    status_filter: str = Query("open", alias="status", description="Filter by status (open, snoozed, resolved, dismissed, all)"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionListResponse:
    items, total, open_count = await attention_service.list_attention_items(db, ws_ctx.workspace_id, status_filter=status_filter)
    return AttentionListResponse(
        items=[AttentionItemResponse(**item) for item in items],
        total=total,
        open_count=open_count
    )

@router.get("/attention/count", response_model=AttentionCountResponse)
async def get_attention_count(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionCountResponse:
    count = await attention_service.get_open_attention_count(db, ws_ctx.workspace_id)
    return AttentionCountResponse(open_count=count)

@router.post("/attention/reconcile", response_model=AttentionListResponse)
async def reconcile_attention(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionListResponse:
    items = await attention_service.reconcile_attention(db, ws_ctx.workspace_id)
    return AttentionListResponse(
        items=[AttentionItemResponse(**item) for item in items],
        total=len(items),
        open_count=len(items)
    )

@router.post("/attention/{id}/resolve", response_model=AttentionItemResponse)
async def resolve_attention(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionItemResponse:
    item = await attention_service.resolve_attention_item(db, ws_ctx.workspace_id, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attention item not found in active workspace."
        )
    return AttentionItemResponse(**item)

@router.post("/attention/{id}/dismiss", response_model=AttentionItemResponse)
async def dismiss_attention(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionItemResponse:
    item = await attention_service.dismiss_attention_item(db, ws_ctx.workspace_id, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attention item not found in active workspace."
        )
    return AttentionItemResponse(**item)

@router.post("/attention/{id}/snooze", response_model=AttentionItemResponse)
async def snooze_attention(
    id: str,
    minutes: int = Query(60, description="Snooze duration in minutes"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> AttentionItemResponse:
    item = await attention_service.snooze_attention_item(db, ws_ctx.workspace_id, id, minutes=minutes)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attention item not found in active workspace."
        )
    return AttentionItemResponse(**item)
