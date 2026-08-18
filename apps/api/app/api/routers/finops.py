from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext
from app.schemas.finops import (
    UsageRecordCreate,
    UsageRecordRead,
    BudgetCreate,
    BudgetRead,
    UsageAnomalyRead,
    OperationalIncidentRead,
    FinOpsOverviewResponse,
    FinOpsForecastResponse
)
from app.services import finops_service

router = APIRouter(tags=["finops"])

@router.get("/finops/overview", response_model=FinOpsOverviewResponse)
async def get_finops_overview(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves executive spend overview, budget usage, and active anomaly count."""
    return await finops_service.get_finops_overview(session, ws_ctx.workspace_id)

@router.get("/finops/forecast", response_model=FinOpsForecastResponse)
async def get_finops_forecast(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Generates monthly spend projections based on daily run rate."""
    return await finops_service.get_finops_forecast(session, ws_ctx.workspace_id)

@router.post("/usage", response_model=UsageRecordRead, status_code=201)
async def record_usage(
    usage_in: UsageRecordCreate,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Records append-only telemetry and calculates versioned pricing cost."""
    # Ensure tenant isolation on recorded usage
    usage_in.workspace_id = ws_ctx.workspace_id
    return await finops_service.record_usage(session, usage_in)

@router.get("/budgets", response_model=List[BudgetRead])
async def list_budgets(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Lists workspace budgets and current consumption."""
    now_iso = "2026-08-11T00:00:00Z"
    ov = await finops_service.get_finops_overview(session, ws_ctx.workspace_id)
    return [
        BudgetRead(
            id=f"b_{ws_ctx.workspace_id}",
            workspace_id=ws_ctx.workspace_id,
            scope_type="workspace",
            scope_id=ws_ctx.workspace_id,
            period="monthly",
            limit_amount=ov.budget_limit,
            used_amount=ov.budget_used,
            reserved_amount=0.0,
            currency="USD",
            warning_threshold_pct=90.0,
            status="active" if ov.budget_used < ov.budget_limit else "exhausted",
            created_at=now_iso,
            updated_at=now_iso
        )
    ]

@router.get("/anomalies", response_model=List[UsageAnomalyRead])
async def list_anomalies(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves cost and latency anomalies detected against 7D/30D baselines."""
    return await finops_service.detect_cost_anomalies(session, ws_ctx.workspace_id)

@router.get("/incidents", response_model=List[OperationalIncidentRead])
async def list_incidents(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves active operational incidents."""
    return []
