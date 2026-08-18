from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.intelligence_governance import (
    KnowledgeGovernanceOverview,
    KnowledgeProvenanceRead,
    SourceAuthorityRead,
    KnowledgeClaimRead,
    KnowledgeConflictRead,
    TrustedContextRequest,
    TrustedContextResponse,
    CitationValidationResponse,
    AIOutputProvenanceRead,
    KnowledgeFeedbackRequest,
    KnowledgeVerificationRequest
)
from app.services import intelligence_governance_service
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_workspace, WorkspaceContext

router = APIRouter(prefix="/knowledge", tags=["Enterprise Intelligence Governance & Trusted Knowledge Fabric"])

@router.get("/governance", response_model=KnowledgeGovernanceOverview)
async def get_governance_overview(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Returns high-level intelligence governance telemetry and health."""
    return await intelligence_governance_service.get_governance_overview(db)

@router.get("/conflicts", response_model=List[KnowledgeConflictRead])
async def list_conflicts(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists active and resolved knowledge conflicts."""
    return await intelligence_governance_service.list_conflicts(db)

@router.post("/conflicts/{conflict_id}/resolve", response_model=KnowledgeConflictRead)
async def resolve_conflict(
    conflict_id: str,
    decision: str = Query(..., description="accepted_a, accepted_b, superseded"),
    notes: Optional[str] = Query(None),
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Resolves a knowledge conflict."""
    conf, err = await intelligence_governance_service.resolve_knowledge_conflict(db, conflict_id=conflict_id, user_id=ws_ctx.user_id, decision=decision, notes=notes)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return conf

@router.get("/claims", response_model=List[KnowledgeClaimRead])
async def list_claims(
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Lists structured knowledge claims."""
    return await intelligence_governance_service.list_claims(db)

@router.post("/trusted-context", response_model=TrustedContextResponse)
async def build_trusted_context(
    req: TrustedContextRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Pre-generation TrustedContextBuilder pipeline enforcing authorization, DLP, freshness, and conflict detection."""
    return await intelligence_governance_service.build_trusted_context(db, workspace_id=ws_ctx.workspace_id, req=req, organization_id=ws_ctx.workspace_id)

@router.get("/{object_id}/provenance", response_model=KnowledgeProvenanceRead)
async def get_provenance(
    object_id: str,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Fetches knowledge object provenance and origin tracking."""
    prov = await intelligence_governance_service.get_provenance_by_object_id(db, knowledge_object_id=object_id)
    if not prov:
        raise HTTPException(status_code=404, detail="Knowledge provenance not found")
    return prov

@router.post("/{object_id}/verify")
async def verify_knowledge_object(
    object_id: str,
    req: KnowledgeVerificationRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Human verification decision on a knowledge object or claim."""
    return await intelligence_governance_service.verify_knowledge_object(
        db, knowledge_object_id=object_id, user_id=ws_ctx.user_id, req=req, organization_id=ws_ctx.workspace_id
    )

# AI Output Provenance & Feedback endpoints
@router.post("/ai/outputs/{output_id}/feedback")
async def submit_output_feedback(
    output_id: str,
    req: KnowledgeFeedbackRequest,
    ws_ctx: WorkspaceContext = Depends(get_current_workspace),
    db: AsyncSession = Depends(get_db)
):
    """Submits operator feedback on an AI output."""
    return await intelligence_governance_service.submit_ai_output_feedback(
        db, output_id=output_id, user_id=ws_ctx.user_id, req=req
    )
