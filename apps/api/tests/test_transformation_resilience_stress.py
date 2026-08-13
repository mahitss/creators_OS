import pytest
import asyncio
from app.services.transformation_resilience_stress_service import TransformationResilienceStressService

def test_hypothesis():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        hyp = res["hypotheses"][0]
        assert "hypothesis" in hyp
        assert len(hyp["assumptions_json"]) >= 1
        assert "expected_outcome" in hyp
    asyncio.run(_test())

def test_failure_injection():
    async def _test():
        inj = await TransformationResilienceStressService.create_failure_injection(None, {
            "injection_type": "dependency_failure",
            "target_id": "dep_compute_cluster_01"
        })
        assert inj["environment"] == "SIMULATION_ONLY"
        assert "sbx_" in inj["sandbox_id"]
    asyncio.run(_test())

def test_compound_failure():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        cfail = res["compoundFailures"][0]
        assert cfail["interaction"] in ["amplifying", "independent", "dampening", "blocking", "cascading"]
        assert "disruption" in cfail["combined_impact"].lower()
    asyncio.run(_test())

def test_reproducibility():
    async def _test():
        sim1 = await TransformationResilienceStressService.run_scenario_simulation(None, "stscen_01", seed=42)
        sim2 = await TransformationResilienceStressService.run_scenario_simulation(None, "stscen_01", seed=42)
        assert sim1["run"]["simulation_version"] == sim2["run"]["simulation_version"]
        assert sim1["result"]["residual_exposure"] == sim2["result"]["residual_exposure"]
    asyncio.run(_test())

def test_detection():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        det = res["detectionResults"][0]
        assert det["detected"] is True
        assert det["detection_time_seconds"] == 12.0
    asyncio.run(_test())

def test_false_negative():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        det = res["detectionResults"][0]
        assert det["false_negative"] is False
    asyncio.run(_test())

def test_intervention():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        ival = res["interventionValidations"][0]
        assert ival["intervention_recommended"] is True
        assert ival["effectiveness_pct"] == 88.5
    asyncio.run(_test())

def test_recovery():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        recres = res["recoveryResults"][0]
        assert recres["stabilization_days"] == 4
        assert recres["risk_reduction_pct"] == 85.0
    asyncio.run(_test())

def test_control_failure():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        cfail_ctrl = res["controlFailures"][0]
        assert "quota" in cfail_ctrl["failure_reason"].lower()
        assert "recommended_improvement" in cfail_ctrl
    asyncio.run(_test())

def test_regression():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        reg = res["regressions"][0]
        assert reg["previous_result"] == "passed"
        assert reg["current_result"] == "failed"
    asyncio.run(_test())

def test_coverage():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        covgap = res["coverageGaps"][0]
        assert covgap["gap_reason"] in ["no_stress_test", "outdated_stress_test", "insufficient_scenario_diversity", "insufficient_recovery_validation"]
    asyncio.run(_test())

def test_playbook():
    async def _test():
        pbook = await TransformationResilienceStressService.test_recovery_playbook(None, "pbook_01")
        assert pbook["readiness_status"] == "ready"
    asyncio.run(_test())

def test_governance():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        govtest = res["governanceTests"][0]
        assert govtest["compliance_passed"] is True
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceStressService.enforce_agent_governance("agent_stress_01", "run_scenario_simulation")
    assert res1["allowed"] is True

    res2 = TransformationResilienceStressService.enforce_agent_governance("agent_stress_01", "inject_production_failures")
    assert res2["allowed"] is False

    res3 = TransformationResilienceStressService.enforce_agent_governance("agent_stress_01", "modify_source_snapshots")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy check: employee stress testing
        p_res = await TransformationResilienceStressService.process_natural_language_stress_query(
            None, "Execute employee stress test and measure individual worker productivity failure"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP check: secret leak
        dlp_res = await TransformationResilienceStressService.process_natural_language_stress_query(
            None, "Run failure injection using secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceStressService.process_natural_language_stress_query(
            None, "Show stress testing status", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())

def test_remediation_label():
    async def _test():
        res = await TransformationResilienceStressService.get_stress_overview(None)
        remed = res["remediationRecommendations"][0]
        assert remed["label"] == "ANALYTICAL RECOMMENDATION — NOT DECISION"
    asyncio.run(_test())
