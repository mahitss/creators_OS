from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.threat_intelligence import (
    ThreatSignalRead,
    WeakSignalRead,
    ThreatPatternRead,
    EmergingThreatRead,
    EarlyWarningRead,
    ThreatMitigationRead,
    ThreatBlindSpotRead,
    ThreatQueryResultRead
)
from app.services.threat_intelligence_service import ThreatIntelligenceService

router = APIRouter(prefix="/api/v1/threats", tags=["threat_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_threat_overview():
    return await ThreatIntelligenceService.get_threat_overview(None)

@router.get("/signals", response_model=List[dict])
async def list_signals():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("signals", [])

@router.get("/weak-signals", response_model=List[dict])
async def list_weak_signals():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("weakSignals", [])

@router.get("/patterns", response_model=List[dict])
async def list_patterns():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("patterns", [])

@router.get("/emerging", response_model=List[dict])
async def list_emerging_threats():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("threats", [])

@router.get("/warnings", response_model=List[dict])
async def list_warnings():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("warnings", [])

@router.post("/warnings/{warning_id}/suppress", response_model=dict)
async def suppress_warning(warning_id: str, reason: str = Query(...), actor: str = Query("usr_threat_architect")):
    return await ThreatIntelligenceService.suppress_early_warning(None, warning_id, {"reason": reason, "actor": actor})

@router.get("/mitigations", response_model=List[dict])
async def list_mitigations():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("mitigations", [])

@router.post("/mitigations/{mitigation_id}/execute", response_model=dict)
async def execute_mitigation(mitigation_id: str):
    return await ThreatIntelligenceService.execute_mitigation(None, mitigation_id)

@router.get("/accuracy", response_model=dict)
async def get_accuracy():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return {
        "precision": overview.get("precisionScore", 0.94),
        "recall": overview.get("recallScore", 0.91),
        "leadTimeHours": 48.5,
        "calibrationStatus": "well_calibrated"
    }

@router.get("/blind-spots", response_model=List[dict])
async def list_blind_spots():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("blindSpots", [])

@router.get("/coverage", response_model=List[dict])
async def list_coverage():
    overview = await ThreatIntelligenceService.get_threat_overview(None)
    return overview.get("coverages", [])

@router.post("/query", response_model=ThreatQueryResultRead)
async def process_threat_query(query: str = Query(...)):
    return await ThreatIntelligenceService.process_natural_language_threat_query(None, query)
