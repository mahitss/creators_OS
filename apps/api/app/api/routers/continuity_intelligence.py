from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.continuity_intelligence import (
    CriticalCapabilityCreate,
    CriticalCapabilityRead,
    BusinessImpactProfileRead,
    ResilienceDependencyRiskRead,
    ResilienceGapRead,
    FailureScenarioRead,
    ContinuityPlanRead,
    RecoveryProcedureRead,
    RecoveryOutcomeRead,
    ResilienceTestRead,
    ResiliencePostureRead,
    VendorResilienceProfileRead,
    DataResilienceProfileRead,
    AIResilienceProfileRead,
    ResilienceQueryResultRead
)
from app.services.continuity_intelligence_service import ContinuityIntelligenceService

router = APIRouter(prefix="/api/v1/resilience", tags=["continuity_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_resilience_overview():
    return await ContinuityIntelligenceService.get_resilience_overview(None)

@router.get("/capabilities", response_model=List[dict])
async def list_capabilities():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("capabilities", [])

@router.post("/capabilities", response_model=dict)
async def create_critical_capability(payload: CriticalCapabilityCreate):
    return await ContinuityIntelligenceService.create_critical_capability(None, payload.model_dump())

@router.get("/capabilities/{cap_id}", response_model=dict)
async def get_capability(cap_id: str):
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    for c in overview.get("capabilities", []):
        if c["id"] == cap_id:
            return c
    raise HTTPException(status_code=404, detail="Capability not found")

@router.get("/dependencies", response_model=List[dict])
async def list_dependencies():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("dependencies", [])

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("scenarios", [])

@router.get("/gaps", response_model=List[dict])
async def list_gaps():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("gaps", [])

@router.get("/plans", response_model=List[dict])
async def list_plans():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("plans", [])

@router.get("/plans/{plan_id}", response_model=dict)
async def get_plan(plan_id: str):
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    for p in overview.get("plans", []):
        if p["id"] == plan_id:
            return p
    raise HTTPException(status_code=404, detail="Continuity plan not found")

@router.post("/plans/{plan_id}/validate", response_model=dict)
async def validate_plan(plan_id: str):
    return await ContinuityIntelligenceService.validate_continuity_plan(None, plan_id)

@router.get("/recovery", response_model=List[dict])
async def list_recovery():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("tests", [])

@router.get("/tests", response_model=List[dict])
async def list_tests():
    overview = await ContinuityIntelligenceService.get_resilience_overview(None)
    return overview.get("tests", [])

@router.post("/query", response_model=ResilienceQueryResultRead)
async def process_resilience_query(query: str = Query(...)):
    return await ContinuityIntelligenceService.process_natural_language_resilience_query(None, query)
