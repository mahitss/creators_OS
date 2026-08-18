# Vapor OS — Google Authentication & OpenID Connect Setup Guide

This guide describes how to configure Google Identity Services (GIS) / OpenID Connect authentication for Vapor OS in both development and production environments.

---

## 1. Architecture Overview

```
Browser (User)
      │
      ▼
1. Google Sign-In (GIS / OIDC)
      │
      ▼ Google ID Token
2. POST /api/v1/auth/google/verify
      │
      ▼ Cryptographic verification of 'iss', 'aud', 'exp', and 'sub'
3. Identity Resolution / JIT Provisioning (User + ExternalIdentity + Workspace)
      │
      ▼
4. VAPOR Application Session Issued (HMAC-SHA256 JWT in HttpOnly Cookie)
      │
      ▼
5. Protected VAPOR APIs & Workspace Isolation
```

> [!IMPORTANT]
> **Decoupled Identity Policy**: Basic Google Sign-In requests **only identity claims** (`sub`, `email`, `name`, `picture`). It does **not** request Gmail, Google Drive, or Google Calendar OAuth scopes. Data access integrations require explicit incremental user consent via `Settings > Integrations`.

---

## 2. Google Cloud Console Configuration

### Step A: Create or Select a Google Cloud Project
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project named `Vapor OS Production` (or select an existing project).

### Step B: Configure the OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**.
2. Select User Type: **Internal** (for workspace organizations) or **External** (for public SaaS).
3. Fill in the App Information:
   - **App name**: `Vapor OS`
   - **User support email**: `support@yourdomain.com`
   - **Developer contact information**: `admin@yourdomain.com`
4. Scopes:
   - Select only standard OpenID Connect scopes: `openid`, `https://www.googleapis.com/auth/userinfo.email`, `https://www.googleapis.com/auth/userinfo.profile`.

### Step C: Create OAuth 2.0 Web Application Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Select Application type: **Web application**.
4. Set **Authorized JavaScript origins**:
   - Development: `http://localhost:3000`, `http://127.0.0.1:3000`
   - Production: `https://your-vapor-domain.com`
5. Set **Authorized redirect URIs**:
   - Development: `http://localhost:3000/login`
   - Production: `https://your-vapor-domain.com/login`
6. Click **Create** and copy your **Client ID** and **Client Secret**.

---

## 3. Environment Variable Configuration

Add the following environment variables to your `.env` file (server-side only):

```env
# Google Identity & OpenID Connect
GOOGLE_CLIENT_ID=xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_REDIRECT_URI=http://localhost:3000/login

# Frontend Public Google Client ID
NEXT_PUBLIC_GOOGLE_CLIENT_ID=xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com

# Core Security
SECRET_KEY=generate_a_random_32_byte_secure_string_for_production_jwt
ENVIRONMENT=production
```

> [!CAUTION]
> Never expose `GOOGLE_CLIENT_SECRET` in frontend files or commit it to source control. Only `NEXT_PUBLIC_GOOGLE_CLIENT_ID` is exposed to the browser for GIS button rendering.

---

## 4. Verification & Testing Checklist

- [x] **Zero-Trust Token Validation**: Server verifies issuer (`accounts.google.com`), expiration, audience, and subject claims.
- [x] **Immutable Identity Key**: Google's `sub` claim is used as the unique external provider identifier.
- [x] **Workspace Isolation**: Each user is bound to their provisioned or invited workspace memberships.
- [x] **Secure Cookies**: Session tokens are issued in `HttpOnly`, `SameSite=Lax`, `Secure` (in production) cookies.
- [x] **Route Protection**: Unauthenticated requests to private routes are redirected to `/login`.
- [x] **Session Revocation**: Calling `POST /api/v1/auth/logout` clears the session cookie and terminates access.
