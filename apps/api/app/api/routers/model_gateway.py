from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.model_gateway import (
    ModelGatewayRequest,
    ModelGatewayResponse,
    ModelRegistryRead,
    ModelProviderRead,
    ModelRoutingDecisionRead,
    ModelHealthRead,
    ModelExperimentCreate,
    ModelExperimentRead,
    ModelAdminActionRequest
)
from app.services import model_gateway_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/ai", tags=["Enterprise AI Model Gateway & Intelligent Model Routing"])

@router.post("/routing/infer", response_model=ModelGatewayResponse)
async def execute_inference(
    req: ModelGatewayRequest,
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Capability-aware, policy-governed Model Gateway inference endpoint."""
    try:
        resp, _ = await model_gateway_service.execute_model_inference(
            db, workspace_id=workspace_id, req=req, organization_id=organization_id
        )
        return resp
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/models", response_model=List[ModelRegistryRead])
async def list_models(
    db: AsyncSession = Depends(get_db)
):
    """Lists registered models."""
    return await model_gateway_service.list_models(db)

@router.get("/models/{model_key}", response_model=ModelRegistryRead)
async def get_model(
    model_key: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches single model metadata."""
    m = await model_gateway_service.get_model_by_key(db, model_key=model_key)
    if not m:
        raise HTTPException(status_code=404, detail="Model not found")
    return m

@router.post("/models/{model_key}/enable", response_model=ModelRegistryRead)
async def enable_model(
    model_key: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: enables a registered model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="available", user_id=x_user_id, organization_id=organization_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return m

@router.post("/models/{model_key}/disable", response_model=ModelRegistryRead)
async def disable_model(
    model_key: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: disables a model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="disabled", user_id=x_user_id, organization_id=organization_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return m

@router.post("/models/{model_key}/deprecate", response_model=ModelRegistryRead)
async def deprecate_model(
    model_key: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    organization_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: deprecates a model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="deprecated", user_id=x_user_id, organization_id=organization_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return m

@router.get("/providers", response_model=List[ModelProviderRead])
async def list_providers(
    db: AsyncSession = Depends(get_db)
):
    """Lists model providers."""
    return await model_gateway_service.list_providers(db)

@router.get("/routing", response_model=List[ModelRoutingDecisionRead])
async def list_routing_decisions(
    db: AsyncSession = Depends(get_db)
):
    """Lists routing decisions audit log."""
    return await model_gateway_service.list_routing_decisions(db)

@router.get("/routing/{request_id}", response_model=ModelRoutingDecisionRead)
async def get_routing_decision(
    request_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches details for a specific routing decision."""
    d = await model_gateway_service.get_routing_decision(db, request_id=request_id)
    if not d:
        raise HTTPException(status_code=404, detail="Routing decision not found")
    return d

@router.get("/health", response_model=List[ModelHealthRead])
async def list_model_healths(
    db: AsyncSession = Depends(get_db)
):
    """Lists model health snapshots."""
    return await model_gateway_service.list_model_healths(db)

@router.get("/experiments", response_model=List[ModelExperimentRead])
async def list_model_experiments(
    db: AsyncSession = Depends(get_db)
):
    """Lists model canary experiments."""
    return await model_gateway_service.list_model_experiments(db)

@router.post("/experiments", response_model=ModelExperimentRead)
async def create_model_experiment(
    req: ModelExperimentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Creates a model canary A/B experiment."""
    return await model_gateway_service.create_model_experiment(db, req=req)

@router.post("/experiments/{exp_id}/stop", response_model=ModelExperimentRead)
async def stop_model_experiment(
    exp_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Stops a model experiment."""
    exp = await model_gateway_service.stop_model_experiment(db, experiment_id=exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp
