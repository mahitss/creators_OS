# V1.0 Observability Gaps Specification

## Summary of Telemetry & Instrumentation Gaps

| Gap ID | Subsystem / Area | Missing Telemetry | Operational Impact | Recommended Instrumentation | Priority |
|---|---|---|---|---|---|
| **GAP-01** | Distributed Tracing | Sub-millisecond spans for internal DB query steps | Low visibility into micro-second query execution variations | OpenTelemetry trace span annotation on SQLAlchemy async session wrappers | **P3** |
| **GAP-02** | Event Mesh | Real-time queue depth histogram breakdown by consumer group | Delayed detection of slow consumer workers under extreme spikes | Prometheus histogram metrics exporter for Redis queue depth | **P3** |
| **GAP-03** | AI Provider Router | Token expenditure tracking per individual tenant | Cost attribution requires manual log parsing | Add structured `token_usage` JSON metadata to audit logs | **P3** |

---

*Note: All telemetry enhancement recommendations are cataloged for post-V1 roadmap consideration. No unnecessary telemetry changes will be introduced during V1.0 operations.*
