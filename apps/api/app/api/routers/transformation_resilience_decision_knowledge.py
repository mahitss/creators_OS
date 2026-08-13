from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_decision_knowledge import (
    TransformationResilienceDecisionKnowledgeDomainRead,
    TransformationResilienceDecisionKnowledgeObjectRead,
    TransformationResilienceDecisionKnowledgeValidationRead,
    TransformationResilienceDecisionKnowledgeContextRead,
    TransformationResilienceDecisionKnowledgeApplicabilityRead,
    TransformationResilienceDecisionKnowledgeConflictRead,
    TransformationResilienceDecisionKnowledgeInvalidationRead,
    TransformationResilienceDecisionKnowledgeReviewRead,
    TransformationResilienceDecisionKnowledgeReuseRead,
    TransformationResilienceDecisionKnowledgePackRead,
    TransformationResilienceDecisionKnowledgeQualityRead,
    TransformationResilienceDecisionKnowledgeGapRead,
    TransformationResilienceDecisionKnowledgeQueryResultRead
)
from app.services.transformation_resilience_decision_knowledge_service import TransformationResilienceDecisionKnowledgeService

router = APIRouter(prefix="/api/v1/transformation-resilience-decision-knowledge", tags=["transformation_resilience_decision_knowledge"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_decision_knowledge_overview():
    return await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)

@router.post("", response_model=dict)
async def create_knowledge_domain(data: dict):
    return {
        "id": "kdom_new",
        "name": data.get("name", "New Decision Knowledge Domain"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceDecisionKnowledgeQueryResultRead)
async def process_knowledge_query(query: str = Query(...)):
    return await TransformationResilienceDecisionKnowledgeService.process_natural_language_knowledge_query(None, query)

@router.get("/gaps", response_model=List[dict])
async def list_knowledge_gaps():
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("gaps", [])

@router.get("/gaps/{id}", response_model=dict)
async def get_knowledge_gap(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    for g in overview.get("gaps", []):
        if g.get("id") == id:
            return g
    return {"id": id, "gap_title": "Missing Precedent", "priority": "high"}

@router.post("/packs", response_model=dict)
async def create_knowledge_pack(data: dict):
    decision_id = data.get("decision_id", "dec_res_01")
    return await TransformationResilienceDecisionKnowledgeService.create_knowledge_pack(None, decision_id)

@router.get("/packs/{id}", response_model=dict)
async def get_knowledge_pack(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    for p in overview.get("packs", []):
        if p.get("id") == id:
            return p
    return {"id": id, "pack_version": "v1.0", "decision_id": "dec_res_01"}

@router.post("/retrieve", response_model=dict)
async def retrieve_knowledge(data: dict):
    decision_context_id = data.get("decision_context_id", "dec_wave_04_hr")
    return await TransformationResilienceDecisionKnowledgeService.retrieve_decision_knowledge(None, decision_context_id)

@router.get("/{id}", response_model=dict)
async def get_knowledge_object(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    for k in overview.get("knowledgeObjects", []):
        if k.get("id") == id:
            return k
    return {"id": id, "statement": "Governed Resilience Decision Knowledge Object", "status": "validated"}

@router.get("/{id}/validation", response_model=List[dict])
async def get_knowledge_validation(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("validations", [])

@router.get("/{id}/applicability", response_model=List[dict])
async def get_knowledge_applicability(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("applicabilities", [])

@router.get("/{id}/conflicts", response_model=List[dict])
async def get_knowledge_conflicts(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("conflicts", [])

@router.get("/{id}/reviews", response_model=List[dict])
async def get_knowledge_reviews(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("reviews", [])

@router.get("/{id}/reuse", response_model=List[dict])
async def list_knowledge_reuse(id: str):
    overview = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
    return overview.get("reuses", [])

@router.post("/{id}/reuse", response_model=dict)
async def record_knowledge_reuse(id: str, data: dict):
    data["knowledge_object_id"] = id
    return await TransformationResilienceDecisionKnowledgeService.record_reuse(None, data)
