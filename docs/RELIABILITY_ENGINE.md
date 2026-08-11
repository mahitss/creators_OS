# Reliability Engine Architecture

## Reliability Pipeline
```
TELEMETRY → HEALTH SIGNAL → INCIDENT → DIAGNOSIS → RECOVERY PLAN → POLICY CHECK → SAFE REMEDIATION → VERIFICATION → RESOLUTION
```

## Controlled Bounds & Safeguards
- **Max Recovery Chain Depth**: Bounded recovery loop protection (`max_recovery_depth <= 5`).
- **Idempotency**: Remediation keys `recoveryId:incidentId:target` guarantee safe execution retries.
