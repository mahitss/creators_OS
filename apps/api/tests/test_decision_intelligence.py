import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import decision_intelligence_service
from app.schemas.decision_intelligence import DecisionSignalCreate, DecisionScenarioCreate

client = TestClient(app)

def test_signal_recording_and_retrieval():
    async def _test():
        sig_data = DecisionSignalCreate(
            organizationId="org_test",
            workspaceId="ws_dec_test",
            type="workflow_volume",
            source="workflow_engine",
            value=150.0,
            unit="count",
            window="1h",
            quality="fresh"
        )
        sig = await decision_intelligence_service.record_signal(None, sig_data)
        assert sig["type"] == "workflow_volume"
        assert sig["value"] == 150.0

        signals = await decision_intelligence_service.get_signals(None, "ws_dec_test")
        assert len(signals) >= 1

    asyncio.run(_test())

def test_baselines_and_anomaly_detection():
    async def _test():
        # Baseline Calculation
        base = await decision_intelligence_service.calculate_baseline(None, "workflow_volume")
        assert base["baseline_value"] > 0

        # Normal variation -> No anomaly
        anom_none = await decision_intelligence_service.detect_anomalies(None, "workflow_volume", current_value=base["baseline_value"] * 1.05)
        assert anom_none is None

        # High spike -> Anomaly detected
        anom_high = await decision_intelligence_service.detect_anomalies(None, "workflow_volume", current_value=base["baseline_value"] * 2.5)
        assert anom_high is not None
        assert anom_high["severity"] in ["high", "critical"]

    asyncio.run(_test())

def test_forecast_generation_and_evaluation():
    async def _test():
        # Statistical Forecast
        fc = await decision_intelligence_service.generate_forecast(None, "workflow_volume")
        assert fc["predicted_value"] > 0
        assert fc["uncertainty"] == 0.10

        # Forecast Evaluation
        eval_res = await decision_intelligence_service.evaluate_forecast(None, fc["id"], actual_value=fc["predicted_value"] * 1.02)
        assert eval_res["mae"] >= 0
        assert eval_res["rmse"] >= 0

    asyncio.run(_test())

def test_scenario_sandbox_simulation():
    async def _test():
        scen_data = DecisionScenarioCreate(
            name="30% Growth Simulation",
            assumptions={"growth_rate": 0.30},
            inputs={"current_jobs_daily": 1000}
        )
        scen = await decision_intelligence_service.create_scenario(None, scen_data)
        sim = await decision_intelligence_service.simulate_scenario(None, scen["id"])

        assert sim["delta"]["jobs_diff"] == 300.0
        assert sim["scenario_output"]["daily_cost"] > sim["baseline"]["daily_cost"]

    asyncio.run(_test())

def test_recommendation_policy_gate_and_decisions():
    async def _test():
        # Generate Recommendation
        rec = await decision_intelligence_service.generate_recommendation(
            None, "cost_optimization", "Provider B has 20% lower latency",
            [{"source": "finops_metrics", "finding": "Provider B cheaper"}],
            "Save $45/mo", risk="low"
        )
        assert rec["status"] == "new"

        # Resolve Accept -> Decision Record + Outcome created
        resolved = await decision_intelligence_service.resolve_recommendation(None, rec["id"], "accept")
        assert resolved["status"] == "accepted"

        # Feedback Recording
        fb = await decision_intelligence_service.record_feedback(None, rec["id"], "useful")
        assert fb["feedback"] == "useful"

    asyncio.run(_test())

def test_decision_intelligence_rest_api():
    # 1. Signals API
    sig_res = client.get("/api/v1/intelligence/signals?workspaceId=ws_default_creator")
    assert sig_res.status_code == 200

    # 2. Anomalies API
    anom_res = client.get("/api/v1/intelligence/anomalies")
    assert anom_res.status_code == 200

    # 3. Forecasts API
    fc_res = client.get("/api/v1/intelligence/forecasts?signalType=workflow_volume")
    assert fc_res.status_code == 200

    # 4. Recommendations API & Accept
    rec_res = client.get("/api/v1/intelligence/recommendations")
    assert rec_res.status_code == 200
    rec_id = rec_res.json()[0]["id"]

    acc_res = client.post(f"/api/v1/intelligence/recommendations/{rec_id}/accept")
    assert acc_res.status_code == 200
    assert acc_res.json()["status"] == "accepted"

    # 5. Decisions API
    dec_res = client.get("/api/v1/intelligence/decisions")
    assert dec_res.status_code == 200

    # 6. Scenarios API & Simulate
    scen_res = client.post("/api/v1/intelligence/scenarios", json={"name": "Test Simulation", "assumptions": {}, "inputs": {}})
    assert scen_res.status_code == 200
    scen_id = scen_res.json()["id"]

    sim_res = client.post(f"/api/v1/intelligence/scenarios/{scen_id}/simulate")
    assert sim_res.status_code == 200

    # 7. Outcomes API
    out_res = client.get("/api/v1/intelligence/outcomes")
    assert out_res.status_code == 200

    # 8. Feedback API
    fb_res = client.post("/api/v1/intelligence/feedback", json={"recommendationId": rec_id, "feedback": "useful"})
    assert fb_res.status_code == 200
