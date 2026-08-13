from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_portfolio import (
    TransformationResiliencePortfolioRead,
    TransformationPortfolioResilienceExposureRead,
    TransformationSharedDependencyRead,
    TransformationSharedCapacityExposureRead,
    TransformationPortfolioCapacityConflictRead,
    TransformationPortfolioFailurePatternRead,
    TransformationPortfolioSystemicRiskRead,
    TransformationPortfolioMultiFailureScenarioRead,
    TransformationPortfolioResilienceInvestmentRead,
    TransformationResilienceInvestmentOverlapRead,
    TransformationResilienceInvestmentGapRead,
    TransformationResiliencePortfolioTradeoffRead,
    TransformationResilienceInvestmentSequenceRead,
    TransformationResilienceOptionValueRead,
    TransformationResilienceDiversificationPlanRead,
    TransformationPortfolioResilienceRoadmapRead,
    TransformationPortfolioResilienceReviewRead,
    TransformationPortfolioResilienceQueryResultRead
)
from app.services.transformation_resilience_portfolio_service import TransformationResiliencePortfolioService

router = APIRouter(prefix="/api/v1/transformation-resilience-portfolio", tags=["transformation_resilience_portfolio"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_portfolio_overview():
    return await TransformationResiliencePortfolioService.get_portfolio_overview(None)

@router.post("", response_model=dict)
async def create_portfolio(data: dict):
    return {
        "id": "port_res_new",
        "name": data.get("name", "New Transformation Resilience Portfolio"),
        "status": "baseline",
        "version": "v2.0"
    }

@router.get("/reviews", response_model=List[dict])
async def list_reviews():
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("reviews", [])

@router.post("/reviews", response_model=dict)
async def create_review(data: dict):
    return {
        "id": "prev_new",
        "portfolio_id": data.get("portfolio_id", "port_res_01"),
        "review_trigger": data.get("review_trigger", "Manual Resilience Review"),
        "status": "open"
    }

@router.get("/reviews/{id}", response_model=dict)
async def get_review(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    for r in overview.get("reviews", []):
        if r.get("id") == id:
            return r
    return {"id": id, "status": "open"}

@router.post("/reviews/{id}/complete", response_model=dict)
async def complete_review(id: str):
    return await TransformationResiliencePortfolioService.complete_portfolio_review(None, id)

@router.post("/query", response_model=TransformationPortfolioResilienceQueryResultRead)
async def process_portfolio_query(query: str = Query(...)):
    return await TransformationResiliencePortfolioService.process_natural_language_portfolio_query(None, query)

@router.get("/{id}", response_model=dict)
async def get_portfolio(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    for p in overview.get("portfolios", []):
        if p.get("id") == id:
            return p
    return {"id": id, "name": "Global Enterprise Transformation Resilience Portfolio 2.0", "status": "baseline"}

@router.get("/{id}/exposure", response_model=List[dict])
async def list_exposures(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("exposures", [])

@router.get("/{id}/shared-dependencies", response_model=List[dict])
async def list_shared_dependencies(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("sharedDependencies", [])

@router.get("/{id}/capacity", response_model=List[dict])
async def list_capacity_exposures(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("capacityExposures", [])

@router.get("/{id}/failure-patterns", response_model=List[dict])
async def list_failure_patterns(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("failurePatterns", [])

@router.get("/{id}/systemic-risks", response_model=List[dict])
async def list_systemic_risks(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("systemicRisks", [])

@router.get("/{id}/multi-failure-scenarios", response_model=List[dict])
async def list_multi_failure_scenarios(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("multiFailures", [])

@router.post("/{id}/multi-failure-scenarios", response_model=dict)
async def create_multi_failure_scenario(id: str, data: dict):
    return await TransformationResiliencePortfolioService.create_multi_failure_scenario(None, id, data)

@router.get("/{id}/investments", response_model=List[dict])
async def list_investments(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("investments", [])

@router.post("/{id}/investments", response_model=dict)
async def create_investment(id: str, data: dict):
    data["portfolio_id"] = id
    return await TransformationResiliencePortfolioService.create_portfolio_resilience_investment(None, data)

@router.get("/{id}/investments/{investmentId}", response_model=dict)
async def get_investment(id: str, investmentId: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    for inv in overview.get("investments", []):
        if inv.get("id") == investmentId:
            return inv
    return {"id": investmentId, "cost": 350000.0}

@router.post("/{id}/investments/{investmentId}/simulate", response_model=dict)
async def simulate_investment(id: str, investmentId: str):
    return await TransformationResiliencePortfolioService.simulate_investment(None, id, investmentId)

@router.get("/{id}/overlaps", response_model=List[dict])
async def list_overlaps(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("overlaps", [])

@router.get("/{id}/gaps", response_model=List[dict])
async def list_gaps(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("gaps", [])

@router.get("/{id}/tradeoffs", response_model=List[dict])
async def list_tradeoffs(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("tradeoffs", [])

@router.get("/{id}/sequences", response_model=List[dict])
async def list_sequences(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("sequences", [])

@router.get("/{id}/option-value", response_model=List[dict])
async def list_option_values(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return overview.get("optionValues", [])

@router.get("/{id}/robustness", response_model=dict)
async def get_robustness(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    return {
        "portfolioId": id,
        "portfolioRobustnessScore": overview.get("portfolioRobustnessScore", 0.94),
        "baselineScenarioScore": 0.94,
        "stressScenarioScore": 0.91,
        "severeDisruptionScenarioScore": 0.88
    }

@router.get("/{id}/fragility", response_model=dict)
async def get_fragility(id: str):
    return {
        "portfolioId": id,
        "fragilityWarning": "Centralized single-vendor auth dependency creates systemic fragility across Wave 2 and Wave 3."
    }

@router.get("/{id}/roadmap", response_model=dict)
async def get_roadmap(id: str):
    overview = await TransformationResiliencePortfolioService.get_portfolio_overview(None)
    roadmaps = overview.get("roadmaps", [])
    if roadmaps:
        return roadmaps[0]
    return {"id": "proad_01", "status": "draft", "total_budget": 750000.0}

@router.post("/{id}/roadmap", response_model=dict)
async def create_roadmap(id: str, data: dict):
    return {
        "id": "proad_new",
        "portfolio_id": id,
        "roadmap_title": data.get("roadmap_title", "New Portfolio Resilience Roadmap"),
        "total_budget": data.get("total_budget", 750000.0),
        "status": "draft"
    }

@router.get("/{id}/verification", response_model=dict)
async def get_verification(id: str):
    return {
        "portfolioId": id,
        "baselineRobustness": 0.94,
        "plannedRobustness": 0.99,
        "actualPostInvestmentRobustness": 0.98,
        "verificationStatus": "verified"
    }
