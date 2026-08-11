# Policy-Controlled Degraded Modes

Defines system degradation behaviors when dependencies experience degradation or outage.

## Degradation Modes
- `read_only`: Disables mutation operations while servicing queries.
- `limited_execution`: Pauses background automated tasks.
- `no_external_actions`: Blocks outbound tool executions (`ActionGateway`).
- `approval_required`: Forces human approval for all external actions.
- `model_fallback`: Routes model requests to compliant secondary providers.
- `queue_only`: Buffers incoming events without immediate execution.
- `manual_operation`: Requires explicit operator authorization.
