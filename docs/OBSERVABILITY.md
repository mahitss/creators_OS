# Vapor OS — Observability Architecture

## 1. Structured Logging
Vapor OS uses structured JSON logging across API endpoints and background workers.
Every log line includes:
- `timestamp`: ISO 8601 UTC string
- `level`: `INFO` | `WARN` | `ERROR`
- `service`: `vapor-api`
- `environment`: Runtime environment (`development`, `staging`, `production`)
- `requestId`: Correlated UUID header
- `method`, `path`, `status_code`, `duration_ms`

## 2. Request Correlation
Incoming HTTP requests receive or generate an `X-Request-ID` header.
This ID is:
- Attached to `request.state.request_id`
- Returned in HTTP response header `X-Request-ID`
- Included in structured exception responses and backend logs

## 3. Health & Diagnostic Probes
- `GET /api/v1/health`: Detailed health report covering database, caching, and AI providers.
- `GET /api/v1/liveness`: Process liveness check returning `HTTP 200 OK`.
- `GET /api/v1/readiness`: Operational readiness check verifying DB connection.
