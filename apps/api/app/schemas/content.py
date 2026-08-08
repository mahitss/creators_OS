from pydantic import BaseModel, Field
from typing import List, Optional

class ContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    type: str = Field("article", pattern="^(article|script|social_post|email|report|outline)$")
    content: str = Field("", description="Initial Markdown or plain text content")
    mission_id: Optional[str] = None

class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, pattern="^(article|script|social_post|email|report|outline)$")
    status: Optional[str] = Field(None, pattern="^(draft|in_review|approved|archived)$")
    content: Optional[str] = None
    mission_id: Optional[str] = None

class ContentGenerateRequest(BaseModel):
    intent: str = Field("draft", pattern="^(draft|rewrite|expand|summarize|improve)$")
    custom_prompt: Optional[str] = None

class ContentResponse(BaseModel):
    id: str
    workspace_id: str
    mission_id: Optional[str] = None
    title: str
    type: str
    status: str
    content: str
    created_by: str
    created_at: str
    updated_at: str
    published_at: Optional[str] = None
    archived_at: Optional[str] = None
    mission_title: Optional[str] = None

class ContentListResponse(BaseModel):
    content_items: List[ContentResponse]
    total: int
