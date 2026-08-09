import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services.knowledge_service import (
    propose_memory_candidate,
    approve_memory_candidate,
    detect_memory_conflicts,
    resolve_memory_conflict,
    invalidate_source_knowledge,
    get_memory_provenance
)
from app.services.memory_service import create_memory, list_memories
from app.services.context_engine import ContextRequest, ContextPurpose, SourceType, ContextEngine

client = TestClient(app)
HEADERS = {"X-User-Id": "usr_alex", "X-Workspace-Id": "ws_mem2_test"}

def test_memory_candidate_proposal_and_human_approval():
    async def _test():
        # 1. Propose Memory Candidate via Knowledge Service
        cand = await propose_memory_candidate(
            None, workspace_id="ws_mem2_test", owner_id="usr_alex",
            statement="Project uses PostgreSQL 16 database.", type_name="requirement",
            scope="workspace", source_references=[{"type": "drive", "title": "Architecture Spec"}],
            reason="Extracted from approved design doc"
        )
        assert cand["status"] == "candidate"
        cand_id = cand["id"]

        # 2. Verify candidate is NOT active yet
        mems, _ = await list_memories(None, workspace_id="ws_mem2_test", is_archived=False)
        active_mems = [m for m in mems if m.get("status") == "active" and m["id"] == cand_id]
        assert len(active_mems) == 0

        # 3. User Approves Candidate
        approved = await approve_memory_candidate(None, workspace_id="ws_mem2_test", candidate_id=cand_id, user_id="usr_alex")
        assert approved["status"] == "active"
        assert approved["approved_by"] == "usr_alex"

    asyncio.run(_test())

def test_conflict_detection_and_resolution():
    async def _test():
        from app.schemas.memory import MemoryCreate
        # 1. Create Active Memory A: Deadline Friday
        mem_a = await create_memory(None, workspace_id="ws_mem2_test", payload=MemoryCreate(
            type="fact",
            title="Project deadline is Friday",
            content="Project deadline is Friday",
            importance="high",
            source_type="manual"
        ))
        mem_a["statement"] = "Project deadline is Friday"
        mem_a["status"] = "active"

        # 2. Propose Memory Candidate B: Deadline Monday (Conflict)
        cand_b = await propose_memory_candidate(
            None, workspace_id="ws_mem2_test", owner_id="usr_alex",
            statement="Project deadline is Monday", type_name="requirement", scope="workspace"
        )

        # 3. Detect Conflicts
        conflicts = await detect_memory_conflicts(None, workspace_id="ws_mem2_test", new_mem=cand_b)
        assert len(conflicts) > 0
        cnf_id = conflicts[0]["id"]

        # 4. Resolve Conflict with keep_b
        res = await resolve_memory_conflict(None, workspace_id="ws_mem2_test", conflict_id=cnf_id, choice="keep_b", user_id="usr_alex")
        assert res["status"] == "resolved"
        assert mem_a["status"] == "superseded"

    asyncio.run(_test())

def test_staleness_propagation_on_source_change():
    async def _test():
        from app.services.knowledge_service import ingest_knowledge_object
        # 1. Ingest Knowledge Object
        k_obj = await ingest_knowledge_object(
            None, workspace_id="ws_mem2_test", scope="workspace", owner_id="usr_alex",
            source_type="document", source_id="doc_specs_01", title="API Specs", content="v1 endpoints"
        )
        assert k_obj["status"] == "fresh"

        # 2. Invalidate Source Knowledge when source hash changes
        stale_objs = await invalidate_source_knowledge(None, workspace_id="ws_mem2_test", source_id="doc_specs_01", new_content_hash="hash_v2_updated")
        assert len(stale_objs) == 1
        assert stale_objs[0]["status"] == "stale"

    asyncio.run(_test())

def test_memory_v2_rest_endpoints():
    # 1. Propose Candidate via REST
    p_res = client.post("/api/v1/memories/candidates", json={
        "statement": "Team uses TypeScript for web components",
        "type_name": "preference",
        "scope": "workspace"
    }, headers=HEADERS)
    assert p_res.status_code == 201
    cand_id = p_res.json()["id"]

    # 2. Approve Candidate via REST
    app_res = client.post(f"/api/v1/memories/candidates/{cand_id}/approve", headers=HEADERS)
    assert app_res.status_code == 200
    assert app_res.json()["status"] == "active"

    # 3. Get Provenance via REST
    prov_res = client.get(f"/api/v1/memories/{cand_id}/provenance", headers=HEADERS)
    assert prov_res.status_code == 200
    assert prov_res.json()["memory_id"] == cand_id
