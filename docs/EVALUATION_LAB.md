# Vapor OS — Agent Evaluation & Simulation Lab

## 1. Overview
Sprint 24 introduces the internal Evaluation and Simulation Lab for Vapor OS. It answers: *"Does Vapor actually behave correctly?"* by evaluating planning, tool selection, context retrieval, permissions, approvals, DAG execution, retries, recovery, prompt injection resistance, budget limits, hallucination resistance, completion criteria, cost, latency, and reliability.

## 2. Core Architecture
- **Synthetic Test Workspaces (`SyntheticWorkspaceFixture`)**: Isolated, disposable workspace fixtures with synthetic users, missions, memories, drive files, emails, calendar events, content items, and attention items. Zero production data leakage.
- **Deterministic Simulation Providers**:
  - `FakeGoogleCalendarProvider`: Simulated calendar events, failure/latency injection, duplicate responses, timeouts. Zero real Google API calls.
  - `FakeGmailProvider`: Synthetic email threads, senders, subjects, prompt injection payloads. Zero real email sending.
  - `FakeDriveProvider`: Documents, PDF fixtures, malicious document payloads, permission failures. Zero real Drive modifications.
  - `FakeAIProvider`: Predictable structured response provider for reproducible regression testing.
- **Parallel Worker Concurrency**: Concurrency capped at `MAX_EVAL_CONCURRENCY = 5` to prevent resource exhaustion.
