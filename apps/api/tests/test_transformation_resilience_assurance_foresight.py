import pytest
import asyncio
from app.services.transformation_resilience_assurance_foresight_service import TransformationResilienceAssuranceForesightService

def test_trend_signal():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        sig = res["signals"][0]
        assert sig["type"] == "capacity_pressure"
        assert sig["confidence"] == 0.94
        assert sig["source_quality"] == 0.95
    asyncio.run(_test())

def test_leading_indicator_state():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        ind = res["indicators"][0]
        assert ind["state"] == "warning"
        assert ind["threshold"] == 0.85
        assert ind["direction"] == "increasing"
    asyncio.run(_test())

def test_assurance_pressure_dimensions():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        press = res["pressures"][0]
        assert press["capacity_pressure"] == 0.85
        assert press["deadline_pressure"] == 0.75
        assert press["conflict_pressure"] == 0.40
        assert press["risk_pressure"] == 0.20
    asyncio.run(_test())

def test_emerging_risk_tracking():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        emr = res["emergingRisks"][0]
        assert emr["status"] == "developing"
        assert emr["horizon"] == "near_term"
        assert emr["confidence"] == 0.92
    asyncio.run(_test())

def test_range_forecast():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        fcst = res["forecasts"][0]
        assert fcst["baseline_value"] == 0.84
        assert fcst["lower_bound"] == 0.88
        assert fcst["central_estimate"] == 0.92
        assert fcst["upper_bound"] == 0.95
        assert fcst["confidence"] == 0.95
    asyncio.run(_test())

def test_forecast_scenarios():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        scen_base = [s for s in res["scenarios"] if s["scenario_type"] == "continue_current_state"][0]
        scen_reseq = [s for s in res["scenarios"] if s["scenario_type"] == "resequence"][0]
        assert scen_base["risk_score"] == 0.25
        assert scen_reseq["risk_score"] == 0.08
    asyncio.run(_test())

def test_early_warnings():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        warn = res["warnings"][0]
        assert warn["severity"] == "high"
        assert warn["status"] == "open"
        assert "Preemptively resequence" in warn["recommended_attention"]
    asyncio.run(_test())

def test_intervention_window():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        win = res["interventionWindows"][0]
        assert win["estimated_duration_days"] == 10
        assert win["confidence"] == 0.92
    asyncio.run(_test())

def test_preventive_options_mandatory_baseline():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        opts = res["preventiveOptions"]
        baseline_opt = [o for o in opts if o["option_type"] == "do_nothing"][0]
        reseq_opt = [o for o in opts if o["option_type"] == "resequence"][0]
        assert baseline_opt["title"] == "Baseline Option: Do Nothing / Continue Current State"
        assert baseline_opt["risk_reduction"] == 0.0
        assert reseq_opt["risk_reduction"] == 0.90
    asyncio.run(_test())

def test_analytical_recommendations_and_invalidation():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        rec = res["recommendations"][0]
        inv = res["invalidationConditions"][0]
        assert rec["label"] == "ANALYTICAL RECOMMENDATION — NOT DECISION"
        assert rec["recommended_option"] == "resequence"
        assert "additional simulation cluster capacity" in inv["condition_description"].lower()
    asyncio.run(_test())

def test_forecast_calibration_and_quality():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        qual = res["qualities"][0]
        assert qual["signal_quality"] == 0.95
        assert qual["forecast_accuracy"] == 0.94
        assert qual["false_positive_rate"] == 0.02
    asyncio.run(_test())

def test_false_positives_and_false_negatives():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        fp = res["falsePositives"][0]
        fn = res["falseNegatives"][0]
        assert "auto-tiering" in fp["cause"]
        assert "changelog telemetry feed was offline" in fn["cause"]
    asyncio.run(_test())

def test_context_shifts_and_regime_changes():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        cshift = res["contextShifts"][0]
        reg = res["regimeChanges"][0]
        assert cshift["dimension"] == "capacity"
        assert reg["status"] == "suspected"
    asyncio.run(_test())

def test_systemic_warnings_cascades_and_escalations():
    async def _test():
        res = await TransformationResilienceAssuranceForesightService.get_assurance_foresight_overview(None)
        syswarn = res["systemicWarnings"][0]
        casc = res["cascades"][0]
        esc = res["escalations"][0]
        assert syswarn["severity"] == "critical"
        assert casc["depth"] == 2
        assert esc["status"] == "escalated"
    asyncio.run(_test())

def test_agent_governance_boundaries():
    res1 = TransformationResilienceAssuranceForesightService.enforce_agent_governance("agent_foresight_01", "detect_trends")
    assert res1["allowed"] is True

    res2 = TransformationResilienceAssuranceForesightService.enforce_agent_governance("agent_foresight_01", "declare_certainty")
    assert res2["allowed"] is False

    res3 = TransformationResilienceAssuranceForesightService.enforce_agent_governance("agent_foresight_01", "accept_risk")
    assert res3["allowed"] is False

def test_anti_surveillance_privacy_and_dlp_checks():
    async def _test():
        # Privacy blocked query
        p_res = await TransformationResilienceAssuranceForesightService.process_natural_language_assurance_foresight_query(
            None, "Calculate employee risk prediction and individual productivity forecast for worker 01"
        )
        assert "blocked" in p_res["evidenceJson"]["error"].lower()

        # DLP blocked query
        dlp_res = await TransformationResilienceAssuranceForesightService.process_natural_language_assurance_foresight_query(
            None, "What risks are emerging for secret key sk_live_secret_key_1234567890?"
        )
        assert "dlp" in dlp_res["evidenceJson"]["error"].lower()
    asyncio.run(_test())


def test_tenant_isolation():
    async def _test():
        t_res = await TransformationResilienceAssuranceForesightService.process_natural_language_assurance_foresight_query(
            None, "What risks are emerging?", caller_org_id="org_rival_corp_99"
        )
        assert "DENY" in t_res["evidenceJson"]["error"]
    asyncio.run(_test())
