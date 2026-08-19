from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.home import ExecutiveBriefResponse
from app.services.home_service import build_executive_brief

router = APIRouter()

@router.get("/home/brief", response_model=ExecutiveBriefResponse)
async def get_home_executive_brief(
    user_name: Optional[str] = Query(None, description="Name of the authenticated user"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: Optional[AsyncSession] = Depends(get_db)
) -> ExecutiveBriefResponse:
    """
    Returns the Executive Brief for the authenticated workspace context.
    Determines attention items, primary recommendations, learned memories, and quiet states.
    """
    resolved_name = user_name or "Operator"
    return await build_executive_brief(
        db=db,
        user_name=resolved_name,
        workspace_id=ws_ctx.workspace_id,
        user_id=ws_ctx.user_id
    )
