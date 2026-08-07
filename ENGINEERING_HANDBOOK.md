# Vapor OS — Founding Engineering Handbook

**Authored by**: Founding CTO, Vapor  
**Target Audience**: Every Software Engineer, AI Engineer, and Infrastructure Contributor to Vapor OS.  
**Policy**: Mandatory reading before opening your first pull request.

---

## SECTION 1: Engineering Philosophy

### 1.1 How We Think
* **Simplicity over Cleverness**: We favor clean, predictable, and maintainable code over complex abstractions. If a junior engineer cannot understand a module in 10 minutes, it is over-engineered.
* **Deterministic First, Stochastic Second**: AI outputs are stochastic; system plumbing must be 100% deterministic. Never rely on an LLM to do what a type checker, state machine, or SQL constraint can guarantee.
* **Sub-100ms Mental Model**: Every system boundary must be designed for sub-100ms responsiveness. Latency is a bug.

### 1.2 How We Make Decisions
1. **Measure Before Refactoring**: Never optimize based on intuition. Benchmark memory, CPU, and network payloads using empirical traces.
2. **Blast Radius Minimization**: Every design decision must isolate failures. If the AI worker node crashes, the desktop shell must remain responsive.
3. **Reversible Decisions**: Prefer architecture that allows easy rollbacks (feature flags, clean DB schema migrations, decoupled micro-packages).

### 1.3 How We Review Code
* **PR Size Budget**: Maximum 300 lines of diff per pull request (excluding auto-generated code and locks). Smaller PRs mean faster, deeper reviews.
* **Review Checklist**:
  1. Does this diff introduce subtle state mutation side effects?
  2. Are all error paths handled explicitly (zero uncaught promises or swallowed exceptions)?
  3. Does this change meet our performance and accessibility budgets?
* **Tone**: Technical, respectful, and constructive. Praise clean patterns; explain *why* a change is requested.

### 1.4 How We Write Documentation
* **Code as Primary Documentation**: Clean variable names, explicit TypeScript types, and Pydantic schemas supersede verbose external docs.
* **Architecture Decision Records (ADRs)**: Any major architectural change requires an ADR in `/docs/adr/` detailing Context, Options Considered, Decision, and Consequences.
* **Inline Docstrings**: Document *why* a complex algorithm exists, not *what* the syntax does.

---

## SECTION 2: Repository Structure

Vapor uses a production-grade monorepo structured via Turborepo / Nx.

```
vapor-monorepo/
├── apps/                  # Deployable applications & desktop runners
│   ├── desktop-shell/     # Tauri + Next.js Desktop Shell app
│   ├── web-dashboard/     # Administrative & cloud telemetry web app
│   └── docs-site/         # Developer documentation portal
│
├── packages/              # Shared internal libraries & components
│   ├── ui/                # Core Design System React component library
│   ├── ts-config/         # Shared TypeScript configurations
│   ├── eslint-config/     # Shared ESLint rules & static analysis
│   ├── core-types/        # Shared TypeScript interfaces & schemas
│   └── ai-client/         # Client-side AI streaming SDK
│
├── services/              # Microservices & background daemons
│   ├── kernel-daemon/     # Rust native OS daemon & PTY process host
│   ├── executive-api/     # FastAPI Python core AI orchestration backend
│   └── worker-sandboxes/  # Sandboxed execution containers (gVisor/Docker)
│
├── docs/                  # System architecture, ADRs, & manuals
│   ├── adr/               # Architecture Decision Records
│   └── specs/             # Workspace & UX specifications
│
├── scripts/               # CI/CD, local dev setup, & database seeding scripts
├── tests/                 # End-to-end (E2E) & cross-service integration suites
├── tools/                 # Internal developer utilities & CLI tools
├── configs/               # Shared environment, Docker, & tailwind configs
└── .github/               # CI/CD workflows, issue templates, & PR actions
```

---

## SECTION 3: Frontend Standards

* **Framework Stack**: Next.js 14+ (App Router), React 18+, TypeScript 5+ (Strict Mode).
* **State Management**:
  * **Global UI State**: Zustand (atomic, un-nested stores for workspace layout & hotkeys).
  * **Realtime Streams**: RxJS / WebSockets observables for PTY terminal log output.
  * **Server State & Caching**: TanStack Query (React Query) for REST/gRPC data fetching.
* **Accessibility (a11y)**: Mandatory keyboard navigation; unique `id` and `aria-label` attributes; contrast ratio $\ge 7:1$.
* **Performance Budget**: FCP $< 0.8\text{s}$; Initial JS bundle $< 120\text{KB}$ gzipped.

---

## SECTION 4: Backend Standards

* **Framework Stack**: FastAPI (Python 3.11+) for AI orchestration; Rust for PTY host daemons.
* **Validation & Schemas**: Pydantic v2 schemas for all payloads; zero untyped dictionaries.
* **Error Handling**: Custom exception hierarchy deriving from `VaporBaseException`; structured JSON error codes.

---

## SECTION 5: Database Standards

* **Database Engine**: PostgreSQL 16+ with `pgvector` extension.
* **Naming**: Plural snake_case tables, singular snake_case columns.
* **Indexing**: B-tree on foreign keys; HNSW on vector embeddings (`dim=1536`).
* **Soft Deletes & Auditing**: `deleted_at TIMESTAMP` for soft deletes; immutable `audit_logs` table.

---

## SECTION 6: AI Architecture Standards

* **Prompts**: Version-controlled text templates in `/services/executive-api/prompts/`.
* **Tools**: Pydantic JSON Schema models; static validation before execution.
* **Fallback**: Multi-provider router: Primary (Gemini Pro/Claude 3.5) $\rightarrow$ Secondary (Gemini Flash/Claude 3 Haiku).

---

## SECTION 7: Testing Standards

* **Pyramid**: Unit (80% coverage), Integration (API & DB boundaries), E2E (Playwright 3 MVP workspaces).
* **AI Evals**: 100+ scenario regression test suite ($>95\%$ accuracy threshold).

---

## SECTION 8: Security & Isolation Standards

* **Auth**: WebAuthn / Passkey native auth; short-lived JWTs.
* **Secrets**: OS Secure Enclave / Keychain integration.
* **Sandboxing**: Background executions run in isolated `gVisor`/Docker containers.

---

## SECTION 9: Performance Budgets & Latency Targets

| Metric | Target Ceiling |
| :--- | :--- |
| **Desktop Shell Boot Time** | $< 500\text{ms}$ |
| **Workspace Navigation** | $< 120\text{ms}$ |
| **PTY Stream Latency** | $< 16\text{ms}$ (60 FPS) |
| **Proactive Baseline Scan** | $< 8\text{s}$ (100k LOC) |

---

## SECTION 10: Definition of Done (DoD)

- [ ] Tests passing (100% green).
- [ ] Documentation updated (ADRs & docstrings).
- [ ] Accessibility verified.
- [ ] Error, loading, and empty states implemented.
- [ ] Performance budgets satisfied.
