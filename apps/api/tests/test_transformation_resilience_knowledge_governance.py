import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_governance_service import TransformationResilienceKnowledgeGovernanceService, _EMITTED_GOVERNANCE_EVENTS

def test_get_knowledge_governance_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        assert res["domainsCount"] >= 1
        assert res["healthsCount"] >= 1
        assert res["trustedCount"] >= 1
        assert res["claimsCount"] >= 1
        assert res["conflictsCount"] >= 1
        assert res["contextDriftsCount"] >= 1
        assert res["reviewsCount"] >= 1
        assert res["revalidationsCount"] >= 1
        assert res["gapsCount"] >= 1
    asyncio.run(_test())

def test_knowledge_health_freshness_and_source_independence():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        h = res["healths"][0]
        e = res["evidence"][0]
        assert h["freshness_score"] == 0.96
        assert h["provenance_score"] == 0.98
        assert e["independence_type"] == "independent"
        assert e["reliability"] == 0.98
    asyncio.run(_test())

def test_claims_supports_and_claim_conflicts():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        c = res["claims"][0]
        cconf = res["conflicts"][0]
        assert c["claim_type"] == "validated"
        assert c["confidence"] == 0.95
        assert cconf["severity"] == "medium"
    asyncio.run(_test())

def test_context_drift_reuse_assurance_and_influence():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        cdrift = res["drifts"][0]
        rass = res["reuses"][0]
        inf = res["influences"][0]
        assert cdrift["status"] == "changing"
        assert rass["successful_reuse_count"] == 5
        assert inf["influence_level"] == "high"
    asyncio.run(_test())

def test_knowledge_risk_reviews_and_revalidation_narrowing():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        risk = res["risks"][0]
        rev = res["reviews"][0]
        assert risk["risk_type"] == "high_influence_low_quality"
        assert rev["priority"] == "high"

        # Execute revalidation with applicability narrowing
        reval = await TransformationResilienceKnowledgeGovernanceService.revalidate_knowledge(None, rev["id"], {
            "review_question": "Does SLA buffer apply to 10Gbps interconnects?",
            "result": "narrowed",
            "new_context": "Applicable specifically to multi-region OAuth token cache gateways."
        })
        assert reval["result"] == "narrowed"
        assert "Applicable specifically" in reval["new_context"]
    asyncio.run(_test())

def test_evidence_gaps_governance_states_and_lineage():
    async def _test():
        res = await TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None)
        gap = res["gaps"][0]
        st = res["states"][0]
        lin = res["lineages"][0]
        assert gap["priority"] == "high"
        assert st["state"] == "trusted"
        assert lin["source_decision_id"] == "dec_res_01"
        assert lin["outcome_id"] == "obs_out_01"
    asyncio.run(_test())

def test_agent_governance_knowledge_assurance_restrictions():
    # Agents may NOT approve knowledge state changes, invalidate institutional knowledge, change governance, or modify historical evidence
    chk_state = TransformationResilienceKnowledgeGovernanceService.enforce_agent_governance("agent_01", "approve_knowledge_state_change")
    assert chk_state["allowed"] is False
    assert "strictly blocked" in chk_state["reason"]

    chk_inv = TransformationResilienceKnowledgeGovernanceService.enforce_agent_governance("agent_01", "invalidate_institutional_knowledge")
    assert chk_inv["allowed"] is False

    chk_read = TransformationResilienceKnowledgeGovernanceService.enforce_agent_governance("agent_01", "monitor_quality")
    assert chk_read["allowed"] is True

def test_process_natural_language_governance_query_privacy_dlp_tenant():
    async def _test():
        # Valid governance query -> succeeds
        valid_q = "Which resilience knowledge is trustworthy and why is this knowledge under review?"
        res = await TransformationResilienceKnowledgeGovernanceService.process_natural_language_governance_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee knowledge scores or behavioral profiles) -> blocked
        surveil_q = "Calculate employee knowledge score and generate individual behavioral profile"
        blocked_surveil = await TransformationResilienceKnowledgeGovernanceService.process_natural_language_governance_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee knowledge scores" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show knowledge health data. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeGovernanceService.process_natural_language_governance_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeGovernanceService.process_natural_language_governance_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeGovernanceService.get_knowledge_governance_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
