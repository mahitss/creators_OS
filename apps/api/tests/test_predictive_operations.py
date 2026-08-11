import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.predictive_operations_service import PredictiveOperationsService

def test_predictions_overview_telemetry():
    async def _test():
        ov = await PredictiveOperationsService.get_predictions_overview(None)
        assert ov is not None
        assert "forecastsCount" in ov
        assert "alertsCount" in ov
        assert "risksCount" in ov
        assert ov["overallAccuracyPct"] >= 90.0
        assert ov["predictionHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_forecast_in_active_status():
    async def _test():
        fc_data = {
            "entityType": "kpi",
            "entityId": "kpi_02",
            "metricId": "metric_cpu_utilization",
            "horizon": "short_term",
            "method": "ensemble_timeseries_v2"
        }
        fc = await PredictiveOperationsService.create_forecast(None, fc_data)
        assert fc["id"] is not None
        assert fc["status"] == "active"
        assert fc["horizon"] == "short_term"

    asyncio.run(_test())

def test_forecast_points_inputs_and_drivers():
    async def _test():
        ov = await PredictiveOperationsService.get_predictions_overview(None)
        assert len(ov["points"]) > 0
        p = ov["points"][0]
        assert p["upper_bound"] >= p["lower_bound"]
        assert p["confidence"] >= 90.0

        assert len(ov["alerts"]) > 0
        a = ov["alerts"][0]
        assert "Likely within" in a["predicted_window"] # Estimated window requirement

        assert len(ov["risks"]) > 0
        r = ov["risks"][0]
        assert "%" in r["probability_range"] # Probability range requirement

    asyncio.run(_test())

def test_capacity_forecasts_and_scenarios():
    async def _test():
        ov = await PredictiveOperationsService.get_predictions_overview(None)
        assert len(ov["capacityForecasts"]) > 0
        c = ov["capacityForecasts"][0]
        assert c["capacity_type"] == "agent"

        assert len(ov["scenarios"]) > 0
        sc = ov["scenarios"][0]
        assert sc["scenario_name"] == "downside"

    asyncio.run(_test())

def test_natural_language_predictive_query_dlp_and_privacy():
    async def _test():
        # Valid query
        res = await PredictiveOperationsService.process_natural_language_predictive_query(None, "What is likely to miss target in the next 30 days?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Secret query -> blocked by DLP
        secret_q = "What is likely to miss target? vpr_12345678901"
        blocked = await PredictiveOperationsService.process_natural_language_predictive_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

        # Anti-surveillance employee query -> blocked by Privacy policy
        priv_q = "Predict which employee to fire next month"
        denied = await PredictiveOperationsService.process_natural_language_predictive_query(None, priv_q)
        assert denied["confidencePct"] == 0.0
        assert "Employee surveillance" in denied["evidenceJson"].get("error", "")

    asyncio.run(_test())
