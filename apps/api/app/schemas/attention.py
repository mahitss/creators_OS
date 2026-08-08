from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ActionLink(BaseModel):
    label: str
    href: str

class AttentionItemResponse(BaseModel):
    id: str
    workspace_id: str
    type: str
    title: str
    description: str
    severity: str
    source_type: str
    source_id: str
    status: str
    primary_action: ActionLink
    created_at: str
    updated_at: str
    snoozed_until: Optional[str] = None
    metadata_dict: Dict[str, Any] = {}

class AttentionListResponse(BaseModel):
    items: List[AttentionItemResponse]
    total: int
    open_count: int

class AttentionCountResponse(BaseModel):
    open_count: int
