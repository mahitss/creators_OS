from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.services.performance_intelligence_service import PerformanceIntelligenceService
from app.schemas.performance_intelligence import (
    KPICreate, KPIRead, KPITargetCreate, KPITargetRead,
    KPIMeasurementCreate, KPIMeasurementRead, KPIVarianceRead,
    KPIAlertRead, KPIDriverRead, KPIForecastRead, KPIScorecardRead,
    KPIQueryResultRead
)

router = APIRouter(prefix="/performance", tags=["performance_intelligence_and_kpi_operating_system"])

@router.get("")
async def get_performance_overview():
    return await PerformanceIntelligenceService.get_performance_overview(None)

@router.get("/kpis", response_model=List[KPIRead])
async def get_kpis():
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIRead(
            id=k["id"],
            organizationId=k["organization_id"],
            workspaceId=k["workspace_id"],
            name=k["name"],
            description=k["description"],
            definition=k["definition"],
            owner=k["owner"],
            status=k["status"],
            category=k["category"],
            unit=k["unit"],
            direction=k["direction"],
            createdAt=k["created_at"],
            updatedAt=k["updated_at"]
        ) for k in ov["kpis"]
    ]

@router.post("/kpis", response_model=KPIRead)
async def create_kpi(payload: KPICreate):
    k = await PerformanceIntelligenceService.create_kpi(None, payload.model_dump())
    return KPIRead(
        id=k["id"],
        organizationId=k["organization_id"],
        workspaceId=k["workspace_id"],
        name=k["name"],
        description=k["description"],
        definition=k["definition"],
        owner=k["owner"],
        status=k["status"],
        category=k["category"],
        unit=k["unit"],
        direction=k["direction"],
        createdAt=k["created_at"],
        updatedAt=k["updated_at"]
    )

@router.get("/kpis/{kpi_id}/history", response_model=List[KPIMeasurementRead])
async def get_kpi_history(kpi_id: str):
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIMeasurementRead(
            id=m["id"],
            kpiId=m["kpi_id"],
            value=m["value"],
            timestamp=m["timestamp"],
            periodStart=m["period_start"],
            periodEnd=m["period_end"],
            source=m["source"],
            quality=m["quality"],
            confidence=m["confidence"]
        ) for m in ov["measurements"] if m["kpi_id"] == kpi_id
    ]

@router.get("/kpis/{kpi_id}/alerts", response_model=List[KPIAlertRead])
async def get_kpi_alerts(kpi_id: str):
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIAlertRead(
            id=a["id"],
            kpiId=a["kpi_id"],
            alertType=a["alert_type"],
            title=a["title"],
            description=a["description"],
            status=a["status"],
            createdAt=a["created_at"]
        ) for a in ov["alerts"] if a["kpi_id"] == kpi_id
    ]

@router.get("/kpis/{kpi_id}/drivers", response_model=List[KPIDriverRead])
async def get_kpi_drivers(kpi_id: str):
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIDriverRead(
            id=d["id"],
            kpiId=d["kpi_id"],
            driverName=d["driver_name"],
            driverType=d["driver_type"],
            associationType=d["association_type"],
            confidencePct=d["confidence_pct"],
            evidenceSummary=d["evidence_summary"]
        ) for d in ov["drivers"] if d["kpi_id"] == kpi_id
    ]

@router.get("/kpis/{kpi_id}/forecasts", response_model=List[KPIForecastRead])
async def get_kpi_forecasts(kpi_id: str):
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIForecastRead(
            id=f["id"],
            kpiId=f["kpi_id"],
            forecastValue=f["forecast_value"],
            lowerBound=f["lower_bound"],
            upperBound=f["upper_bound"],
            confidencePct=f["confidence_pct"],
            generatedAt=f["generated_at"]
        ) for f in ov["forecasts"] if f["kpi_id"] == kpi_id
    ]

@router.get("/scorecards", response_model=List[KPIScorecardRead])
async def get_scorecards():
    ov = await PerformanceIntelligenceService.get_performance_overview(None)
    return [
        KPIScorecardRead(
            id=s["id"],
            organizationId=s["organization_id"],
            name=s["name"],
            scorecardType=s["scorecard_type"],
            kpiIdsJson=s["kpi_ids_json"]
        ) for s in ov["scorecards"]
    ]

@router.post("/query", response_model=KPIQueryResultRead)
async def query_performance(query_payload: Dict[str, str]):
    q = query_payload.get("query", "")
    res = await PerformanceIntelligenceService.process_natural_language_performance_query(None, q)
    return KPIQueryResultRead(
        query=res["query"],
        results=res["results"],
        evidenceJson=res["evidenceJson"],
        confidencePct=res["confidencePct"]
    )
