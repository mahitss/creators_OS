from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.integration import (
    IntegrationConnectionResponse,
    IntegrationListResponse,
    OAuthConnectUrlResponse,
)
from app.services import integration_service

router = APIRouter()

DEFAULT_WORKSPACE_ID = "ws_default_01"

def get_current_workspace_id(x_workspace_id: Optional[str] = Header(None)) -> str:
    return x_workspace_id or DEFAULT_WORKSPACE_ID

@router.get("/integrations", response_model=IntegrationListResponse)
async def list_integrations(
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> IntegrationListResponse:
    connections, total = await integration_service.list_connections(db, workspace_id)
    return IntegrationListResponse(
        connections=[IntegrationConnectionResponse(**conn) for conn in connections],
        total=total
    )

@router.get("/integrations/{provider}", response_model=IntegrationConnectionResponse)
async def get_integration(
    provider: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> IntegrationConnectionResponse:
    conn = await integration_service.get_connection(db, workspace_id, provider)
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration provider '{provider}' is disconnected or not configured."
        )
    return IntegrationConnectionResponse(**conn)

@router.post("/integrations/{provider}/connect", response_model=OAuthConnectUrlResponse)
async def connect_integration(
    provider: str,
    workspace_id: str = Depends(get_current_workspace_id),
) -> OAuthConnectUrlResponse:
    try:
        auth_url, state = await integration_service.generate_connect_url(workspace_id, provider)
        return OAuthConnectUrlResponse(authorization_url=auth_url, state=state)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get("/integrations/{provider}/callback", response_model=IntegrationConnectionResponse)
async def oauth_callback(
    provider: str,
    code: str = Query(..., description="Authorization code from provider"),
    state: str = Query(..., description="CSRF state token"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> IntegrationConnectionResponse:
    try:
        conn = await integration_service.handle_oauth_callback(db, workspace_id, provider, code, state)
        return IntegrationConnectionResponse(**conn)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post("/integrations/{provider}/disconnect", response_model=IntegrationConnectionResponse)
async def disconnect_integration(
    provider: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> IntegrationConnectionResponse:
    conn = await integration_service.disconnect_provider(db, workspace_id, provider)
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration provider '{provider}' not found."
        )
    return IntegrationConnectionResponse(**conn)

@router.post("/integrations/{provider}/refresh", response_model=IntegrationConnectionResponse)
async def refresh_integration(
    provider: str,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
) -> IntegrationConnectionResponse:
    conn = await integration_service.refresh_connection(db, workspace_id, provider)
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration provider '{provider}' not found."
        )
    return IntegrationConnectionResponse(**conn)
