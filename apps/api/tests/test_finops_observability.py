import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.finops import UsageRecordCreate
from app.services import finops_service

client = TestClient(app)

def test_versioned_pricing_and_cost_calculation():
    # 1. GPT-4o Cost calculation: 1000 input, 1000 output -> $0.005 + $0.015 = $0.020
    cost, version = finops_service.calculate_usage_cost("openai", "gpt-4o", 1000, 1000)
    assert cost == 0.020
    assert version == 1

    # 2. GPT-4o-mini Cost calculation: 10,000 input, 10,000 output -> $0.0015 + $0.0060 = $0.0075
    cost_mini, version_mini = finops_service.calculate_usage_cost("openai", "gpt-4o-mini", 10000, 10000)
    assert cost_mini == 0.0075

def test_atomic_pre_execution_budget_reservation_and_hard_limit():
    async def _test():
        ws_id = "ws_race_test"

        # 1. Budget reservation under limit -> SUCCESS
        safe, msg, res_id = await finops_service.check_and_reserve_budget(None, ws_id, estimated_cost=80.0, trace_id="tr_1")
        assert safe is True
        assert res_id is not None

        # 2. Concurrent budget reservation exceeding $100 limit -> DENY (Overspend Race Defense)
        safe2, msg2, res_id2 = await finops_service.check_and_reserve_budget(None, ws_id, estimated_cost=30.0, trace_id="tr_2")
        assert safe2 is False
        assert "Hard Budget Limit Exceeded" in msg2
        assert res_id2 is None

        # 3. Release unused budget reservation
        released = await finops_service.release_budget_reservation(None, res_id, actual_cost=75.0)
        assert released is True

    asyncio.run(_test())

def test_usage_recording_and_anomaly_detection():
    async def _test():
        ws_id = "ws_anomaly_test"
        u_in = UsageRecordCreate(
            workspaceId=ws_id,
            traceId="tr_anom_1",
            spanId="sp_anom_1",
            provider="openai",
            model="gpt-4o",
            input_units=5000,
            output_units=2000,
            duration_ms=450
        )
        rec = await finops_service.record_usage(None, u_in)
        assert rec["workspace_id"] == ws_id
        assert rec["cost"] > 0
        assert rec["pricing_version"] == 1

        # Anomaly detection
        anomalies = await finops_service.detect_cost_anomalies(None, ws_id)
        assert len(anomalies) >= 1

    asyncio.run(_test())

def test_finops_overview_and_infrastructure_rest_api():
    # 1. Overview API
    res = client.get("/api/v1/finops/overview?workspaceId=ws_default_creator")
    assert res.status_code == 200
    data = res.json()
    assert "budget_remaining" in data
    assert data["currency"] == "USD"

    # 2. Forecast API
    fc_res = client.get("/api/v1/finops/forecast?workspaceId=ws_default_creator")
    assert fc_res.status_code == 200
    assert "projected_end_of_month_cost" in fc_res.json()

    # 3. Model Infrastructure Health API
    infra_res = client.get("/api/v1/infrastructure/models")
    assert infra_res.status_code == 200
    models = infra_res.json()
    assert len(models) >= 3
    assert models[0]["status"] == "healthy"
