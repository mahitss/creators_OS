from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_portfolio import (
    TransformationPortfolioRead,
    TransformationCandidateRead,
    TransformationDependencyGraphRead,
    TransformationSequenceRead,
    TransformationSequenceComparisonRead,
    TransformationPortfolioBottleneckRead,
    TransformationWaveRead,
    TransformationPortfolioRebalanceRead,
    TransformationPortfolioQueryResultRead
)
from app.services.transformation_portfolio_service import TransformationPortfolioService

router = APIRouter(prefix="/api/v1/transformation-portfolio", tags=["transformation_portfolio"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_portfolio_overview():
    return await TransformationPortfolioService.get_portfolio_overview(None)

@router.get("/portfolios", response_model=List[dict])
async def list_portfolios():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("portfolios", [])

@router.get("/candidates", response_model=List[dict])
async def list_candidates():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("candidates", [])

@router.get("/dependencies", response_model=List[dict])
async def list_dependencies():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("graphs", [])

@router.get("/sequences", response_model=List[dict])
async def list_sequences():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("sequences", [])

@router.get("/comparisons", response_model=List[dict])
async def list_comparisons():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("comparisons", [])

@router.get("/capacity", response_model=List[dict])
async def list_capacity_plans():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("capacityPlans", [])

@router.get("/lockin-risks", response_model=List[dict])
async def list_lockin_risks():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("lockInRisks", [])

@router.get("/waves", response_model=List[dict])
async def list_waves():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("waves", [])

@router.get("/minimum-sets", response_model=List[dict])
async def list_minimum_sets():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("minimumSets", [])

@router.get("/rebalances", response_model=List[dict])
async def list_rebalances():
    overview = await TransformationPortfolioService.get_portfolio_overview(None)
    return overview.get("rebalances", [])

@router.post("/rebalances/{rebalance_id}/approve", response_model=dict)
async def approve_rebalance(rebalance_id: str, actor_id: str = Query("usr_chief_investment_officer")):
    return await TransformationPortfolioService.approve_rebalance(None, rebalance_id, actor_id)

@router.post("/rebalances/{rebalance_id}/execute", response_model=dict)
async def execute_rebalance(rebalance_id: str):
    return await TransformationPortfolioService.execute_rebalance(None, rebalance_id)

@router.post("/query", response_model=TransformationPortfolioQueryResultRead)
async def process_portfolio_query(query: str = Query(...)):
    return await TransformationPortfolioService.process_natural_language_portfolio_query(None, query)
