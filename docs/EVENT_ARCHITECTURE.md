# Event Architecture & Ingestion Pipeline

## Overview
Vapor OS implements a high-throughput, normalized event ingestion architecture designed to react to meaningful environmental changes (Gmail, Calendar, Drive, Missions, Agents, Approvals, Policies, Workspace) without generating notification noise or executing un-gated side-effects.

## Ingestion & Processing Flow
```
EXTERNAL / INTERNAL EVENT
        ↓
EVENT INGESTION (Fast-ACK HTTP 202)
        ↓
NORMALIZATION (SystemEvent Schema)
        ↓
DEDUPLICATION (Idempotency Key & EventDeduplication Cache)
        ↓
EVENT ROUTER (Event-to-Scope Routing)
        ↓
RULE & TRIGGER EVALUATION (Structured Schema Conditions)
        ↓
POLICY ENGINE (PolicyEngine.evaluate_policy)
        ↓
SIGNAL & INSIGHT EXTRACTION (Deterministic Filtering)
        ↓
PROPOSED ACTION (Attention / Insight / Approval / Agent Run)
        ↓
REALTIME SSE BROADCAST & OBSERVABILITY
```

## SystemEvent Model
Every incoming event is normalized into a unified `SystemEvent` representation:
- `workspace_id`: Workspace isolation scope.
- `source`: Provider identifier (`gmail`, `calendar`, `drive`, `mission`, `agent`, `approval`, `workspace`, `policy`, `integration`, `system`).
- `event_type`: Standardized event string (e.g. `calendar.event_updated`, `gmail.thread_updated`).
- `resource_type` & `resource_id`: Subject resource references.
- `dedupe_key`: Deterministic SHA-256 hash or provider event ID preventing duplicate action execution.
- `metadata_dict`: Untrusted payload metadata, sanitized prior to evaluation.

## Deduplication & Idempotency
- Duplicate webhooks or repeated event deliveries are checked against the `EventDeduplication` table (`dedupe_key`).
- Duplicate events are immediately acknowledged and marked with status `ignored` without re-running trigger rules or policy checks.
