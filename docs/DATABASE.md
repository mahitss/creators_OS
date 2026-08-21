# KINETIQ — Database Engineering & Schema Specification

## 1. Engine & Connectivity
- **Engine**: PostgreSQL 16 (Neon Serverless Connection Pooler)
- **ORM**: SQLAlchemy 2.0 with `DeclarativeBase`
- **Driver**: `asyncpg` (Asynchronous Connection Pool)
- **Primary Keys**: UUIDv4 (`UUID(as_uuid=True)`)
- **Timestamps**: UTC timezone-aware `DateTime(timezone=True)`

---

## 2. Core Relational Entities

### 2.1 Multi-Tenant Organization Hierarchy
- `users`: User identities (`id`, `email`, `name`, `avatar_url`, `created_at`, `updated_at`).
- `organizations`: Enterprise accounts (`id`, `name`, `slug`, `owner_id`, `created_at`).
- `workspaces`: Tenant boundary partitions (`id`, `org_id`, `name`, `root_path`, `settings`, `created_at`).
- `workspace_memberships`: User-to-workspace mapping (`user_id`, `workspace_id`, `role`, `status`).

### 2.2 Mission & Agent Execution
- `missions`: Top-level goals (`id`, `workspace_id`, `title`, `status`, `priority`, `created_by`, `created_at`).
- `mission_plans`: Multi-step DAG plans (`id`, `mission_id`, `version`, `status`, `goal`, `summary`).
- `mission_steps`: Discrete execution nodes (`id`, `plan_id`, `step_index`, `title`, `status`, `tool_name`).
- `mission_activities`: Audit log of mission actions (`id`, `mission_id`, `action`, `details`, `created_at`).

### 2.3 Long-Term Intelligence & Memory
- `memories`: Learned concepts, procedural memories, episodic records (`id`, `workspace_id`, `title`, `content`, `type`).
- `memory_embeddings`: Vector embeddings for semantic search and retrieval.

---

## 3. Composite Indexing & Query Optimization
- `idx_ws_membership_user_ws`: Unique index on `(user_id, workspace_id)`.
- `idx_missions_workspace_status`: Compound index on `(workspace_id, status)`.
- `idx_missions_workspace_created`: Compound index on `(workspace_id, created_at)`.
- `idx_memories_workspace_type`: Compound index on `(workspace_id, type)`.
