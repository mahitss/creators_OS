# VAPOR OS — COMPLETE PLATFORM DOCUMENTATION & OPERATING MANUAL

---

## 1. Executive Summary & Platform Architecture

**Vapor OS** is an enterprise-grade autonomous operating system designed for executive intelligence, agentic workflow orchestration, proactive context synthesis, zero-trust governance, and transformation resilience. 

```mermaid
graph TD
    User([Executive / Operator]) -->|Browser HTTPS / WSS| WebClient[Next.js 14 Frontend AppShell]
    WebClient -->|/api/v1/* Proxy Rewrites| FastAPICore[FastAPI Core Kernel API :8000]
    
    subgraph "Core Kernel Subsystems"
        FastAPICore --> ContextEngine[Unified Context Engine]
        FastAPICore --> AgentRuntime[Agent Runtime 2.0 & Mesh]
        FastAPICore --> PolicyEngine[Policy Engine & Action Gateway]
        FastAPICore --> DecisionEngine[Decision Intelligence & Learning]
        FastAPICore --> ResilienceEngine[Resilience & Digital Twin]
    end
    
    subgraph "Persistence & Telemetry"
        ContextEngine --> PostgreSQL[(PostgreSQL 16 Database)]
        AgentRuntime --> Redis[(Redis 7 Cache & Event Broker)]
        FastAPICore --> OTel[OpenTelemetry & Prometheus Metrics]
    end
```

### Architectural Highlights
- **Frontend**: Next.js 14.2 (App Router + Pages Router hybrid support), React 18, TailwindCSS, Lucide Icons, unified 55-route enterprise `AppShell`.
- **Backend Kernel**: Python 3.12+ / FastAPI with 94 modular routers, Pydantic v2 schemas, and asynchronous connection pools.
- **Context & Storage**: PostgreSQL (SQLAlchemy 2.0 asyncpg), Redis caching/event streaming, OpenTelemetry query span instrumentation.
- **Multi-Tenant Security**: Dynamic tenant isolation via `X-Workspace-Id` and `X-User-Id` headers with DLP secret redaction and policy-based action enforcement.

---

## 2. Getting Started & Quickstart Guide

### 2.1 Prerequisites
- **Node.js**: `v20.x` or higher
- **pnpm**: `v9.x` or higher
- **Python**: `3.11+` / `3.12+` with `uvicorn` and `pytest`
- **PostgreSQL & Redis**: (Local daemon or Docker Compose)

### 2.2 Environment Configuration (`.env`)
Create a `.env` file at the repository root:
```env
# Application Environment
ENVIRONMENT=development
NODE_ENV=development
LOG_LEVEL=info

# Web Client Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# FastAPI Core Kernel Configuration
PORT=8000
HOST=0.0.0.0
SECRET_KEY=dev_vapor_secret_key_minimum_32_characters_long_for_hs256!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Database & Cache Configuration
DATABASE_URL=postgresql+asyncpg://vapor_user:vapor_password@localhost:5432/vapor_os
REDIS_URL=redis://localhost:6379/0
```

### 2.3 Starting the Backend
```bash
# Set PYTHONPATH and launch FastAPI Uvicorn server on port 8000
$env:PYTHONPATH="apps/api;."
uvicorn app.main:app --port 8000 --host 127.0.0.1 --reload
```

### 2.4 Starting the Frontend
```bash
# In the workspace root
pnpm --filter vapor-web dev
# Frontend is now accessible at http://localhost:3000
```

### 2.5 Verifying System Health
```bash
# Verify backend kernel directly
curl http://127.0.0.1:8000/api/v1/health

# Verify via Next.js proxy
curl http://localhost:3000/api/v1/health
```

---

## 3. Core Functional Modules & Navigation Subsystems

Vapor OS provides **55 integrated operational modules** organized into four functional command pillars:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VAPOR OS APP SHELL                             │
├─────────────────────┬─────────────────────┬─────────────────┬───────────────┤
│ 1. COMMAND & BRIEF  │ 2. INTELLIGENCE &   │ 3. AUTOMATION & │ 4. RESILIENCE │
│                     │    CONTEXT          │    AGENTS       │    & OPS      │
├─────────────────────┼─────────────────────┼─────────────────┼───────────────┤
│ • Executive Brief   │ • Content Studio    │ • Automations   │ • Command Ctr │
│ • Attention Inbox   │ • Gmail Triage      │ • Workflows     │ • Control Twr │
│ • Autonomous Miss.  │ • Drive Browser     │ • AI Agent Mesh │ • Digital Twin│
│ • Work Queue        │ • Memory Vault      │ • Skill Fabric  │ • FinOps      │
│ • Strategic Intel   │ • Semantic Graph    │ • Capabilities  │ • SecOps      │
│ • Strategic Fores.  │ • Governance Hub    │ • Decision Eng. │ • Event Mesh  │
│ • Portfolio Intel   │ • AI Evaluations    │ • Prescriptive  │ • Identity SSO│
│ • Execution Gov.    │ • AI Model Gateway  │ • Predictive    │ • Data DLP    │
└─────────────────────┴─────────────────────┴─────────────────┴───────────────┘
```

### Pillar 1: Command & Briefing

1. **Executive Brief (`/`)**
   - *Purpose*: High-level situational awareness hub for leadership.
   - *Key Functions*:
     - Dynamic time-of-day greeting and contextual summary statement.
     - Metric KPI strip (Active Missions, Attention Items, Memory Growth).
     - Proactive recommendations and primary call-to-action cards.
     - Quick launch shortcuts to core operational centers.

2. **Attention Inbox (`/attention`)**
   - *Purpose*: Centralized triage center for items requiring human intervention.
   - *Key Functions*:
     - Aggregates paused/failed mission steps, unreviewed memory candidates, and deliverable approvals.
     - Severity classification (`low`, `medium`, `high`, `urgent`).
     - Auto-reconciles and auto-resolves when root blockage is cleared.

3. **Autonomous Missions (`/missions`)**
   - *Purpose*: Multi-step agentic mission planning, execution, and tracking.
   - *Key Functions*:
     - Plan decomposition into discrete DAG steps.
     - Real-time step state machine (`pending`, `in_progress`, `paused`, `completed`, `failed`).
     - Interactive execution control: Play, Pause, Retry, and Step Inspection.

4. **Work Queue (`/work`)**
   - *Purpose*: Granular operator task pipeline and active agent work allocation.
   - *Key Functions*: Task status filtering, assignment queues, deadline tracking, and blocker escalations.

5. **Strategic Intelligence (`/strategy`) & Strategic Foresight (`/foresight`)**
   - *Purpose*: Long-range strategic goal modeling, driver analysis, and scenario forecasting.
   - *Key Functions*: Strategic assumption validation, trend detection, probabilistic foresight simulations.

6. **Portfolio Intelligence (`/portfolio`) & Execution Governance (`/execution`)**
   - *Purpose*: Program portfolio tracking, resource allocation, and execution variance control.
   - *Key Functions*: Milestone gating, cross-program dependency mapping, delivery drift alerts.

7. **Operating Model & Map (`/operating-model`, `/organization`)**
   - *Purpose*: Visual topology of organizational units, teams, agents, and capability ownership.

---

### Pillar 2: Intelligence & Context

8. **Content Studio (`/content`)**
   - *Purpose*: AI-assisted document drafting, asset generation, and artifact review.
   - *Key Functions*: Markdown editing, prompt-driven generation, artifact version history, and publishing.

9. **Gmail Triage (`/gmail`) & Google Drive (`/drive`)**
   - *Purpose*: Secure integration hubs for enterprise email and document indexing.
   - *Key Functions*: Thread classification, action item extraction, semantic file indexing, and context grounding.

10. **Memory Vault & Learning Fabric (`/memory`)**
    - *Purpose*: Long-term cognitive memory repository for the agent runtime.
    - *Key Functions*:
      - Memory extraction from completed missions.
      - Human review and approval workflow for new candidate memories.
      - Category segmentation: `episodic`, `semantic`, `procedural`, `working`.

11. **Semantic Graph & Intelligence Governance (`/knowledge`, `/knowledge/graph`, `/knowledge/governance`)**
    - *Purpose*: Unified enterprise knowledge graph and context verification plane.
    - *Key Functions*: Entity-relationship graph explorer, knowledge freshness tracking, citation provenance.

12. **AI Evaluation Lab & Model Gateway (`/ai/evaluation`, `/ai/models`)**
    - *Purpose*: LLM benchmark evaluation, latency/token cost tracking, and model routing.
    - *Key Functions*: Automated evaluation test runs, regression detection, model latency comparison.

---

### Pillar 3: Automation & Agents

13. **Workflows Engine & Canvas (`/workflows`, `/workflows/optimization`)**
    - *Purpose*: Visual DAG workflow orchestrator for complex automation pipelines.
    - *Key Functions*: Visual node canvas, conditional branching, telemetry profiling, and self-optimizing loop execution.

14. **AI Agent Mesh & Skill Fabric (`/agents/mesh`, `/agents/skills`, `/capabilities`)**
    - *Purpose*: Autonomous multi-agent coordination fabric.
    - *Key Functions*:
      - Agent registry with role, status, and assigned workloads.
      - Dynamic skill loading and versioning.
      - Capability discovery, security sandbox validation, and delegation rules.

15. **Decision Engine & Intelligence (`/decisions`, `/intelligence`, `/transformation-decision-learning`)**
    - *Purpose*: Algorithmic decision support, tradeoff evaluation, and post-decision learning.
    - *Key Functions*: Decision packet generation, counterfactual simulation, outcome attribution, and regret minimization.

16. **Prescriptive & Predictive Operations (`/optimization`, `/predictions`)**
    - *Purpose*: Proactive operational forecasting and optimization levers.
    - *Key Functions*: Capacity forecasting, anomaly prediction, automated constraint-based optimization proposals.

---

### Pillar 4: Resilience, Operations & Governance

17. **Resilience Command Center & Control Tower (`/transformation-resilience-command-center`, `/transformation-control`)**
    - *Purpose*: Single pane of glass for systemic stability, transformation progress, and risk monitoring.
    - *Key Functions*: Systemic health gauge, early warning triggers, active intervention coordination.

18. **Digital Twin Simulation (`/transformation-simulation`) & War Room (`/transformation-war-room`)**
    - *Purpose*: 3D/virtual digital twin for operational stress testing and incident war room response.
    - *Key Functions*: Failure injection testing, multi-scenario simulation, live incident collaboration channel.

19. **Resilience Engineering & Recovery Engine (`/transformation-resilience-engineering`, `/transformation-recovery`)**
    - *Purpose*: Automated self-healing, state recovery, and circuit breaker governance.
    - *Key Functions*: Recovery plan execution, circuit breaker tripping, rollback orchestration.

20. **FinOps, SecOps & Enterprise Admin (`/finops`, `/security`, `/security/operations`, `/admin/governance`, `/admin/identity`, `/admin/data`, `/admin/events`, `/settings`)**
    - *Purpose*: Enterprise platform operations, cost attribution, and security enforcement.
    - *Key Functions*:
      - Cloud & AI token spend attribution.
      - Real-time incident response and security containment.
      - SCIM 2.0 provisioning and SAML/OIDC SSO configuration.
      - Regex-based Data Loss Prevention (DLP) redaction.
      - Distributed Event Mesh tracking.

---

## 4. API & Integration Reference

All client-to-server requests are routed through Next.js proxy rewrites to the FastAPI Core Kernel at `/api/v1/*`.

### 4.1 Authentication & Multi-Tenant Headers
Every API request must include workspace and user context headers:
```http
X-Workspace-Id: ws_default_01
X-User-Id: usr_alex
Authorization: Bearer <jwt_token>
```

### 4.2 Core API Endpoints

#### 1. System Health Probes
- **`GET /api/v1/health`** (or root **`GET /health`**)
  - *Response*:
    ```json
    {
      "status": "healthy",
      "version": "1.0.0",
      "environment": "development",
      "services": { "database": true, "redis": true },
      "timestamp": "2026-08-17T15:54:34.125736+00:00",
      "details": {
        "database_engine": "postgresql+asyncpg",
        "caching_engine": "redis",
        "ai_provider": "deterministic_mock_provider"
      }
    }
    ```

#### 2. Executive Brief
- **`GET /api/v1/home/brief?user_name=Alex`**
  - *Parameters*: `user_name` (optional, string)
  - *Response*: `ExecutiveBriefResponse` containing greeting, metrics, quick actions, and attention summary.

#### 3. Attention Center
- **`GET /api/v1/attention/count`**
  - *Response*: `{"open_count": 0}`
- **`GET /api/v1/attention`**
  - *Response*: `{"items": [], "total": 0, "open_count": 0}`
- **`POST /api/v1/attention/{id}/resolve`**
  - *Response*: `{"status": "resolved"}`

#### 4. Missions Orchestrator
- **`GET /api/v1/missions`**
  - *Response*: `{"missions": [], "total": 0}`
- **`POST /api/v1/missions`**
  - *Payload*: `{"title": "string", "description": "string", "goal": "string"}`
- **`GET /api/v1/missions/{id}`**
  - *Response*: Full mission DAG, steps, and execution status.

#### 5. Real User Monitoring (RUM) Telemetry
- **`POST /api/v1/telemetry/web-vitals`**
  - *Payload*:
    ```json
    {
      "name": "LCP",
      "value": 1200,
      "rating": "good",
      "delta": 1200,
      "id": "vitals_1723910000_abcde",
      "timestamp": 1723910000000,
      "url": "http://localhost:3000/"
    }
    ```
  - *Response*: `{"status": "accepted", "timestamp": "2026-08-17T15:52:26.551324+00:00"}`

#### 6. Global Search
- **`GET /api/v1/search?q={query}`**
  - *Response*: Unified search results across missions, memories, deliverables, and knowledge nodes.

---

## 5. Verification & Testing Playbook

### 5.1 Backend Test Suite (Pytest)
```bash
$env:PYTHONPATH="apps/api;."
pytest apps/api/tests -q
# Result: 643 passed across 94 test modules
```

### 5.2 Frontend Test Suite (Vitest)
```bash
pnpm --filter vapor-web test
# Result: 20/20 passed across 13 test files
```

### 5.3 Live E2E Acceptance Suite
```bash
# Exercises all 55 navigation routes, 10 redirects, custom 404, and API proxy endpoints
node apps/web/test-e2e-acceptance.js
# Result: 79/79 passed
```

### 5.4 Production Build Smoke Test
```bash
pnpm --filter vapor-web build
# Result: 95/95 static and server-rendered pages built successfully
```

---

## 6. Troubleshooting & Operational FAQs

1. **Proxy Returns HTTP 500 in Development / Production**
   - *Cause*: `apps/web/next.config.js` backend origin could not resolve host (e.g. `vapor-api`).
   - *Resolution*: Ensure `API_PROXY_TARGET` or `API_INTERNAL_URL` is set, or defaults to `http://127.0.0.1:8000`.

2. **Database Health Check Shows `database: false`**
   - *Cause*: PostgreSQL is not running on port 5432 or credentials in `.env` are invalid.
   - *Resolution*: Start PostgreSQL daemon or update `DATABASE_URL` in `.env`.

3. **Frontend Shows Error State on Navigation**
   - *Behavior*: Vapor OS frontend components truthfully display the diagnostic error state when backend connectivity is lost, rather than masking failures with empty data.
   - *Resolution*: Ensure FastAPI backend process is running on port 8000 and click **Retry Connection**.
