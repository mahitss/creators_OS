from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.foresight_intelligence import (
    ForesightProgramRead,
    FutureDriverRead,
    StrategicTrendRead,
    StrategicAssumptionRead,
    FutureScenarioRead,
    ScenarioIndicatorRead,
    StrategicOptionRead,
    StrategicBetRead,
    ForesightQueryResultRead
)
from app.services.foresight_intelligence_service import ForesightIntelligenceService

router = APIRouter(prefix="/api/v1/foresight", tags=["foresight_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_foresight_overview():
    return await ForesightIntelligenceService.get_foresight_overview(None)

@router.get("/programs", response_model=List[dict])
async def list_programs():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("programs", [])

@router.get("/drivers", response_model=List[dict])
async def list_drivers():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("drivers", [])

@router.get("/trends", response_model=List[dict])
async def list_trends():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("trends", [])

@router.get("/assumptions", response_model=List[dict])
async def list_assumptions():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("assumptions", [])

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("scenarios", [])

@router.get("/indicators", response_model=List[dict])
async def list_indicators():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("indicators", [])

@router.get("/options", response_model=List[dict])
async def list_options():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("options", [])

@router.get("/bets", response_model=List[dict])
async def list_bets():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("bets", [])

@router.get("/exposures", response_model=List[dict])
async def list_exposures():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("exposures", [])

@router.get("/red-teams", response_model=List[dict])
async def list_red_teams():
    overview = await ForesightIntelligenceService.get_foresight_overview(None)
    return overview.get("redTeams", [])

@router.post("/reviews/{program_id}/complete", response_model=dict)
async def complete_review(program_id: str):
    return await ForesightIntelligenceService.complete_foresight_review(None, program_id, {})

@router.post("/query", response_model=ForesightQueryResultRead)
async def process_foresight_query(query: str = Query(...)):
    return await ForesightIntelligenceService.process_natural_language_foresight_query(None, query)
