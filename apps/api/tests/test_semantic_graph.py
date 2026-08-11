import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import semantic_graph_service
from app.schemas.semantic_graph import SemanticRelationshipCreate, ContextPackCreate

def test_entity_resolution_and_deduplication():
    async def _test():
        # First creation
        e1 = await semantic_graph_service.resolve_or_create_entity(
            None, org_id="org_default_creator", workspace_id="ws_default_01",
            entity_type="document", entity_id="doc_gdrive_99", display_name="Shared Specs",
            provider="google_drive", external_id="gdrive_doc_99", resource_type="document"
        )
        assert e1["id"] is not None

        # Duplicate resolution attempt with same provider & external_id returns SAME entity
        e2 = await semantic_graph_service.resolve_or_create_entity(
            None, org_id="org_default_creator", workspace_id="ws_default_01",
            entity_type="document", entity_id="doc_gdrive_99", display_name="Shared Specs Duplicate",
            provider="google_drive", external_id="gdrive_doc_99", resource_type="document"
        )
        assert e1["id"] == e2["id"]
    asyncio.run(_test())

def test_native_vs_ai_suggested_relationship_status():
    async def _test():
        # Native relationship -> active status
        req_native = SemanticRelationshipCreate(
            fromEntityId="ent_proj_01",
            relationshipType="contains",
            toEntityId="ent_doc_01",
            source="native"
        )
        rel_n, err1 = await semantic_graph_service.create_relationship(None, org_id="org_default_creator", workspace_id="ws_default_01", req=req_native)
        assert err1 is None
        assert rel_n["status"] == "active"

        # AI-suggested relationship -> proposed status
        req_ai = SemanticRelationshipCreate(
            fromEntityId="ent_doc_01",
            relationshipType="related_to",
            toEntityId="ent_wf_01",
            source="ai_suggested",
            confidence="medium"
        )
        rel_ai, err2 = await semantic_graph_service.create_relationship(None, org_id="org_default_creator", workspace_id="ws_default_01", req=req_ai)
        assert err2 is None
        assert rel_ai["status"] == "proposed"
    asyncio.run(_test())

def test_human_approval_promotes_ai_proposal():
    async def _test():
        req_ai = SemanticRelationshipCreate(
            fromEntityId="ent_miss_01",
            relationshipType="references",
            toEntityId="ent_doc_01",
            source="ai_suggested"
        )
        rel_ai, _ = await semantic_graph_service.create_relationship(None, org_id="org_default_creator", workspace_id="ws_default_01", req=req_ai)
        assert rel_ai["status"] == "proposed"

        # Approve proposal
        approved, err = await semantic_graph_service.approve_ai_relationship_proposal(None, rel_ai["id"], approver_id="usr_executive_01")
        assert err is None
        assert approved["status"] == "verified"
    asyncio.run(_test())

def test_authorization_aware_neighbor_query():
    async def _test():
        res = await semantic_graph_service.query_neighbors(None, entity_id="ent_wf_01", org_id="org_default_creator")
        assert res["entity"] is not None
        assert len(res["neighbors"]) >= 1
    asyncio.run(_test())

def test_path_finder_traversal():
    async def _test():
        path = await semantic_graph_service.find_path(None, from_entity_id="ent_usr_01", to_entity_id="ent_wf_01", max_depth=5)
        assert len(path) >= 2
        assert path[0]["id"] == "ent_usr_01"
    asyncio.run(_test())

def test_impact_analysis_blast_radius():
    async def _test():
        impact = await semantic_graph_service.calculate_impact(None, entity_id="ent_miss_01")
        assert impact["rootEntityId"] == "ent_miss_01"
        assert impact["totalImpactedCount"] >= 1
    asyncio.run(_test())

def test_context_pack_generation():
    async def _test():
        req = ContextPackCreate(scope="agent_mesh_task", rootEntityId="ent_wf_01", maxDepth=2, maxNodes=20)
        pack = await semantic_graph_service.build_context_pack(None, org_id="org_default_creator", workspace_id="ws_default_01", req=req)
        assert pack["id"] is not None
        assert pack["expires_at"] is not None
        assert len(pack["entities"]) >= 1
    asyncio.run(_test())

def test_graph_health_metrics():
    async def _test():
        health = await semantic_graph_service.get_graph_health(None)
        assert health["entity_count"] >= 10
        assert health["relationship_count"] >= 8
        assert health["sync_lag_seconds"] >= 0.0
    asyncio.run(_test())
