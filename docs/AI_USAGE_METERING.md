# Granular AI Usage Metering Architecture

`AIUsageEvent` tracks 11 resource consumption types:
`model_input`, `model_output`, `embedding`, `retrieval`, `tool_call`, `workflow_execution`, `agent_execution`, `storage`, `compute`, `network`, `integration`.

## Metering Telemetry
Records input, output, cached, and reasoning tokens along with execution latency and tenant context.
