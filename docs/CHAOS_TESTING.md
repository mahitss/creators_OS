# Vapor OS — Fault Injection & Chaos Testing

## 1. Controlled Fault Injection Protocols
Chaos testing in Vapor OS operates exclusively within synthetic test workspaces to evaluate system resilience under adverse conditions.

## 2. Injected Fault Scenarios
- **API Timeout / Latency Injection**: `FakeGoogleCalendarProvider` simulates network timeouts and latency spikes up to 5000ms.
- **Permission Revocation**: `FakeDriveProvider` simulates active OAuth token scope revocation during file retrieval.
- **Worker Process Death**: `agent_recovery.py` tests recovery of expired 30-second leases without step re-execution.
- **Duplicate Tool Call Invalidation**: `input_hash` idempotency checks in `ToolExecution` prevent double execution during network retries.
