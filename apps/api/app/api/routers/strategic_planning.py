from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.services.strategic_planning_service import StrategicPlanningService
from app.schemas.strategic_planning import (
    StrategicPlanCreate, StrategicPlanRead, StrategicObjectiveCreate,
    StrategicObjectiveRead, StrategicInitiativeCreate, StrategicInitiativeRead,
    StrategicAssumptionCreate, StrategicAssumptionRead, StrategicRecommendationRead,
    StrategicReviewRead, StrategicDriftRead, StrategicScenarioRead, StrategyQueryResultRead
)

router = APIRouter(prefix="/strategy", tags=["strategic_planning_and_scenario_intelligence"])

@router.get("")
async def get_strategy_overview():
    return await StrategicPlanningService.get_strategy_overview(None)

@router.post("/plans", response_model=StrategicPlanRead)
async def create_plan(payload: StrategicPlanCreate):
    p = await StrategicPlanningService.create_plan(None, payload.model_dump())
    return StrategicPlanRead(
        id=p["id"],
        organizationId=p["organization_id"],
        workspaceId=p["workspace_id"],
        name=p["name"],
        description=p["description"],
        owner=p["owner"],
        status=p["status"],
        startDate=p["start_date"],
        endDate=p["end_date"],
        version=p["version"],
        createdAt=p["created_at"],
        updatedAt=p["updated_at"]
    )

@router.get("/plans/{p_id}", response_model=StrategicPlanRead)
async def get_plan_by_id(p_id: str):
    ov = await StrategicPlanningService.get_strategy_overview(None, p_id)
    p = ov["plan"]
    return StrategicPlanRead(
        id=p["id"],
        organizationId=p["organization_id"],
        workspaceId=p["workspace_id"],
        name=p["name"],
        description=p["description"],
        owner=p["owner"],
        status=p["status"],
        startDate=p["start_date"],
        endDate=p["end_date"],
        version=p["version"],
        createdAt=p["created_at"],
        updatedAt=p["updated_at"]
    )

@router.get("/objectives", response_model=List[StrategicObjectiveRead])
async def get_objectives():
    ov = await StrategicPlanningService.get_strategy_overview(None)
    return [
        StrategicObjectiveRead(
            id=o["id"],
            planId=o["plan_id"],
            name=o["name"],
            description=o["description"],
            priority=o["priority"],
            owner=o["owner"],
            status=o["status"],
            target=o["target"],
            currentState=o["current_state"],
            deadline=o["deadline"]
        ) for o in ov["objectives"]
    ]

@router.get("/assumptions", response_model=List[StrategicAssumptionRead])
async def get_assumptions():
    ov = await StrategicPlanningService.get_strategy_overview(None)
    return [
        StrategicAssumptionRead(
            id=a["id"],
            planId=a["plan_id"],
            statement=a["statement"],
            source=a["source"],
            confidence=a["confidence"],
            assumptionType=a["assumption_type"],
            validity=a["validity"],
            createdAt=a["created_at"],
            verifiedAt=a.get("verified_at"),
            expiresAt=a.get("expires_at")
        ) for a in ov["assumptions"]
    ]

@router.post("/assumptions/{a_id}/verify", response_model=StrategicAssumptionRead)
async def verify_assumption(a_id: str):
    a = await StrategicPlanningService.verify_assumption(None, a_id)
    return StrategicAssumptionRead(
        id=a["id"],
        planId=a["plan_id"],
        statement=a["statement"],
        source=a["source"],
        confidence=a["confidence"],
        assumptionType=a["assumption_type"],
        validity=a["validity"],
        createdAt=a["created_at"],
        verifiedAt=a.get("verified_at"),
        expiresAt=a.get("expires_at")
    )

@router.get("/recommendations", response_model=List[StrategicRecommendationRead])
async def get_recommendations():
    ov = await StrategicPlanningService.get_strategy_overview(None)
    return [
        StrategicRecommendationRead(
            id=r["id"],
            planId=r["plan_id"],
            recommendation=r["recommendation"],
            evidenceJson=r["evidence_json"],
            alternativesJson=r["alternatives_json"],
            tradeoffsJson=r["tradeoffs_json"],
            risksJson=r["risks_json"],
            assumptionsJson=r["assumptions_json"],
            confidencePct=r["confidence_pct"]
        ) for r in ov["recommendations"]
    ]

@router.get("/scenarios", response_model=List[StrategicScenarioRead])
async def get_scenarios():
    return [
        StrategicScenarioRead(
            id="scen_base_01",
            name="Base Case Execution",
            scenarioType="base_case",
            changedAssumptions=[],
            impactSummary={"revenue": "$12M", "on_schedule_pct": 95},
            confidencePct=95.0
        ),
        StrategicScenarioRead(
            id="scen_downside_01",
            name="Downside Market Compression",
            scenarioType="downside",
            changedAssumptions=["Market demand growth slows to 10%"],
            impactSummary={"revenue": "$9.5M", "on_schedule_pct": 80},
            confidencePct=85.0
        )
    ]

@router.post("/query", response_model=StrategyQueryResultRead)
async def query_strategy(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await StrategicPlanningService.process_natural_language_strategy_query(None, q)
    return StrategyQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )
