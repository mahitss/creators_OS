import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import skill_fabric_service
from app.schemas.skill_fabric import AgentSkillCreate, SkillInvokeRequest

def test_create_and_invoke_skill():
    async def _test():
        req = AgentSkillCreate(
            name="Data Summarization Skill",
            description="Summarizes complex data payloads",
            skillType="analysis",
            sideEffectContract="read-only",
            requiredCapabilities=["reasoning"]
        )
        skill, version = await skill_fabric_service.create_skill(
            None, workspace_id="ws_test_01", req=req
        )
        assert skill["status"] == "active"
        assert version["side_effect_contract"] == "read-only"

        inv_req = SkillInvokeRequest(inputPayload={"data": "test_payload"})
        resp = await skill_fabric_service.invoke_skill(
            None, workspace_id="ws_test_01", skill_id=skill["id"], req=inv_req
        )
        assert resp["status"] == "completed"
        assert resp["skill_id"] == skill["id"]
        assert resp["execution_id"] is not None
    asyncio.run(_test())

def test_circular_dependency_rejection():
    async def _test():
        inv_req = SkillInvokeRequest(
            inputPayload={},
            callingSkillIds=["sk_doc_analysis_01"] # Circular call
        )
        with pytest.raises(ValueError, match="Circular skill dependency"):
            await skill_fabric_service.invoke_skill(
                None, workspace_id="ws_default_01", skill_id="sk_doc_analysis_01", req=inv_req
            )
    asyncio.run(_test())

def test_max_recursion_depth_rejection():
    async def _test():
        inv_req = SkillInvokeRequest(
            inputPayload={},
            callingSkillIds=["sk_a", "sk_b", "sk_c"],
            maxDepth=3
        )
        with pytest.raises(ValueError, match="Max skill recursion depth"):
            await skill_fabric_service.invoke_skill(
                None, workspace_id="ws_default_01", skill_id="sk_doc_analysis_01", req=inv_req
            )
    asyncio.run(_test())

def test_skill_candidates_list():
    async def _test():
        candidates = await skill_fabric_service.list_candidates(None, workspace_id="ws_default_01")
        assert len(candidates) >= 1
        assert candidates[0]["status"] == "pending"
    asyncio.run(_test())

def test_skill_health_and_versions():
    async def _test():
        versions = await skill_fabric_service.get_versions(None, skill_id="sk_doc_analysis_01")
        assert len(versions) >= 1
        assert versions[0]["side_effect_contract"] == "read-only"

        health = await skill_fabric_service.get_health(None, version_id="skv_doc_analysis_01_v1")
        assert health is not None
        assert health["quality_score"] == 0.96
    asyncio.run(_test())
