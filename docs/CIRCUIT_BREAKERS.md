# Circuit Breaker Architecture

Prevents cascade failures across external APIs, model providers, and database endpoints.

## State Transitions
`closed -> open -> half_open`

- **Closed**: Normal request flow.
- **Open**: Requests fail fast without hitting failing external dependencies.
- **Half-Open**: Probes dependency with limited test traffic to verify recovery.
