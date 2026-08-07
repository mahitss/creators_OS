# Vapor OS Monorepo Architecture Overview

This monorepo houses the complete platform foundation for Vapor OS.

---

## Directory Matrix

* `/apps/web`: Next.js 14 App Router desktop shell.
* `/apps/api`: FastAPI Python async kernel backend API server.
* `/packages/ui`: Design System tokens, atomic React components (`Button`, `Input`, `Card`, `Modal`, `Typography`).
* `/packages/types`: Shared TypeScript interface definitions for Users, Workspaces, Proposals, and System Health.
* `/packages/database`: SQLAlchemy 2.0 async ORM models (`User`, `Organization`, `Workspace`, `Session`).
* `/packages/ai`: Multi-provider LLM client abstraction supporting OpenAI, Anthropic, Gemini, and OpenRouter with fallback routing.
* `/packages/config`: Shared ESLint, Prettier, and TypeScript configurations.
* `/packages/utils`: Shared utility functions (`formatDate`, `clsx`, `truncateText`).
* `/docker`: Containerization scripts and Docker Compose stack.
* `.github/workflows/ci.yml`: Automated CI/CD test and lint runner.
