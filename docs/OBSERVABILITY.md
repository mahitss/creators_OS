# KINETIQ — Observability & Real Telemetry Architecture

## 1. Observability Principles

1. **Zero Synthetic Telemetry**: No simulated CPU spikes, fake latencies, or hardcoded metrics.
2. **Distributed Tracing**: `X-Request-Id` propagated across middleware, API routers, database queries, and AI model invocations.
3. **Structured Logging**: JSON log records with timestamps, log levels, request paths, user identities, and execution latencies.

---

## 2. Core Metrics Tracked

| Metric | Subsystem | Unit | Collection Method |
|---|---|---|---|
| `db_query_duration_ms` | PostgreSQL Tier | Milliseconds | Query timing wrapper / engine listener |
| `ai_inference_latency_ms` | Model Gateway | Milliseconds | `OpenRouterClient` request stopwatch |
| `ai_token_usage_total` | Model Gateway | Count | API response token metadata |
| `ai_cost_usd_total` | FinOps Engine | USD | Model rate calculation per token |
| `mission_execution_duration_s` | Orchestrator | Seconds | Task start/completion timestamp delta |
| `http_request_duration_ms` | FastAPI Core | Milliseconds | `RequestLoggingMiddleware` |

---

## 3. Health & Readiness Probes

- **Liveness**: `GET /health` -> Returns `200 OK` if the core web process is responsive.
- **Readiness**: `GET /api/v1/health` -> Probes PostgreSQL connection pool, Redis cache ping, and OpenRouter client readiness.
