# VAPOR OS — SECURITY AUTHORIZATION MATRIX

**Document Status:** P0 ARCHITECTURE HARDENED & ENFORCED  
**Security Boundary Model:** Zero-Trust (Strict JWT/Session Token + Server-Side Workspace Membership & RBAC Enforcement)  
**Authoritative Identity Source:** Verified cryptographic session token (`Bearer <jwt>` or HttpOnly `vapor_session_token` cookie) mapped to database-backed Workspace Membership records. Raw client headers (`X-User-Id`, `X-Workspace-Id`, `X-User-Role`) are **strictly non-authoritative** and cannot authenticate or escalate privileges.

---

## 1. Global Authentication & RBAC Policy Rules

| Role Level | Hierarchy & Privileges | Permitted Endpoints |
|---|---|---|
| **Anonymous / Unauthenticated** | No access to workspace resources or control plane. | `/api/v1/auth/login`, `/api/v1/auth/google`, `/api/v1/auth/session`, `/api/v1/health` |
| **Viewer** | Read-only tenant-scoped access. Cannot create/modify/delete workspace resources. | GET `/api/v1/missions`, GET `/api/v1/memories`, GET `/api/v1/content`, GET `/api/v1/deliverables`, GET `/api/v1/knowledge`, GET `/api/v1/graph` |
| **Member** | Standard workspace contributor. Can create and execute missions, workflows, memories, and tools within authorized workspace. | All Viewer endpoints + POST/PATCH on workspace entities (`/missions`, `/memories`, `/workflows`, `/deliverables`, `/integrations/actions/execute`) |
| **Admin** | Workspace Administrator. Can manage members, invite users, update roles, manage IAM policies, configure IdP, and execute control-plane governance actions. | All Member endpoints + `/api/v1/admin/*`, `/api/v1/workspaces/{id}/invitations`, `/api/v1/workspaces/{id}/members/{uid}/*`, `/api/v1/policies/rules` (write), `/api/v1/evaluations/*`, `/api/v1/scim/v2/*` |
| **Owner** | Workspace Creator / Sole Owner. Full administrative authority + workspace deletion & ownership transfer. | All Admin endpoints + Workspace Ownership Management |

---

## 2. Complete Router Authorization Matrix (101 Routers)

| Router / Prefix | Authentication Dependency | Authorization Level | Tenant Isolation Check | CSRF Protection |
|---|---|---|---|---|
| `auth.py` (`/api/v1/auth`) | Optional for login/session; `get_current_user` for token refresh/logout | Public / Authenticated | N/A | Origin / Referer Checked |
| `admin_agents.py` (`/api/v1/admin/agents`) | `Depends(require_admin)` | **Admin / Owner** | `ws_ctx.workspace_id` scoped | Origin / Referer Checked |
| `governance.py` (`/api/v1/admin`) | `Depends(require_admin)` | **Admin / Owner** | `ws_ctx.workspace_id` scoped | Origin / Referer Checked |
| `identity.py` (`/api/v1/admin/identity`) | `Depends(require_admin)` | **Admin / Owner** | `ws_ctx.workspace_id` scoped | Origin / Referer Checked |
| `scim.py` (`/api/v1/scim/v2`) | `Depends(require_admin)` | **Admin / Owner** | `ws_ctx.workspace_id` scoped | Origin / Referer Checked |
| `evaluations.py` (`/api/v1/evaluations`) | `Depends(require_admin)` | **Admin / Owner** | Suite / Run Tenant Scoped | Origin / Referer Checked |
| `workspace.py` (`/api/v1/workspaces`) | `get_current_workspace` (read) / `require_admin` (mutate) | **Member** (read) / **Admin** (write) | Path `id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `missions.py` (`/api/v1/missions`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `memories.py` (`/api/v1/memories`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `content.py` (`/api/v1/content`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `deliverables.py` (`/api/v1/deliverables`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `drive.py` (`/api/v1/drive`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `gmail.py` (`/api/v1/gmail`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `calendar.py` (`/api/v1/calendar`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `search.py` (`/api/v1/search`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `home.py` (`/api/v1/home`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `attention.py` (`/api/v1/attention`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `agent_runs.py` (`/api/v1/agent-runs`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `agent_mesh.py` (`/api/v1/agents`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `agent_runtime_v2.py` (`/api/v1/agents/executions`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `automations.py` (`/api/v1/automations`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `capability_registry.py` (`/api/v1/capabilities`) | `get_current_workspace` (read) / `require_admin` (register/approve) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `decision_engine.py` (`/api/v1/decisions`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `decision_intelligence.py` (`/api/v1/intelligence`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `delegations.py` (`/api/v1/delegations`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `enterprise_evaluation.py` (`/api/v1/ai/evaluation`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `events.py` (`/api/v1/events`) | `get_current_workspace` (read) / `require_admin` (replay/subscribe) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `finops.py` (`/api/v1/finops`, `/api/v1/usage`, `/api/v1/budgets`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `governance_v2.py` (`/api/v1/governance`) | `get_current_workspace` (read) / `require_admin` (create/breakglass) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `graph.py` (`/api/v1/graph`) | `get_current_workspace` (read) / `require_admin` (approve) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `integrations.py` (`/api/v1/integrations`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `knowledge.py` (`/api/v1/knowledge`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `knowledge_governance.py` (`/api/v1/knowledge/governance`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `learning_fabric.py` (`/api/v1/memory`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `mission_orchestration.py` (`/api/v1/missions`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `model_gateway.py` (`/api/v1/ai`) | `get_current_workspace` (infer/stream) / `require_admin` (enable/disable) | **Member** (infer) / **Admin** (manage) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `operations.py` (`/api/v1/operations`) | `get_current_workspace` (read) / `require_admin` (approve/reject) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `policies.py` (`/api/v1/policies`) | `get_current_workspace` (eval) / `require_admin` (create rule) | **Member** (eval) / **Admin** (create) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `skill_fabric.py` (`/api/v1/agents/skills`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `workflow_ai.py` (`/api/v1/workflows/ai`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `workflow_optimization.py` (`/api/v1/workflows/{id}/optimization`) | `get_current_workspace` (read) / `require_admin` (approve/publish/rollback) | **Member** (read) / **Admin** (write) | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| `workflows.py` (`/api/v1/workflows`) | `Depends(get_current_workspace)` | **Member** | `Model.workspace_id == ws_ctx.workspace_id` | Origin / Referer Checked |
| 42 Transformation Intelligence Routers (`transformation_*.py`) | `Depends(get_current_user)` / `Depends(get_current_workspace)` | **Member** | Tenant-Scoped Database Query Filter | Origin / Referer Checked |

---

## 3. Defense Mechanisms & Residual Risk Posture

1. **Header-Based Forgery Defeated:** All raw header parameters (`X-User-Id`, `X-Workspace-Id`, `X-User-Role`) stripped and replaced with cryptographically signed token claims validated against database tenant memberships.
2. **Tenant Boundary Enforcement:** All workspace entity queries explicitly filter with `where(Model.workspace_id == ws_ctx.workspace_id)`. Cross-workspace attempts return `403 Forbidden` or `404 Not Found`.
3. **Privilege Escalation Neutralization:** Admin and Owner endpoints enforce `ws_ctx.role in ["admin", "owner"]`. Self-escalation via PATCH `/workspaces/{id}/members/{uid}/role` is strictly prohibited.
4. **CSRF & CORS Hardening:** Wildcard origins with credentials eliminated. `CSRFProtectionMiddleware` rejects non-allowlisted `Origin` or `Referer` headers on state-mutating HTTP methods (`POST`, `PUT`, `PATCH`, `DELETE`).
5. **Fail-Fast Secret Key Entropy:** At application startup, `validate_production_secrets()` checks `SECRET_KEY` length (>= 32 bytes) and rejects default/insecure keys in staging/production.
