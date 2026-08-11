from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_decisions import (
    TransformationDecisionCaseRead,
    TransformationDecisionQuestionRead,
    TransformationEvidencePackRead,
    TransformationEvidenceItemRead,
    TransformationEvidenceConflictRead,
    TransformationDecisionAssumptionRead,
    TransformationDecisionOptionRead,
    TransformationDecisionTradeoffRead,
    TransformationDecisionRecommendationRead,
    TransformationDecisionPacketRead,
    TransformationDecisionReadinessRead,
    TransformationDecisionLearningRead,
    TransformationDecisionReassessmentRead,
    TransformationQueryResultRead
)
from app.services.transformation_decisions_service import TransformationDecisionsService

router = APIRouter(prefix="/api/v1/transformation-decisions", tags=["transformation_decisions"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_decisions_overview():
    return await TransformationDecisionsService.get_decisions_overview(None)

@router.post("", response_model=dict)
async def create_decision_case(data: dict):
    return {"id": "case_new", "status": "draft", "title": data.get("title", "New Transformation Decision Case")}

@router.get("/{id}", response_model=dict)
async def get_decision_case(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    cases = overview.get("cases", [])
    for c in cases:
        if c.get("id") == id:
            return c
    return {"id": id, "title": "Wave 2 Scale Authorization", "status": "ready"}

@router.patch("/{id}", response_model=dict)
async def update_decision_case(id: str, data: dict):
    return {"id": id, "updated": True, "data": data}

@router.get("/{id}/evidence", response_model=List[dict])
async def list_case_evidence(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    return overview.get("items", [])

@router.get("/{id}/options", response_model=List[dict])
async def list_case_options(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    return overview.get("options", [])

@router.get("/{id}/scenarios", response_model=List[dict])
async def list_case_scenarios(id: str):
    return [
        {"scenarioId": "baseline", "outcome": "$4.2M OpEx Reduction", "uncertainty": "low"},
        {"scenarioId": "disruptive", "outcome": "$6.1M OpEx Reduction", "uncertainty": "medium"}
    ]

@router.get("/{id}/tradeoffs", response_model=List[dict])
async def list_case_tradeoffs(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    return overview.get("tradeoffs", [])

@router.post("/{id}/analyze", response_model=dict)
async def analyze_decision_case(id: str):
    return {"id": id, "analysisStatus": "completed", "qualityScore": 0.94}

@router.post("/{id}/compare", response_model=dict)
async def compare_options(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    return {"id": id, "options": overview.get("options", []), "tradeoffs": overview.get("tradeoffs", [])}

@router.post("/{id}/simulate", response_model=dict)
async def simulate_case(id: str):
    return {"id": id, "simulationStatus": "completed", "robustOptionId": "opt_scale_full"}

@router.get("/{id}/readiness", response_model=dict)
async def get_case_readiness(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    readinesses = overview.get("readinesses", [])
    for r in readinesses:
        if r.get("decision_case_id") == id:
            return r
    return {"id": id, "status": "ready"}

@router.get("/{id}/recommendation", response_model=dict)
async def get_case_recommendation(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    recs = overview.get("recommendations", [])
    for r in recs:
        if r.get("decision_case_id") == id:
            return r
    return {"id": id, "recommendedOptionId": "opt_scale_full", "confidence": "high"}

@router.get("/{id}/packet", response_model=dict)
async def get_case_packet(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    packets = overview.get("packets", [])
    for p in packets:
        if p.get("decision_case_id") == id:
            return p
    return {"id": id, "versionTag": "v1.0"}

@router.post("/{id}/packet/generate", response_model=dict)
async def generate_case_packet(id: str):
    return {"id": id, "versionTag": "v1.1", "packetGenerated": True}

@router.get("/{id}/packet/history", response_model=List[dict])
async def get_packet_history(id: str):
    overview = await TransformationDecisionsService.get_decisions_overview(None)
    return overview.get("packets", [])

@router.post("/{id}/submit", response_model=dict)
async def submit_case_for_approval(id: str):
    return {"id": id, "status": "under_review", "submitted": True}

@router.post("/{id}/approve", response_model=dict)
async def approve_decision_case(id: str):
    return {"id": id, "status": "approved", "approved": True, "approver": "Executive Transformation Steering Committee"}

@router.post("/{id}/reject", response_model=dict)
async def reject_decision_case(id: str):
    return {"id": id, "status": "rejected", "rejected": True}

@router.post("/{id}/reassess", response_model=dict)
async def reassess_decision_case(id: str):
    return {"id": id, "status": "reassessing", "reassessmentTriggered": True}

@router.post("/{id}/execute", response_model=dict)
async def execute_decision(id: str):
    return {"id": id, "status": "executing", "actionGatewayTriggered": True}

@router.post("/{id}/verify", response_model=dict)
async def verify_decision_outcome(id: str):
    return {"id": id, "status": "verified", "verified": True}

@router.post("/query", response_model=TransformationQueryResultRead)
async def process_decision_query(query: str = Query(...)):
    return await TransformationDecisionsService.process_natural_language_decision_query(None, query)
