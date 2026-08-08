import sys
from pathlib import Path

# Ensure apps/api is in Python path
api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.services import telemetry_service, ai_eval_service
from app.core import prompt_registry

client = TestClient(app)

def test_request_correlation_and_headers():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert "X-Request-ID" in res.headers
    assert "X-Process-Time-Ms" in res.headers

def test_health_liveness_readiness_probes():
    # 1. /health
    h_res = client.get("/api/v1/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] in ["healthy", "degraded"]

    # 2. /liveness
    l_res = client.get("/api/v1/liveness")
    assert l_res.status_code == 200
    assert l_res.json()["status"] == "alive"

    # 3. /readiness
    r_res = client.get("/api/v1/readiness")
    assert r_res.status_code == 200
    assert r_res.json()["status"] == "ready"

def test_telemetry_recording_and_privacy():
    rec = telemetry_service.record_ai_telemetry(
        operation="mission_planning",
        provider="mock_ai_provider",
        latency_ms=150.0,
        input_tokens=100,
        output_tokens=200,
        success=True
    )
    assert rec["operation"] == "mission_planning"
    assert rec["total_tokens"] == 300
    assert "prompt" not in rec # Strict Privacy: prompt text not stored in telemetry

    summary = telemetry_service.get_telemetry_summary()
    assert summary["total_requests"] > 0
    assert summary["success_rate"] == 1.0

def test_prompt_registry_active_retrieval():
    prompt = prompt_registry.get_active_prompt("mission_planning")
    assert prompt is not None
    assert prompt["version"] == "1.0.0"
    assert prompt["active_flag"] is True

def test_ai_evaluation_contract_suite():
    sample_plan_output = {
        "goal": "Build Docker Container",
        "summary": "Step by step dockerization.",
        "steps": [
            {"order": 1, "title": "Write Dockerfile"},
            {"order": 2, "title": "Build Image"}
        ],
        "deliverables": ["Dockerfile"]
    }
    result = ai_eval_service.evaluate_ai_output("mission_planning", sample_plan_output)
    assert result["passed"] is True
    assert result["score"] == 1.0
