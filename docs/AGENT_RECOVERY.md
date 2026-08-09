# Vapor OS — Agent Recovery & Persistence Architecture

## 1. Overview
The Agent Recovery Manager (`apps/api/app/services/agent_recovery.py`) enables Vapor AI agents to survive worker crashes, server restarts, network timeouts, and provider delays without restarting from zero or replaying completed actions.

## 2. Checkpointing Model
- `AgentCheckpoint`: Stores state (`current_step`, `completed_steps`, `pending_action`, `budget_state`, `iteration_count`).
- Checkpoints save after meaningful step transitions (tool execution success, approval request, resume).
- Zero Chain-of-Thought Storage: Hidden model reasoning is never persisted.

## 3. Worker Lease & Stale Run Claiming
- Workers hold a 30-second heartbeat lease (`lease_expires_at`).
- When a worker dies, its lease expires. The recovery process claims stale runs by updating `lease_worker_id` and incrementing state `version`.

## 4. Operational Stuck Agent Signals & Control Center (Sprint 25)
- The Agent Control Center (`/admin/agents`) surface expired lease runs, step timeouts ($>120\text{s}$), and stale heartbeats ($>60\text{s}$) in real-time.
- Operators can trigger `retry_safe_step` or `resume` actions safely, generating an audit entry in `OperatorAuditLog`.
