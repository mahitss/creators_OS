from fastapi import APIRouter, Query
from app.schemas.home import ExecutiveBriefResponse
from app.services.home_service import build_executive_brief

router = APIRouter()

@router.get("/home/brief", response_model=ExecutiveBriefResponse)
async def get_home_executive_brief(
    user_name: str = Query("Alex", description="Name of the authenticated user")
) -> ExecutiveBriefResponse:
    """
    Returns the real Executive Brief for the authenticated user context.
    Provides answers to:
    1. What deserves my attention right now?
    2. What has Vapor already handled for me?
    3. What should I do next?
    """
    return await build_executive_brief(user_name=user_name)
