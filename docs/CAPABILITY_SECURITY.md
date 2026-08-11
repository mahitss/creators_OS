# Capability Security & Unified Invocation Routing

`invokeCapability()` routes execution to underlying enterprise engines:

- `skill` $\rightarrow$ `AgentRuntimeV2` (via `skill_fabric_service`)
- `tool` $\rightarrow$ `ActionGateway`
- `model` $\rightarrow$ `ModelGateway`
- `workflow` $\rightarrow$ `WorkflowEngine`
- `connector` $\rightarrow$ `IntegrationFabric`
- `knowledge_source` $\rightarrow$ `TrustedContextBuilder`

## Security Boundaries
- Packages containing credentials (`secret`, `token`) are automatically rejected during publish.
- Prevents capability permission self-escalation and circular call stack execution.
