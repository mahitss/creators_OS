# Controlled Event Replay Engine

## Operational Event Replay
Administrators can trigger controlled event replay for historical events via `POST /api/v1/events/replay/{id}`.

## Security & Idempotency Safeguards
1. **Administrative Authorization Required**: Replay requests require explicit `X-User-Id` header and audit reason.
2. **Current Policy Re-verification**: Replayed events are evaluated against *current* security policies and role permissions. Historical permissions are never assumed.
3. **Audit Trail**: Replay execution generates an `EventReplay` database record and logs an `AuditEvent`.
