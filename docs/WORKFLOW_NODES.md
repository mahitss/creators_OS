# Workflow Node Specification

## Supported Nodes
- `trigger`: Ingests event or schedule occurrence.
- `condition`: Structured comparison (`equals`, `contains`, `greater_than`, etc.).
- `branch`: If/else fan-out (max 10 branches).
- `agent`: AgentDefinition task execution.
- `tool`: ToolRegistry tool invocation (policy-evaluated).
- `approval`: Human approval gate.
- `delay`: Scheduled delay.
- `transform`: Deterministic field mapping & string formatting.
- `notification`: In-app notification creation.
- `mission`: Creates/starts a Mission.
- `end`: Explicit workflow termination node.
