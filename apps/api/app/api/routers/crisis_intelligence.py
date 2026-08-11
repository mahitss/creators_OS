from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.crisis_intelligence import (
    CrisisCreate,
    CrisisRead,
    CrisisSignalRead,
    CrisisImpactAssessmentRead,
    CrisisCommandRead,
    CrisisResponseOptionRead,
    CrisisCommunicationRead,
    CrisisTimelineEventRead,
    AfterActionReviewRead,
    CrisisDrillRead,
    CrisisQueryResultRead
)
from app.services.crisis_intelligence_service import CrisisIntelligenceService

router = APIRouter(prefix="/api/v1/crisis", tags=["crisis_intelligence"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_crisis_overview():
    return await CrisisIntelligenceService.get_crisis_overview(None)

@router.get("/list", response_model=List[dict])
async def list_crises():
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return overview.get("crises", [])

@router.post("", response_model=dict)
async def create_crisis(payload: CrisisCreate):
    return await CrisisIntelligenceService.create_crisis(None, payload.model_dump())

@router.get("/signals", response_model=List[dict])
async def list_signals():
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return overview.get("signals", [])

@router.get("/drills", response_model=List[dict])
async def list_drills():
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return overview.get("drills", [])

@router.get("/{crisis_id}", response_model=dict)
async def get_crisis(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    for c in overview.get("crises", []):
        if c["id"] == crisis_id:
            return c
    raise HTTPException(status_code=404, detail="Crisis not found")

@router.post("/{crisis_id}/resolve", response_model=dict)
async def resolve_crisis(crisis_id: str, criteria: str = Query(...), evidence: str = Query(...)):
    return await CrisisIntelligenceService.resolve_crisis(None, crisis_id, {"criteria": criteria, "evidence": evidence})

@router.get("/{crisis_id}/impact", response_model=List[dict])
async def get_crisis_impact(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return [i for i in overview.get("impacts", []) if i.get("crisis_id") == crisis_id]

@router.get("/{crisis_id}/command", response_model=List[dict])
async def get_crisis_command(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return [cm for cm in overview.get("commands", []) if cm.get("crisis_id") == crisis_id]

@router.get("/{crisis_id}/options", response_model=List[dict])
async def get_crisis_options(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return [o for o in overview.get("options", []) if o.get("crisis_id") == crisis_id]

@router.get("/{crisis_id}/communications", response_model=List[dict])
async def get_crisis_communications(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return [co for co in overview.get("comms", []) if co.get("crisis_id") == crisis_id]

@router.get("/{crisis_id}/timeline", response_model=List[dict])
async def get_crisis_timeline(crisis_id: str):
    overview = await CrisisIntelligenceService.get_crisis_overview(None)
    return [t for t in overview.get("timeline", []) if t.get("crisis_id") == crisis_id]

@router.post("/query", response_model=CrisisQueryResultRead)
async def process_crisis_query(query: str = Query(...)):
    return await CrisisIntelligenceService.process_natural_language_crisis_query(None, query)
