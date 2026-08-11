# Emergency Access & Break-Glass Protocol

## Break-Glass Emergency Controls
In critical outage scenarios where standard 2-person approval channels are unreachable:

1. **Time-Limited Session**: Break-glass access grants explicit temporary emergency operator rights for a max duration of 1 hour.
2. **High-Visibility Alerting**: Triggering break-glass emits an emergency alert to all workspace owners and security administrators.
3. **Mandatory Audit & Postmortem**: Every action performed during break-glass generates immutable `AuditEvent` entries tagged with `is_break_glass=true`.
