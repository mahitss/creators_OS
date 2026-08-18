from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.drive import (
    DriveFileResponse,
    DriveFileListResponse,
    DriveStatusResponse,
    DocumentContentResponse,
    MissionDocumentReferenceResponse,
)
from app.services import drive_service, integration_service

router = APIRouter()

@router.get("/drive/status", response_model=DriveStatusResponse)
async def get_drive_status(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveStatusResponse:
    conn = await integration_service.get_connection(db, ws_ctx.workspace_id, "google")
    if not conn or conn["status"] != "connected":
        return DriveStatusResponse(
            is_connected=False,
            last_synced_at=None,
            file_count=0
        )

    files, total = await drive_service.list_drive_files(db, ws_ctx.workspace_id)
    return DriveStatusResponse(
        is_connected=True,
        last_synced_at=conn.get("last_synced_at"),
        file_count=total
    )

@router.get("/drive/files", response_model=DriveFileListResponse)
async def list_drive_files(
    q: Optional[str] = Query(None, description="Search query across file name and description"),
    mime_type: Optional[str] = Query(None, description="Filter by MIME type"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveFileListResponse:
    files, total = await drive_service.list_drive_files(db, ws_ctx.workspace_id, search_query=q, mime_type=mime_type)
    return DriveFileListResponse(
        files=[DriveFileResponse(**f) for f in files],
        total=total
    )

@router.get("/drive/files/{id}", response_model=DriveFileResponse)
async def get_drive_file(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveFileResponse:
    f = await drive_service.get_drive_file(db, ws_ctx.workspace_id, id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drive file not found in active workspace."
        )
    return DriveFileResponse(**f)

@router.get("/drive/files/{id}/content", response_model=DocumentContentResponse)
async def extract_drive_content(
    id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DocumentContentResponse:
    try:
        content_data = await drive_service.extract_file_content(db, ws_ctx.workspace_id, id)
        return DocumentContentResponse(**content_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/drive/sync", response_model=DriveStatusResponse)
async def sync_drive(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveStatusResponse:
    try:
        status_data = await drive_service.sync_drive_data(db, ws_ctx.workspace_id)
        return DriveStatusResponse(**status_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/missions/{mission_id}/documents", response_model=List[MissionDocumentReferenceResponse])
async def list_mission_documents(
    mission_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[MissionDocumentReferenceResponse]:
    try:
        refs = await drive_service.list_mission_documents(db, ws_ctx.workspace_id, mission_id)
        return [MissionDocumentReferenceResponse(**r) for r in refs]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/missions/{mission_id}/documents/{file_id}", response_model=MissionDocumentReferenceResponse)
async def attach_document_to_mission(
    mission_id: str,
    file_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionDocumentReferenceResponse:
    try:
        ref = await drive_service.attach_document_to_mission(db, ws_ctx.workspace_id, mission_id, file_id)
        return MissionDocumentReferenceResponse(**ref)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete("/missions/{mission_id}/documents/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def detach_document_from_mission(
    mission_id: str,
    file_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
):
    try:
        await drive_service.detach_document_from_mission(db, ws_ctx.workspace_id, mission_id, file_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
