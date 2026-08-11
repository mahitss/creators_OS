# Enterprise Agent Capability Registry

Vapor OS Capability Registry provides a centralized enterprise registry making agents, skills, tools, workflows, connectors, models, knowledge sources, and automations discoverable and composable.

## Architecture Pipeline

```
CAPABILITY -> REGISTRY -> METADATA -> COMPATIBILITY -> AUTHORIZATION -> POLICY -> DISCOVERY -> COMPOSITION -> INVOCATION -> EVALUATION
```

## Core Principle
"Discovery does NOT imply permission": A capability may be discoverable in the registry catalog but not invokable without explicit authorization, or visible while requiring formal installation approval.
