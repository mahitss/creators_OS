import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import learning_fabric_service
from app.schemas.learning_fabric import AgentMemoryCreate, MemoryCorrectRequest, MemoryConflictResolveRequest

def test_create_memory_with_secret_rejection():
    async def _test():
        # Valid Memory
        req_valid = AgentMemoryCreate(
            ownerId="ag_test_01",
            title="Project Gamma Stack",
            content="Project Gamma uses PostgreSQL and FastAPI."
        )
        mem, prov = await learning_fabric_service.create_memory(
            None, workspace_id="ws_test_01", req=req_valid
        )
        assert mem["status"] == "active"
        assert prov["source_type"] == "user_input"

        # Memory containing secret key (Must fail)
        req_secret = AgentMemoryCreate(
            ownerId="ag_test_01",
            title="Leaked Key",
            content="API key sk-12345678901234567890123456789012"
        )
        with pytest.raises(ValueError, match="secret"):
            await learning_fabric_service.create_memory(
                None, workspace_id="ws_test_01", req=req_secret
            )
    asyncio.run(_test())

def test_search_and_rank_memories():
    async def _test():
        results = await learning_fabric_service.search_memories(
            None, workspace_id="ws_default_01", query="Deployment"
        )
        assert len(results) >= 1
        assert "Service X" in results[0]["title"]
    asyncio.run(_test())

def test_human_correction_and_versioning():
    async def _test():
        req_correct = MemoryCorrectRequest(
            correctedTitle="Service X Updated Region",
            correctedContent="Service X region updated to us-west-2.",
            reason="Architecture shift"
        )
        updated = await learning_fabric_service.correct_memory(
            None, memory_id="mem_gov_001", req=req_correct, user_id="usr_lead_01"
        )
        assert updated["content"] == "Service X region updated to us-west-2."

        history = await learning_fabric_service.get_history(None, memory_id="mem_gov_001")
        assert len(history) >= 2
        assert history[-1]["source"] == "human_correction"
    asyncio.run(_test())

def test_invalidate_memory():
    async def _test():
        deprecated = await learning_fabric_service.invalidate_memory(None, memory_id="mem_gov_002")
        assert deprecated["status"] == "deprecated"
    asyncio.run(_test())

def test_conflict_resolution():
    async def _test():
        req_res = MemoryConflictResolveRequest(
            resolution="resolved_a",
            notes="Authoritative record A confirmed."
        )
        conf = await learning_fabric_service.resolve_conflict(
            None, workspace_id="ws_default_01", conflict_id="conf_001", req=req_res, user_id="usr_op_01"
        )
        assert conf["status"] == "resolved_a"
        assert conf["resolved_by"] == "usr_op_01"
    asyncio.run(_test())
