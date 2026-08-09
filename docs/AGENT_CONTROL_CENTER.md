# Vapor OS — Agent Control Center & Live Operations Architecture

## 1. Overview
Sprint 25 introduces the internal **Agent Control Center** (`/admin/agents`). It provides real-time observability, telemetry aggregation, stuck-agent signal detection, tool failure analysis, provider health monitoring, and policy-governed operator control actions.

## 2. Server-Side Access Control
Access to `/admin/agents` and `/api/v1/admin/*` APIs is strictly enforced server-side via `enforce_admin_authorization`. Standard workspace users are denied access (403 Forbidden).

## 3. Real-Time Telemetry & Event Streaming
- **Server-Sent Events (SSE)**: Streamed via `GET /api/v1/admin/agents/events`. Emits safe operational events (`agent.started`, `agent.step.started`, `agent.step.completed`, `agent.approval.requested`, `agent.approval.resolved`, `agent.recovered`, `agent.failed`, `agent.completed`, `agent.cancelled`).
- **Zero Prompt / CoT Leakage**: Event payloads exclude private prompts, internal chain-of-thought, or OAuth credentials.

## 4. Policy-Governed Operator Actions
Operators can trigger state machine actions:
- `pause`: Transitions active run to `paused`.
- `resume`: Resumes paused run to `running`.
- `cancel`: Cancels run (`cancelled`).
- `retry_safe_step`: Retries execution of last failed safe step.

All operator actions generate an immutable entry in `OperatorAuditLog`. Operators cannot override approval requirements or execute arbitrary tools.
