from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.drive import (
    DriveFileResponse,
    DriveFileListResponse,
    DriveStatusResponse,
    DocumentContentResponse,
    MissionDocumentReferenceResponse,
)
from app.services import drive_service, integration_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/drive/status", response_model=DriveStatusResponse)
async def get_drive_status(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveStatusResponse:
    conn = await integration_service.get_connection(db, workspace_id, "google")
    if not conn or conn["status"] != "connected":
        return DriveStatusResponse(
            is_connected=False,
            last_synced_at=None,
            file_count=0
        )

    files, total = await drive_service.list_drive_files(db, workspace_id)
    return DriveStatusResponse(
        is_connected=True,
        last_synced_at=conn.get("last_synced_at"),
        file_count=total
    )

@router.get("/drive/files", response_model=DriveFileListResponse)
async def list_drive_files(
    q: Optional[str] = Query(None, description="Search query across file name and description"),
    mime_type: Optional[str] = Query(None, description="Filter by MIME type"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveFileListResponse:
    files, total = await drive_service.list_drive_files(db, workspace_id, search_query=q, mime_type=mime_type)
    return DriveFileListResponse(
        files=[DriveFileResponse(**f) for f in files],
        total=total
    )

@router.get("/drive/files/{id}", response_model=DriveFileResponse)
async def get_drive_file(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveFileResponse:
    f = await drive_service.get_drive_file(db, workspace_id, id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drive file not found in active workspace."
        )
    return DriveFileResponse(**f)

@router.get("/drive/files/{id}/content", response_model=DocumentContentResponse)
async def extract_drive_content(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DocumentContentResponse:
    try:
        content_data = await drive_service.extract_file_content(db, workspace_id, id)
        return DocumentContentResponse(**content_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/drive/sync", response_model=DriveStatusResponse)
async def sync_drive(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DriveStatusResponse:
    try:
        status_data = await drive_service.sync_drive_data(db, workspace_id)
        return DriveStatusResponse(**status_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/missions/{mission_id}/documents/{file_id}", response_model=MissionDocumentReferenceResponse)
async def attach_document_to_mission(
    mission_id: str,
    file_id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> MissionDocumentReferenceResponse:
    try:
        ref = await drive_service.attach_document_to_mission(db, workspace_id, mission_id, file_id)
        return MissionDocumentReferenceResponse(**ref)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/missions/{mission_id}/documents", response_model=List[MissionDocumentReferenceResponse])
async def list_mission_documents(
    mission_id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> List[MissionDocumentReferenceResponse]:
    refs = await drive_service.list_mission_documents(db, workspace_id, mission_id)
    return [MissionDocumentReferenceResponse(**r) for r in refs]
