# Vapor OS — Production Operations Runbook & SRE Guide

**Version**: `v1.0.1-patch`  
**Environment**: Production (`prod-us-east-1`)  
**Maintained By**: Platform Engineering & SRE Team  
**Engineering State**: **ENGINEERING_FREEZE ACTIVE (ROADMAP EXHAUSTED)**  

---

## 1. Operating SLOs & Service Targets

| Dimension | Target SLO | Current Production Baseline | Alert Threshold (Trigger Pager) |
|---|---|---|---|
| **Service Availability** | $\ge 99.9\%$ | **100.0%** | $< 99.9\%$ over 5 min |
| **HTTP 5xx Error Rate** | $< 0.01\%$ | **0.00%** | $\ge 0.05\%$ over 5 min |
| **API Latency (p50)** | $< 25\text{ms}$ | **13.8ms** | $> 50\text{ms}$ over 10 min |
| **API Latency (p95)** | $< 100\text{ms}$ | **37.9ms** | $> 150\text{ms}$ over 5 min |
| **API Latency (p99)** | $< 250\text{ms}$ | **44.8ms** | $> 350\text{ms}$ over 5 min |
| **Database Latency (p99)** | $< 15\text{ms}$ | **7.8ms** | $> 25\text{ms}$ over 5 min |
| **DB Pool Utilization** | $< 50\%$ | **12.1%** | $> 75\%$ for $> 3\text{ min}$ |
| **Redis Cache Hit Ratio** | $> 85\%$ | **94.8%** | $< 70\%$ over 15 min |
| **Worker Queue Depth** | $< 50$ | **0.0** | $> 100$ queued for $> 2\text{ min}$ |
| **Frontend Web Vitals (LCP)** | $< 2.5\text{s}$ | **1.11s** | $> 3.5\text{s}$ p90 over 15 min |
| **AI Provider Fallback Latency** | $< 1000\text{ms}$ | **418ms** | $> 2000\text{ms}$ TTFT |
| **AI Provider Failures** | $< 0.1\%$ | **0.00%** | $\ge 1.0\%$ over 5 min |
| **Tenant Isolation Boundary** | 100% Strict | **100% Strict (`ATT_SYNCHRONIZED`)** | Any cross-tenant access attempt (Immediate P1) |
| **DLP Secret Redaction** | 100% Masked | **100% Masked** | Any unmasked credential detected (Immediate P1) |
| **Failover RTO** | $< 60\text{s}$ | **$\le 30\text{s}$** | $> 60\text{s}$ during failover event |

---

## 2. Standard Health Check & Inspection Procedures

### 2.1 API & System Health
```bash
# Verify API Gateway liveness & readiness
curl -f http://localhost:8000/health
curl -f http://localhost:8000/health/liveness
curl -f http://localhost:8000/health/readiness

# Check Prometheus Telemetry & Redis Queue Metrics
curl -s http://localhost:8000/metrics | grep redis_queue
```

### 2.2 Automated Test Suite Verification
```bash
# Run core test suite with PYTHONPATH set
powershell -Command "$env:PYTHONPATH='apps/api'; python -m pytest apps/api/tests"
```

### 2.3 Monorepo Workspace Verification
```bash
# Run typechecks across all 6 packages
pnpm typecheck
```

---

## 3. Incident Severity Levels & Response Protocols

```
┌──────────┬──────────────────────────────────────────┬──────────────┬────────────────────────────┐
│ Severity │ Definition                               │ Response SLA │ Lead Incident Commander    │
├──────────┼──────────────────────────────────────────┼──────────────┼────────────────────────────┤
│ P1       │ Critical outage, tenant boundary breach, │ < 15 minutes │ Principal SRE + Security   │
│          │ DLP leak, or global data corruption      │              │ Lead                       │
│ P2       │ Degraded performance (p95 > 150ms), AI   │ < 1 hour     │ On-Call Platform Engineer  │
│          │ primary failover, or worker backlog > 100│              │                            │
│ P3       │ Non-blocking telemetry gap, minor UI bug │ Next Business│ SRE Maintenance Queue      │
│          │ or transient warning                     │ Day          │                            │
└──────────┴──────────────────────────────────────────┴──────────────┴────────────────────────────┘
```

### Response Lifecycle:
1. **Detection**: Prometheus alert triggers PagerDuty / alertmanager webhook.
2. **Triage**: Incident Commander assesses impact, isolates blast radius, and establishes incident war room.
3. **Containment**: Apply circuit breaker isolation, trigger multi-cloud failover, or enable read-only emergency mode.
4. **Recovery / Rollback**: Execute targeted runbook playbook or rollback to verified commit baseline (`a520501`).
5. **Communication**: Update internal status dashboard and notify affected enterprise tenant administrators.
6. **Post-Incident Review (PIR)**: Complete blameless retrospective within 48 hours; log evidence before creating any remediation action.

---

## 4. Operational Troubleshooting Playbooks

### Playbook 1: Database Latency Spike or Connection Exhaustion
1. **Symptom**: DB latency p99 $> 25\text{ms}$ or pool utilization $> 75\%$.
2. **Diagnosis**: Check active queries in PostgreSQL pg_stat_activity and OpenTelemetry DB span traces (`@trace_db_query`).
3. **Mitigation**:
   - Check connection pool metrics via `/health`.
   - Terminate rogue unindexed long-running read transactions.
   - If cluster degraded, initiate failover to warm read-replica or secondary region.

### Playbook 2: Redis Failure or Queue Backlog
1. **Symptom**: Queue depth $> 100$ or Prometheus metric `redis_consumer_queue_lag_seconds` $> 30\text{s}$.
2. **Diagnosis**: Check worker node memory and CPU utilization.
3. **Mitigation**:
   - Scale async worker pods from $N$ to $2N$.
   - If Redis node unreachable, Redis sentinel/cluster automatically elects new master; verify workers reconnect within 5 seconds.

### Playbook 3: AI Provider Failure & Fallback Recovery
1. **Symptom**: Primary AI provider returns 502/504 or error rate $> 1.0\%$.
2. **Action**: The automated fallback harness (`ai_provider.py`) automatically routes requests to the secondary model provider.
3. **Verification**: Inspect `/telemetry/ai-usage` to confirm failover traffic routing and assert zero dropped client sessions.

### Playbook 4: Cross-Tenant Isolation or DLP Security Alert
1. **Symptom**: PolicyEngine alert `ATT_SYNC_MISMATCH` or DLP secret detection alert.
2. **Action (IMMEDIATE)**:
   - Revoke affected session tokens immediately via Redis revocation blocklist.
   - Force policy sync attestation: `attest_federated_policy_sync()`.
   - Isolate affected tenant workspace to read-only mode until security audit verifies containment.

### Playbook 5: Production Rollback Procedure
If a breaking deployment occurs:
```bash
# 1. Roll back to last verified stable commit
git checkout a520501

# 2. Verify test suite
powershell -Command "$env:PYTHONPATH='apps/api'; python -m pytest apps/api/tests/test_pydantic_v2_modernization.py apps/api/tests/test_health.py"

# 3. Deploy container images tagged with commit a520501
```

---

## 5. Change Management & Governance Policy

$$\mathbf{CORE \quad OPERATIONAL \quad PRINCIPLE: \quad NO \quad EVIDENCE \implies NO \quad ENGINEERING \quad WORK}$$

### Rules for Opening New Engineering Cycles:
1. **Engineering Work is ONLY Justified When**:
   - A confirmed P1/P2 production security incident occurs.
   - Production telemetry breaches documented SLO thresholds (e.g. API p95 $> 100\text{ms}$ over sustained window).
   - An explicit, validated business or product management requirement is formally approved.
2. **Required Artifacts for Any Change**:
   - Pre-implementation baseline telemetry.
   - `docs/ENGINEERING_CHANGE_<name>.md` detailing root cause, scope, and regression test plan.
   - Verified rollback procedure.
   - Post-deployment 60-minute stability audit.

---

## 6. V1.1 Engineering Gate Status

```
CURRENT EVIDENCE-BACKED V1.1 CANDIDATES: 0 (ROADMAP EXHAUSTED)
ENGINEERING FREEZE                      : ACTIVE
```

No speculative features, architectural refactoring, microservice decoupling, or database migrations are permitted without empirical production justification.
