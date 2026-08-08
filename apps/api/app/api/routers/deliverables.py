from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.deliverable import DeliverableSuggestionResponse, DeliverableSuggestionListResponse
from app.schemas.content import ContentResponse
from app.services import deliverable_intelligence_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"
DEFAULT_USER_ID = "usr_creator_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> str:
    return x_user_id or DEFAULT_USER_ID

@router.get("/missions/{id}/deliverable-suggestions", response_model=DeliverableSuggestionListResponse)
async def list_mission_deliverable_suggestions(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DeliverableSuggestionListResponse:
    items, total = await deliverable_intelligence_service.list_suggestions_for_mission(db, workspace_id, id)
    return DeliverableSuggestionListResponse(
        suggestions=[DeliverableSuggestionResponse(**s) for s in items],
        total=total
    )

@router.post("/missions/{id}/deliverable-suggestions/analyze", response_model=Optional[DeliverableSuggestionResponse])
async def analyze_mission_deliverables(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> Optional[DeliverableSuggestionResponse]:
    sugg = await deliverable_intelligence_service.analyze_mission_for_deliverables(db, workspace_id, id)
    if not sugg:
        return None
    return DeliverableSuggestionResponse(**sugg)

@router.post("/deliverable-suggestions/{id}/accept", response_model=ContentResponse)
async def accept_deliverable_suggestion(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    user_id: str = Depends(get_current_user_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> ContentResponse:
    sugg, new_content = await deliverable_intelligence_service.accept_suggestion(db, workspace_id, user_id, id)
    if not sugg or not new_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverable suggestion not found in active workspace."
        )
    return ContentResponse(**new_content)

@router.post("/deliverable-suggestions/{id}/dismiss", response_model=DeliverableSuggestionResponse)
async def dismiss_deliverable_suggestion(
    id: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> DeliverableSuggestionResponse:
    sugg = await deliverable_intelligence_service.dismiss_suggestion(db, workspace_id, id)
    if not sugg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deliverable suggestion not found in active workspace."
        )
    return DeliverableSuggestionResponse(**sugg)
