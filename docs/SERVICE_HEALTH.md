# Service Health Telemetry & Evidence Modeling

## Evidence-Backed Health Status
Status is strictly determined from actual telemetry signals (`healthy`, `degraded`, `warning`, `critical`). Opaque numeric health scores (e.g. `Vapor Health = 87`) are explicitly prohibited.

## Subsystem Health Sources
- `ReliabilityEngine`: Active incidents and circuit breaker states.
- `EventMesh`: Throughput (EPS), P95 Latency, Consumer Lag, DLQ Count.
- `IntegrationFabric`: Provider status and connection error rates.
- `FinOps`: Budget thresholds and cost anomaly signals.
- `DataSecurity`: DLP blocks and policy denial events.
