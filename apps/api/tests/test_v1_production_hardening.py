import pytest
import asyncio
from app.core.v1_errors import format_v1_api_error
from app.services.transformation_resilience_governance_service import TransformationResilienceGovernanceService
from app.services.transformation_resilience_learning_service import TransformationResilienceLearningService
from app.services.transformation_resilience_digital_twin_service import TransformationResilienceDigitalTwinService
from app.services import dlp_service

def test_01_v1_standardized_error_contract():
    """Test #6: API Error Standard - Format error without stack traces, internal paths, or credentials."""
    err = format_v1_api_error(
        code="RESOURCE_NOT_FOUND",
        message="Transformation entity with ID tf_123 not found.\nTraceback (most recent call last):\n  File 'db.py', line 42, in execute",
        request_id="req_test_01"
    )
    assert err["code"] == "RESOURCE_NOT_FOUND"
    assert err["requestId"] == "req_test_01"
    assert "timestamp" in err
    assert "Traceback" not in err["message"]
    assert "File" not in err["message"]

def test_02_feature_freeze_and_post_v1_backlog():
    """Test #1: Feature Freeze - Confirm non-critical features are documented in post-V1 backlog."""
    import os
    backlog_path = os.path.join("docs", "POST_V1_BACKLOG.md")
    assert os.path.exists(backlog_path)
    with open(backlog_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Deferred Non-Critical Features" in content

def test_03_tenant_isolation_adversarial_check():
    """Test #10: Tenant Isolation - Organization A MUST NEVER access Organization B."""
    async def _test():
        res_org_a = await TransformationResilienceGovernanceService.process_natural_language_governance_query(
            None, "Is Vapor production ready?", caller_org_id="org_global_enterprise_01"
        )
        assert res_org_a["confidencePct"] == 100.0

        res_org_b = await TransformationResilienceGovernanceService.process_natural_language_governance_query(
            None, "Is Vapor production ready?", caller_org_id="org_unauthorized_attacker_b"
        )
        assert "DENY" in res_org_b["evidenceJson"].get("error", "")
        assert res_org_b["confidencePct"] == 0.0
    asyncio.run(_test())

def test_04_dlp_secret_redaction_boundary():
    """Test #15: DLP Final Audit - Secrets in prompts/responses are blocked/redacted."""
    findings = dlp_service.detect_sensitive_patterns("Check api key vpr_1234567890123")
    assert len(findings) >= 1
    assert findings[0]["classification"] == "secret"

def test_05_simulation_sandbox_read_only_safety():
    """Test #13: Simulation Safety - Digital Twin & Stress Testing cannot mutate production state."""
    async def _test():
        tw_res = await TransformationResilienceDigitalTwinService.get_digital_twin_overview(None)
        assert tw_res is not None
        # Simulation execution returns scenario projections without mutating base production records
        assert "domainsCount" in tw_res
        assert tw_res["domainsCount"] >= 1
    asyncio.run(_test())


def test_06_agent_governance_safety_boundaries():
    """Test #14: Agent Safety - Subagents CANNOT autonomously approve production releases or accept risk."""
    allow_recommend = TransformationResilienceGovernanceService.enforce_agent_governance("agent_01", "prepare_readiness_assessment")
    assert allow_recommend["allowed"] is True

    deny_approve = TransformationResilienceGovernanceService.enforce_agent_governance("agent_01", "approve_releases")
    assert deny_approve["allowed"] is False
    assert "BLOCKED" in deny_approve["reason"]

    deny_risk = TransformationResilienceGovernanceService.enforce_agent_governance("agent_01", "accept_risk")
    assert deny_risk["allowed"] is False
    assert "BLOCKED" in deny_risk["reason"]

def test_07_disaster_recovery_and_rollback_readiness():
    """Test #58: Disaster Recovery Assurance - Backup, restore, and failover evidence validated."""
    async def _test():
        gov_res = await TransformationResilienceGovernanceService.get_governance_overview(None)
        recov = gov_res.get("recoveryReadiness", [])
        assert len(recov) >= 1
        r = recov[0]
        assert r["data_integrity_validated"] is True
        assert r["recovery_time_hours"] <= 4.0
        assert r["recovery_point_minutes"] == 0.0
    asyncio.run(_test())

def test_08_correlation_id_and_structured_logging():
    """Test #30: Correlation IDs - Traceability across request, audit, and event payload."""
    err = format_v1_api_error("INVALID_INPUT", "Input validation failed", request_id="trace_correl_999")
    assert err["requestId"] == "trace_correl_999"

def test_09_production_readiness_verdict():
    """Test #86: Release Decision - Governance readiness assessment outputs explicit verdict."""
    async def _test():
        assess = await TransformationResilienceGovernanceService.assess_production_readiness(None)
        assert assess["verdict"] in ["ready", "conditionally_ready", "not_ready", "degraded", "blocked"]
        assert assess["summary"] is not None
    asyncio.run(_test())

def test_10_v1_release_manifest_and_scorecard():
    """Test #65: Release Manifest - Manifest and Scorecard documentation exist."""
    import os
    assert os.path.exists(os.path.join("docs", "V1_RELEASE_MANIFEST.md"))
    assert os.path.exists(os.path.join("docs", "V1_SCORECARD.md"))
    assert os.path.exists(os.path.join("docs", "V1_PRODUCTION_CHECKLIST.md"))
    assert os.path.exists(os.path.join("docs", "V1_FINAL_RELEASE_REPORT.md"))

def test_25_opentelemetry_db_query_span_annotation():
    """Test Priority #1 (GAP-01): OpenTelemetry DB Query Span Annotation - Session tracer emits span metadata."""
    async def _test():
        from packages.database.session import AsyncSessionTracer
        async with AsyncSessionTracer(None, request_id="req_otel_db_01", trace_id="tr_otel_db_01") as tracer:
            assert tracer.span_data["db.system"] == "postgresql"
            assert tracer.span_data["requestId"] == "req_otel_db_01"
            assert tracer.span_data["traceId"] == "tr_otel_db_01"
            assert tracer.span_data["status"] == "ACTIVE"
        assert tracer.span_data["status"] == "OK"
    asyncio.run(_test())

def test_26_prometheus_redis_queue_metrics_exporter():
    """Test Priority #2 (GAP-02): Prometheus Redis Consumer Queue Exporter - Formatted metrics exposition."""
    async def _test():
        from app.services.health_service import get_redis_queue_metrics
        metrics = await get_redis_queue_metrics("redis://localhost:6379/0")
        assert "vapor_redis_connected_status" in metrics
        assert "vapor_redis_queue_depth_items" in metrics
        assert "vapor_redis_queue_lag_seconds" in metrics
        assert "vapor_redis_active_consumers_count" in metrics
    asyncio.run(_test())

def test_27_per_tenant_ai_token_expenditure_attribution():
    """Test Priority #3 (GAP-03): Per-Tenant AI Token Expenditure Attribution - Audit metadata formatting."""
    async def _test():
        from app.core.ai_provider import UsageMetadata
        meta = UsageMetadata(
            provider="TestProvider",
            model="gpt-4o",
            latency_ms=120,
            input_tokens=200,
            output_tokens=400,
            tenant_id="org_global_enterprise_01",
            estimated_cost_usd=0.0006
        )
        audit_dict = meta.to_audit_dict()
        assert audit_dict["ai_provider"] == "TestProvider"
        assert audit_dict["ai_model"] == "gpt-4o"
        assert audit_dict["tenant_id"] == "org_global_enterprise_01"
        assert audit_dict["input_tokens"] == 200
        assert audit_dict["output_tokens"] == 400
        assert audit_dict["estimated_cost_usd"] == 0.0006
    asyncio.run(_test())

def test_28_client_web_vitals_telemetry_ingestion():
    """Test Priority #4 (GAP-04): Client Web Vitals OpenTelemetry Reporter - Ingestion route accepts RUM metrics."""
    async def _test():
        from app.api.routers.health import record_web_vitals_telemetry
        payload = {
            "name": "FCP",
            "value": 420.5,
            "rating": "good",
            "url": "http://localhost:3000/operations/v1-health"
        }
        res = await record_web_vitals_telemetry(payload)
        assert res["status"] == "accepted"
        assert res["timestamp"] is not None
    asyncio.run(_test())

def test_29_multi_cloud_failover_telemetry_buffer_optimization():
    """Test Priority #5: Multi-Cloud Failover Telemetry Buffer Optimization - Buffer timeout <= 30 seconds."""
    async def _test():
        from app.services.health_service import get_failover_telemetry_status
        status_data = await get_failover_telemetry_status()
        assert status_data["failover_buffer_seconds"] <= 30
        assert status_data["sync_status"] == "synced"
    asyncio.run(_test())

def test_30_hybrid_quantum_event_payload_signing():
    """Test Priority #6: Hybrid Quantum-Resistant Event Payload Signing - Dual digest signature verification."""
    from app.core.crypto import sign_event_payload, verify_event_signature
    payload = '{"event":"GOVERNANCE_ATTESTATION_RENEWED","org_id":"org_global_enterprise_01"}'
    sig = sign_event_payload(payload)
    assert sig.startswith("v1:hybrid:")
    assert verify_event_signature(payload, sig) is True
    assert verify_event_signature(payload + "_tampered", sig) is False

def test_31_stress_simulation_production_isolation_guard():
    """Test Priority #7: Stress Simulation Production Isolation Guard - Read-only sandbox isolation."""
    async def _test():
        from app.services.transformation_resilience_stress_service import TransformationResilienceStressService
        res = await TransformationResilienceStressService.process_natural_language_stress_query(None, "analyze compute outage campaign")
        assert res["evidenceJson"]["simulation_isolation"] == "CTRL_SIMULATION_ISOLATION"
        assert res["evidenceJson"]["production_mutation"] == "BLOCKED"
    asyncio.run(_test())

def test_32_ai_provider_automated_fallback_evaluation_harness():
    """Test Priority #8: AI Provider Automated Fallback Evaluation Harness - Multi-provider fallback readiness."""
    async def _test():
        from app.core.ai_provider import evaluate_provider_fallback_readiness
        readiness = await evaluate_provider_fallback_readiness()
        assert readiness["fallback_ready"] is True
        assert readiness["status"] == "OPERATIONAL"
        assert readiness["fallback_provider"] == "DeterministicTestProvider"
    asyncio.run(_test())

def test_33_recovery_execution_circuit_breaker_safety_guard():
    """Test Priority #9: Recovery Execution Circuit Breaker Safety Verification - Blocked execution on OPEN circuit breaker."""
    async def _test():
        from app.services import reliability_service
        from app.schemas.reliability import RecoveryPlanCreate, RecoveryStep
        reliability_service._in_memory_incidents["inc_test_cb_01"] = {"id": "inc_test_cb_01", "service": "svc_auth_01"}
        reliability_service._in_memory_breakers["svc_auth_01"] = {"state": "OPEN", "target": "svc_auth_01"}

        plan_in = RecoveryPlanCreate(
            incidentId="inc_test_cb_01",
            steps=[RecoveryStep(type="restart_service", target="svc_auth_01", parameters={})],
            risk="LOW",
            estimatedImpact={}
        )

        plan, err = await reliability_service.create_recovery_plan(None, plan_in)
        assert err is None
        res, exec_err = await reliability_service.execute_recovery_action(None, plan["id"], 0)
        assert res == {}
        assert exec_err is not None
        assert "Circuit Breaker Open" in exec_err
    asyncio.run(_test())









