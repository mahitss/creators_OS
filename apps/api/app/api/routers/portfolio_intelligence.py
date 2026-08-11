from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.services.portfolio_intelligence_service import PortfolioIntelligenceService
from app.schemas.portfolio_intelligence import (
    PortfolioCreate, PortfolioRead, ProgramCreate, ProgramRead,
    PortfolioResourceConflictRead, PortfolioOverlapRead,
    PortfolioOutcomeVarianceRead, PortfolioRecommendationRead,
    PortfolioReviewRead, PortfolioScenarioRead, PortfolioQueryResultRead
)

router = APIRouter(prefix="/portfolio", tags=["portfolio_intelligence_and_investment_optimization"])

@router.get("")
async def get_portfolio_overview():
    return await PortfolioIntelligenceService.get_portfolio_overview(None)

@router.post("", response_model=PortfolioRead)
async def create_portfolio(payload: PortfolioCreate):
    p = await PortfolioIntelligenceService.create_portfolio(None, payload.model_dump())
    return PortfolioRead(
        id=p["id"],
        organizationId=p["organization_id"],
        workspaceId=p["workspace_id"],
        name=p["name"],
        description=p["description"],
        owner=p["owner"],
        status=p["status"],
        createdAt=p["created_at"],
        updatedAt=p["updated_at"]
    )

@router.get("/{p_id}", response_model=PortfolioRead)
async def get_portfolio_by_id(p_id: str):
    ov = await PortfolioIntelligenceService.get_portfolio_overview(None, p_id)
    p = ov["portfolio"]
    return PortfolioRead(
        id=p["id"],
        organizationId=p["organization_id"],
        workspaceId=p["workspace_id"],
        name=p["name"],
        description=p["description"],
        owner=p["owner"],
        status=p["status"],
        createdAt=p["created_at"],
        updatedAt=p["updated_at"]
    )

@router.get("/programs", response_model=List[ProgramRead])
async def get_programs():
    ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
    return [
        ProgramRead(
            id=pr["id"],
            portfolioId=pr["portfolio_id"],
            name=pr["name"],
            description=pr["description"],
            owner=pr["owner"],
            status=pr["status"],
            priority=pr["priority"],
            targetOutcome=pr["target_outcome"]
        ) for pr in ov["programs"]
    ]

@router.get("/conflicts", response_model=List[PortfolioResourceConflictRead])
async def get_resource_conflicts():
    ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
    return [
        PortfolioResourceConflictRead(
            id=c["id"],
            portfolioId=c["portfolio_id"],
            resourceType=c["resource_type"],
            competingInitiativesJson=c["competing_initiatives_json"],
            timeWindow=c["time_window"],
            capacityGapSummary=c["capacity_gap_summary"],
            status=c["status"]
        ) for c in ov["conflicts"]
    ]

@router.get("/overlaps", response_model=List[PortfolioOverlapRead])
async def get_overlaps():
    ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
    return [
        PortfolioOverlapRead(
            id=o["id"],
            portfolioId=o["portfolio_id"],
            initiativeIdsJson=o["initiative_ids_json"],
            overlapType=o["overlap_type"],
            similaritySummary=o["similarity_summary"],
            status=o["status"]
        ) for o in ov["overlaps"]
    ]

@router.get("/recommendations", response_model=List[PortfolioRecommendationRead])
async def get_recommendations():
    ov = await PortfolioIntelligenceService.get_portfolio_overview(None)
    return [
        PortfolioRecommendationRead(
            id=r["id"],
            portfolioId=r["portfolio_id"],
            recommendation=r["recommendation"],
            evidenceJson=r["evidence_json"],
            alternativesJson=r["alternatives_json"],
            tradeoffsJson=r["tradeoffs_json"],
            reversibility=r["reversibility"],
            approvalStatus=r["approval_status"],
            confidencePct=r["confidence_pct"]
        ) for r in ov["recommendations"]
    ]

@router.post("/query", response_model=PortfolioQueryResultRead)
async def query_portfolio(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await PortfolioIntelligenceService.process_natural_language_portfolio_query(None, q)
    return PortfolioQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )
