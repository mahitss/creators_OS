# V1.0 Service Dependency Map

## Enterprise Service Inventory

| Service / Subsystem | Purpose | Criticality | Failure Behavior | Health Endpoint | Observability | Owner |
|---|---|---|---|---|---|---|
| **FastAPI Core Gateway** | REST API Routing & Auth | CRITICAL | Fail-closed | `/health` | Prometheus / OpenTelemetry | Platform SRE Lead |
| **PostgreSQL Database** | Persistent Domain Storage | CRITICAL | Graceful error response | `/health` | DB Query Latency / Connection Pool | Database Architect |
| **Event Mesh (Async Mesh)** | Event Publication & Sub | HIGH | Queue fallback / Retry | `/health` | Event Lag / Dead-Letter Queue | Event Mesh Lead |
| **Digital Twin Engine** | Counterfactual Simulation | MEDIUM | Sandbox isolation | `/api/v1/transformation-resilience-digital-twin/status` | Simulation Execution Latency | Digital Twin Architect |
| **Stress Testing Engine** | Continuous Stress Testing | MEDIUM | Read-only simulation fallback | `/api/v1/transformation-resilience-stress/status` | Stress Run Latency | Stress Testing Lead |
| **Resilience Optimization** | Multi-Objective Strategy | MEDIUM | Read-only strategy fallback | `/api/v1/transformation-resilience-optimization/status` | Optimization Latency | Optimization Lead |
| **Resilience Learning** | Outcome Calibration | MEDIUM | Governed proposal queue | `/api/v1/transformation-resilience-learning/status` | Calibration Lag | Learning Architect |
| **Resilience Governance** | Assurance & Readiness | CRITICAL | Fail-safe readiness verdict | `/api/v1/transformation-resilience-governance/status` | Control Attestation Coverage | Governance Architect |
