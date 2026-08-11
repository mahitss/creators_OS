# Controlled Event Replay & Outbox Recovery

Manages event stream gap detection, transactional outbox reconstruction, and bounded replay.

## Replay Safety Controls
- Replay operations must be authorized.
- Replayed events carry original idempotency keys.
- Duplicate consumer executions are filtered.
