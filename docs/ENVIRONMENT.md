# Vapor OS — Environment Configuration Guide

This document defines all environment variables consumed across the monorepo applications and microservices.

---

## Variable Reference Table

| Variable | Description | Default / Example | Required |
| :--- | :--- | :--- | :--- |
| `NODE_ENV` | Client runtime environment (`development` / `production`). | `development` | Yes |
| `ENVIRONMENT` | Backend system tier. | `development` | Yes |
| `LOG_LEVEL` | Minimum logging threshold. | `info` | No |
| `NEXT_PUBLIC_APP_URL` | Web client base URL. | `http://localhost:3000` | Yes |
| `NEXT_PUBLIC_API_URL` | Gateway API target endpoint. | `http://localhost:8000/api/v1` | Yes |
| `PORT` | FastAPI daemon binding port. | `8000` | Yes |
| `SECRET_KEY` | JWT signature encryption key (min 32 chars). | *Secret string* | Yes |
| `DATABASE_URL` | Async PostgreSQL connection string. | `postgresql+asyncpg://...` | Yes |
| `REDIS_URL` | Redis caching & pubsub broker connection string. | `redis://localhost:6379/0` | Yes |
