# KINETIQ — Security Architecture & Threat Model

## 1. Zero Trust Security Architecture

KINETIQ implements an enterprise Zero-Trust architecture adhering to NIST 800-207 guidelines.

### 1.1 Authentication & Identity Boundaries
- **JWT & Session Cookie Verification**: All protected `/api/v1` routes require verified JWT bearer tokens or HttpOnly session cookies (`vapor_session_token`).
- **Server-Side Identity Verification**: Client headers (`X-User-Id`, `X-User-Role`) are never trusted. Identity is derived strictly from cryptographic token verification and server-side database records.
- **Fail-Closed Enforcement**: Any unauthenticated request or expired token receives an immediate HTTP 401 Unauthorized response without executing business logic.

### 1.2 Enterprise Authorization (RBAC)
- **Roles**: `OWNER`, `ADMIN`, `OPERATOR`, `ANALYST`, `VIEWER`.
- **Permissions**: `READ`, `CREATE`, `UPDATE`, `DELETE`, `EXECUTE`, `ADMINISTER`.
- **Enforcement Primitives**:
  ```python
  @router.post("/execute")
  async def execute_action(
      ctx: AuthenticatedContext = Depends(authorize("EXECUTE", "mission_engine"))
  ):
      ...
  ```

### 1.3 Tenant Isolation
- Every database query enforces tenant scoping (`workspace_id`).
- Switching to a workspace where the user lacks active membership returns HTTP 403 Forbidden.

### 1.4 Attack Surface Hardening
- **CSP**: `default-src 'self'`.
- **HSTS**: `max-age=31536000; includeSubDomains; preload`.
- **X-Frame-Options**: `DENY`.
- **CSRF**: Double-submit cookie verification on all mutating requests (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Rate Limiting**: Sliding-window limiter (300 requests/minute per client IP / tenant).
