# Control Actions & 7-Step Gateway Pipeline

## 7-Step Pipeline
1. **IDENTITY**: Verifies authenticated operator `X-User-Id` header.
2. **AUTHORIZATION**: Evaluates role permissions via PolicyEngine.
3. **RISK**: Classifies action risk (`low`, `medium`, `high`, `critical`).
4. **APPROVAL**: Requires 2-person approval for `high` and `critical` risk.
5. **EXECUTION**: Dispatches command to underlying subsystem.
6. **VERIFICATION**: Validates post-execution state change.
7. **AUDIT**: Records immutable audit entry in `AuditEvent`.

## Registered Control Actions
- `pause_service`
- `resume_service`
- `disable_agent`
- `cancel_workflow`
- `replay_event`
- `disable_integration`
- `revoke_session`
- `retry_ingestion`
