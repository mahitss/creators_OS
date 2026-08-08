from pydantic import BaseModel
from typing import List, Dict, Any

class DeliverableSuggestionResponse(BaseModel):
    id: str
    workspace_id: str
    mission_id: str
    type: str
    title: str
    reason: str
    source_data: Dict[str, Any] = {}
    confidence: float
    status: str
    created_at: str
    updated_at: str

class DeliverableSuggestionListResponse(BaseModel):
    suggestions: List[DeliverableSuggestionResponse]
    total: int
