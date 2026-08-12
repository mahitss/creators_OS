from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_engineering import (
    TransformationResilienceEngineeringDomainRead,
    TransformationResilienceBaselineRead,
    TransformationFailureModeRead,
    TransformationFailureModeAnalysisRead,
    TransformationSystemicWeaknessRead,
    TransformationSinglePointOfFailureRead,
    TransformationRedundancyOptionRead,
    TransformationSubstitutionOptionRead,
    TransformationCapacityBufferOptionRead,
    TransformationOptionalityAnalysisRead,
    TransformationResilienceInvestmentCandidateRead,
    TransformationCascadingFailureAnalysisRead,
    TransformationResilienceInterventionRead,
    TransformationResilienceRoadmapRead,
    TransformationResilienceComparisonRead,
    TransformationResilienceLessonRead,
    TransformationResiliencePatternRead,
    TransformationResilienceWarningRead,
    TransformationResilienceQueryResultRead
)
from app.services.transformation_resilience_engineering_service import TransformationResilienceEngineeringService

router = APIRouter(prefix="/api/v1/transformation-resilience-engineering", tags=["transformation_resilience_engineering"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_resilience_overview():
    return await TransformationResilienceEngineeringService.get_resilience_overview(None)

@router.post("", response_model=dict)
async def create_resilience_domain(data: dict):
    return {"id": "red_new", "name": data.get("name", "New Resilience Engineering Domain"), "status": "baseline", "version": "v2.0"}

@router.get("/investments", response_model=List[dict])
async def list_investments():
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("investments", [])

@router.post("/investments", response_model=dict)
async def create_investment(data: dict):
    return {"id": "inv_new", "improvementTitle": data.get("improvementTitle", "New Investment"), "investmentAmount": data.get("investmentAmount", 250000.0), "priority": "high"}

@router.get("/investments/{id}", response_model=dict)
async def get_investment(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    for inv in overview.get("investments", []):
        if inv.get("id") == id:
            return inv
    return {"id": id, "investmentAmount": 250000.0}

@router.post("/investments/{id}/simulate", response_model=dict)
async def simulate_investment(id: str):
    return {"investmentId": id, "simulationCompleted": True, "riskReductionPct": 45.0, "paybackHorizon": "Q4 2026"}

@router.get("/roadmaps", response_model=List[dict])
async def list_roadmaps():
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("roadmaps", [])

@router.post("/roadmaps", response_model=dict)
async def create_roadmap(data: dict):
    return {"id": "road_new", "investmentTotal": data.get("investmentTotal", 430000.0), "status": "draft"}

@router.get("/roadmaps/{id}", response_model=dict)
async def get_roadmap(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    for r in overview.get("roadmaps", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "draft"}

@router.get("/roadmaps/{id}/verification", response_model=dict)
async def get_roadmap_verification(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("comparisons", [{}])[0]

@router.get("/{id}", response_model=dict)
async def get_resilience_domain(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    for d in overview.get("domains", []):
        if d.get("id") == id:
            return d
    return {"id": id, "name": "Global Transformation Resilience Engineering Domain", "status": "baseline"}

@router.get("/{id}/baseline", response_model=dict)
async def get_baseline(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("baselines", [{}])[0]

@router.get("/{id}/failure-modes", response_model=List[dict])
async def list_failure_modes(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("failureModes", [])

@router.get("/{id}/weaknesses", response_model=List[dict])
async def list_weaknesses(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("weaknesses", [])

@router.get("/{id}/single-points-of-failure", response_model=List[dict])
async def list_spofs(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("spofs", [])

@router.get("/{id}/redundancy", response_model=List[dict])
async def list_redundancies(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("redundancies", [])

@router.get("/{id}/substitution", response_model=List[dict])
async def list_substitutions(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("substitutions", [])

@router.get("/{id}/capacity-buffers", response_model=List[dict])
async def list_buffers(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("buffers", [])

@router.get("/{id}/optionality", response_model=dict)
async def get_optionality(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("optionalities", [{}])[0]

@router.get("/{id}/cascading-failures", response_model=List[dict])
async def list_cascading_failures(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("cascades", [])

@router.get("/{id}/patterns", response_model=List[dict])
async def list_patterns(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("patterns", [])

@router.get("/{id}/warnings", response_model=List[dict])
async def list_warnings(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("warnings", [])

@router.get("/{id}/lessons", response_model=List[dict])
async def list_lessons(id: str):
    overview = await TransformationResilienceEngineeringService.get_resilience_overview(None)
    return overview.get("lessons", [])

@router.post("/query", response_model=TransformationResilienceQueryResultRead)
async def process_resilience_query(query: str = Query(...)):
    return await TransformationResilienceEngineeringService.process_natural_language_resilience_query(None, query)
