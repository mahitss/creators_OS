import pytest
import asyncio
import time
from app.services.transformation_resilience_decision_lifecycle_service import TransformationResilienceDecisionLifecycleService, _EMITTED_DECISION_EVENTS

def test_get_decision_lifecycle_overview():
    async def _test():
        res = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
        assert res["domainsCount"] >= 1
        assert res["questionsCount"] >= 1
        assert res["decisionsCount"] >= 1
        assert res["optionsCount"] >= 3
        assert res["evidencePacksCount"] >= 1
        assert res["precedentsCount"] >= 1
    asyncio.run(_test())

def test_decision_questions_context_and_assumptions():
    async def _test():
        res = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
        q = res["questions"][0]
        ctx = res["contexts"][0]
        assm = res["assumptions"][0]
        assert "Should Enterprise Board approve $350,000 funding" in q["question"]
        assert q["trigger"] == "warning"
        assert ctx["resilience_state_json"]["recoverability"] == 0.95
        assert assm["sensitivity"] == "critical"
    asyncio.run(_test())

def test_options_scenarios_and_tradeoff_matrix():
    async def _test():
        res = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
        opts = res["options"]
        scen = res["scenarios"][0]
        to = res["tradeoffs"][0]
        assert len(opts) == 3
        assert opts[0]["optionality_score"] == 0.96
        assert "baseline" in scen["evaluated_scenarios_json"]
        assert len(to["tradeoff_matrix_json"]["comparison"]) >= 3
    asyncio.run(_test())

def test_recommendation_labeling_and_approval_routing():
    async def _test():
        res = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
        rec = res["recommendations"][0]
        assert rec["label"] == "RECOMMENDATION - NOT DECISION"
        assert rec["required_approval"] == "PolicyEngine + Enterprise Executive Board"
    asyncio.run(_test())

def test_human_decision_making_and_action_gateway_execution():
    async def _test():
        # Human decision maker approves Option A
        dec = await TransformationResilienceDecisionLifecycleService.make_decision(
            session=None,
            dec_id="dec_res_01",
            selected_option_id="opt_01",
            rationale="Approved by Chief Resilience Officer based on digital twin simulation.",
            decider_id="Chief Resilience Officer"
        )
        assert dec["status"] == "approved"
        assert dec["selected_option_id"] == "opt_01"

        # Execution routes through ActionGateway
        exec_res = await TransformationResilienceDecisionLifecycleService.execute_decision(
            session=None,
            dec_id="dec_res_01",
            payload={"initiated_by": "Authorized Human Decision Owner"}
        )
        assert exec_res["status"] == "executing"
        assert "action-gateway" in exec_res["action_gateway_route"]
    asyncio.run(_test())

def test_verification_effectiveness_and_decision_failures():
    async def _test():
        res = await TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None)
        verif = res["verifications"][0]
        eff = res["effectivenesses"][0]
        fail = res["failures"][0]
        assert verif["variance_pct"] == 2.1
        assert eff["risk_reduction_pct"] == 65.0
        assert fail["failure_classification"] == "bad_assumption"
    asyncio.run(_test())

def test_agent_governance_decision_lifecycle_restrictions():
    # Agents are strictly blocked from approving, rejecting, funding, executing material changes, or overriding decision owners
    chk_appr = TransformationResilienceDecisionLifecycleService.enforce_agent_governance("agent_01", "approve")
    assert chk_appr["allowed"] is False
    assert "strictly blocked" in chk_appr["reason"]

    chk_rej = TransformationResilienceDecisionLifecycleService.enforce_agent_governance("agent_01", "reject")
    assert chk_rej["allowed"] is False

    chk_exec = TransformationResilienceDecisionLifecycleService.enforce_agent_governance("agent_01", "execute_material_change")
    assert chk_exec["allowed"] is False

    chk_read = TransformationResilienceDecisionLifecycleService.enforce_agent_governance("agent_01", "draft_recommendation")
    assert chk_read["allowed"] is True

def test_process_natural_language_decision_query_privacy_dlp_tenant():
    async def _test():
        # Valid decision lifecycle query -> succeeds
        valid_q = "What resilience decisions need attention and what evidence supports option A?"
        res = await TransformationResilienceDecisionLifecycleService.process_natural_language_decision_query(None, valid_q)
        assert res["query"] == valid_q
        assert len(res["results"]) > 0
        assert res["confidencePct"] == 99.0

        # Anti-Surveillance / Privacy safeguard breach (individual personnel decision ranking) -> blocked
        surveil_q = "Rank personnel decision profiles and create individual decision rankings"
        blocked_surveil = await TransformationResilienceDecisionLifecycleService.process_natural_language_decision_query(None, surveil_q)
        assert blocked_surveil["confidencePct"] == 0.0
        assert "strictly prohibits individual personnel decision profiling" in blocked_surveil["evidenceJson"].get("error", "")

        # DLP secret query -> blocked by DLP
        dlp_q = "Show decision evidence pack. vpr_99999999999"
        blocked_dlp = await TransformationResilienceDecisionLifecycleService.process_natural_language_decision_query(None, dlp_q)
        assert blocked_dlp["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked_dlp["evidenceJson"].get("error", "")

        # Tenant Isolation breach -> DENY
        tenant_blocked = await TransformationResilienceDecisionLifecycleService.process_natural_language_decision_query(None, valid_q, caller_org_id="org_unauthorized_99")
        assert tenant_blocked["confidencePct"] == 0.0
        assert "Organization tenant isolation breach" in tenant_blocked["evidenceJson"].get("error", "")
    asyncio.run(_test())

def test_load_and_chaos_simulation():
    async def _test():
        t0 = time.time()
        tasks = [TransformationResilienceDecisionLifecycleService.get_decision_lifecycle_overview(None) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0
        assert len(results) == 100
        assert elapsed < 5.0
    asyncio.run(_test())
