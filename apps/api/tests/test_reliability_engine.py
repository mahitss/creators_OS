import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.reliability import HealthSignalCreate, RecoveryPlanCreate, RecoveryStep
from app.services import reliability_service

client = TestClient(app)

def test_health_signal_ingestion_and_incident_correlation():
    async def _test():
        # 1. Ingest signal
        sig_in = HealthSignalCreate(
            workspaceId="ws_test_rel",
            service="openai_provider",
            resourceType="provider",
            resourceId="openai/gpt-4o",
            severity="high",
            signalType="provider_failure",
            observedValue=1.0,
            baselineValue=0.0
        )
        sig = await reliability_service.ingest_health_signal(None, sig_in)
        assert sig["service"] == "openai_provider"
        assert "incident_id" in sig

        # 2. Verify Incident Correlation (second signal correlates into same incident)
        sig2 = await reliability_service.ingest_health_signal(None, sig_in)
        assert sig2["incident_id"] == sig["incident_id"]

    asyncio.run(_test())

def test_evidence_backed_ai_diagnosis():
    async def _test():
        sig_in = HealthSignalCreate(
            service="calendar_api",
            resourceType="integration",
            resourceId="gmail_oauth",
            severity="warning",
            signalType="integration_failure",
            observedValue=5.0
        )
        sig = await reliability_service.ingest_health_signal(None, sig_in)
        inc_id = sig["incident_id"]

        diag = await reliability_service.diagnose_incident(None, inc_id)
        assert diag["incident_id"] == inc_id
        assert len(diag["observed"]) >= 1
        assert len(diag["correlated"]) >= 1
        assert len(diag["suspected"]) >= 1
        assert diag["confidence"] > 0.5

    asyncio.run(_test())

def test_idempotent_recovery_execution_and_loop_protection():
    async def _test():
        # 1. Create Recovery Plan
        sig_in = HealthSignalCreate(service="worker_pool", resourceType="worker", resourceId="w_01", signalType="worker_failure", observedValue=1.0)
        sig = await reliability_service.ingest_health_signal(None, sig_in)
        inc_id = sig["incident_id"]

        plan_in = RecoveryPlanCreate(
            incidentId=inc_id,
            steps=[
                RecoveryStep(type="restart_worker", target="worker_pool_01", parameters={}),
                RecoveryStep(type="retry_transient_job", target="job_123", parameters={})
            ]
        )
        plan, err = await reliability_service.create_recovery_plan(None, plan_in)
        assert err is None
        assert plan["status"] == "proposed"

        # 2. Execute Step (Idempotent)
        execution, err = await reliability_service.execute_recovery_action(None, plan["id"], 0)
        assert err is None
        assert execution["status"] == "verified"

        # 3. Idempotent Retry (Returns same result without re-executing side effects)
        execution2, err2 = await reliability_service.execute_recovery_action(None, plan["id"], 0)
        assert err2 is None
        assert execution2["id"] == execution["id"]

    asyncio.run(_test())

def test_circuit_breaker_transitions_and_forbidden_action_protection():
    async def _test():
        service = "anthropic_test_cb"

        # 1. Record 3 failures to trigger CLOSED -> OPEN transition
        await reliability_service.record_circuit_breaker_failure(None, service)
        await reliability_service.record_circuit_breaker_failure(None, service)
        cb = await reliability_service.record_circuit_breaker_failure(None, service)
        assert cb["status"] == "open"

        # 2. Forbidden Recovery Action Protection
        sig_in = HealthSignalCreate(service="security_test", resourceType="system", resourceId="sec_01", signalType="budget_exhaustion", observedValue=1.0)
        sig = await reliability_service.ingest_health_signal(None, sig_in)

        forbidden_plan = RecoveryPlanCreate(
            incidentId=sig["incident_id"],
            steps=[RecoveryStep(type="modify_policy", target="policy_engine", parameters={})]
        )
        plan, err = await reliability_service.create_recovery_plan(None, forbidden_plan)
        assert plan == {}
        assert "Forbidden Recovery Action Denied" in err

    asyncio.run(_test())

def test_reliability_rest_api():
    # 1. Signal Ingestion API
    res = client.post("/api/v1/health/signals", json={
        "service": "api_gateway",
        "resourceType": "gateway",
        "resourceId": "gw_01",
        "severity": "warning",
        "signalType": "latency_degradation",
        "observedValue": 850.0
    })
    assert res.status_code == 201
    data = res.json()
    assert data["service"] == "api_gateway"

    # 2. Circuit Breaker API
    cb_res = client.get("/api/v1/circuit-breakers/api_gateway")
    assert cb_res.status_code == 200

    # 3. Runbooks API
    rb_res = client.get("/api/v1/runbooks")
    assert rb_res.status_code == 200
    assert len(rb_res.json()) >= 1
