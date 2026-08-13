# V1.0 Incident Response Runbook

## Incident Lifecycle & Severity Classification
- **SEV-1 (Critical)**: Tenant isolation breach, data corruption, or total API outage. Response time < 15 minutes.
- **SEV-2 (High)**: Major service degradation or failed release gate. Response time < 1 hour.
- **SEV-3 (Moderate)**: Minor telemetry latency or documentation gap. Response time < 24 hours.

## Containment & Rollback Procedure
1. Identify correlation ID and affected service module.
2. Trigger automated calibration/configuration rollback (`rollback_calibration_change` or PolicyEngine release gate block).
3. Notify Incident Commander and log immutable audit event.
