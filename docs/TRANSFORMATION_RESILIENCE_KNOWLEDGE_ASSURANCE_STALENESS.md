# Plan Staleness Tracking & Stale Execution Protection

## Staleness Statuses
- `current`
- `aging`
- `stale`
- `materially_stale`
- `unknown`

## Stale Execution Protection
If a plan becomes materially stale while executing, execution pauses or routes to governance according to policy.
