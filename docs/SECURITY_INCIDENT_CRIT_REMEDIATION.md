# Vapor OS — Security Incident & Critical Vulnerability Remediation Report

**Classification**: HIGH-SEVERITY SECURITY REMEDIATION  
**Incident Reference**: VAPOR-SEC-2026-CRIT-01/02/03  
**Status**: REMEDIATED & VERIFIED  
**Date**: August 2026  

---

## 1. Incident Overview

During independent security auditing, three critical security vulnerabilities were confirmed in the Vapor OS Core Kernel:

1. **CRIT-01: Header-Based Administrative Authentication Bypass** (`apps/api/app/api/routers/admin_agents.py`)
2. **CRIT-02: Unauthenticated Passkey Token Forgery** (`apps/api/app/api/routers/auth.py`)
3. **CRIT-03: Permissive CORS Wildcard with Credentials** (`apps/api/app/main.py`)

---

## 2. Deep Root-Cause Analysis & Remediation Specifications

### CRIT-01: Header-Based Admin Authentication Bypass
- **Affected File**: `apps/api/app/api/routers/admin_agents.py`
- **Affected Endpoints**: `GET /api/v1/admin/agents/overview`, `POST /api/v1/admin/agents/action`, `GET /api/v1/admin/agents/runs`
- **Root Cause**: `enforce_admin_authorization` fell back to trusting unverified `X-User-Id` and `X-Workspace-Id` HTTP headers and performed substring checks (`"admin" in user_id_lower`) rather than requiring a cryptographically signed session token and database membership lookup.
- **Attack Path**: An attacker sent `GET /api/v1/admin/agents/overview` with headers `X-User-Id: usr_admin_01` and `X-Workspace-Id: ws_default_01` without providing an `Authorization` Bearer token or session cookie. The endpoint returned `HTTP 200 OK` with sensitive agent telemetry.
- **Remediation**:
  - Replaced `enforce_admin_authorization` with standard `require_admin` and `get_current_user` FastAPI dependencies.
  - Stripped all header-based authentication fallbacks.
  - Required valid HMAC-SHA256 JWT tokens with verified `role: "admin"` or database-backed `WorkspaceMembership`.

---

### CRIT-02: Unauthenticated Passkey Token Forgery
- **Affected File**: `apps/api/app/api/routers/auth.py`
- **Affected Endpoint**: `POST /api/v1/auth/passkey/verify`
- **Root Cause**: When a passkey verification request was submitted without an active server-issued challenge, the code executed an `else:` branch that dynamically synthesized a `user_id`, assigned `role: "admin"` if `"admin"` appeared in the email string, and signed an authenticated JWT session token.
- **Attack Path**: An attacker sent `POST /api/v1/auth/passkey/verify` with `{"email": "admin@target.com", "credential_id": "12345678"}`. The server returned a valid session token granting administrative privileges.
- **Remediation**:
  - Eliminated the unauthenticated fallback `else:` block completely.
  - Required an active, unexpired challenge in `_pending_challenges` for the requested email.
  - Required matching challenge verification and registered credential validation.
  - Sourced user roles strictly from persisted workspace membership rather than email string matching.

---

### CRIT-03: Permissive CORS Wildcard with Credentials
- **Affected File**: `apps/api/app/main.py`
- **Affected Endpoints**: Global API Middleware Stack
- **Root Cause**: Duplicate middleware configuration blocks at lines 214 and 350 initialized `CORSMiddleware` with `allow_origins=["*"]` and `allow_credentials=True`.
- **Attack Path**: A malicious website (`https://attacker.example`) executed cross-origin `fetch` requests with `credentials: 'include'` to read authenticated API responses and leak user data.
- **Remediation**:
  - Removed duplicate `CORSMiddleware` blocks.
  - Enforced strict origin whitelisting using `settings.CORS_ORIGINS` (`http://localhost:3000`, `http://127.0.0.1:3000`, `https://vapor.os`).
  - Wildcard `*` with credentials permanently blocked.

---

## 3. Regression Test Coverage

Automated security regression tests implemented in `apps/api/tests/test_critical_security_remediation.py`:
1. `test_admin_requires_authenticated_session`
2. `test_admin_headers_cannot_authenticate`
3. `test_admin_headers_cannot_escalate_member`
4. `test_workspace_header_cannot_change_tenant`
5. `test_passkey_requires_challenge`
6. `test_passkey_invalid_signature_rejected`
7. `test_passkey_wrong_origin_rejected`
8. `test_passkey_wrong_rp_id_rejected`
9. `test_passkey_unknown_credential_rejected`
10. `test_email_cannot_assign_admin_role`
11. `test_cors_rejects_untrusted_origin`
12. `test_cors_allows_configured_origin`
