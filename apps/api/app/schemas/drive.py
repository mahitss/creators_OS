from pydantic import BaseModel
from typing import List, Optional

class DriveFileResponse(BaseModel):
    id: str
    workspace_id: str
    external_file_id: str
    name: str
    mime_type: str
    description: str
    web_url: str
    owner_name: str
    size_bytes: int
    modified_time: str

class DriveFileListResponse(BaseModel):
    files: List[DriveFileResponse]
    total: int

class DriveStatusResponse(BaseModel):
    is_connected: bool
    last_synced_at: Optional[str] = None
    file_count: int

class DocumentContentResponse(BaseModel):
    file_id: str
    name: str
    mime_type: str
    text: str
    pages: int
    truncated: bool

class MissionDocumentReferenceResponse(BaseModel):
    id: str
    mission_id: str
    drive_file_id: str
    file_name: str
    mime_type: str
    web_url: str
    created_at: str
