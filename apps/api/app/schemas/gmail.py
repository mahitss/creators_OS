from pydantic import BaseModel
from typing import List, Optional

class GmailThreadResponse(BaseModel):
    id: str
    workspace_id: str
    external_thread_id: str
    subject: str
    last_message_at: str
    message_count: int
    snippet: str

class GmailMessageResponse(BaseModel):
    id: str
    workspace_id: str
    thread_id: str
    external_message_id: str
    sender_name: str
    sender_email: str
    subject: str
    snippet: str
    received_at: str
    is_unread: bool
    label_ids: List[str]
    ai_classification: str
    ai_summary: Optional[str] = None
    full_body: Optional[str] = None

class GmailThreadListResponse(BaseModel):
    threads: List[GmailThreadResponse]
    total: int

class GmailStatusResponse(BaseModel):
    is_connected: bool
    last_synced_at: Optional[str] = None
    thread_count: int
    unread_count: int

class EmailSummaryResponse(BaseModel):
    message_id: str
    classification: str
    importance: str
    summary: str
    reason: str

class CreateMissionFromEmailResponse(BaseModel):
    mission_id: str
    title: str
    description: str
