from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.services.predictive_operations_service import PredictiveOperationsService
from app.schemas.predictive_operations import (
    ForecastCreate, ForecastRead, ForecastPointRead,
    PredictiveAlertRead, PredictiveRiskRead, PredictiveRecommendationRead,
    CapacityForecastRead, ForecastScenarioRead, ForecastAccuracyRead,
    PredictiveQueryResultRead
)

router = APIRouter(prefix="/predictions", tags=["predictive_operations_and_forecast_intelligence"])

@router.get("")
async def get_predictions_overview():
    return await PredictiveOperationsService.get_predictions_overview(None)

@router.get("/forecasts", response_model=List[ForecastRead])
async def get_forecasts():
    ov = await PredictiveOperationsService.get_predictions_overview(None)
    return [
        ForecastRead(
            id=f["id"],
            organizationId=f["organization_id"],
            workspaceId=f["workspace_id"],
            entityType=f["entity_type"],
            entityId=f["entity_id"],
            metricId=f.get("metric_id"),
            horizon=f["horizon"],
            method=f["method"],
            status=f["status"],
            createdAt=f["created_at"],
            updatedAt=f["updated_at"]
        ) for f in ov["forecasts"]
    ]

@router.post("/forecasts", response_model=ForecastRead)
async def create_forecast(payload: ForecastCreate):
    f = await PredictiveOperationsService.create_forecast(None, payload.model_dump())
    return ForecastRead(
        id=f["id"],
        organizationId=f["organization_id"],
        workspaceId=f["workspace_id"],
        entityType=f["entity_type"],
        entityId=f["entity_id"],
        metricId=f.get("metric_id"),
        horizon=f["horizon"],
        method=f["method"],
        status=f["status"],
        createdAt=f["created_at"],
        updatedAt=f["updated_at"]
    )

@router.get("/alerts", response_model=List[PredictiveAlertRead])
async def get_alerts():
    ov = await PredictiveOperationsService.get_predictions_overview(None)
    return [
        PredictiveAlertRead(
            id=a["id"],
            forecastId=a["forecast_id"],
            alertType=a["alert_type"],
            predictedWindow=a["predicted_window"],
            confidence=a["confidence"],
            status=a["status"],
            createdAt=a["created_at"]
        ) for a in ov["alerts"]
    ]

@router.get("/risks", response_model=List[PredictiveRiskRead])
async def get_risks():
    ov = await PredictiveOperationsService.get_predictions_overview(None)
    return [
        PredictiveRiskRead(
            id=r["id"],
            forecastId=r["forecast_id"],
            riskId=r["risk_id"],
            affectedEntityId=r["affected_entity_id"],
            probabilityRange=r["probability_range"],
            impact=r["impact"],
            evidence=r["evidence"]
        ) for r in ov["risks"]
    ]

@router.get("/scenarios", response_model=List[ForecastScenarioRead])
async def get_scenarios():
    ov = await PredictiveOperationsService.get_predictions_overview(None)
    return [
        ForecastScenarioRead(
            id=s["id"],
            forecastId=s["forecast_id"],
            scenarioName=s["scenario_name"],
            scenarioParamsJson=s["scenario_params_json"],
            outputDistributionJson=s["output_distribution_json"]
        ) for s in ov["scenarios"]
    ]

@router.post("/query", response_model=PredictiveQueryResultRead)
async def query_predictions(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await PredictiveOperationsService.process_natural_language_predictive_query(None, q)
    return PredictiveQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )
