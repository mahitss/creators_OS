# V1.0 Production Baseline Specification

**Application Release Version**: `1.0.0`  
**Git Tag**: `v1.0.0-live`  
**Git Commit Hash**: `7e93986`  
**Database Schema Version**: `v2.0-sprint110`  
**Deployment Environment**: Production (`prod-us-east-1`)  
**Baseline Date**: 2026-08-13  

---

## 1. Workspaces & Core Services

| Workspace / Package | Package Name | Baseline Version | Runtime / Framework |
|---|---|---|---|
| **Root Workspace** | `vapor` | `1.0.0` | Node.js v20+ / Turbo v1.13 |
| **Web Frontend** | `vapor-web` | `1.0.0` | Next.js 14.1 / React 18.2 |
| **API Core Gateway** | `apps/api` | `1.0.0` | Python 3.13.5 / FastAPI 0.110 |
| **Database Models** | `@vapor/database` | `1.0.0` | SQLAlchemy 2.0 Async / AsyncPG |
| **AI Provider Router** | `@vapor/ai` | `1.0.0` | TypeScript Workspace Package |
| **TypeScript Types** | `@vapor/types` | `1.0.0` | TypeScript 5.4 |
| **UI Components** | `@vapor/ui` | `1.0.0` | Tailwind CSS / Lucide React |
| **Shared Utilities** | `@vapor/utils` | `1.0.0` | TypeScript Workspace Package |

---

## 2. Active Feature Flags

| Feature Flag Key | Purpose | Active Value | Environment |
|---|---|---|---|
| `DLP_ENFORCEMENT_ENABLED` | Redacts sensitive credentials & PII | `true` | Production |
| `CTRL_SIMULATION_ISOLATION` | Restricts Digital Twin & Stress runs to read-only sandboxes | `true` | Production |
| `AGENT_GOVERNANCE_STRICT` | Blocks subagents from approving releases / risk | `true` | Production |
| `POLICY_ENGINE_FAIL_CLOSED` | Ensures release gates default to review on failure | `true` | Production |
| `AUDIT_LOG_IMMUTABLE` | Mandates append-only DB audit persistence | `true` | Production |

---

## 3. Database & Event Schemas
- **Database Engine**: PostgreSQL 16 with AsyncPG driver. 146+ domain models defined in `packages/database/models.py`.
- **Event Mesh**: Redis Cluster 7.2 with pub/sub event channels (`events.py`) and durable queue consumers.
