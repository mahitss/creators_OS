# Governed Security Response Plans

Response plans specify versioned containment and remediation actions targeting agents, capabilities, tools, sessions, and missions.

## Response Action Types
- `monitor`
- `notify`
- `restrict`
- `rate_limit`
- `quarantine`
- `pause_agent`
- `disable_capability`
- `block_tool`
- `revoke_session`
- `require_approval`
- `revalidate_decision`
- `pause_mission`
- `cancel_mission`

## Safety Protections
- **Dry-Run Simulation**: Test expected response impact in Simulation Lab prior to execution.
- **Canary Isolation**: Limit containment scope to affected target before organization-wide rollout.
- **Response Locks & Idempotency**: Prevents race conditions and duplicate action execution.
