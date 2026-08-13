from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.transformation_resilience_knowledge_governance import (
    TransformationResilienceKnowledgeAssuranceDomainRead,
    TransformationResilienceKnowledgeHealthRead,
    TransformationResilienceKnowledgeEvidenceAssuranceRead,
    TransformationResilienceKnowledgeClaimRead,
    TransformationResilienceKnowledgeClaimSupportRead,
    TransformationResilienceKnowledgeClaimConflictRead,
    TransformationResilienceKnowledgeContextDriftRead,
    TransformationResilienceKnowledgeReuseAssuranceRead,
    TransformationResilienceKnowledgeInfluenceRead,
    TransformationResilienceKnowledgeRiskRead,
    TransformationResilienceKnowledgeAssuranceReviewRead,
    TransformationResilienceKnowledgeAssuranceReviewPacketRead,
    TransformationResilienceKnowledgeRevalidationRead,
    TransformationResilienceKnowledgeLineageRead,
    TransformationResilienceKnowledgeEvidenceGapRead,
    TransformationResilienceKnowledgeGovernanceStateRead,
    TransformationResilienceKnowledgeGovernanceQueryResultRead
)
from app.services.transformation_resilience_knowledge_governance_service import TransformationResilienceKnowledgeGovernanceService

router = APIRouter(prefix="/api/v1/transformation-resilience-knowledge-governance", tags=["transformation_resilience_knowledge_governance"])

@router.get("", response_model=dict)
@router.get("/overview", response_model=dict)
async def get_knowledge_governance_overview():
    return await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)

@router.post("", response_model=dict)
async def create_assurance_domain(data: dict):
    return {
        "id": "adom_new",
        "name": data.get("name", "New Knowledge Assurance Domain"),
        "status": "active"
    }

@router.post("/query", response_model=TransformationResilienceKnowledgeGovernanceQueryResultRead)
async def process_governance_query(query: str = Query(...)):
    return await TransformationResilienceKnowledgeGovernanceService.process_natural_language_governance_query(None, query)

@router.get("/gaps", response_model=List[dict])
async def list_evidence_gaps():
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("gaps", [])

@router.get("/gaps/{gapId}", response_model=dict)
async def get_evidence_gap(gapId: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    for g in overview.get("gaps", []):
        if g.get("id") == gapId:
            return g
    return {"id": gapId, "gap_title": "Lack of Independent Corroboration", "priority": "high"}

@router.get("/{id}", response_model=dict)
async def get_assurance_domain(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    for dom in overview.get("domains", []):
        if dom.get("id") == id:
            return dom
    return {"id": id, "name": "Global Enterprise Continuous Knowledge Assurance & Evidence Quality 2.0", "status": "active"}

@router.get("/{id}/health", response_model=List[dict])
async def get_knowledge_health(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("healths", [])

@router.get("/{id}/evidence", response_model=List[dict])
async def get_evidence_assurance(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("evidence", [])

@router.get("/{id}/claims", response_model=List[dict])
async def list_claims(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("claims", [])

@router.get("/{id}/conflicts", response_model=List[dict])
async def list_conflicts(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("conflicts", [])

@router.get("/{id}/context-drift", response_model=List[dict])
async def list_context_drifts(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("drifts", [])

@router.get("/{id}/reuse", response_model=List[dict])
async def list_reuse_assurances(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("reuses", [])

@router.get("/{id}/risks", response_model=List[dict])
async def list_knowledge_risks(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("risks", [])

@router.get("/{id}/influence", response_model=List[dict])
async def list_influences(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("influences", [])

@router.get("/{id}/reviews", response_model=List[dict])
async def list_assurance_reviews(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("reviews", [])

@router.post("/{id}/reviews", response_model=dict)
async def request_assurance_review(id: str, data: dict):
    return {
        "id": "arev_new",
        "knowledge_object_id": id,
        "trigger": data.get("trigger", "manual_review_request"),
        "priority": "high",
        "status": "pending"
    }

@router.get("/{id}/reviews/{reviewId}", response_model=dict)
async def get_review_packet(id: str, reviewId: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    for p in overview.get("packets", []):
        if p.get("review_id") == reviewId:
            return p
    return {"id": "apack_01", "review_id": reviewId, "recommended_action": "revalidate"}

@router.post("/{id}/reviews/{reviewId}/revalidate", response_model=dict)
async def revalidate_knowledge(id: str, reviewId: str, data: dict):
    return await TransformationResilienceKnowledgeGovernanceService.revalidate_knowledge(None, reviewId, data)

@router.get("/{id}/lineage", response_model=List[dict])
async def get_knowledge_lineage(id: str):
    overview = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
    return overview.get("lineages", [])
