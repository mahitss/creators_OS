# Vapor OS — Development Guide

## Prerequisites
* **Node.js**: $\ge 18.0.0$
* **pnpm**: $\ge 8.0.0$
* **Python**: $\ge 3.11$
* **Docker & Docker Compose**: For local PostgreSQL 16 & Redis 7.

## Local Setup & Quick Start

1. **Clone & Install Dependencies**:
   ```bash
   git clone https://github.com/mahitss/creators_OS.git vapor
   cd vapor
   pnpm install
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   ```

3. **Boot Database Stack**:
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Start Development Apps**:
   ```bash
   pnpm dev
   ```
   * Web App Shell: [http://localhost:3000](http://localhost:3000)
   * FastAPI Core Kernel: [http://localhost:8000](http://localhost:8000)
   * API Health Check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

5. **Run Testing Suite**:
   ```bash
   # Frontend Unit Tests
   pnpm --filter vapor-web test

   # Backend API Health Test
   pytest apps/api/tests
   ```
