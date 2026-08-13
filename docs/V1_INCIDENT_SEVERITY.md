# V1.0 Incident Severity Classification & SLA Specification

## Incident Severity Level Definitions

| Severity | Definition & Operational Impact | Response SLA | Resolution Target | Escalation Requirement |
|---|---|---|---|---|
| **SEV-0** | **Critical Outage / Security Breach**: Total system outage, active tenant data leakage, production data corruption, or uncontained agent mutation. | **< 5 Minutes** | **< 1 Hour** | Immediate VP / Executive Lead Page |
| **SEV-1** | **Major Service Degradation**: Critical feature domain unavailable (e.g. Governance or Command Center down), p95 latency > 2,000ms, or AI provider outage without fallback. | **< 15 Minutes** | **< 4 Hours** | Principal Architect & SRE Lead |
| **SEV-2** | **Minor Functional Issue**: Non-critical workspace component failure, transient rate-limit spikes, or isolated UI rendering bug with workaround. | **< 1 Hour** | **< 24 Hours** | Staff Engineer & Feature Owner |
| **SEV-3** | **Low Impact / Cosmetic**: Minor visual glitch, documentation discrepancy, or background telemetry delay without operational impairment. | **< 24 Hours** | **< 72 Hours** | On-Call Engineer |

---

## Production Incident Containment Workflow
1. **DETECT**: Alert triggered or customer report logged via telemetry stream.
2. **CONTAIN**: Isolate affected service, initiate circuit breaker, or invoke feature flag override.
3. **DIAGNOSE**: Inspect structured JSON logs via `requestId` / `traceId` correlation.
4. **REMEDIATE**: Apply hotfix via pull request or execute documented rollback (`rollback_calibration_change` / container revert).
5. **VERIFY**: Confirm resolution with automated smoke tests.
6. **POST-MORTEM**: Document root cause, timeline, and preventive actions in `docs/V1_INCIDENT_LOG.md`.
