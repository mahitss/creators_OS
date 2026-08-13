import pytest
import asyncio
from app.services.transformation_resilience_assurance_interventions_service import TransformationResilienceAssuranceInterventionsService

def test_trigger():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        trig = res["triggers"][0]
        assert trig["type"] == "early_warning"
        assert trig["validation_status"] == "validated"
        assert trig["confidence"] == 0.95
    asyncio.run(_test())

def test_invalid_trigger():
    # If trigger validation fails, material action must be blocked
    res = TransformationResilienceAssuranceInterventionsService.enforce_agent_governance("agent_01", "activate_irreversible_intervention")
    assert res["allowed"] is False

def test_options_with_mandatory_baseline():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        opts = res["options"]
        base_opt = [o for o in opts if o["option_type"] == "continue_current_state"][0]
        reseq_opt = [o for o in opts if o["option_type"] == "resequence"][0]
        assert base_opt["title"] == "Baseline Option: Continue Current State / Do Nothing"
        assert base_opt["risk_reduction"] == 0.0
        assert reseq_opt["risk_reduction"] == 0.90
    asyncio.run(_test())

def test_option_reversibility_governance():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        opts = res["options"]
        rev_opt = [o for o in opts if o["reversibility"] == "reversible"][0]
        part_opt = [o for o in opts if o["reversibility"] == "partially_reversible"][0]
        assert rev_opt["reversibility"] == "reversible"
        assert part_opt["reversibility"] == "partially_reversible"
    asyncio.run(_test())

def test_scenario_simulations():
    async def _test():
        scen = await TransformationResilienceAssuranceInterventionsService.simulate_intervention_scenario(None, "icase_01", {"scenario_type": "resequence"})
        assert scen["case_id"] == "icase_01"
        assert scen["scenario_type"] == "resequence"
        assert scen["risk_reduction"] == 0.90
    asyncio.run(_test())

def test_failure_scenario_modeling():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        fail = res["failures"][0]
        assert fail["failure_type"] == "execution_failure"
        assert "DNS resolution error" in fail["cause"]
    asyncio.run(_test())

def test_rollback_plan():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        rplan = res["rollbackPlans"][0]
        assert rplan["authorization_required"] == "Governance Board Authorization"
        assert rplan["expected_recovery_time_hours"] == 2
    asyncio.run(_test())

def test_contingency_readiness_dimensions():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        rd = res["readinesses"][0]
        assert rd["evidence_readiness"] == "ready"
        assert rd["resource_readiness"] == "ready"
        assert rd["dependency_readiness"] == "partially_ready"
        assert rd["overall_status"] == "partially_ready"
    asyncio.run(_test())

def test_approval_enforcement():
    async def _test():
        app_res = await TransformationResilienceAssuranceInterventionsService.request_intervention_approval(None, "icase_01")
        assert app_res["status"] == "awaiting_decision"
    asyncio.run(_test())

def test_action_gateway_execution():
    async def _test():
        exec_res = await TransformationResilienceAssuranceInterventionsService.execute_intervention_action(None, "iact_01")
        assert exec_res["status"] == "completed"
    asyncio.run(_test())

def test_stale_intervention_protection():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        exp = res["expirations"][0]
        assert "Intervention window closes" in exp["reason"]
    asyncio.run(_test())

def test_intervention_conflict_detection():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        conf = res["conflicts"][0]
        assert conf["severity"] == "high"
        assert "HR Cloud testing window" in conf["conflict_summary"]
    asyncio.run(_test())

def test_intervention_cascade():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        casc = res["cascades"][0]
        assert casc["severity"] == "material"
        assert casc["confidence"] == 0.92
    asyncio.run(_test())

def test_contingency_readiness_and_activation():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        cplan = res["contingencyPlans"][0]
        assert cplan["status"] == "ready"
        assert cplan["capacity_reserved"] == "2 backup compute nodes"
    asyncio.run(_test())

def test_effectiveness_dimensions():
    async def _test():
        res = await TransformationResilienceAssuranceInterventionsService.get_assurance_interventions_overview(None)
        eff = res["effectivenesses"][0]
        assert eff["lead_time_days"] == 14.0
        assert eff["risk_reduction"] == 0.90
        assert eff["rollback_success"] is True
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceAssuranceInterventionsService.enforce_agent_governance("agent_intervention_01", "prepare_options")
    assert res1["allowed"] is True

    res2 = TransformationResilienceAssuranceInterventionsService.enforce_agent_governance("agent_intervention_01", "approve")
    assert res2["allowed"] is False

    res3 = TransformationResilienceAssuranceInterventionsService.enforce_agent_governance("agent_intervention_01", "activate_irreversible_intervention")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy blocked query
        p_res = await TransformationResilienceAssuranceInterventionsService.process_natural_language_assurance_intervention_query(
            None, "Calculate employee intervention score and worker productivity prediction for employee 01"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP blocked query
        dlp_res = await TransformationResilienceAssuranceInterventionsService.process_natural_language_assurance_intervention_query(
            None, "What intervention options are available for secret key sk_live_secret_key_1234567890?"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceAssuranceInterventionsService.process_natural_language_assurance_intervention_query(
            None, "Which warnings require intervention?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())
