import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_optimization import (
    TransformationResilienceOptimizationDomainRead,
    TransformationResilienceOptimizationObjectiveRead,
    TransformationResilienceOptimizationConstraintRead,
    TransformationResilienceOptimizationProblemRead,
    TransformationResilienceOptimizationCandidateRead,
    TransformationResilienceOptimizationCandidateImpactRead,
    TransformationResilienceOptimizationScenarioRead,
    TransformationResilienceOptimizationRunRead,
    TransformationResilienceOptimizationParetoPointRead,
    TransformationResilienceOptimizationTradeoffRead,
    TransformationResilienceOptimizationResourceScenarioRead,
    TransformationResilienceOptimizationInvestmentCaseRead,
    TransformationResilienceOptimizationControlCandidateRead,
    TransformationResilienceOptimizationRedundancyCandidateRead,
    TransformationResilienceOptimizationGapPriorityRead,
    TransformationResilienceOptimizationRecommendationRead,
    TransformationResilienceOptimizationSensitivityRead,
    TransformationResilienceOptimizationRobustnessRead,
    TransformationResilienceOptimizationOutcomeRead,
    TransformationResilienceOptimizationQueryResultRead
)
from app.services.transformation_resilience_optimization_service import TransformationResilienceOptimizationService

router = APIRouter(prefix="/api/v1/transformation-resilience-optimization", tags=["transformation_resilience_optimization"])

@router.get("", response_model=dict)
@router.get("/status", response_model=dict)
async def get_optimization_status():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    domains = overview.get("domains", [])
    if domains:
        return domains[0]
    return {"id": "optdom_01", "name": "Resilience Optimization 2.0", "status": "active"}

@router.get("/problems", response_model=List[dict])
async def list_problems():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("problems", [])

@router.post("/problems", response_model=dict)
async def create_problem(data: dict):
    return {
        "id": f"prob_{uuid.uuid4().hex[:8]}",
        "name": data.get("name", "New Optimization Problem"),
        "baseline_strategy": "continue_current_state"
    }

@router.get("/problems/{id}", response_model=dict)
async def get_problem(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    for p in overview.get("problems", []):
        if p.get("id") == id:
            return p
    return {"id": id, "name": "HR Cloud Optimization", "baseline_strategy": "continue_current_state"}

@router.get("/objectives", response_model=List[dict])
async def list_objectives():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("objectives", [])

@router.post("/objectives", response_model=dict)
async def create_objective(data: dict):
    return {
        "id": f"obj_{uuid.uuid4().hex[:8]}",
        "objective_type": data.get("objective_type", "risk_reduction"),
        "target_value": data.get("target_value", 0.95)
    }

@router.get("/candidates", response_model=List[dict])
async def list_candidates():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("candidates", [])

@router.post("/candidates", response_model=dict)
async def create_candidate(data: dict):
    return {
        "id": f"cand_{uuid.uuid4().hex[:8]}",
        "title": data.get("title", "New Resilience Candidate"),
        "reversibility": "reversible"
    }

@router.post("/problems/{id}/run", response_model=dict)
async def run_problem(id: str, algorithm: str = "pareto_analysis"):
    return await TransformationResilienceOptimizationService.run_optimization_problem(None, id, algorithm)

@router.get("/runs", response_model=List[dict])
async def list_runs():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("runs", [])

@router.get("/runs/{id}", response_model=dict)
async def get_run(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    for r in overview.get("runs", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "completed"}

@router.get("/problems/{id}/pareto", response_model=List[dict])
async def get_pareto_points(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("paretoPoints", [])

@router.get("/problems/{id}/tradeoffs", response_model=List[dict])
async def get_tradeoffs(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("tradeoffs", [])

@router.get("/investments", response_model=List[dict])
async def list_investments():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("investmentCases", [])

@router.get("/investments/{id}", response_model=dict)
async def get_investment(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    for inv in overview.get("investmentCases", []):
        if inv.get("id") == id or inv.get("candidate_id") == id:
            return inv
    return {"id": id, "label": "ANALYTICAL INVESTMENT CASE — NOT APPROVED BUDGET"}

@router.post("/problems/{id}/sensitivity", response_model=dict)
async def run_sensitivity(id: str, varied_parameter: str = "cost"):
    return await TransformationResilienceOptimizationService.run_sensitivity_analysis(None, id, varied_parameter)

@router.get("/problems/{id}/robustness", response_model=dict)
async def get_robustness(id: str):
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    robs = overview.get("robustnesses", [])
    if robs:
        return robs[0]
    return {"recommendation_id": "rec_01", "stability_score": 0.94}

@router.get("/outcomes", response_model=List[dict])
async def list_outcomes():
    overview = await TransformationResilienceOptimizationService.get_optimization_overview(None)
    return overview.get("outcomes", [])

@router.post("/query", response_model=TransformationResilienceOptimizationQueryResultRead)
async def process_optimization_query(query: str = Query(...)):
    return await TransformationResilienceOptimizationService.process_natural_language_optimization_query(None, query)
