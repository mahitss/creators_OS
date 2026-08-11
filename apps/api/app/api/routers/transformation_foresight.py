from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_foresight import (
    TransformationForesightDomainRead,
    TransformationFutureDriverRead,
    TransformationDriverTrendRead,
    TransformationWeakSignalRead,
    TransformationEmergingPatternRead,
    TransformationFutureStateRead,
    TransformationScenarioImpactRead,
    TransformationSecondOrderEffectRead,
    TransformationVulnerabilityProfileRead,
    TransformationOpportunityProfileRead,
    TransformationNoRegretActionRead,
    TransformationForesightTriggerRead,
    TransformationForecastVersionRead,
    TransformationForesightReviewRead,
    TransformationQueryResultRead
)
from app.services.transformation_foresight_service import TransformationForesightService

router = APIRouter(prefix="/api/v1/transformation-foresight", tags=["transformation_foresight"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_foresight_overview():
    return await TransformationForesightService.get_foresight_overview(None)

@router.get("/drivers", response_model=List[dict])
async def list_drivers():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("drivers", [])

@router.get("/weak-signals", response_model=List[dict])
async def list_weak_signals():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("signals", [])

@router.get("/patterns", response_model=List[dict])
async def list_patterns():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("patterns", [])

@router.get("/trends", response_model=List[dict])
async def list_trends():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("trends", [])

@router.get("/future-states", response_model=List[dict])
async def list_future_states():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("futureStates", [])

@router.get("/scenarios", response_model=List[dict])
async def list_scenarios():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("scenarioImpacts", [])

@router.get("/scenarios/{id}", response_model=dict)
async def get_scenario(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    scenarios = overview.get("scenarioImpacts", [])
    for sc in scenarios:
        if sc.get("id") == id or sc.get("scenario_id") == id:
            return sc
    raise HTTPException(status_code=404, detail="Scenario not found")

@router.get("/scenarios/{id}/exposure", response_model=dict)
async def get_scenario_exposure(id: str):
    return {
        "scenarioId": id,
        "exposureScore": 0.12,
        "exposedTransformations": ["cand_01", "cand_02"],
        "timeToImpact": "medium_term"
    }

@router.get("/scenarios/{id}/impacts", response_model=List[dict])
async def list_scenario_impacts(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("secondOrderEffects", [])

@router.get("/vulnerability", response_model=List[dict])
async def list_vulnerabilities():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("vulnerabilities", [])

@router.get("/vulnerability/{transformation_id}", response_model=dict)
async def get_transformation_vulnerability(transformation_id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    vulns = overview.get("vulnerabilities", [])
    for v in vulns:
        if v.get("transformation_id") == transformation_id:
            return v
    return {
        "transformationId": transformation_id,
        "vulnerabilityDimensionsJson": {"dependency": 0.12, "capacity": 0.15},
        "overallScore": 0.15
    }

@router.get("/opportunities", response_model=List[dict])
async def list_opportunities():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("opportunities", [])

@router.get("/robustness", response_model=dict)
async def get_robustness():
    return {
        "robustTransformations": ["cand_01", "cand_02"],
        "fragileTransformations": [],
        "overallRobustnessScore": 0.94
    }

@router.get("/triggers", response_model=List[dict])
async def list_triggers():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("triggers", [])

@router.post("/triggers", response_model=dict)
async def create_trigger(data: dict):
    return {"id": "trig_new", "status": "watching", "evidence": data}

@router.get("/triggers/{id}", response_model=dict)
async def get_trigger(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    triggers = overview.get("triggers", [])
    for tr in triggers:
        if tr.get("id") == id:
            return tr
    return {"id": id, "status": "watching"}

@router.post("/triggers/{id}/acknowledge", response_model=dict)
async def acknowledge_trigger(id: str):
    return {"id": id, "status": "acknowledged", "acknowledged": True}

@router.post("/triggers/{id}/resolve", response_model=dict)
async def resolve_trigger(id: str):
    return {"id": id, "status": "resolved", "resolved": True}

@router.get("/forecasts", response_model=List[dict])
async def list_forecasts():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("forecastVersions", [])

@router.get("/forecasts/{id}", response_model=dict)
async def get_forecast(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    fv = overview.get("forecastVersions", [])
    for f in fv:
        if f.get("id") == id:
            return f
    return {"id": id, "versionTag": "v2026.3.1", "confidence": 0.93}

@router.get("/forecasts/{id}/history", response_model=List[dict])
async def get_forecast_history(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("forecastVersions", [])

@router.get("/calibration", response_model=dict)
async def get_calibration():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return {
        "calibrationAccuracyPct": overview.get("calibrationAccuracyPct", 96.0),
        "errors": overview.get("forecastErrors", [])
    }

@router.get("/reviews", response_model=List[dict])
async def list_reviews():
    overview = await TransformationForesightService.get_foresight_overview(None)
    return overview.get("reviews", [])

@router.post("/reviews", response_model=dict)
async def create_review(data: dict):
    return {"id": "rev_new", "status": "created", "summary": data}

@router.get("/reviews/{id}", response_model=dict)
async def get_review(id: str):
    overview = await TransformationForesightService.get_foresight_overview(None)
    reviews = overview.get("reviews", [])
    for r in reviews:
        if r.get("id") == id:
            return r
    return {"id": id, "status": "active"}

@router.post("/reviews/{id}/complete", response_model=dict)
async def complete_review(id: str):
    return {"id": id, "status": "completed", "completed": True}

@router.post("/query", response_model=TransformationQueryResultRead)
async def process_foresight_query(query: str = Query(...)):
    return await TransformationForesightService.process_natural_language_foresight_query(None, query)
