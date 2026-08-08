from pydantic import BaseModel
from typing import List, Optional

class CalendarResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    timezone: str
    is_primary: bool
    created_at: str

class CalendarEventResponse(BaseModel):
    id: str
    workspace_id: str
    calendar_id: str
    external_event_id: str
    title: str
    description: str
    location: str
    start_at: str
    end_at: str
    timezone: str
    status: str
    organizer: str
    attendee_count: int
    is_all_day: bool

class CalendarEventListResponse(BaseModel):
    events: List[CalendarEventResponse]
    total: int

class CalendarSyncStatusResponse(BaseModel):
    is_connected: bool
    last_synced_at: Optional[str] = None
    calendar_count: int
    event_count: int
