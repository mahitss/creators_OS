from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.execution_intelligence import (
    ExecutionObjectiveRead,
    StrategicAlignmentAssessmentRead,
    ExecutionCoverageRead,
    StrategicExecutionPathRead,
    ExecutionDriftSignalRead,
    ExecutionDependencyBlockerRead,
    ExecutionRecommendationRead,
    ExecutionQueryResultRead
)
from app.services.execution_intelligence_service import ExecutionIntelligenceService

router = APIRouter(prefix="/api/v1/execution-intelligence", tags=["execution_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_execution_intelligence_overview():
    return await ExecutionIntelligenceService.get_execution_intelligence_overview(None)

@router.get("/objectives", response_model=List[dict])
async def list_objectives():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("objectives", [])

@router.get("/alignment", response_model=List[dict])
async def list_alignments():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("alignments", [])

@router.get("/coverage", response_model=List[dict])
async def list_coverages():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("coverages", [])

@router.get("/drift", response_model=List[dict])
async def list_drifts():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("drifts", [])

@router.get("/blockers", response_model=List[dict])
async def list_blockers():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("blockers", [])

@router.get("/decision-gaps", response_model=List[dict])
async def list_decision_gaps():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("decisionGaps", [])

@router.get("/outcomes", response_model=List[dict])
async def list_outcomes():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("outcomeGaps", [])

@router.get("/recommendations", response_model=List[dict])
async def list_recommendations():
    overview = await ExecutionIntelligenceService.get_execution_intelligence_overview(None)
    return overview.get("recommendations", [])

@router.post("/recommendations/{rec_id}/approve", response_model=dict)
async def approve_recommendation(rec_id: str, actor_id: str = Query("usr_chief_technology_officer")):
    return await ExecutionIntelligenceService.approve_execution_recommendation(None, rec_id, actor_id)

@router.post("/recommendations/{rec_id}/execute", response_model=dict)
async def execute_recommendation(rec_id: str):
    return await ExecutionIntelligenceService.execute_recommendation(None, rec_id)

@router.post("/query", response_model=ExecutionQueryResultRead)
async def process_execution_query(query: str = Query(...)):
    return await ExecutionIntelligenceService.process_natural_language_execution_query(None, query)
