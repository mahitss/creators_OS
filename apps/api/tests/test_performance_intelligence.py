import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.performance_intelligence_service import PerformanceIntelligenceService

def test_performance_overview_telemetry():
    async def _test():
        ov = await PerformanceIntelligenceService.get_performance_overview(None)
        assert ov is not None
        assert "kpisCount" in ov
        assert "onTrackRatePct" in ov
        assert "staleCount" in ov
        assert "alertsCount" in ov
        assert ov["performanceHealthScore"] >= 0.90

    asyncio.run(_test())

def test_create_kpi_in_active_status():
    async def _test():
        k_data = {
            "name": "API Response P99 Latency",
            "description": "P99 latency across core GraphQL and REST API endpoints.",
            "definition": "PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY response_ms)",
            "owner": "usr_tech_lead",
            "category": "operational",
            "unit": "milliseconds",
            "direction": "lower_is_better"
        }
        kpi = await PerformanceIntelligenceService.create_kpi(None, k_data)
        assert kpi["id"] is not None
        assert kpi["status"] == "active"
        assert kpi["direction"] == "lower_is_better"

    asyncio.run(_test())

def test_kpi_targets_measurements_and_variances():
    async def _test():
        ov = await PerformanceIntelligenceService.get_performance_overview(None)
        assert len(ov["targets"]) > 0
        t = ov["targets"][0]
        assert t["version"] == 1
        assert t["target_value"] == 300.0

        assert len(ov["measurements"]) > 0
        m = ov["measurements"][0]
        assert m["quality"] == "verified"
        assert m["confidence"] >= 90.0

        assert len(ov["variances"]) > 0
        v = ov["variances"][0]
        assert v["status"] == "on_track"

    asyncio.run(_test())

def test_kpi_drivers_and_forecasts():
    async def _test():
        ov = await PerformanceIntelligenceService.get_performance_overview(None)
        assert len(ov["drivers"]) > 0
        d = ov["drivers"][0]
        assert d["association_type"] == "correlated" # No unevidenced causality

        assert len(ov["forecasts"]) > 0
        fc = ov["forecasts"][0]
        assert fc["confidence_pct"] >= 80.0
        assert fc["upper_bound"] >= fc["lower_bound"]

    asyncio.run(_test())

def test_natural_language_performance_query_and_dlp():
    async def _test():
        # Valid performance query
        res = await PerformanceIntelligenceService.process_natural_language_performance_query(None, "Which KPIs are deteriorating?")
        assert res["confidencePct"] > 80.0
        assert len(res["results"]) > 0

        # Secret query -> blocked by DLP
        secret_q = "Which KPIs are deteriorating? sk_live_666655554444"
        blocked = await PerformanceIntelligenceService.process_natural_language_performance_query(None, secret_q)
        assert blocked["confidencePct"] == 0.0
        assert "DLP secret boundary" in blocked["evidenceJson"].get("error", "")

    asyncio.run(_test())
