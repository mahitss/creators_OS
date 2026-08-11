from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.adaptive_strategy import (
    AdaptiveStrategyRead,
    StrategicThesisRead,
    StrategyIndicatorRead,
    StrategyDriftSignalRead,
    PortfolioReconfigurationRead,
    StrategicExperimentRead,
    AdaptiveStrategyQueryResultRead
)
from app.services.adaptive_strategy_service import AdaptiveStrategyService

router = APIRouter(prefix="/api/v1/strategy/adaptive", tags=["adaptive_strategy"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_adaptive_strategy_overview():
    return await AdaptiveStrategyService.get_adaptive_strategy_overview(None)

@router.get("/strategies", response_model=List[dict])
async def list_strategies():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("strategies", [])

@router.get("/theses", response_model=List[dict])
async def list_theses():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("theses", [])

@router.get("/indicators", response_model=List[dict])
async def list_indicators():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("indicators", [])

@router.get("/drift", response_model=List[dict])
async def list_drifts():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("drifts", [])

@router.get("/reconfigurations", response_model=List[dict])
async def list_reconfigurations():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("reconfigurations", [])

@router.post("/reconfigurations/{reconfig_id}/approve", response_model=dict)
async def approve_reconfiguration(reconfig_id: str, actor_id: str = Query("usr_chief_strategy_officer")):
    return await AdaptiveStrategyService.approve_reconfiguration(None, reconfig_id, actor_id)

@router.post("/reconfigurations/{reconfig_id}/execute", response_model=dict)
async def execute_reconfiguration(reconfig_id: str):
    return await AdaptiveStrategyService.execute_reconfiguration(None, reconfig_id)

@router.get("/experiments", response_model=List[dict])
async def list_experiments():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("experiments", [])

@router.get("/bottlenecks", response_model=List[dict])
async def list_bottlenecks():
    overview = await AdaptiveStrategyService.get_adaptive_strategy_overview(None)
    return overview.get("bottlenecks", [])

@router.post("/query", response_model=AdaptiveStrategyQueryResultRead)
async def process_adaptive_strategy_query(query: str = Query(...)):
    return await AdaptiveStrategyService.process_natural_language_adaptive_strategy_query(None, query)
