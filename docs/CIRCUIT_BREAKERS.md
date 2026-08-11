# Service Circuit Breakers

## State Machine
- **CLOSED**: Normal operation.
- **OPEN**: Triggered when failure count reaches threshold (e.g. 3 failures). Stops traffic and initiates fallback.
- **HALF_OPEN**: Cooldown period (60s) expires. Tests single trial request. Transition back to CLOSED on success, or OPEN on failure.
