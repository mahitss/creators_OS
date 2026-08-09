# Vapor OS — Agent Runtime Foundation Architecture

## 1. Overview
The Agent Runtime (`apps/api/app/services/agent_runtime.py`) provides a controlled, permission-governed execution environment for AI agents to execute multi-step mission goals safely.

## 2. Central Agent Policy Engine Integration (Sprint 26 & 27)
- AI Model: Decides WHAT action to take.
- Central Policy Engine (`policy_engine.py`): Decides WHAT IS ALLOWED based on User Role, Workspace Policy, System Policy, Autonomy Level, and Tool Risk Matrix.
- Effective Permissions: Strict intersection of User permissions + Workspace permissions + Mission permissions + System policy + Tool policy.

## 3. Risk Level Policy Matrix
- `READ`: Automatic tool execution.
- `WRITE` / `EXTERNAL_SIDE_EFFECT`: Requires user approval via Attention Item (`waiting_for_approval`).
- `DESTRUCTIVE`: Blocked completely.

## 4. Execution Loop & Limits
- `max_iterations`: Bounded loop (default 20 iterations max).
- Token Budget: Enforced per run via Sprint 19 `ContextEngine`.
- Zero Chain-of-Thought Storage: Stores user-safe action summaries only.

## 5. Live Operations & Control Center (Sprint 25)
- Server-Sent Events (SSE) stream operational state changes (`agent.started`, `agent.step.completed`, `agent.approval.requested`) to `/admin/agents`.
- Operators inspect telemetry, stuck signals, and trigger policy-governed control actions (`pause`, `resume`, `cancel`, `retry`) with full audit logging in `OperatorAuditLog`.
