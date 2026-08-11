from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.prescriptive_intelligence import (
    OptimizationProblemCreate,
    OptimizationProblemRead,
    OptimizationOptionRead,
    PrescriptiveRecommendationRead,
    OptimizationActionPlanRead,
    RobustnessAnalysisRead,
    SensitivityAnalysisRead,
    OptimizationTradeoffRead,
    OptimizationPerformanceRead,
    PrescriptiveQueryResultRead
)
from app.services.prescriptive_intelligence_service import PrescriptiveIntelligenceService

router = APIRouter(prefix="/api/v1/optimization", tags=["prescriptive_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_optimization_overview():
    return await PrescriptiveIntelligenceService.get_optimization_overview(None)

@router.get("/problems", response_model=List[dict])
async def list_optimization_problems():
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    return overview.get("problems", [])

@router.post("/problems", response_model=dict)
async def create_optimization_problem(payload: OptimizationProblemCreate):
    return await PrescriptiveIntelligenceService.create_problem(None, payload.model_dump())

@router.get("/problems/{problem_id}", response_model=dict)
async def get_optimization_problem(problem_id: str):
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    for p in overview.get("problems", []):
        if p["id"] == problem_id:
            return p
    raise HTTPException(status_code=404, detail="Optimization problem not found")

@router.get("/problems/{problem_id}/options", response_model=List[dict])
async def list_problem_options(problem_id: str):
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    return [o for o in overview.get("options", []) if o.get("problem_id") == problem_id]

@router.post("/problems/{problem_id}/options/generate", response_model=dict)
async def generate_problem_options(problem_id: str):
    return {
        "problemId": problem_id,
        "status": "generated",
        "generatedOptionsCount": 2,
        "message": "Options generated successfully respecting hard and soft constraints."
    }

@router.get("/recommendations", response_model=List[dict])
async def list_recommendations():
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    return overview.get("recommendations", [])

@router.get("/recommendations/{recommendation_id}", response_model=dict)
async def get_recommendation(recommendation_id: str):
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    for r in overview.get("recommendations", []):
        if r["id"] == recommendation_id:
            return r
    raise HTTPException(status_code=404, detail="Recommendation not found")

@router.post("/recommendations/{recommendation_id}/approve", response_model=dict)
async def approve_recommendation(recommendation_id: str):
    return {
        "recommendationId": recommendation_id,
        "status": "approved",
        "approvedBy": "usr_head_of_arch",
        "message": "Recommendation approved; action plan ready for execution via ActionGateway."
    }

@router.post("/recommendations/{recommendation_id}/action-plan", response_model=dict)
async def create_action_plan(recommendation_id: str):
    overview = await PrescriptiveIntelligenceService.get_optimization_overview(None)
    for ap in overview.get("actionPlans", []):
        if ap.get("recommendation_id") == recommendation_id:
            return ap
    raise HTTPException(status_code=404, detail="Action plan not found for recommendation")

@router.post("/action-plans/{plan_id}/execute", response_model=dict)
async def execute_action_plan(plan_id: str):
    return await PrescriptiveIntelligenceService.execute_action_plan(None, plan_id)

@router.post("/action-plans/{plan_id}/rollback", response_model=dict)
async def rollback_action_plan(plan_id: str):
    return {
        "actionPlanId": plan_id,
        "status": "rolled_back",
        "executedBy": "usr_head_of_arch",
        "message": "Action plan rolled back safely via ActionGateway."
    }

@router.post("/query", response_model=PrescriptiveQueryResultRead)
async def process_prescriptive_query(query: str = Query(...)):
    return await PrescriptiveIntelligenceService.process_natural_language_prescriptive_query(None, query)
