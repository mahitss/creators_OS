# V1.0 Architecture Decisions Record

## Architectural Boundary & Modification Policy

### 1. IMMUTABLE ARCHITECTURE (Must NOT Change)
- **FastAPI Core Kernel Gateway**: Standardized error schema (`format_v1_api_error`), request correlation ID pass-through (`requestId`, `traceId`, `correlationId`).
- **PostgreSQL SQLAlchemy 2.0 Async Engine**: 146+ async models in `packages/database/models.py`. Foreign key integrity, unique indexes, soft deletion.
- **Multi-Tenant Boundary Filtering**: `caller_org_id == "org_global_enterprise_01"`; cross-organization requests return `DENY`.
- **Simulation Read-Only Isolation**: `CTRL_SIMULATION_ISOLATION` guardrail keeping Digital Twin, Stress Testing, and Optimization projections strictly read-only.
- **Subagent Governance Enforcer**: `TransformationResilienceGovernanceService.enforce_agent_governance` blocking subagents from approving releases or accepting risk.

### 2. AREAS FOR FUTURE TELEMETRY IMPROVEMENT
- Addition of OpenTelemetry query span annotations on SQLAlchemy session wrappers (GAP-01).
- Prometheus Redis consumer queue depth histogram metrics exporter (GAP-02).

### 3. WHAT SHOULD BE SIMPLIFIED
- Streamlining 90-day human control attestation renewal reminders.

### 4. FUTURE ARCHITECTURAL INVESTIGATIONS
- Global Multi-Cloud Resilience Mesh 3.0 (Post-V1 backlog candidate).
