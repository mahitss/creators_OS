# KINETIQ — Event Mesh & Asynchronous Architecture

## 1. Event Mesh Overview

The Kinetiq Event Mesh provides decoupled, reliable, and immutable message passing across autonomous agents, background worker pools, and external webhooks.

```
[Agent Action / Mission Router]
               |
        Publish Event
               |
               v
      [Event Mesh Engine]
     (Redis Pub/Sub / Outbox)
               |
     +---------+---------+
     |                   |
     v                   v
[Worker Pool]    [WebSocket Mesh]
 (Async Task)     (Live Frontend UI)
```

---

## 2. Event Envelope Schema

All events adhere to the standard envelope:

```json
{
  "event_id": "evt_01J8F9X2K3A...",
  "event_type": "MISSION_STEP_COMPLETED",
  "tenant_id": "org_enterprise_alpha",
  "workspace_id": "ws_production_01",
  "actor_id": "usr_alex_lead",
  "timestamp": "2026-08-22T00:10:00Z",
  "correlation_id": "corr_8f1c8b3a",
  "version": "1.0",
  "payload": {
    "mission_id": "mis_99a8b7",
    "step_id": "stp_01",
    "status": "SUCCESS",
    "duration_ms": 342
  }
}
```

---

## 3. Supported Event Types

| Category | Event Name | Trigger |
|---|---|---|
| **Mission** | `MISSION_CREATED` | User or automated scheduler creates a new mission |
| **Mission** | `MISSION_STEP_STARTED` | Worker begins executing a step |
| **Mission** | `MISSION_STEP_COMPLETED` | Step finishes execution with validated output |
| **Model** | `MODEL_INFERENCE_REQUESTED` | Agent requests LLM completion |
| **Model** | `MODEL_FALLBACK_TRIGGERED` | Primary model unavailable; routed to fallback tier |
| **Governance** | `POLICY_VIOLATION_BLOCKED` | Zero-Trust / DLP guardrail prevents unauthorized tool execution |
