# Enterprise Transformation Resilience Scenario Validity

## Scenario Invalidation Engine

When a key resilience assumption drifts or changes, affected digital twin and simulation scenarios are marked:
* `valid`: Scenario assumptions match live sensing telemetry.
* `degraded`: Scenario assumptions show minor drift.
* `invalid`: Core scenario assumptions are broken.
* `needs_review`: Scenario requires re-evaluation before leadership review.

Scenarios with invalidated assumptions are never silently reused.
