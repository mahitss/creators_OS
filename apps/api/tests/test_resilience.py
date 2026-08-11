import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.resilience_service import ResilienceService

def test_resilience_dashboard_telemetry():
    async def _test():
        dash = await ResilienceService.get_dashboard_summary(None)
        assert dash is not None
        assert "overallStatus" in dash
        assert "totalComponentsCount" in dash
        assert "capacity" in dash

    asyncio.run(_test())

def test_model_outage_fallback_and_safe_failure():
    async def _test():
        # Compliant fallback test
        res = await ResilienceService.evaluate_model_fallback(None, "openai", "gpt-4o", False)
        assert res["status"] == "fallback_selected"
        assert res["security_controls_active"] is True

        # Non-compliant / unavailable fallback test
        res_safe = await ResilienceService.evaluate_model_fallback(None, "untrusted_provider", "custom_model", True)
        assert res_safe["status"] in ["fallback_selected", "failed_safely"]
        assert res_safe["security_controls_active"] is True

    asyncio.run(_test())

def test_split_brain_state_lease_protection():
    async def _test():
        # Worker 1 acquires lease
        lease1 = await ResilienceService.acquire_state_lease(None, "mission_res_01", "worker_node_01", 10)
        assert lease1["status"] == "acquired"

        # Worker 2 attempts to acquire same lease -> Denied
        lease2 = await ResilienceService.acquire_state_lease(None, "mission_res_01", "worker_node_02", 10)
        assert lease2["status"] == "denied"
        assert "Split-brain protection" in lease2["reason"]

    asyncio.run(_test())

def test_external_action_reconciliation_and_idempotency():
    async def _test():
        key = "idempotency_key_test_01"
        rec1 = await ResilienceService.reconcile_external_action(None, key, "send_email", {"to": "user@example.com"})
        assert rec1["reconciled"] is True
        assert rec1["duplicate_detected"] is False

        # Retry with same idempotency key
        rec2 = await ResilienceService.reconcile_external_action(None, key, "send_email", {"to": "user@example.com"})
        assert rec2["reconciled"] is True
        assert rec2["duplicate_detected"] is True

    asyncio.run(_test())

def test_circuit_breaker_transitions():
    async def _test():
        cb = await ResilienceService.check_circuit_breaker(None, "external_api_v1")
        assert cb["state"] == "closed"

        # Trip circuit breaker
        tripped = await ResilienceService.trip_circuit_breaker(None, "external_api_v1")
        assert tripped["state"] == "open"
        assert tripped["failure_count"] >= 1

    asyncio.run(_test())

def test_dead_letter_and_replay():
    async def _test():
        dl = await ResilienceService.push_dead_letter(None, "msg_99", "event_queue", "Consumer timeout")
        assert dl["id"] is not None
        assert dl["status"] == "pending"

        # Controlled replay
        rp = await ResilienceService.replay_dead_letter(None, dl["id"])
        assert rp["status"] == "replayed"

    asyncio.run(_test())

def test_disaster_recovery_simulation_and_chaos():
    async def _test():
        rp = await ResilienceService.create_recovery_plan(None, {
            "name": "Test DR Plan",
            "componentsJson": ["db", "queue"],
            "rtoSeconds": 120,
            "rpoSeconds": 30,
            "recoveryOrderJson": ["1. DB", "2. Queue"]
        })
        assert rp["id"] is not None

        sim = await ResilienceService.simulate_recovery_plan(None, rp["id"])
        assert sim["simulation_result"] == "SUCCESS"

        # Chaos experiment abort
        start = await ResilienceService.start_chaos_experiment(None, "exp_latency_inj_01")
        assert start["status"] == "running"

        abort = await ResilienceService.abort_chaos_experiment(None, "exp_latency_inj_01", "Blast radius threshold reached")
        assert abort["status"] == "aborted"

    asyncio.run(_test())
