# Vapor OS — AI Chief of Staff & Enterprise Resilience OS (v1.0.0-rc1)

> **RELEASE CANDIDATE STATUS**: `v1.0.0-rc1` | **VERDICT**: `READY_FOR_V1`
> Vapor OS is a hardened, evidence-based Enterprise Transformation Resilience Operating System & AI Chief of Staff.

See [V1 Final Release Report](file:///c:/Users/pc/OneDrive/Desktop/Hack%20vibe/docs/V1_FINAL_RELEASE_REPORT.md), [V1 Release Manifest](file:///c:/Users/pc/OneDrive/Desktop/Hack%20vibe/docs/V1_RELEASE_MANIFEST.md), [V1 Production Checklist](file:///c:/Users/pc/OneDrive/Desktop/Hack%20vibe/docs/V1_PRODUCTION_CHECKLIST.md), and [V1 Scorecard](file:///c:/Users/pc/OneDrive/Desktop/Hack%20vibe/docs/V1_SCORECARD.md).

---


## Repository Structure

```
vapor/
├── apps/
│   ├── web/               # Next.js App Router desktop shell
│   └── api/               # FastAPI Python core kernel backend
├── packages/
│   ├── ui/                # Minimal foundation primitives (Button, Input, Card, Dialog, Badge, Spinner, Skeleton)
│   ├── database/          # PostgreSQL SQLAlchemy 2.0 async engine & session management
│   ├── ai/                # AI provider abstractions (OpenAI, Anthropic, Gemini, OpenRouter, streaming)
│   ├── types/             # Shared TypeScript domain interfaces
│   ├── config/            # Shared ESLint, Prettier, TS configurations
│   └── utils/             # Framework-independent helper functions
├── docs/                  # Architecture, Development, Environment & Contributing guides
├── scripts/               # Local setup & seed tooling
├── .github/               # CI/CD GitHub Actions workflows
├── pnpm-workspace.yaml    # pnpm workspace definition
└── turbo.json             # Turborepo pipeline configuration
```

---

## Requirements

* **Node.js**: $\ge 18.0.0$
* **pnpm**: $\ge 8.0.0$ (`npm i -g pnpm`)
* **Python**: $\ge 3.11$
* **Docker & Docker Compose**: For local PostgreSQL 16 & Redis 7.

---

## Local Development Setup

1. **Install Dependencies**:
   ```bash
   pnpm install
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```

3. **Start PostgreSQL 16 & Redis Services**:
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Run Applications in Parallel**:
   ```bash
   pnpm dev
   ```

   * **Web Client**: [http://localhost:3000](http://localhost:3000)
   * **FastAPI Kernel API**: [http://localhost:8000](http://localhost:8000)
   * **API Docs**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
   * **Real Health Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## Testing & Quality Commands

```bash
# Run all workspace linting
pnpm lint

# Run all TypeScript typechecks
pnpm typecheck

# Run Web Client Vitest Suite
pnpm --filter vapor-web test

# Run FastAPI Pytest Suite
pytest apps/api/tests

# Run Monorepo Build
pnpm build
```

---

## Documentation Index

* 📐 [Architecture Guide](./docs/ARCHITECTURE.md)
* 🛠️ [Development Setup](./docs/DEVELOPMENT.md)
* 🔑 [Environment Variables](./docs/ENVIRONMENT.md)
* 🤝 [Contributing Guidelines](./docs/CONTRIBUTING.md)
