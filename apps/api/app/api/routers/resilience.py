from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.resilience_service import ResilienceService
from app.schemas.resilience import (
    ComponentHealthRead, FailureEventRead, DegradationModeRead,
    CircuitBreakerStateRead, DeadLetterEntryRead,
    RecoveryPlanCreate, RecoveryPlanRead,
    ResilienceExperimentCreate, ResilienceExperimentRead,
    ResilienceSLORead, ReliabilityBudgetRead, CapacitySnapshotRead
)

router = APIRouter(prefix="/resilience", tags=["resilience_and_business_continuity"])

@router.get("")
async def get_resilience_dashboard():
    return await ResilienceService.get_dashboard_summary(None)

@router.get("/components", response_model=List[ComponentHealthRead])
async def get_resilience_components():
    dash = await ResilienceService.get_dashboard_summary(None)
    return [
        ComponentHealthRead(
            id=c["id"],
            componentId=c["component_id"],
            componentType=c["component_type"],
            status=c["status"],
            latencyMs=c["latency_ms"],
            errorRate=c["error_rate"],
            availabilityPct=c["availability_pct"],
            lastHealthyAt=c["last_healthy_at"],
            updatedAt=c["updated_at"]
        ) for c in dash["components"]
    ]

@router.get("/components/{component_id}", response_model=ComponentHealthRead)
async def get_resilience_component_detail(component_id: str):
    dash = await ResilienceService.get_dashboard_summary(None)
    for c in dash["components"]:
        if c["component_id"] == component_id:
            return ComponentHealthRead(
                id=c["id"],
                componentId=c["component_id"],
                componentType=c["component_type"],
                status=c["status"],
                latencyMs=c["latency_ms"],
                errorRate=c["error_rate"],
                availabilityPct=c["availability_pct"],
                lastHealthyAt=c["last_healthy_at"],
                updatedAt=c["updated_at"]
            )
    raise HTTPException(status_code=404, detail=f"Component '{component_id}' not found.")

@router.get("/failures")
async def get_resilience_failures():
    dash = await ResilienceService.get_dashboard_summary(None)
    return dash.get("failures", [])

@router.get("/degradation", response_model=List[DegradationModeRead])
async def get_degradation_modes():
    dash = await ResilienceService.get_dashboard_summary(None)
    return [
        DegradationModeRead(
            id=d["id"],
            scope=d["scope"],
            mode=d["mode"],
            reason=d["reason"],
            status=d["status"],
            expiresAt=d.get("expires_at"),
            createdAt=d["created_at"]
        ) for d in dash["degradations"]
    ]

@router.get("/recovery-plans", response_model=List[RecoveryPlanRead])
async def get_recovery_plans():
    dash = await ResilienceService.get_dashboard_summary(None)
    plans = dash.get("recovery_plans", [])
    if not plans:
        # Default seeded plan
        plans = [{
            "id": "rp_dr_regional_01",
            "name": "Primary Region Failover & State Reconstruction Plan",
            "components_json": ["database", "event_mesh", "agent_runtime_v2"],
            "rto_seconds": 300,
            "rpo_seconds": 60,
            "recovery_order_json": ["1. Database", "2. Runtime", "3. Outbox"],
            "status": "active",
            "created_at": "2026-08-11T04:00:00Z"
        }]
    return [
        RecoveryPlanRead(
            id=p["id"],
            name=p["name"],
            componentsJson=p["components_json"],
            rtoSeconds=p["rto_seconds"],
            rpoSeconds=p["rpo_seconds"],
            recoveryOrderJson=p["recovery_order_json"],
            status=p["status"],
            createdAt=p["created_at"]
        ) for p in plans
    ]

@router.post("/recovery-plans", response_model=RecoveryPlanRead)
async def create_recovery_plan(payload: RecoveryPlanCreate):
    plan = await ResilienceService.create_recovery_plan(None, payload.model_dump())
    return RecoveryPlanRead(
        id=plan["id"],
        name=plan["name"],
        componentsJson=plan["components_json"],
        rtoSeconds=plan["rto_seconds"],
        rpoSeconds=plan["rpo_seconds"],
        recoveryOrderJson=plan["recovery_order_json"],
        status=plan["status"],
        createdAt=plan["created_at"]
    )

@router.get("/recovery-plans/{plan_id}", response_model=RecoveryPlanRead)
async def get_recovery_plan_detail(plan_id: str):
    plans = await get_recovery_plans()
    for p in plans:
        if p.id == plan_id:
            return p
    raise HTTPException(status_code=404, detail=f"Recovery plan '{plan_id}' not found.")

@router.post("/recovery-plans/{plan_id}/simulate")
async def simulate_recovery_plan_endpoint(plan_id: str):
    return await ResilienceService.simulate_recovery_plan(None, plan_id)

@router.post("/recovery-plans/{plan_id}/execute")
async def execute_recovery_plan_endpoint(plan_id: str):
    return {"plan_id": plan_id, "status": "executing", "initiated_at": "2026-08-11T04:00:00Z"}

@router.get("/experiments", response_model=List[ResilienceExperimentRead])
async def get_chaos_experiments():
    return [
        ResilienceExperimentRead(
            id="exp_latency_inj_01",
            name="Model Provider Latency Spike Simulation",
            experimentType="latency_injection",
            targetScope="sandbox_workspace",
            blastRadiusJson={"max_affected_missions": 5},
            abortConditionsJson={"max_error_rate": 0.05},
            status="draft",
            createdAt="2026-08-11T04:00:00Z"
        )
    ]

@router.post("/experiments", response_model=ResilienceExperimentRead)
async def create_chaos_experiment(payload: ResilienceExperimentCreate):
    rec = payload.model_dump()
    return ResilienceExperimentRead(
        id="exp_custom_01",
        name=rec["name"],
        experimentType=rec["experimentType"],
        targetScope=rec["targetScope"],
        blastRadiusJson=rec["blastRadiusJson"],
        abortConditionsJson=rec["abortConditionsJson"],
        status="draft",
        createdAt="2026-08-11T04:00:00Z"
    )

@router.get("/experiments/{exp_id}", response_model=ResilienceExperimentRead)
async def get_chaos_experiment_detail(exp_id: str):
    exps = await get_chaos_experiments()
    for e in exps:
        if e.id == exp_id:
            return e
    raise HTTPException(status_code=404, detail=f"Experiment '{exp_id}' not found.")

@router.post("/experiments/{exp_id}/start")
async def start_chaos_experiment_endpoint(exp_id: str):
    return await ResilienceService.start_chaos_experiment(None, exp_id)

@router.post("/experiments/{exp_id}/abort")
async def abort_chaos_experiment_endpoint(exp_id: str, reason: str = Query("Blast radius threshold reached")):
    return await ResilienceService.abort_chaos_experiment(None, exp_id, reason)

@router.get("/slos", response_model=List[ResilienceSLORead])
async def get_resilience_slos():
    dash = await ResilienceService.get_dashboard_summary(None)
    return [
        ResilienceSLORead(
            id=s["id"],
            sloName=s["slo_name"],
            targetAvailabilityPct=s["target_availability_pct"],
            currentAvailabilityPct=s["current_availability_pct"],
            targetLatencyMs=s["target_latency_ms"],
            currentLatencyMs=s["current_latency_ms"],
            status=s["status"],
            updatedAt=s["updated_at"]
        ) for s in dash["slos"]
    ]

@router.get("/budgets", response_model=List[ReliabilityBudgetRead])
async def get_reliability_budgets():
    return [
        ReliabilityBudgetRead(
            id="bgt_default",
            organizationId="org_default_creator",
            allowedErrorPct=0.1,
            currentBurnRate=0.015,
            budgetRemainingPct=85.0,
            updatedAt="2026-08-11T04:00:00Z"
        )
    ]

@router.get("/capacity", response_model=CapacitySnapshotRead)
async def get_capacity_snapshot():
    dash = await ResilienceService.get_dashboard_summary(None)
    cap = dash["capacity"]
    return CapacitySnapshotRead(
        id="cap_curr_01",
        cpuPct=cap["cpuPct"],
        memoryPct=cap["memoryPct"],
        queueDepth=cap["queueDepth"],
        concurrencyLevel=cap["concurrencyLevel"],
        loadSheddingActive=cap["loadSheddingActive"],
        createdAt="2026-08-11T04:00:00Z"
    )
