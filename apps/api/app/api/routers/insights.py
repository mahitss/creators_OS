from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.automations import InsightRead
from app.services import proactive_service

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("", response_model=List[InsightRead])
async def list_insights(
    workspace_id: str = Query(..., alias="workspaceId"),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db)
):
    """Lists proactive high-signal insights for a workspace."""
    insights = await proactive_service.list_workspace_insights(session, workspace_id, status_filter=status)
    return insights

@router.post("/{insight_id}/dismiss", response_model=dict)
async def dismiss_insight(
    insight_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Dismisses an insight."""
    res = await proactive_service.update_insight_status(session, insight_id, "dismissed")
    if not res:
        raise HTTPException(status_code=404, detail="Insight not found.")
    return res

@router.post("/{insight_id}/act", response_model=dict)
async def act_on_insight(
    insight_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Marks an insight as acted upon."""
    res = await proactive_service.update_insight_status(session, insight_id, "acted_on")
    if not res:
        raise HTTPException(status_code=404, detail="Insight not found.")
    return res
