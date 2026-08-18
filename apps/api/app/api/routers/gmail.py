from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.gmail import (
    GmailThreadResponse,
    GmailMessageResponse,
    GmailThreadListResponse,
    GmailStatusResponse,
    EmailSummaryResponse,
    CreateMissionFromEmailResponse,
)
from app.services import gmail_service, integration_service

router = APIRouter()

@router.get("/gmail/status", response_model=GmailStatusResponse)
async def get_gmail_status(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> GmailStatusResponse:
    conn = await integration_service.get_connection(db, ws_ctx.workspace_id, "google")
    if not conn or conn["status"] != "connected":
        return GmailStatusResponse(
            is_connected=False,
            last_synced_at=None,
            thread_count=0,
            unread_count=0
        )

    threads, total_threads = await gmail_service.list_threads(db, ws_ctx.workspace_id, filter_type="all")
    unread_threads, unread_count = await gmail_service.list_threads(db, ws_ctx.workspace_id, filter_type="unread")

    return GmailStatusResponse(
        is_connected=True,
        last_synced_at=conn.get("last_synced_at"),
        thread_count=total_threads,
        unread_count=unread_count
    )

@router.get("/gmail/threads", response_model=GmailThreadListResponse)
async def list_gmail_threads(
    filter_type: str = Query("all", alias="filter", description="Filter threads (all, unread, needs_response)"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> GmailThreadListResponse:
    threads, total = await gmail_service.list_threads(db, ws_ctx.workspace_id, filter_type=filter_type)
    return GmailThreadListResponse(
        threads=[GmailThreadResponse(**t) for t in threads],
        total=total
    )

@router.get("/gmail/messages/{id}", response_model=GmailMessageResponse)
async def get_gmail_message(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> GmailMessageResponse:
    msg = await gmail_service.get_message(db, ws_ctx.workspace_id, id)
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gmail message not found in active workspace."
        )
    return GmailMessageResponse(**msg)

@router.post("/gmail/messages/{id}/summarize", response_model=EmailSummaryResponse)
async def summarize_email(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> EmailSummaryResponse:
    try:
        summary_data = await gmail_service.classify_and_summarize_message(db, ws_ctx.workspace_id, id)
        return EmailSummaryResponse(**summary_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post("/gmail/messages/{id}/create-mission", response_model=CreateMissionFromEmailResponse)
async def create_mission_from_email(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> CreateMissionFromEmailResponse:
    try:
        result = await gmail_service.create_mission_from_email(db, ws_ctx.workspace_id, id)
        return CreateMissionFromEmailResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post("/gmail/sync", response_model=GmailStatusResponse)
async def sync_gmail(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> GmailStatusResponse:
    try:
        status_data = await gmail_service.sync_gmail_data(db, ws_ctx.workspace_id)
        return GmailStatusResponse(**status_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
