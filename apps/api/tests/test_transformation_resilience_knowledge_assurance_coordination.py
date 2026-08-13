import pytest
import asyncio
import time
from app.services.transformation_resilience_knowledge_assurance_coordination_service import (
    TransformationResilienceKnowledgeAssuranceCoordinationService,
    _EMITTED_COORDINATION_EVENTS
)

def test_get_knowledge_assurance_coordination_overview():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        assert res["domainsCount"] >= 1
        assert res["activePlansCount"] == 3
        assert res["relationshipsCount"] >= 1
        assert res["resourcesCount"] >= 1
        assert res["contentionsCount"] >= 1
        assert res["evidenceContentionsCount"] >= 1
        assert res["reviewContentionsCount"] >= 1
        assert res["simulationContentionsCount"] >= 1
        assert res["deadlineCollisionsCount"] >= 1
        assert res["bottlenecksCount"] >= 1
        assert res["coordinationOptionsCount"] >= 1
        assert res["coordinationPlansCount"] >= 1
        assert res["cascadesCount"] >= 1
    asyncio.run(_test())

def test_active_plans_and_plan_relationships():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        active_set = res["activeSets"][0]
        rel = res["relationships"][0]
        assert len(active_set["active_plan_ids_json"]) == 3
        assert rel["source_plan_id"] == "aplan_01"
        assert rel["target_plan_id"] == "aplan_hr_cloud_02"
        assert rel["relationship_type"] == "blocks"
    asyncio.run(_test())

def test_resource_demands_availabilities_and_contentions():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        rcont = res["contentions"][0]
        econt = res["evidenceContentions"][0]
        rvcont = res["reviewContentions"][0]
        scont = res["simulationContentions"][0]
        dcoll = res["deadlineCollisions"][0]
        assert rcont["severity"] == "high"
        assert econt["evidence_source_id"] == "ev_src_interconnect_01"
        assert rvcont["review_domain"] == "cloud_security"
        assert rvcont["review_capacity_deficit"] == 0.30
        assert scont["compute_deficit_pct"] == 20.0
        assert "shared_deadline" in dcoll
    asyncio.run(_test())

def test_portfolio_bottlenecks_and_options():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        bot = res["bottlenecks"][0]
        opt = res["options"][0]
        assert bot["bottleneck_type"] == "simulation_capacity"
        assert bot["severity"] == "critical"
        assert opt["option_type"] == "sequence"
        assert opt["coverage"] == 0.92
    asyncio.run(_test())

def test_create_coordination_plan_and_analytical_recommendation_label():
    async def _test():
        plan = await TransformationResilienceKnowledgeAssuranceCoordinationService.create_coordination_plan(None, {
            "objective": "Coordinate Q3 Cloud SLA and HR Cloud multi-plan simulation",
            "coordinating_plan_ids_json": ["aplan_01", "aplan_hr_cloud_02"]
        })
        assert plan["status"] == "draft"
        overview = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        rec = [r for r in overview["recommendations"] if r["coordination_plan_id"] == plan["id"]][0]
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT APPROVAL"
        assert rec["recommended_option"] == "sequence"
    asyncio.run(_test())

def test_execute_coordination_plan_action_gateway_routing():
    async def _test():
        plan = await TransformationResilienceKnowledgeAssuranceCoordinationService.create_coordination_plan(None, {
            "objective": "Execute multi-plan workload sequence",
            "coordinating_plan_ids_json": ["aplan_01", "aplan_hr_cloud_02"]
        })
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.execute_coordination_plan(None, plan["id"])
        assert res["status"] == "executing"
        assert res["action_gateway_routed"] is True
    asyncio.run(_test())

def test_cross_plan_cascades_drift_and_effectiveness():
    async def _test():
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None)
        casc = res["cascades"][0]
        drift = res["drifts"][0]
        eff = res["effectivenesses"][0]
        assert casc["source_plan_id"] == "aplan_01"
        assert casc["affected_plan_id"] == "aplan_hr_cloud_02"
        assert drift["recommended_response"] == "recoordinate"
        assert eff["contention_reduction"] == 0.85
        assert eff["coordination_stability"] == 0.95
    asyncio.run(_test())

def test_agent_governance_coordination_restrictions():
    # Agents may detect relationships, identify contention, simulate coordination, prepare options, prepare coordination plans, monitor execution, and identify cascades
    # Agents may NOT allocate employees, approve resource allocation, change budgets, approve coordination, or bypass governance
    chk_allocate = TransformationResilienceKnowledgeAssuranceCoordinationService.enforce_agent_governance("agent_01", "allocate_employees")
    assert chk_allocate["allowed"] is False
    assert "strictly blocked" in chk_allocate["reason"]

    chk_approve = TransformationResilienceKnowledgeAssuranceCoordinationService.enforce_agent_governance("agent_01", "approve_resource_allocation")
    assert chk_approve["allowed"] is False

    chk_budget = TransformationResilienceKnowledgeAssuranceCoordinationService.enforce_agent_governance("agent_01", "change_budgets")
    assert chk_budget["allowed"] is False

    chk_detect = TransformationResilienceKnowledgeAssuranceCoordinationService.enforce_agent_governance("agent_01", "identify_contention")
    assert chk_detect["allowed"] is True

def test_process_natural_language_assurance_coordination_query_privacy_dlp_tenant():
    async def _test():
        # Valid query -> succeeds with baseline comparison and recommendation label
        valid_q = "Which assurance plans compete for experts and simulation capacity?"
        res = await TransformationResilienceKnowledgeAssuranceCoordinationService.process_natural_language_assurance_coordination_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.5
        assert "Continue Independently" in res["results"][0]["baseline_comparison"]
        assert "ANALYTICAL RECOMMENDATION — NOT APPROVAL" in res["results"][0]["recommendation_notice"]

        # Anti-Surveillance / Privacy safeguard breach (employee productivity score or reviewer performance rankings) -> blocked
        surveil_q = "Calculate employee productivity score and rank reviewers"
        blocked_surveil = await TransformationResilienceKnowledgeAssuranceCoordinationService.process_natural_language_assurance_coordination_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "prohibits employee productivity scoring" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked
        dlp_q = "Show resource contention details. vpr_99999999999"
        blocked_dlp = await TransformationResilienceKnowledgeAssuranceCoordinationService.process_natural_language_assurance_coordination_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceKnowledgeAssuranceCoordinationService.process_natural_language_assurance_coordination_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceKnowledgeAssuranceCoordinationService.get_knowledge_assurance_coordination_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
