# Event-Driven Projection Architecture & Degraded Mode

## Event Projections & Idempotency
Consumes event streams, updating materialized command projections idempotently (preventing double-counting).

## Replay & Degraded Mode
Supports audited projection rebuilds from event history. Displays projection lag seconds, errors count, and last processed event ID. If event processing lags, explicitly flags degraded state rather than pretending data is live.
