# Post-V1 Backlog (Validated Roadmap Candidates)

## Deferred Non-Critical Features & Roadmap Candidates

| Category | Problem / Opportunity | Empirical Evidence | Impact | Priority | Estimated Complexity |
|---|---|---|---|---|---|
| **BUG** | None | 0 active production bugs | None | — | — |
| **RELIABILITY** | Cloud Failover Telemetry Buffer | 5-minute latency buffer permitted during active failover | Reduces failover telemetry latency to < 10 seconds | **P3** | Low (Config tweak) |
| **SECURITY** | Quantum-Resistant Event Signing | Standard HMAC-SHA256 signatures active | Future-proofs event mesh against post-quantum attacks | **P3** | Medium |
| **PERFORMANCE** | OpenTelemetry DB Query Spans (GAP-01) | Sub-millisecond DB query step details require manual trace logging | Improves micro-second query bottleneck diagnostics | **P3** | Low |
| **UX** | Real-Time AR/VR Digital Twin Visualization | 2D desktop workspace shell (`/transformation-resilience-digital-twin`) active | Immersive 3D/VR dependency visualization | **P3** | High |
| **COST** | Per-Tenant AI Token Usage Attribution (GAP-03) | Token usage currently parsed via audit log strings | Enables automated tenant cost reporting | **P3** | Low |
| **FEATURE** | Hardware-Level Physical Failure Injectors | Software failure injection engine active (Sprint 106) | Simulates physical rack/datacenter hardware power loss | **P3** | High |
| **ARCHITECTURE** | Global Multi-Cloud Resilience Mesh 3.0 | Cross-region failover active via primary region heartbeat | Federated cross-tenant policy synchronization | **P3** | High |

---

*Note: All items in this backlog are non-blocking P3 candidates. Feature freeze remains active for V1.0 Operations.*
