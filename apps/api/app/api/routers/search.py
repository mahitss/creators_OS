from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.search import SearchResult, SearchListResponse
from app.services import search_service

router = APIRouter()

@router.get("/search", response_model=SearchListResponse)
async def search_workspace_entities(
    q: str = Query("", description="Search query string"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db),
) -> SearchListResponse:
    results, total = await search_service.global_search(db, ws_ctx.workspace_id, q, limit=20)
    return SearchListResponse(
        results=[SearchResult(**r) for r in results],
        total=total
    )
