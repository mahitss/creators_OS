import pytest
import asyncio
import time
from app.services.transformation_resilience_decision_knowledge_service import TransformationResilienceDecisionKnowledgeService, _EMITTED_KNOWLEDGE_EVENTS

def test_get_decision_knowledge_overview():
    async def _test():
        res = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
        assert res["domainsCount"] >= 1
        assert res["knowledgeObjectsCount"] >= 3
        assert res["validatedObjectsCount"] >= 2
        assert res["contestedObjectsCount"] >= 1
        assert res["conflictsCount"] >= 1
        assert res["packsCount"] >= 1
        assert res["gapsCount"] >= 1
        assert len(res["ignoredLessons"]) >= 1
    asyncio.run(_test())

def test_knowledge_object_provenance_and_versioning():
    async def _test():
        res = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
        kobj = res["knowledgeObjects"][0]
        assert kobj["type"] == "lesson"
        assert kobj["version"] == 1
        assert "source_decision_id" in kobj
        assert kobj["confidence"] == 0.95

        # Update knowledge object -> Versioning test
        updated = await TransformationResilienceDecisionKnowledgeService.update_knowledge_object(None, kobj["id"], {
            "statement": "Secondary Cloud Region latency assumptions must include a +20ms vendor SLA buffer."
        })
        assert updated["version"] == 2
        assert kobj["version"] == 1  # Historical version preserved
    asyncio.run(_test())

def test_knowledge_validation_context_and_applicability():
    async def _test():
        res = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
        val = res["validations"][0]
        ctx = res["contexts"][0]
        app = res["applicabilities"][0]
        assert val["supporting_cases_count"] == 6
        assert val["evidence_quality"] == 0.96
        assert ctx["transformation_type"] == "Cloud Infrastructure Resilience"
        assert app["level"] == "high"
        assert app["applicability_score"] == 0.94
    asyncio.run(_test())

def test_knowledge_conflicts_invalidations_and_reviews():
    async def _test():
        res = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
        conf = res["conflicts"][0]
        inv = res["invalidations"][0]
        rev = res["reviews"][0]
        assert "Lesson A requires strict SLA buffering" in conf["conflicting_claims"]
        assert inv["trigger"] == "new_contradictory_evidence"
        assert rev["status"] == "pending_review"
    asyncio.run(_test())

def test_knowledge_reuse_and_reuse_failure():
    async def _test():
        res = await TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None)
        reuses = res["reuses"]
        assert len(reuses) >= 1
        assert reuses[0]["result"] == "successful"

        # Record unsuccessful reuse -> test outcome update event
        unsucc = await TransformationResilienceDecisionKnowledgeService.record_reuse(None, {
            "knowledge_object_id": "kobj_less_02",
            "decision_id": "dec_failed_wave",
            "context_description": "Legacy mainframe sync context mismatch",
            "result": "unsuccessful",
            "outcome_summary": "Eventual consistency caused sync timeouts."
        })
        assert unsucc["result"] == "unsuccessful"
    asyncio.run(_test())

def test_create_knowledge_pack_and_retrieval():
    async def _test():
        pack = await TransformationResilienceDecisionKnowledgeService.create_knowledge_pack(None, "dec_res_02")
        assert pack["decision_id"] == "dec_res_02"
        assert pack["pack_version"] == "v1.0"
        assert len(pack["lessons_json"]) > 0

        # Retrieval with explanation
        ret = await TransformationResilienceDecisionKnowledgeService.retrieve_decision_knowledge(None, "dec_res_02")
        assert ret["decisionContextId"] == "dec_res_02"
        assert len(ret["retrievedKnowledge"]) > 0
        assert "Matched dependency profile" in ret["retrievedKnowledge"][0]["reasonRetrieved"]
    asyncio.run(_test())

def test_agent_governance_decision_knowledge_restrictions():
    # Agents may NOT validate governance policy, invalidate governance, modify historical knowledge, or approve decisions
    chk_val = TransformationResilienceDecisionKnowledgeService.enforce_agent_governance("agent_01", "validate_governance_policy")
    assert chk_val["allowed"] is False
    assert "strictly blocked" in chk_val["reason"]

    chk_inv = TransformationResilienceDecisionKnowledgeService.enforce_agent_governance("agent_01", "invalidate_historical_knowledge")
    assert chk_inv["allowed"] is False

    chk_read = TransformationResilienceDecisionKnowledgeService.enforce_agent_governance("agent_01", "retrieve_knowledge")
    assert chk_read["allowed"] is True

def test_process_natural_language_knowledge_query_privacy_dlp_tenant():
    async def _test():
        # Valid knowledge query -> succeeds
        valid_q = "What have we learned about this dependency and show relevant precedents?"
        res = await TransformationResilienceDecisionKnowledgeService.process_natural_language_knowledge_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee knowledge profiles or ranking systems) -> blocked
        surveil_q = "Generate employee knowledge profiles and rank personnel performance"
        blocked_surveil = await TransformationResilienceDecisionKnowledgeService.process_natural_language_knowledge_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee knowledge profiles" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show decision knowledge objects. vpr_99999999999"
        blocked_dlp = await TransformationResilienceDecisionKnowledgeService.process_natural_language_knowledge_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceDecisionKnowledgeService.process_natural_language_knowledge_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceDecisionKnowledgeService.get_decision_knowledge_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
