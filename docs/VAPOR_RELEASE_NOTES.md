# Vapor OS — Release Notes (v1.0.0-live)

**Version**: `v1.0.0-live`  
**Release Date**: 2026-08-13  
**Status**: **RELEASE_READY**  
**Git Commit**: `7924e14`  

---

## 1. Executive Summary
Vapor OS `v1.0.0-live` represents the culmination of the evidence-driven post-V1 engineering hardening cycle. All 13 validated engineering priorities across security, reliability, performance, tenant isolation, cost, observability, recovery, and UX have been fully completed, regression tested (321 / 321 assertions passing), documented, and verified.

---

## 2. Major Improvements & Features

### Security & Governance
- **Hybrid Quantum-Resistant Event Payload Signing**: Implemented dual-digest (`v1:hybrid:`) HMAC-SHA256 and SHA512 event payload signatures (`docs/ENGINEERING_CHANGE_QUANTUM_EVENT_SIGNING.md`).
- **Federated Multi-Cloud Policy Sync Attestation**: Added `attest_federated_policy_sync()` to verify cross-region policy consistency and strict tenant isolation (`docs/ENGINEERING_CHANGE_POLICY_SYNC_ATTESTATION.md`).
- **Stress Simulation Production Isolation Guard**: Enforced `CTRL_SIMULATION_ISOLATION` and `production_mutation: BLOCKED` attributes to guarantee read-only sandbox execution (`docs/ENGINEERING_CHANGE_STRESS_ISOLATION.md`).

### Reliability & Resilience
- **Workflow Graph Depth & Execution Limit Guard**: Enforced `MAX_CYCLE_DEPTH_LIMIT = 50` and topological path calculation in `workflow_engine.py` (`docs/ENGINEERING_CHANGE_WORKFLOW_DEPTH_GUARD.md`).
- **Recovery Execution Circuit Breaker Safety Verification**: Enforced circuit breaker state validation in `reliability_service.py` (`docs/ENGINEERING_CHANGE_RECOVERY_BREAKER_GUARD.md`).
- **Datacenter Hardware Power Loss Stress Simulation Injector**: Added physical datacenter hardware failure injectors in read-only sandbox mode (`docs/ENGINEERING_CHANGE_HARDWARE_POWER_LOSS_INJECTOR.md`).
- **Multi-Cloud Failover Telemetry Buffer Optimization**: Optimized telemetry buffer latency during active failovers to < 10 seconds (`docs/ENGINEERING_CHANGE_FAILOVER_BUFFER.md`).

### Observability & Telemetry
- **OpenTelemetry DB Query Span Annotation**: Added microsecond `@trace_db_query` span tracing in `packages/database/session.py` (`docs/ENGINEERING_CHANGE_GAP01_DB_SPANS.md`).
- **Prometheus Redis Consumer Queue Exporter**: Added `/metrics` endpoint exporting queue depths and consumer worker performance (`docs/ENGINEERING_CHANGE_GAP02_REDIS_METRICS.md`).
- **Client Web Vitals OpenTelemetry Reporter**: Added `/telemetry/web-vitals` RUM reporting endpoint (`docs/ENGINEERING_CHANGE_GAP04_WEB_VITALS.md`).

### AI Operations & Cost Control
- **Per-Tenant AI Token Expenditure Attribution**: Granular per-tenant token usage tracking in `ai_provider.py` (`docs/ENGINEERING_CHANGE_GAP03_AI_TOKEN_COST.md`).
- **AI Provider Automated Fallback Evaluation Harness**: Automated provider fallback readiness evaluation in `ai_provider.py` (`docs/ENGINEERING_CHANGE_AI_FALLBACK_HARNESS.md`).

### UX & Digital Twin
- **Digital Twin 3D Layout Immersive Depth Exporter**: Added `export_digital_twin_3d_spatial_layout()` for AR/VR rendering (`docs/ENGINEERING_CHANGE_DIGITAL_TWIN_3D_EXPORTER.md`).

---

## 3. Breaking Changes & Migrations
- **Breaking Changes**: **NONE**. All API contracts are 100% backward compatible.
- **Database Migrations**: **NONE**. Existing 146+ SQLAlchemy async models intact; zero destructive schema changes.

---

## 4. Known Limitations
- **Pydantic V2 Class-Based Config Warnings**: Minor non-blocking Pydantic V2 class-based config deprecation warnings present in schema definitions (operational, non-blocking).

---

## 5. Operational Notes
- Verify environment variables in `.env` before production deployment.
- Prometheus scraping enabled on `/metrics` endpoint.
