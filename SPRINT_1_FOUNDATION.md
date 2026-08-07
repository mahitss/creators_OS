# Vapor OS — Sprint 1: Foundation Technical Specification

**Authored by**: Founding Engineering Team (CTO, Principal Frontend, Principal Backend, AI Systems, DevOps, Staff Designer)  
**Objective**: Build the production-grade platform foundation upon which all future Vapor OS features will be constructed.

---

## SECTION 1: Project Setup & Repository Structure

### 1.1 Monorepo Architecture
Vapor OS uses a Turborepo-managed monorepo structure with strict package boundaries.

```
vapor-os/
├── apps/
│   ├── desktop-shell/        # Tauri + Next.js 14 App Router desktop client
│   └── api-server/           # FastAPI Python core backend server
├── packages/
│   ├── ui/                   # Design system components & tokens
│   ├── core-types/           # Shared TypeScript interfaces & JSON schemas
│   ├── ai-sdk/               # Model abstraction & streaming client
│   ├── db-schema/            # Prisma / Drizzle DB schema & migrations
│   └── config/               # Shared ESLint, Prettier, TS configs
├── .github/workflows/        # CI/CD test, lint, and build pipelines
├── docker/                   # Development & sandbox container configs
├── scripts/                  # Seed scripts & dev environment tooling
└── docs/                     # API specs & architecture decision records
```

---

## SECTION 2: Technology Stack & Rationale

| Layer | Chosen Technology | Rationale |
| :--- | :--- | :--- |
| **Desktop Shell** | **Tauri 2.0 + Next.js 14** | Native OS integration with $< 15\text{MB}$ bundle size and $< 80\text{MB}$ RAM usage. |
| **Backend API** | **FastAPI (Python 3.11)** | High-async performance, native Pydantic v2 validation, and AI/ML SDK compatibility. |
| **Database** | **PostgreSQL 16 + pgvector** | Battle-tested relational engine with vector similarity search. |
| **ORM** | **Prisma / Drizzle** | Type-safe query generation with automated migration tracking. |
| **Auth** | **NextAuth v5 / Passkey API** | Native WebAuthn passkey support, JWT session encryption. |
| **Realtime Engine** | **WebSockets + NATS PubSub** | Sub-16ms latency streaming for live PTY terminal outputs. |
| **AI Layer** | **Vercel AI SDK + Custom Router** | Multi-provider fallback streaming (Gemini Pro, Claude 3.5, OpenAI). |
| **Caching** | **Redis 7 (KeyDB)** | In-memory key-value store for session tokens, rate limits, and AST caches. |

---

## SECTION 3: Design System Foundation

* **Typography**: Primary font *Inter*, Monospace font *JetBrains Mono*. Tabular lining figures enabled (`tabular-nums`).
* **Colors**: Base Dark (`#090A0F`), Panel (`#12141C`), Emerald Pulse (`#10B981`), Cyan Pulse (`#06B6D4`).
* **Grid & Breakpoints**: Strict 8pt spatial grid ($4\text{px}, 8\text{px}, 16\text{px}, 24\text{px}, 32\text{px}$). Breakpoints: `sm`: 768px, `md`: 1024px, `lg`: 1280px.

---

## SECTION 4: Authentication Architecture

* **Modes**: Passkey / WebAuthn + OAuth2 (GitHub/Google) + Local Sovereign Key.
* **Sessions**: Encrypted HTTP-only cookies containing short-lived JWTs (15-min expiration) with sliding refresh.
* **RBAC**: `OWNER`, `MEMBER`, `READONLY` capability scope bindings.

---

## SECTION 5: Initial Database Schema (PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    owner_id UUID REFERENCES users(id) ON DELETE RESTRICT
);

CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    root_path TEXT NOT NULL
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);
```

---

## SECTION 6: API Contracts

* `GET /api/v1/health`: Health status payload.
* `POST /api/v1/auth/passkey/register`: Initiates WebAuthn passkey registration.
* `GET /api/v1/workspaces`: Lists user accessible workspaces.

---

## SECTION 7: AI Infrastructure Layer

* **Abstraction**: Unified `streamCompletion()` API.
* **Prompt Management**: Versioned handlebars templates in `/packages/ai-sdk/prompts/`.
* **Fallback Router**: Auto-switches from Gemini Pro to Claude 3.5 Sonnet within $250\text{ms}$ on rate limit (HTTP 429).

---

## SECTION 8: Developer Experience & Tooling

* **ESLint & Prettier**: Strict TypeScript rules, single quotes, 2 spaces, trailing commas.
* **Husky & Commitlint**: Enforces Conventional Commits (`feat:`, `fix:`, `docs:`).
* **CI/CD Pipeline**: GitHub Actions running typechecks, Vitest unit tests, and Playwright E2E suites.

---

## SECTION 9: Testing & Quality Assurance

* **Vitest**: Unit test suite targeting $> 80\%$ statement coverage.
* **Playwright**: E2E test suite asserting auth flows, workspace folder binding, and proposal authorization.
* **Accessibility**: `@axe-core/playwright` asserting 0 high/critical WCAG violations.

---

## SECTION 10: Sprint 1 Milestones & Deliverables

1. **M1**: Monorepo Setup & Turborepo Config
2. **M2**: Database Schema & Auth Pipeline
3. **M3**: Core API Contracts & Health Endpoints
4. **M4**: Design System Tokens & Base UI Components
5. **M5**: AI Model Router & Streaming Client
6. **M6**: CI/CD Pipelines & E2E Testing Suite
