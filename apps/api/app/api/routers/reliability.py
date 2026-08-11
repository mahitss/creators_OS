from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.reliability import (
    HealthSignalCreate,
    HealthSignalRead,
    IncidentDiagnosisRead,
    RecoveryPlanCreate,
    RecoveryPlanRead,
    RecoveryExecutionRead,
    CircuitBreakerRead,
    RunbookRead,
    ProblemRead
)
from app.services import reliability_service

router = APIRouter(tags=["reliability"])

@router.post("/health/signals", response_model=HealthSignalRead, status_code=201)
async def ingest_health_signal(
    signal_in: HealthSignalCreate,
    session: AsyncSession = Depends(get_db)
):
    """Ingests operational health signals and correlates them into active incidents."""
    return await reliability_service.ingest_health_signal(session, signal_in)

@router.get("/incidents/{incident_id}/diagnosis", response_model=IncidentDiagnosisRead)
async def diagnose_incident(
    incident_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Generates an evidence-backed AI diagnosis separating OBSERVED, CORRELATED, and SUSPECTED findings."""
    res = await reliability_service.diagnose_incident(session, incident_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@router.post("/recovery/plans", response_model=RecoveryPlanRead, status_code=201)
async def create_recovery_plan(
    plan_in: RecoveryPlanCreate,
    session: AsyncSession = Depends(get_db)
):
    """Creates a policy-controlled, idempotent recovery plan with loop depth protection."""
    plan, error = await reliability_service.create_recovery_plan(session, plan_in)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return plan

@router.post("/recovery/plans/{plan_id}/steps/{step_index}/execute", response_model=RecoveryExecutionRead)
async def execute_recovery_step(
    plan_id: str,
    step_index: int,
    session: AsyncSession = Depends(get_db)
):
    """Executes a registered safe recovery step with PolicyEngine pre-flight verification and idempotency keys."""
    execution, error = await reliability_service.execute_recovery_action(session, plan_id, step_index)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return execution

@router.get("/circuit-breakers/{service}", response_model=CircuitBreakerRead)
async def get_circuit_breaker(
    service: str,
    session: AsyncSession = Depends(get_db)
):
    """Retrieves service circuit breaker status (Closed, Open, Half-Open)."""
    return await reliability_service.get_circuit_breaker_status(session, service)

@router.get("/runbooks", response_model=List[RunbookRead])
async def list_runbooks(
    session: AsyncSession = Depends(get_db)
):
    """Lists registered operational runbooks."""
    now_iso = "2026-08-11T00:00:00Z"
    return [
        RunbookRead(
            id="rb_provider_failover",
            service="model_router",
            name="Model Provider Fallback Runbook",
            trigger_condition={"signal_type": "provider_failure", "threshold": 3},
            steps=[{"type": "switch_configured_fallback_model", "target": "openai/gpt-4o-mini"}],
            verification={"endpoint_ping": "PASSED"},
            rollback={"restore_primary": True},
            owner="sre",
            version=1,
            status="active",
            created_at=now_iso
        )
    ]
