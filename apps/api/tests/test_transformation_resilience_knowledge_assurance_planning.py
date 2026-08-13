import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_assurance_planning_service import TransformationResilienceKnowledgeAssurancePlanningService, _EMITTED_PLANNING_EVENTS

def test_get_knowledge_assurance_planning_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        assert res["domainsCount"] >= 1
        assert res["portfoliosCount"] >= 1
        assert res["systemicRisksCount"] >= 1
        assert res["rootCausesCount"] >= 1
        assert res["leversCount"] >= 1
        assert res["optionsCount"] >= 1
        assert res["plansCount"] >= 1
        assert res["approvedPlansCount"] >= 1
    asyncio.run(_test())

def test_portfolio_exposure_systemic_risks_and_root_causes():
    async def _test():
        res = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        port = res["portfolios"][0]
        sysr = res["systemicRisks"][0]
        rcg = res["rootCauses"][0]
        assert port["exposure_score"] == 0.88
        assert sysr["breadth"] == 5
        assert sysr["dependency_centrality"] == 0.92
        assert sysr["decision_influence"] == 0.95
        assert rcg["root_cause_type"] == "stale_source"
    asyncio.run(_test())

def test_remediation_levers_capacity_and_capacity_gaps():
    async def _test():
        res = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        lever = res["levers"][0]
        cap = res["capacities"][0]
        cons = res["constraints"][0]
        assert lever["lever_type"] == "shared_evidence_source"
        assert cap["specialist_capacity"] == 0.75
        assert cons["constraint_type"] == "limited_experts"
        assert "Specialist Capacity Deficit" in res["capacityGap"]
    asyncio.run(_test())

def test_assurance_options_sequences_and_scenarios():
    async def _test():
        res = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        opt = res["options"][0]
        seq = res["sequences"][0]
        scen = res["scenarios"][0]
        assert opt["option_type"] == "parallel"
        assert opt["time_est"] == "14 days"
        assert len(seq["sequence_order_json"]) > 0
        assert scen["coverage"] == 0.95
    asyncio.run(_test())

def test_plan_creation_analytical_recommendation_and_residual_risk():
    async def _test():
        new_plan = await TransformationResilienceKnowledgeAssurancePlanningService.create_assurance_plan(None, {
            "objective": "Execute multi-region cloud SLA assurance plan",
            "scope": "enterprise"
        })
        assert new_plan["status"] == "draft"
        assert new_plan["risk_coverage"] == 0.92
        assert new_plan["residual_risk"] == 0.08

        overview = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        rec = overview["recommendations"][0]
        resr = overview["residuals"][0]
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT APPROVAL"
        assert resr["severity"] == "low"
    asyncio.run(_test())

def test_plan_submit_for_approval_and_execution():
    async def _test():
        res = await TransformationResilienceKnowledgeAssurancePlanningService.submit_assurance_plan_for_approval(None, "aplan_01")
        assert res["status"] == "pending_approval"
        assert res["approval_routed"] is True
    asyncio.run(_test())

def test_verifications_effectiveness_and_failures():
    async def _test():
        overview = await TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None)
        pverif = overview["verifications"][0]
        peff = overview["effectivenesses"][0]
        pfail = overview["failures"][0]
        assert pverif["planned_coverage"] == 0.92
        assert peff["risk_reduction"] == 0.85
        assert pfail["failure_type"] == "capacity_failure"
    asyncio.run(_test())

def test_agent_governance_assurance_planning_restrictions():
    # Agents may NOT approve plans, accept risk, allocate organizational budget, change governance, or execute material changes
    chk_plan = TransformationResilienceKnowledgeAssurancePlanningService.enforce_agent_governance("agent_01", "approve_plan")
    assert chk_plan["allowed"] is False
    assert "strictly blocked" in chk_plan["reason"]

    chk_budget = TransformationResilienceKnowledgeAssurancePlanningService.enforce_agent_governance("agent_01", "allocate_budget")
    assert chk_budget["allowed"] is False

    chk_draft = TransformationResilienceKnowledgeAssurancePlanningService.enforce_agent_governance("agent_01", "draft_options")
    assert chk_draft["allowed"] is True

def test_process_natural_language_assurance_planning_query_privacy_dlp_tenant():
    async def _test():
        # Valid planning query -> succeeds
        valid_q = "Where is knowledge assurance weakest and what assurance plan is recommended?"
        res = await TransformationResilienceKnowledgeAssurancePlanningService.process_natural_language_assurance_planning_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5

        # Anti-Surveillance / Privacy safeguard breach (employee productivity scoring or employee rankings) -> blocked
        surveil_q = "Calculate employee productivity score and rank personnel by remediation performance"
        blocked_surveil = await TransformationResilienceKnowledgeAssurancePlanningService.process_natural_language_assurance_planning_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits employee productivity scoring" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show assurance portfolio plans. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeAssurancePlanningService.process_natural_language_assurance_planning_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeAssurancePlanningService.process_natural_language_assurance_planning_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeAssurancePlanningService.get_knowledge_assurance_planning_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
