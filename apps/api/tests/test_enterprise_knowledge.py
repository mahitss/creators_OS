import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import knowledge_service
from app.schemas.knowledge import KnowledgeQueryRequest

client = TestClient(app)

def test_ingestion_and_chunking():
    async def _test():
        src_id = "src_test_01"
        ws_id = "ws_test_01"
        org_id = "org_test_01"

        # 1. Ingest new document
        doc, created = await knowledge_service.ingest_document(
            None, src_id, "ext_doc_01", ws_id, org_id, "Architecture Guide",
            "This document explains the Enterprise Knowledge Fabric chunking and indexing strategy.",
            classification="internal"
        )
        assert created is True
        assert doc["title"] == "Architecture Guide"

        # 2. Ingest duplicate document -> Incremental change detection skips re-indexing
        doc_dup, created_dup = await knowledge_service.ingest_document(
            None, src_id, "ext_doc_01", ws_id, org_id, "Architecture Guide",
            "This document explains the Enterprise Knowledge Fabric chunking and indexing strategy.",
            classification="internal"
        )
        assert created_dup is False

    asyncio.run(_test())

def test_secure_retrieval_and_authorization_gate():
    async def _test():
        ws_id = "ws_search_test"
        org_id = "org_search_test"

        # 1. Ingest restricted document
        await knowledge_service.ingest_document(
            None, "src_sec_01", "ext_sec_01", ws_id, org_id, "Secret Roadmap",
            "Restricted document containing secret key vpr_live_secret_key_891429814 for executive eyes only.",
            classification="restricted"
        )

        # 2. Query as non-admin with low classification ceiling -> Authorization Gate filters out restricted doc
        req_unauth = KnowledgeQueryRequest(
            query="secret key roadmap",
            workspaceId=ws_id,
            organizationId=org_id,
            classificationCeiling="internal"
        )
        results_unauth = await knowledge_service.search_knowledge(None, req_unauth, user_id="usr_member", user_role="member")
        # Should be empty because user lacks restricted access
        assert len(results_unauth) == 0

        # 3. Query as admin with restricted ceiling -> Authorized, but secret key is redacted by DLP gate
        req_auth = KnowledgeQueryRequest(
            query="secret key roadmap",
            workspaceId=ws_id,
            organizationId=org_id,
            classificationCeiling="restricted"
        )
        results_auth = await knowledge_service.search_knowledge(None, req_auth, user_id="usr_admin", user_role="admin")
        assert len(results_auth) >= 1
        assert "vpr_live_secret_key_891429814" not in results_auth[0]["snippet"]
        assert "[REDACTED_SECRET]" in results_auth[0]["snippet"]

    asyncio.run(_test())

def test_grounded_ai_ask_and_citations():
    async def _test():
        ws_id = "ws_ask_test"
        org_id = "org_ask_test"

        await knowledge_service.ingest_document(
            None, "src_ask_01", "ext_ask_01", ws_id, org_id, "Q3 Specs",
            "Q3 Product Launch specifies permission-aware retrieval and grounded AI citations.",
            classification="internal"
        )

        req = KnowledgeQueryRequest(
            query="What does Q3 specify?",
            workspaceId=ws_id,
            organizationId=org_id,
            classificationCeiling="internal"
        )

        ask_res = await knowledge_service.ask_knowledge(None, req, user_id="usr_admin", user_role="admin")
        assert ask_res.evidence_status == "strong_evidence"
        assert len(ask_res.citations) >= 1
        assert ask_res.citations[0].title == "Q3 Specs"
        assert "https://vapor.app/docs/" in ask_res.citations[0].source_url

    asyncio.run(_test())

def test_knowledge_fabric_rest_api():
    # 1. Overview API
    overview_res = client.get("/api/v1/knowledge?workspaceId=ws_default_creator")
    assert overview_res.status_code == 200
    assert overview_res.json()["sync_health"] == "healthy"

    # 2. Collections API
    col_res = client.get("/api/v1/knowledge/collections?workspaceId=ws_default_creator")
    assert col_res.status_code == 200
    assert len(col_res.json()) >= 2

    # 3. Sources API
    src_res = client.get("/api/v1/knowledge/sources?workspaceId=ws_default_creator")
    assert src_res.status_code == 200

    # 4. Documents API
    doc_res = client.get("/api/v1/knowledge/documents?workspaceId=ws_default_creator")
    assert doc_res.status_code == 200

    # 5. Search API
    search_res = client.post("/api/v1/knowledge/search", json={
        "query": "Q3 Product Launch",
        "workspaceId": "ws_default_creator",
        "organizationId": "org_default_creator"
    })
    assert search_res.status_code == 200

    # 6. Ask API
    ask_res = client.post("/api/v1/knowledge/ask", json={
        "query": "What are the Q3 Product Specs?",
        "workspaceId": "ws_default_creator",
        "organizationId": "org_default_creator"
    })
    assert ask_res.status_code == 200
    assert ask_res.json()["evidence_status"] in ["strong_evidence", "insufficient_evidence"]

    # 7. Graph API
    graph_res = client.get("/api/v1/knowledge/graph?workspaceId=ws_default_creator")
    assert graph_res.status_code == 200
    assert "entities" in graph_res.json()
