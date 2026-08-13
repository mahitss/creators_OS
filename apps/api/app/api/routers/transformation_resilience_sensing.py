from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_sensing import (
    TransformationResilienceSensingDomainRead,
    TransformationResilienceObservationRead,
    TransformationResilienceObservationQualityRead,
    TransformationResilienceSignalNormalizationRead,
    TransformationResilienceDynamicBaselineRead,
    TransformationResilienceDriftRead,
    TransformationResilienceStructuralChangeRead,
    TransformationResilienceAlertEvaluationRead,
    TransformationResilienceSensingWarningRead,
    TransformationResilienceSignalCorrelationRead,
    TransformationResilienceStateChangeRead,
    TransformationResilienceTrendRead,
    TransformationResilienceForecastRead,
    TransformationResilienceAssumptionRead,
    TransformationResilienceAssumptionDriftRead,
    TransformationResilienceInvestmentReviewTriggerRead,
    TransformationPortfolioResilienceStateRead,
    TransformationResilienceSensingQueryResultRead
)
from app.services.transformation_resilience_sensing_service import TransformationResilienceSensingService

router = APIRouter(prefix="/api/v1/transformation-resilience-sensing", tags=["transformation_resilience_sensing"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_sensing_overview():
    return await TransformationResilienceSensingService.get_sensing_overview(None)

@router.post("", response_model=dict)
async def create_sensing_domain(data: dict):
    return {
        "id": "sens_dom_new",
        "name": data.get("name", "New Resilience Sensing Domain"),
        "status": "active",
        "version": "v2.0"
    }

@router.post("/query", response_model=TransformationResilienceSensingQueryResultRead)
async def process_sensing_query(query: str = Query(...)):
    return await TransformationResilienceSensingService.process_natural_language_sensing_query(None, query)

@router.get("/{id}", response_model=dict)
async def get_sensing_domain(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    for d in overview.get("domains", []):
        if d.get("id") == id:
            return d
    return {"id": id, "name": "Global Enterprise Transformation Resilience Sensing 2.0 Domain", "status": "active"}

@router.get("/{id}/state", response_model=dict)
async def get_sensing_state(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("portfolioState", {})

@router.get("/{id}/observations", response_model=List[dict])
async def list_observations(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("observations", [])

@router.get("/{id}/quality", response_model=List[dict])
async def list_qualities(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("qualities", [])

@router.get("/{id}/drift", response_model=List[dict])
async def list_drifts(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("drifts", [])

@router.get("/{id}/structural-changes", response_model=List[dict])
async def list_structural_changes(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("structuralChanges", [])

@router.get("/{id}/warnings", response_model=List[dict])
async def list_warnings(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("warnings", [])

@router.get("/{id}/correlations", response_model=List[dict])
async def list_correlations(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("correlations", [])

@router.get("/{id}/trends", response_model=List[dict])
async def list_trends(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("trends", [])

@router.get("/{id}/forecasts", response_model=List[dict])
async def list_forecasts(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("forecasts", [])

@router.get("/{id}/forecast-validation", response_model=dict)
async def get_forecast_validation(id: str):
    return {
        "domainId": id,
        "forecastErrorPct": 3.2,
        "forecastBias": "slightly_conservative",
        "calibrationScore": 0.96
    }

@router.get("/{id}/assumptions", response_model=List[dict])
async def list_assumptions(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("assumptions", [])

@router.get("/{id}/assumption-drift", response_model=List[dict])
async def list_assumption_drifts(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("assumptionDrifts", [])

@router.get("/{id}/scenario-validity", response_model=dict)
async def get_scenario_validity(id: str):
    return {
        "domainId": id,
        "validScenariosCount": 12,
        "degradedScenariosCount": 2,
        "invalidScenariosCount": 1,
        "needsReviewScenariosCount": 2
    }

@router.get("/{id}/investment-reviews", response_model=List[dict])
async def list_investment_reviews(id: str):
    overview = await TransformationResilienceSensingService.get_sensing_overview(None)
    return overview.get("investmentTriggers", [])

@router.get("/{id}/decision-reviews", response_model=List[dict])
async def list_decision_reviews(id: str):
    return [
        {
            "id": "dec_trig_01",
            "domain_id": id,
            "decision_case_id": "case_iam_arch_01",
            "reason": "Primary Auth SLA assumption drifted from valid to degraded.",
            "severity": "high",
            "status": "review_triggered"
        }
    ]

@router.post("/{id}/reviews/{reviewId}/acknowledge", response_model=dict)
async def acknowledge_review(id: str, reviewId: str):
    return await TransformationResilienceSensingService.acknowledge_review(None, reviewId)
