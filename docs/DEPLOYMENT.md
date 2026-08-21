# KINETIQ — Production Deployment & Operations Guide

## 1. Containerization & Architecture

KINETIQ services run as stateless, highly-scalable container workloads orchestrated via Kubernetes or modern container PaaS (e.g. AWS ECS, GCP Cloud Run, Render, Fly.io).

```
[Load Balancer / Cloudflare Edge]
                |
     +----------+----------+
     |                     |
[apps/web (Next.js)]  [apps/api (FastAPI)]
 (Port 3000)           (Port 8000)
                           |
     +----------+----------+
     |          |
[PostgreSQL] [Redis]
```

---

## 2. Environment Configuration

### Required Environment Variables

```bash
# Core Server Config
ENVIRONMENT=production
PROJECT_NAME="Kinetiq Enterprise AI OS"
VERSION="1.0.0"
SECRET_KEY="<strong_random_secret>"
ALGORITHM="HS256"

# Database Connection (Neon PostgreSQL)
DATABASE_URL="postgresql+asyncpg://<user>:<pass>@<neon_host>/<dbname>?ssl=require"

# Redis Cache & Event Broker
REDIS_URL="rediss://:<pass>@<redis_host>:<port>"

# AI Gateway
OPENROUTER_API_KEY="sk-or-v1-..."
OPENROUTER_DEFAULT_MODEL="openrouter/free"
```

---

## 3. Build & CI Verification Pipeline

1. **Lint & Format**: `pnpm lint`
2. **Typecheck**: `pnpm build`
3. **Frontend Tests**: `pnpm --filter vapor-web test`
4. **Backend Tests**: `python -m pytest apps/api/tests`
5. **Docker Build**:
   ```bash
   docker build -t kinetiq-api -f apps/api/Dockerfile .
   docker build -t kinetiq-web -f apps/web/Dockerfile .
   ```
