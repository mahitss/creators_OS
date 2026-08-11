# Observability & Tracing Architecture

## Tracing Model
Every execution span maintains a hierarchical parent/child context:
`WorkflowRun` $\rightarrow$ `AgentRun` $\rightarrow$ `ModelCall` $\rightarrow$ `ToolCall` $\rightarrow$ `Retrieval` $\rightarrow$ `External API`.

## Security & Privacy Safeguards
1. **Zero Raw Content Exposure**: Full email bodies, documents, OAuth tokens, API keys, passwords, system prompts, and chain-of-thought are strictly excluded from traces.
2. **Workspace Isolation**: Usage and telemetry metrics enforce strict workspace boundary filters; cross-workspace data leakage is strictly prevented.
