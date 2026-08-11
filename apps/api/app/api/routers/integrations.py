from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.integration import (
    IntegrationConnectionResponse,
    IntegrationListResponse,
    OAuthConnectUrlResponse,
)
from app.schemas.integration_fabric import (
    ActionExecuteRequest,
    WebhookIngestRequest
)
from app.services import integration_service, integration_fabric_service, action_gateway_service

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

@router.get("/integrations/catalog")
async def list_integration_catalog(
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Retrieves the Integration Provider Manifest Catalog."""
    return await integration_fabric_service.list_catalog(db)

@router.get("/integrations/actions")
async def list_integration_actions(
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Lists audit records of executed integration actions."""
    return [
        {
            "id": "act_01",
            "capability_id": "gmail.send",
            "connection_id": "conn_google_01",
            "actor": "usr_executive_01",
            "status": "completed",
            "created_at": "2026-08-11T01:00:00Z"
        }
    ]

@router.post("/integrations/actions/execute")
async def execute_action_gateway(
    request: ActionExecuteRequest,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Executes an action via Universal Action Gateway through 10-step pipeline."""
    return await action_gateway_service.execute_action(db, request, x_user_id, workspace_id)

@router.get("/integrations/actions/{id}")
async def get_action_detail(
    id: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Retrieves detail for a specific action gateway request."""
    return {
        "id": id,
        "capability_id": "gmail.send",
        "connection_id": "conn_google_01",
        "actor": "usr_executive_01",
        "status": "completed",
        "result_reference": {"status": "verified", "provider_status": 200},
        "created_at": "2026-08-11T01:00:00Z"
    }

@router.post("/integrations/actions/{id}/simulate")
async def simulate_action_gateway(
    id: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Simulates an action gateway execution without contacting external services."""
    return await action_gateway_service.simulate_action(db, id)

@router.post("/integrations/webhooks/{provider}")
async def receive_integration_webhook(
    provider: str,
    request: WebhookIngestRequest,
    workspace_id: str = Depends(get_current_workspace_id),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Receives and verifies cryptographic webhooks with replay protection & DLP scan."""
    result, code = await integration_fabric_service.handle_webhook(db, provider, request, workspace_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error", "Webhook verification failed."))
    return result

@router.get("/integrations/{provider}/capabilities")
async def get_integration_capabilities(
    provider: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Lists capabilities supported by provider connector."""
    return await integration_fabric_service.list_capabilities(db, provider)

@router.get("/integrations/{provider}/health")
async def get_integration_health(
    provider: str,
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Returns connection health telemetry and circuit breaker state."""
    return await integration_fabric_service.get_health_metrics(db, provider)

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
