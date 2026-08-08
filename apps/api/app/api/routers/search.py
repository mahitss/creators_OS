from typing import Optional
from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.search import SearchResult, SearchListResponse
from app.services import search_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/search", response_model=SearchListResponse)
async def search_workspace_entities(
    q: str = Query("", description="Search query string"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> SearchListResponse:
    results, total = await search_service.global_search(db, workspace_id, q, limit=20)
    return SearchListResponse(
        results=[SearchResult(**r) for r in results],
        total=total
    )
