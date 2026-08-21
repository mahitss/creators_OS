# KINETIQ — System Architecture Specification

## 1. System Overview

KINETIQ is a production-grade enterprise AI operating system and resilience control plane. It integrates real-time telemetry, model routing, autonomous agent execution, multi-tenant isolation, and continuous governance assurance into a single unified platform.

```
+-----------------------------------------------------------------------+
|                         KINETIQ WEB INTERFACE                         |
|   (Next.js 14 App Router / Matte Black Command Center / 60 FPS Canvas) |
+-----------------------------------------------------------------------+
                                   |
                     HTTP / JSON / Server-Sent Events
                                   |
+-----------------------------------------------------------------------+
|                         FASTAPI CORE KERNEL                           |
|  - SecurityHeadersMiddleware (CSP, HSTS, X-Frame-Options: DENY)        |
|  - AuthenticationEnforcementMiddleware (Fail-closed JWT/Cookie verify)|
|  - CSRFProtectionMiddleware (Double-submit token protection)          |
|  - RateLimitMiddleware (Sliding-window request governor)              |
|  - RequestLoggingMiddleware (X-Request-Id tracing & telemetry)        |
+-----------------------------------------------------------------------+
       |                           |                          |
+---------------+          +---------------+          +---------------+
|  AI GATEWAY   |          |  EVENT MESH   |          | DATABASE TIER |
| OpenRouter    |          | Redis Pub/Sub |          | Neon Postgres |
| Model Router  |          | Async Queues  |          | SQLAlchemy 2  |
| Fallbacks     |          | Event Outbox  |          | Tenant Scoped |
+---------------+          +---------------+          +---------------+
```

---

## 2. Layer Separation & Domain Boundaries

1. **UI Layer (`apps/web`)**: Next.js 14 App Router, Server Components for layouts, Client Components for dynamic controls, Lucide icons, `@vapor/ui` tokens.
2. **API & Routing Layer (`apps/api/app/api/routers`)**: 101 domain routers validating request schemas and enforcing server-side identity context.
3. **Authorization & Security (`apps/api/app/dependencies/auth.py`)**: Centralized RBAC primitives (`require_role`, `authorize`, `require_admin`, `require_owner`) and workspace tenant boundaries.
4. **Service Layer (`apps/api/app/services`)**: Business logic, DAG execution, context compaction, policy enforcement, and audit event generation.
5. **Database & Persistence Layer (`packages/database`)**: Neon PostgreSQL connection pooler, SQLAlchemy declarative models with UUID primary keys and composite indices.

---

## 3. Subsystem Specifications

- **AI Gateway**: Provider-agnostic model routing with automatic fallback to `openrouter/free` on model unavailability (404/503), token usage accounting, and rate limiting.
- **Agent Runtime**: Goal-directed DAG execution with explicit capability allowlists and execution budgets.
- **Multi-Tenancy**: Organization -> Workspace -> Member hierarchy with strict query isolation by `workspace_id`.
