# Vapor OS — Agent Runtime Foundation Architecture

## 1. Overview
The Agent Runtime (`apps/api/app/services/agent_runtime.py`) provides a controlled, permission-governed execution environment for AI agents to execute multi-step mission goals safely.

## 2. Model vs. Runtime Division
- AI Model: Decides WHAT action to take.
- Runtime Engine: Decides WHAT IS ALLOWED. Never permits direct code execution, shell commands, raw SQL, or unauthorized HTTP calls.

## 3. Risk Level Policy Matrix
- `READ`: Automatic tool execution.
- `WRITE` / `EXTERNAL_SIDE_EFFECT`: Requires user approval via Attention Item (`waiting_for_approval`).
- `DESTRUCTIVE`: Blocked completely.

## 4. Execution Loop & Limits
- `max_iterations`: Bounded loop (default 20 iterations max).
- Token Budget: Enforced per run via Sprint 19 `ContextEngine`.
- Zero Chain-of-Thought Storage: Stores user-safe action summaries only.

## 5. Evaluation & Simulation Lab Integration (Sprint 24)
- Runtime execution is continuously benchmarked against the 30-case Golden Core Suite (`eval_golden_suite.py`).
- Isolated synthetic workspace fixtures (`SyntheticWorkspaceFixture`) prevent real production user data contamination.
- Release gates block deployments on hard security failures or regression drops $>5\%$.

## 6. Live Operations & Control Center (Sprint 25)
- Server-Sent Events (SSE) stream operational state changes (`agent.started`, `agent.step.completed`, `agent.approval.requested`) to `/admin/agents`.
- Operators inspect telemetry, stuck signals, and trigger policy-governed control actions (`pause`, `resume`, `cancel`, `retry`) with full audit logging in `OperatorAuditLog`.
