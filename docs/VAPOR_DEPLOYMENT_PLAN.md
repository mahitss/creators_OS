# Vapor OS — Production Deployment & Rollback Plan (v1.0.0-live)

**Version**: `v1.0.0-live`  
**Date**: 2026-08-13  
**Status**: **RELEASE_READY**  
**Environment**: Production (`prod-us-east-1`)  

---

## 1. Pre-Deployment Verification Checklist
- [x] Monorepo typecheck clean across 6 packages (`pnpm typecheck`).
- [x] Pytest suite 100% passing (321 / 321 assertions across 24 test modules).
- [x] Git working tree clean on `main` (`origin/main` commit `7924e14`).
- [x] Environment secrets and database configuration verified.

---

## 2. Deployment Sequence
1. **Prepare Artifacts**: Build production Docker container images for API and Web services (`docker build -t vapor/api:v1.0.0-live .`).
2. **Database Health Check**: Verify async PostgreSQL connection pool availability and read/write latency (< 10ms).
3. **Deploy Worker Nodes**: Rolling restart of Redis background worker pods.
4. **Deploy API Services**: Blue/Green deployment of FastAPI backend service pods.
5. **Deploy Frontend Web Apps**: Deploy Next.js / Vite web application assets (`vapor-web`).
6. **Prometheus Scraping**: Confirm `/metrics` endpoint active.

---

## 3. Production Smoke Tests
- **Endpoint `GET /health`**: Assert status 200 OK.
- **Endpoint `GET /metrics`**: Assert Prometheus metrics stream output.
- **Endpoint `POST /telemetry/web-vitals`**: Assert HTTP 200 receipt of RUM payload.
- **Tenant Isolation Attestation**: Call `attest_federated_policy_sync()` and verify `sync_status == "ATT_SYNCHRONIZED"`.
- **Quantum Signing Attestation**: Verify dual-digest signature generation (`v1:hybrid:`).

---

## 4. Post-Deployment Observability Period
Monitor for 60 minutes following deployment:
- HTTP API p99 latency (< 50ms)
- Database query latency p99 (< 10ms)
- Redis worker queue depth (< 10 messages)
- Error log count (0 unhandled exceptions)

---

## 5. Rollback Plan & Trigger Criteria

### Trigger Criteria
- Unhandled HTTP 5xx error rate > 0.05% over 5 consecutive minutes.
- API p99 latency > 250ms over 5 consecutive minutes.
- Confirmed security or tenant boundary alert.

### Rollback Procedure
1. **Traffic Shift**: Revert load balancer router rules to Blue (previous stable build).
2. **Container Rollback**: Redeploy previous Docker container tag (`vapor/api:v0.9.9`).
3. **Database State**: No database rollback required (zero schema migrations were applied in this release).
4. **Post-Rollback Verification**: Run smoke test suite to confirm operational stability.
