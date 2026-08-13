# Next Engineering Priorities (Top Evidence-Backed Priorities)

## Evidence-Backed Engineering Priority List (Top 5 Priorities)

### 1. OpenTelemetry Database Query Span Annotation (GAP-01) [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_GAP01_DB_SPANS.md`)
- **Problem**: Sub-millisecond internal DB query step details require manual trace logging.
- **Evidence**: `docs/V1_OBSERVABILITY_GAPS.md` GAP-01.
- **Impact**: Improves micro-second query bottleneck diagnostics.
- **Risk**: Low (Pure telemetry wrapper).
- **Complexity**: Low.
- **Expected Benefit**: Complete trace context across complex async DB transactions.
- **Priority**: **P3**


### 2. Prometheus Redis Consumer Queue Exporter (GAP-02) [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_GAP02_REDIS_METRICS.md`)
- **Problem**: Consumer group queue depth histograms currently sampled via background polling.
- **Evidence**: `docs/V1_OBSERVABILITY_GAPS.md` GAP-02.
- **Impact**: Enhances event queue burst detection.
- **Risk**: Low.
- **Complexity**: Low.
- **Expected Benefit**: Real-time queue lag metrics in Prometheus/Grafana.
- **Priority**: **P3**


### 3. Per-Tenant AI Token Expenditure Attribution (GAP-03) [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_GAP03_AI_TOKEN_COST.md`)
- **Problem**: Token usage is currently parsed from structured audit log strings.
- **Evidence**: `docs/V1_OBSERVABILITY_GAPS.md` GAP-03.
- **Impact**: Enables automated per-tenant AI cost breakdown.
- **Risk**: Low.
- **Complexity**: Low.
- **Expected Benefit**: Precise cloud financial reporting per tenant workspace.
- **Priority**: **P3**


### 4. Client Web Vitals OpenTelemetry Reporter (GAP-04) [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_GAP04_WEB_VITALS.md`)
- **Problem**: Client-side rendering timing depends on server-side gateway telemetry.
- **Evidence**: `docs/V1_MONTH1_OBSERVABILITY_GAPS.md` GAP-04.
- **Impact**: Provides end-to-end user web performance visibility.
- **Risk**: Low.
- **Complexity**: Low.
- **Expected Benefit**: Precise Real User Monitoring (RUM) for Next.js desktop workspace.
- **Priority**: **P3**


### 5. Multi-Cloud Failover Telemetry Buffer Optimization [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_FAILOVER_BUFFER.md`)
- **Problem**: Temporary 5-minute latency buffer permitted during secondary region failover.
- **Evidence**: `docs/V1_RELIABILITY_ROADMAP.md` & `docs/NEXT_ENGINEERING_PRIORITIES.md`.
- **Impact**: Reduces secondary region failover telemetry synchronization delay from 300s to 30s.
- **Risk**: Low.
- **Complexity**: Low.
- **Expected Benefit**: Fast secondary region failover telemetry synchronization.
- **Priority**: **P3**


### 6. Hybrid Quantum-Resistant Event Payload Signing (SECURITY) [COMPLETED]
- **Status**: **COMPLETED & VERIFIED** (See `docs/ENGINEERING_CHANGE_QUANTUM_EVENT_SIGNING.md`)
- **Problem**: Standard single-hash signatures lack post-quantum hybrid dual-digest verification.
- **Evidence**: `docs/POST_V1_BACKLOG.md` Security Category.
- **Impact**: Provides post-quantum event payload authentication integrity.
- **Risk**: Low.
- **Complexity**: Medium.
- **Expected Benefit**: Quantum-safe event signature validation.
- **Priority**: **P3**

