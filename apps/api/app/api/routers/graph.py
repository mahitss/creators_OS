from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.semantic_graph import (
    SemanticEntityRead,
    SemanticRelationshipCreate,
    SemanticRelationshipRead,
    ContextPackCreate,
    ContextPackRead,
    GraphImpactResponse,
    GraphHealthRead
)
from app.services import semantic_graph_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/graph", tags=["Enterprise Semantic Graph & Unified Business Context"])

@router.get("/entities/{entity_type}/{entity_id}", response_model=SemanticEntityRead)
async def get_entity(
    entity_type: str,
    entity_id: str,
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Fetches or resolves a semantic entity by type and domain ID."""
    ent = await semantic_graph_service.resolve_or_create_entity(
        db, org_id=org_id, workspace_id=workspace_id, entity_type=entity_type, entity_id=entity_id, display_name=f"{entity_type.capitalize()} {entity_id}"
    )
    return ent

@router.get("/entities/{entity_id}/neighbors")
async def get_neighbors(
    entity_id: str,
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Returns authorization-filtered 1-hop graph neighbors."""
    return await semantic_graph_service.query_neighbors(db, entity_id=entity_id, org_id=org_id, workspace_id=workspace_id)

@router.get("/path")
async def find_graph_path(
    from_entity_id: str = Query(..., alias="fromEntityId"),
    to_entity_id: str = Query(..., alias="toEntityId"),
    max_depth: int = Query(4, alias="maxDepth"),
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Finds bounded traversal path between two entities."""
    return await semantic_graph_service.find_path(db, from_entity_id=from_entity_id, to_entity_id=to_entity_id, max_depth=max_depth, org_id=org_id)

@router.get("/impact/{entity_id}", response_model=GraphImpactResponse)
async def get_impact_analysis(
    entity_id: str,
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Calculates blast radius and impacted downstream workflows, agents, and integrations."""
    return await semantic_graph_service.calculate_impact(db, entity_id=entity_id, org_id=org_id)

@router.get("/relationships", response_model=List[SemanticRelationshipRead])
async def list_relationships(
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Lists semantic relationships."""
    return await semantic_graph_service.list_ai_proposals(db, org_id=org_id)

@router.post("/relationships", response_model=SemanticRelationshipRead)
async def create_relationship(
    req: SemanticRelationshipCreate,
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Creates a semantic relationship."""
    rel, err = await semantic_graph_service.create_relationship(db, org_id=org_id, workspace_id=workspace_id, req=req)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return rel

@router.post("/relationships/{rel_id}/approve", response_model=SemanticRelationshipRead)
async def approve_ai_proposal(
    rel_id: str,
    x_user_id: str = Header("usr_executive_01", alias="X-User-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Human review approval promoting AI relationship proposal to verified."""
    rel, err = await semantic_graph_service.approve_ai_relationship_proposal(db, rel_id=rel_id, approver_id=x_user_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return rel

@router.post("/context-pack", response_model=ContextPackRead)
async def create_context_pack(
    req: ContextPackCreate,
    org_id: str = Header("org_default_creator", alias="X-Organization-Id"),
    workspace_id: str = Header("ws_default_01", alias="X-Workspace-Id"),
    db: AsyncSession = Depends(get_db)
):
    """Generates an expiring, authorization-filtered subgraph ContextPack."""
    return await semantic_graph_service.build_context_pack(db, org_id=org_id, workspace_id=workspace_id, req=req)

@router.get("/health", response_model=GraphHealthRead)
async def get_health(
    db: AsyncSession = Depends(get_db)
):
    """Returns graph health quality indicators."""
    return await semantic_graph_service.get_graph_health(db)
