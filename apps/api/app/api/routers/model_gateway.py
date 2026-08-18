from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
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
from app.dependencies.auth import get_current_user, get_current_workspace, require_admin, AuthenticatedUser, WorkspaceContext

router = APIRouter(prefix="/ai", tags=["Enterprise AI Model Gateway & Intelligent Model Routing"])

@router.post("/routing/infer", response_model=ModelGatewayResponse)
@router.post("/respond", response_model=ModelGatewayResponse)
async def execute_inference(
    req: ModelGatewayRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Capability-aware, policy-governed Model Gateway inference endpoint."""
    try:
        resp, _ = await model_gateway_service.execute_model_inference(
            db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id
        )
        return resp
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.post("/stream")
async def stream_inference(
    req: ModelGatewayRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace)
):
    """Server-Sent Events (SSE) AI streaming endpoint via OpenRouter."""
    async def sse_generator():
        async for chunk in model_gateway_service.stream_model_inference(req):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

@router.post("/tool-call")
async def execute_tool_call(
    prompt: str = Query(..., description="User prompt"),
    tools: List[Dict[str, Any]] = [],
    model: Optional[str] = Query(None, description="Target model key"),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace)
):
    """Executes policy-governed tool calling via OpenRouter."""
    try:
        return await model_gateway_service.execute_model_tool_call(prompt=prompt, tools=tools, model_key=model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_ai_health():
    """Live internal AI gateway health verification for OpenRouter."""
    return await model_gateway_service.get_gateway_health()

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
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: enables a registered model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="available", user_id=ws_ctx.user_id, organization_id=ws_ctx.workspace_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return m

@router.post("/models/{model_key}/disable", response_model=ModelRegistryRead)
async def disable_model(
    model_key: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: disables a model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="disabled", user_id=ws_ctx.user_id, organization_id=ws_ctx.workspace_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return m

@router.post("/models/{model_key}/deprecate", response_model=ModelRegistryRead)
async def deprecate_model(
    model_key: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Admin action: deprecates a model."""
    m, err = await model_gateway_service.set_model_status(db, model_key=model_key, new_status="deprecated", user_id=ws_ctx.user_id, organization_id=ws_ctx.workspace_id)
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
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists routing decisions audit log."""
    return await model_gateway_service.list_routing_decisions(db)

@router.get("/routing/{request_id}", response_model=ModelRoutingDecisionRead)
async def get_routing_decision(
    request_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
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
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists model canary experiments."""
    return await model_gateway_service.list_model_experiments(db)

@router.post("/experiments", response_model=ModelExperimentRead)
async def create_model_experiment(
    req: ModelExperimentCreate,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Creates a model canary A/B experiment."""
    return await model_gateway_service.create_model_experiment(db, req=req)

@router.post("/experiments/{exp_id}/stop", response_model=ModelExperimentRead)
async def stop_model_experiment(
    exp_id: str,
    ws_ctx: WorkspaceContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Stops a model experiment."""
    exp = await model_gateway_service.stop_model_experiment(db, experiment_id=exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp
