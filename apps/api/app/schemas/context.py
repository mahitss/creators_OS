from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CitationItemRead(BaseModel):
    source_type: str = Field(..., alias="sourceType")
    source_id: str = Field(..., alias="sourceId")
    title: str
    snippet: Optional[str] = None
    workspace_id: str = Field(..., alias="workspaceId")
    confidence: Optional[float] = 1.0

    class Config:
        populate_by_name = True


class ContextSectionRead(BaseModel):
    name: str
    content: str
    estimated_tokens: int = Field(..., alias="estimatedTokens")
    is_untrusted: bool = Field(default=False, alias="isUntrusted")

    class Config:
        populate_by_name = True


class ContextPreviewRequest(BaseModel):
    agent_id: str
    agent_version_id: Optional[str] = None
    mission_id: Optional[str] = None
    goal: Optional[str] = ""
    user_context: Optional[Dict[str, Any]] = None
    max_context_tokens: Optional[int] = 16384


class ContextPreviewResponse(BaseModel):
    sections: List[ContextSectionRead]
    total_estimated_tokens: int = Field(..., alias="totalEstimatedTokens")
    token_ceiling: int = Field(..., alias="tokenCeiling")
    is_budget_exceeded: bool = Field(default=False, alias="isBudgetExceeded")
    citations: List[CitationItemRead]
    sources: List[Dict[str, Any]]

    class Config:
        populate_by_name = True


class ContextSnapshotRead(BaseModel):
    id: str
    agent_run_id: str = Field(..., alias="agentRunId")
    workspace_id: str = Field(..., alias="workspaceId")
    sources: List[Dict[str, Any]]
    memory_ids: List[str] = Field(default_factory=list, alias="memoryIds")
    knowledge_ids: List[str] = Field(default_factory=list, alias="knowledgeIds")
    document_ids: List[str] = Field(default_factory=list, alias="documentIds")
    policy_version: str = Field(default="v1", alias="policyVersion")
    agent_version_id: Optional[str] = Field(None, alias="agentVersionId")
    token_budget: int = Field(default=16384, alias="tokenBudget")
    estimated_tokens: int = Field(default=0, alias="estimatedTokens")
    created_at: str = Field(..., alias="createdAt")

    class Config:
        populate_by_name = True
