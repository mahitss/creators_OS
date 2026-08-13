import pytest
import asyncio
from app.services.transformation_resilience_digital_twin_service import TransformationResilienceDigitalTwinService

def test_synchronization():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        sync = res["synchronizations"][0]
        assert sync["synchronization_mode"] == "event_driven"
        assert sync["rebuild_status"] == "idle"
    asyncio.run(_test())

def test_snapshot():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        snap = res["snapshots"][0]
        assert snap["version"] == "v2.0"
        assert snap["transformations_count"] == 8
        assert len(snap["state_hash"]) > 0
    asyncio.run(_test())

def test_freshness():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        state = res["states"][0]
        assert state["freshness"] == 1.0
        assert state["completeness"] == 0.98
    asyncio.run(_test())

def test_reality_comparison():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        rcomp = res["realityComparisons"][0]
        assert "Production" in rcomp["production_state_summary"]
        assert "divergence" in rcomp["difference_description"].lower()
    asyncio.run(_test())

def test_scenario_fork():
    async def _test():
        fork = await TransformationResilienceDigitalTwinService.create_scenario_fork(None, "dtsnap_v2_0", "Resilience Architect")
        assert fork["base_snapshot_id"] == "dtsnap_v2_0"
        assert "fork_" in fork["id"]
    asyncio.run(_test())

def test_what_if():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.run_what_if_analysis(None, [{"change_type": "dependency_failure", "target_object_id": "dep_compute_cluster_01"}])
        assert res["isolation_status"] == "strictly_isolated_non_production"
        assert res["risk_score"] == 0.84
    asyncio.run(_test())

def test_multi_change():
    async def _test():
        changes = [
            {"change_type": "dependency_failure", "target_object_id": "dep_compute_cluster_01"},
            {"change_type": "deadline_change", "target_object_id": "aplan_01", "parameters": {"shift_days": 14}}
        ]
        res = await TransformationResilienceDigitalTwinService.run_what_if_analysis(None, changes, horizon_days=45)
        assert res["changes_processed"] == 2
        assert res["deadline_impact_days"] == 10
    asyncio.run(_test())

def test_stress():
    async def _test():
        stress = await TransformationResilienceDigitalTwinService.run_stress_test(None, "capacity_stress", "critical")
        assert stress["stress_type"] == "capacity_stress"
        assert stress["severity"] == "critical"
    asyncio.run(_test())

def test_shock():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        shock = res["shockScenarios"][0]
        assert shock["shock_name"] == "Global Multi-Cloud Data Center Outage"
        assert len(shock["recovery_assumptions_json"]) >= 1
    asyncio.run(_test())

def test_recovery():
    async def _test():
        rec = await TransformationResilienceDigitalTwinService.run_recovery_simulation(None, "contingency_recovery")
        assert rec["recovery_mode"] == "contingency_recovery"
        assert rec["time_to_stabilization_days"] == 5
        assert rec["risk_reduction_pct"] == 85.0
    asyncio.run(_test())

def test_experiment():
    async def _test():
        exp_res = await TransformationResilienceDigitalTwinService.run_experiment(None, {
            "title": "Redundancy Test Experiment",
            "hypothesis": "Secondary cluster failover reduces exposure by >80%",
            "expected_result": "Exposure drops to Low"
        })
        assert exp_res["experiment"]["status"] == "completed"
        assert exp_res["result"]["confidence"] == 0.94
    asyncio.run(_test())

def test_reproducibility():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        expres = res["experimentResults"][0]
        assert expres["snapshot_version"] == "v2.0"
        assert expres["scenario_version"] == "v2.0"
    asyncio.run(_test())

def test_validation():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        val = res["validations"][0]
        assert val["accuracy_pct"] == 94.5
        assert val["divergence_pct"] == 2.5
    asyncio.run(_test())

def test_model_error():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        merr = res["modelErrors"][0]
        assert merr["error_type"] == "recovery_error"
        assert merr["predicted_value"] == "3 days"
        assert merr["observed_value"] == "5 days"
    asyncio.run(_test())

def test_drift():
    async def _test():
        res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        drift = res["drifts"][0]
        assert drift["drift_type"] == "behavior_drift"
        assert drift["drift_magnitude"] == 0.03
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceDigitalTwinService.enforce_agent_governance("agent_dt_01", "create_scenario_fork")
    assert res1["allowed"] is True

    res2 = TransformationResilienceDigitalTwinService.enforce_agent_governance("agent_dt_01", "modify_production_through_simulation")
    assert res2["allowed"] is False

    res3 = TransformationResilienceDigitalTwinService.enforce_agent_governance("agent_dt_01", "execute_production_actions")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy blocked query
        p_res = await TransformationResilienceDigitalTwinService.process_natural_language_digital_twin_query(
            None, "Create employee digital twin and simulate individual behavioral productivity"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP blocked query
        dlp_res = await TransformationResilienceDigitalTwinService.process_natural_language_digital_twin_query(
            None, "Simulate outage using secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceDigitalTwinService.process_natural_language_digital_twin_query(
            None, "Show live digital twin state", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())
