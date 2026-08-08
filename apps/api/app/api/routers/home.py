from typing import Optional
from fastapi import APIRouter, Query, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_db
from app.schemas.home import ExecutiveBriefResponse
from app.services.home_service import build_executive_brief

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/home/brief", response_model=ExecutiveBriefResponse)
async def get_home_executive_brief(
    user_name: str = Query("Alex", description="Name of the authenticated user"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db)
) -> ExecutiveBriefResponse:
    """
    Returns the Executive Brief for the authenticated workspace context.
    Determines attention items, primary recommendations, learned memories, and quiet states.
    """
    return await build_executive_brief(db=db, user_name=user_name, workspace_id=workspace_id)
