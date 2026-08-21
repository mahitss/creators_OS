# KINETIQ — Core API Specification

## 1. Overview & Base URL
- **API Version**: `v1`
- **Base URL**: `/api/v1`
- **Protocol**: HTTP/1.1 and HTTP/2 over TLS 1.3
- **Format**: JSON (Request & Response)

---

## 2. Global Request & Response Headers

### Request Headers
- `Authorization`: `Bearer <jwt_token>` (or session cookie `vapor_session_token`)
- `X-Workspace-Id`: `<workspace_uuid>` (Optional workspace selector, verified against memberships)
- `X-CSRF-Token`: Double-submit CSRF token on mutating requests

### Response Headers
- `X-Request-Id`: Unique UUID for distributed request tracing
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Remaining request allowance

---

## 3. Core Route Taxonomy

| Subsystem | Prefix | Description | Auth Level |
|---|---|---|---|
| **Health** | `/health`, `/api/v1/health` | System health check (PostgreSQL, Redis, AI gateway) | Public |
| **Auth** | `/api/v1/auth` | Login, logout, session verification, passkeys, Google OAuth | Public / Authenticated |
| **Home** | `/api/v1/home` | Executive brief, needs attention, recent activity, system telemetry | Authenticated |
| **Missions** | `/api/v1/missions` | Mission planning, DAG orchestrator, step execution | Authenticated |
| **Model Gateway** | `/api/v1/model-gateway` | Model routing, inference execution, policy check | Authenticated |
| **Memories** | `/api/v1/memories` | Long-term memory vault, episodic recall, semantic embeddings | Authenticated |
| **Governance** | `/api/v1/governance` | Policy rules, zero-trust enforcement, DLP controls | Admin / Operator |
| **FinOps** | `/api/v1/finops` | AI token accounting, cost attribution, budget forecasting | Analyst / Admin |
| **SecOps** | `/api/v1/secops` | Threat intelligence, incident response, vulnerability telemetry | Admin / SecOps |

---

## 4. Standardized Error Response

```json
{
  "error_code": "RESOURCE_NOT_FOUND",
  "message": "The requested mission was not found in the target workspace.",
  "request_id": "req_8f1c8b3a",
  "path": "/api/v1/missions/mis_12345",
  "details": null
}
```
