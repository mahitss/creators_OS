# Event Reliability, Bounded Retries & Dead Letter Queues

## Delivery Guarantees & Fault Tolerance
- **Idempotency**: Consumers track processed `eventId` keys to prevent duplicate execution side effects during retries.
- **Exponential Backoff**: Transient delivery failures undergo bounded exponential retries with jitter.
- **Dead Letter Queue (`EventDeadLetter`)**: Exhausted delivery attempts route to the Dead Letter Queue for inspection.
- **Circuit Breakers**: Consumer health monitoring halts delivery to failing downstream integrations.
