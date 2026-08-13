import pytest
import asyncio
from app.services.transformation_resilience_learning_service import TransformationResilienceLearningService

def test_expectation():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        exp = res["expectations"][0]
        assert exp["source_system"] == "foresight"
        assert exp["model_version"] == "v2.0"
    asyncio.run(_test())

def test_actual():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        act = res["actualOutcomes"][0]
        assert act["validation_status"] == "validated"
    asyncio.run(_test())

def test_comparison():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        comp = res["outcomeComparisons"][0]
        assert comp["direction"] == "worse_than_expected"
        assert comp["variance_score"] == 0.15
    asyncio.run(_test())

def test_prediction_error():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        perr = res["predictionErrors"][0]
        assert perr["error_type"] == "severity_error"
        assert perr["severity_delta"] == 0.15
    asyncio.run(_test())

def test_warning_quality():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        wqual = res["warningQuality"]
        assert wqual["precision_pct"] == 95.0
        assert wqual["recall_pct"] == 92.0
        assert wqual["avg_lead_time_hours"] == 48.0
        assert wqual["false_positive_rate"] == 0.05
        assert wqual["false_negative_rate"] == 0.08
    asyncio.run(_test())

def test_intervention():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        inteff = res["interventionEffectiveness"][0]
        assert inteff["risk_reduction_score"] == 0.85
    asyncio.run(_test())

def test_recovery():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        recout = res["recoveryOutcomes"][0]
        assert recout["expected_recovery_hours"] == 24.0
        assert recout["actual_recovery_hours"] == 24.0
    asyncio.run(_test())

def test_assumption():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        afail = res["assumptionFailures"][0]
        assert "bandwidth quota" in afail["actual"].lower()
        assert "failover" in afail["impact_description"].lower()
    asyncio.run(_test())


def test_pattern():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        patt = res["patterns"][0]
        assert patt["pattern_type"] == "warning_failure"
    asyncio.run(_test())

def test_pattern_confirmation():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        patt = res["patterns"][0]
        assert patt["status"] == "confirmed"
    asyncio.run(_test())

def test_calibration():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        prop = res["calibrationProposals"][0]
        assert prop["status"] == "review"
        assert prop["governance_requirement"] == "policy_approval_required"
    asyncio.run(_test())

def test_governed_apply():
    async def _test():
        prop = await TransformationResilienceLearningService.approve_calibration_proposal(None, "calprop_01")
        assert prop["status"] == "approved"

        chg = await TransformationResilienceLearningService.apply_calibration_proposal(None, "calprop_01", "Governed Resilience Board")
        assert chg["calibration_version"] == "v2.1"
        assert chg["applied_by"] == "Governed Resilience Board"
    asyncio.run(_test())

def test_rollback():
    async def _test():
        rollback_rec = await TransformationResilienceLearningService.rollback_calibration_change(None, "calchg_01", "Validation failed", "Governed Resilience Board")
        assert rollback_rec["previous_version_restored"] == "v2.0"
        assert rollback_rec["rollback_reason"] == "Validation failed"
    asyncio.run(_test())

def test_model_drift():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        mdrift = res["modelDrifts"][0]
        assert mdrift["drift_type"] == "data_drift"
        assert mdrift["magnitude"] == 0.02
    asyncio.run(_test())

def test_model_regression():
    async def _test():
        res = await TransformationResilienceLearningService.get_learning_overview(None)
        mreg = res["modelRegressions"][0]
        assert mreg["regression_type"] == "performance_deterioration"
    asyncio.run(_test())

def test_experiment():
    async def _test():
        exp = await TransformationResilienceLearningService.run_calibration_experiment(None, "Validation Experiment", "threshold = 0.80", "threshold = 0.75")
        assert exp["status"] == "completed"
        assert exp["confidence"] == 0.98
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceLearningService.enforce_agent_governance("agent_learn_01", "compare_expected_vs_actual")
    assert res1["allowed"] is True

    res2 = TransformationResilienceLearningService.enforce_agent_governance("agent_learn_01", "silently_change_production_models")
    assert res2["allowed"] is False

    res3 = TransformationResilienceLearningService.enforce_agent_governance("agent_learn_01", "apply_governed_calibration_without_authorization")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy check: employee behavioral surveillance
        p_res = await TransformationResilienceLearningService.process_natural_language_learning_query(
            None, "Perform employee behavioral surveillance and individual productivity scoring across teams"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP check: secret leak
        dlp_res = await TransformationResilienceLearningService.process_natural_language_learning_query(
            None, "Run learning cycle using secret key sk_live_secret_key_1234567890"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())

def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceLearningService.process_natural_language_learning_query(
            None, "What did Vapor get wrong recently?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())

def test_audit():
    async def _test():
        chg = await TransformationResilienceLearningService.apply_calibration_proposal(None, "calprop_01", "Governed Resilience Board")
        assert "id" in chg
        assert chg["applied_by"] == "Governed Resilience Board"
    asyncio.run(_test())
