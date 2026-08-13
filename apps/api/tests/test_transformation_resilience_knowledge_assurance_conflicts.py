import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_assurance_conflict_service import (
    TransformationResilienceKnowledgeAssuranceConflictService,
    _EMITTED_CONFLICT_EVENTS
)

def test_get_knowledge_assurance_conflict_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
        assert res["domainsCount"] >= 1
        assert res["conflictCasesCount"] >= 1
        assert res["criticalConflictsCount"] >= 1
        assert res["rootCausesCount"] >= 1
        assert res["optionsCount"] >= 2
        assert res["decisionPacketsCount"] >= 1
        assert res["resolutionPlansCount"] >= 1
        assert res["residualConflictsCount"] >= 1
        assert res["cascadesCount"] >= 1
        assert res["clustersCount"] >= 1
        assert res["systemicConflictsCount"] >= 1
        assert res["patternsCount"] >= 1
    asyncio.run(_test())

def test_conflict_cases_and_root_cause_analysis():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
        ccase = res["cases"][0]
        rcause = res["rootCauses"][0]
        assert ccase["conflict_type"] == "resource"
        assert ccase["severity"] == "high"
        assert rcause["root_cause_category"] == "shared_resource"
        assert rcause["frequency"] == 3
    asyncio.run(_test())

def test_resolution_options_tradeoffs_and_baseline_option():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
        options = res["options"]
        base_opt = [o for o in options if o["option_type"] == "continue_without_change"][0]
        seq_opt = [o for o in options if o["option_type"] == "sequence"][0]
        trade = res["tradeoffs"][0]
        assert base_opt["risk_score"] == 0.25
        assert base_opt["coverage_score"] == 0.84
        assert seq_opt["risk_score"] == 0.08
        assert seq_opt["coverage_score"] == 0.92
        assert trade["dimension_a"] == "coverage"
        assert trade["dimension_b"] == "speed"
    asyncio.run(_test())

def test_decision_packet_creation_and_recommendation_label():
    async def _test():
        dpkt = await TransformationResilienceKnowledgeAssuranceConflictService.prepare_decision_packet(None, "ccase_01")
        assert dpkt["conflict_case_id"] == "ccase_01"
        assert dpkt["required_authority"] == "governance_authority"
        assert dpkt["residual_risk"] == 0.08
        overview = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
        rec = overview["recommendations"][0]
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT DECISION"
        assert rec["recommended_option"] == "sequence"
    asyncio.run(_test())

def test_submit_decision_and_resolve_conflict_action_gateway():
    async def _test():
        sub = await TransformationResilienceKnowledgeAssuranceConflictService.submit_decision(None, "ccase_01", {"selected_option": "sequence"})
        assert sub["status"] == "approved"
        assert sub["decision_lifecycle_routed"] is True
        assert sub["approval_routed"] is True

        res = await TransformationResilienceKnowledgeAssuranceConflictService.resolve_conflict(None, "ccase_01", {"selected_option": "sequence"})
        assert res["status"] == "resolving"
        assert res["action_gateway_routed"] is True
    asyncio.run(_test())

def test_residual_conflicts_cascades_systemic_and_patterns():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None)
        rconf = res["residualConflicts"][0]
        casc = res["cascades"][0]
        sys = res["systemic"][0]
        patt = res["patterns"][0]
        assert "legacy SSO" in rconf["remaining_conflict"]
        assert casc["source_conflict_id"] == "ccase_01"
        assert sys["severity"] == "critical"
        assert patt["reusability_score"] == 0.92
    asyncio.run(_test())

def test_agent_governance_conflict_restrictions():
    # Agents may detect conflicts, classify conflicts, analyze impact, generate options, run simulations, prepare decision packets, monitor resolution, and detect cascades
    # Agents may NOT select material resolution, approve conflicts, accept risk, allocate resources, change budgets, or override governance
    chk_select = TransformationResilienceKnowledgeAssuranceConflictService.enforce_agent_governance("agent_01", "select_material_resolution")
    assert chk_select["allowed"] is False
    assert "strictly blocked" in chk_select["reason"]

    chk_approve = TransformationResilienceKnowledgeAssuranceConflictService.enforce_agent_governance("agent_01", "approve_conflict")
    assert chk_approve["allowed"] is False

    chk_risk = TransformationResilienceKnowledgeAssuranceConflictService.enforce_agent_governance("agent_01", "accept_risk")
    assert chk_risk["allowed"] is False

    chk_analyze = TransformationResilienceKnowledgeAssuranceConflictService.enforce_agent_governance("agent_01", "prepare_decision_packets")
    assert chk_analyze["allowed"] is True

def test_process_natural_language_assurance_conflict_query_privacy_dlp_tenant():
    async def _test():
        # Valid query -> succeeds with baseline option and governance notice
        valid_q = "Show critical assurance conflicts and root causes."
        res = await TransformationResilienceKnowledgeAssuranceConflictService.process_natural_language_assurance_conflict_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5
        assert "Continue Without Change" in res["results"][0]["baseline_option"]
        assert "ANALYTICAL RECOMMENDATION — NOT DECISION" in res["results"][0]["recommendation_notice"]

        # Anti-Surveillance / Privacy safeguard breach (employee performance rankings or worker utilization score) -> blocked
        surveil_q = "Calculate employee performance ranking and rank worker utilization score"
        blocked_surveil = await TransformationResilienceKnowledgeAssuranceConflictService.process_natural_language_assurance_conflict_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "prohibits employee performance rankings" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked
        dlp_q = "Show conflict cases details. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeAssuranceConflictService.process_natural_language_assurance_conflict_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeAssuranceConflictService.process_natural_language_assurance_conflict_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeAssuranceConflictService.get_knowledge_assurance_conflict_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
