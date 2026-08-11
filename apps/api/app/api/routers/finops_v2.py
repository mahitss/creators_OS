from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from app.services.finops_v2_service import FinOpsV2Service
from app.schemas.finops_v2 import (
    AIUsageEventRead, AIPriceCatalogRead, CostCalculationRead,
    AIBudgetCreate, AIBudgetRead, CostForecastRead,
    OptimizationRecommendationRead, CostOptimizationExperimentCreate,
    CostOptimizationExperimentRead, AICapacitySnapshotRead,
    CostReconciliationRead, CostAdjustmentCreate
)

router = APIRouter(prefix="/finops", tags=["finops_and_capacity_intelligence"])

@router.get("")
async def get_finops_overview():
    return await FinOpsV2Service.get_overview_dashboard(None)

@router.get("/usage")
async def get_usage_events():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    return dash.get("usage_events", [])

@router.get("/costs")
async def get_total_costs():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    return {"totalSpend": dash["totalSpend"], "currency": dash["currency"]}

@router.get("/costs/by-model")
async def get_costs_by_model():
    return await FinOpsV2Service.get_attributed_costs(None, "model")

@router.get("/costs/by-agent")
async def get_costs_by_agent():
    return await FinOpsV2Service.get_attributed_costs(None, "agent")

@router.get("/costs/by-mission")
async def get_costs_by_mission():
    return await FinOpsV2Service.get_attributed_costs(None, "mission")

@router.get("/costs/by-workspace")
async def get_costs_by_workspace():
    return await FinOpsV2Service.get_attributed_costs(None, "workspace")

@router.get("/budgets", response_model=List[AIBudgetRead])
async def get_ai_budgets():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    return [
        AIBudgetRead(
            id=b["id"],
            organizationId=b["organization_id"],
            workspaceId=b.get("workspace_id"),
            teamId=b.get("team_id"),
            agentId=b.get("agent_id"),
            missionId=b.get("mission_id"),
            scope=b["scope"],
            period=b["period"],
            limitAmount=b["limit_amount"],
            currency=b["currency"],
            spentAmount=b["spent_amount"],
            committedAmount=b["committed_amount"],
            forecastAmount=b["forecast_amount"],
            remainingAmount=b["remaining_amount"],
            softThresholdPct=b["soft_threshold_pct"],
            hardLimitAction=b["hard_limit_action"],
            status=b["status"]
        ) for b in dash["budgets"]
    ]

@router.get("/forecasts", response_model=CostForecastRead)
async def get_cost_forecast():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    fc = dash["forecast"]
    return CostForecastRead(
        id=fc["id"],
        organizationId=fc["organization_id"],
        scope=fc["scope"],
        currentPeriodExpected=fc["current_period_expected"],
        lowerBound=fc["lower_bound"],
        upperBound=fc["upper_bound"],
        confidencePct=fc["confidence_pct"],
        createdAt=fc["created_at"]
    )

@router.get("/anomalies")
async def get_spend_anomalies():
    return [
        {
            "id": "anom_01",
            "organization_id": "org_default_creator",
            "spike_magnitude_pct": 145.0,
            "anomaly_classification": "unexpected",
            "driver_summary": "Unusual token consumption spike in Code Reviewer Agent loop",
            "created_at": "2026-08-11T04:00:00Z"
        }
    ]

@router.get("/capacity", response_model=AICapacitySnapshotRead)
async def get_finops_capacity():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    cap = dash["capacity"]
    return AICapacitySnapshotRead(
        id="cap_snap_01",
        concurrencyUsed=cap["concurrencyUsed"],
        concurrencyLimit=cap["concurrencyLimit"],
        queueDepth=cap["queueDepth"],
        providerLimitsJson={"openai_rpm": 10000, "google_tpm": 2000000},
        loadSheddingRecommended=cap["loadSheddingRecommended"],
        createdAt="2026-08-11T04:00:00Z"
    )

@router.get("/optimizations", response_model=List[OptimizationRecommendationRead])
async def get_optimization_recommendations():
    dash = await FinOpsV2Service.get_overview_dashboard(None)
    return [
        OptimizationRecommendationRead(
            id=r["id"],
            organizationId=r["organization_id"],
            type=r["type"],
            estimatedSavings=r["estimated_savings"],
            qualityImpact=r["quality_impact"],
            latencyImpact=r["latency_impact"],
            riskLevel=r["risk_level"],
            confidencePct=r["confidence_pct"],
            evidenceJson=r["evidence_json"],
            approvalStatus=r["approval_status"]
        ) for r in dash["recommendations"]
    ]

@router.post("/optimizations/{rec_id}/simulate")
async def simulate_optimization(rec_id: str):
    return {
        "recommendation_id": rec_id,
        "simulation_result": "SUCCESS",
        "quality_evaluation_score": 4.82,
        "pass_quality_threshold": True,
        "estimated_savings_usd": 145.0
    }

@router.post("/optimizations/{rec_id}/approve")
async def approve_optimization(rec_id: str):
    r = await FinOpsV2Service.approve_recommendation(None, rec_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Recommendation '{rec_id}' not found.")
    return r

@router.post("/optimizations/{rec_id}/apply")
async def apply_optimization(rec_id: str):
    r = await FinOpsV2Service.apply_recommendation(None, rec_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Recommendation '{rec_id}' not found.")
    return r

@router.post("/optimizations/{rec_id}/revert")
async def revert_optimization(rec_id: str):
    r = await FinOpsV2Service.revert_recommendation(None, rec_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Recommendation '{rec_id}' not found.")
    return r

@router.get("/experiments", response_model=List[CostOptimizationExperimentRead])
async def get_optimization_experiments():
    return [
        CostOptimizationExperimentRead(
            id="exp_opt_01",
            recommendationId="rec_model_switch_01",
            baselineConfigJson={"model": "gpt-4o"},
            optimizedConfigJson={"model": "gemini-1.5-pro"},
            baselineCost=15.0,
            optimizedCost=8.5,
            baselineQuality=4.8,
            optimizedQuality=4.78,
            status="running",
            createdAt="2026-08-11T04:00:00Z"
        )
    ]

@router.post("/experiments", response_model=CostOptimizationExperimentRead)
async def create_optimization_experiment(payload: CostOptimizationExperimentCreate):
    rec = payload.model_dump()
    return CostOptimizationExperimentRead(
        id="exp_opt_custom",
        recommendationId=rec["recommendationId"],
        baselineConfigJson=rec["baselineConfigJson"],
        optimizedConfigJson=rec["optimizedConfigJson"],
        baselineCost=12.0,
        optimizedCost=6.0,
        baselineQuality=4.8,
        optimizedQuality=4.8,
        status="running",
        createdAt="2026-08-11T04:00:00Z"
    )

@router.post("/experiments/{exp_id}/start")
async def start_optimization_experiment(exp_id: str):
    return {"id": exp_id, "status": "running"}

@router.post("/experiments/{exp_id}/stop")
async def stop_optimization_experiment(exp_id: str):
    return {"id": exp_id, "status": "completed"}
