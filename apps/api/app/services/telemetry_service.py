import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

_in_memory_telemetry: List[dict] = []

def record_ai_telemetry(
    operation: str, # mission_planning, mission_execution, memory_extraction, memory_retrieval, executive_brief, deliverable_analysis, content_generation
    provider: str = "mock_ai_provider",
    model: str = "gpt-4o",
    latency_ms: float = 120.0,
    input_tokens: int = 150,
    output_tokens: int = 350,
    success: bool = True,
    failure_category: str = "none", # provider_unavailable, timeout, rate_limit, authentication, invalid_response, schema_validation, context_limit, internal_error, none
    request_id: Optional[str] = None
) -> dict:
    telemetry_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    total_tokens = input_tokens + output_tokens
    estimated_cost = round((input_tokens * 0.000005) + (output_tokens * 0.000015), 6)

    record = {
        "id": telemetry_id,
        "request_id": request_id,
        "operation": operation,
        "provider": provider,
        "model": model,
        "latency_ms": round(latency_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": estimated_cost,
        "success": success,
        "failure_category": failure_category,
        "timestamp": now_iso
    }

    _in_memory_telemetry.append(record)
    return record

def get_telemetry_records(limit: int = 50) -> List[dict]:
    return sorted(_in_memory_telemetry, key=lambda x: x["timestamp"], reverse=True)[:limit]

def get_telemetry_summary() -> Dict[str, Any]:
    if not _in_memory_telemetry:
        return {
            "total_requests": 0,
            "success_rate": 1.0,
            "avg_latency_ms": 0.0,
            "total_tokens": 0,
            "total_cost": 0.0
        }

    total = len(_in_memory_telemetry)
    successes = sum(1 for r in _in_memory_telemetry if r["success"])
    total_tokens = sum(r["total_tokens"] for r in _in_memory_telemetry)
    total_cost = sum(r["estimated_cost"] for r in _in_memory_telemetry)
    avg_latency = sum(r["latency_ms"] for r in _in_memory_telemetry) / total

    return {
        "total_requests": total,
        "success_rate": round(successes / total, 4),
        "avg_latency_ms": round(avg_latency, 2),
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 6)
    }
