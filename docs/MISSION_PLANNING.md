# Mission Planning & DAG Execution

This document details the Mission Planning lifecycle in Vapor OS Mission Intelligence 2.0.

## Decomposition Lifecycle
1. **Objective Analysis**: Evaluates constraints, deadlines, budgets, and success criteria.
2. **DAG Construction**: Generates ordered `MissionStep` objects representing execution, data, approval, or resource dependencies.
3. **Parallel Safety**: Independent steps execute in parallel. Shared mutable resources require lock serialization or conflict policy resolution.
4. **Executor Resolution**: Steps are assigned to agents, skills (`SkillFabric`), tools (`ActionGateway`), workflows (`WorkflowEngine`), or human tasks (`ApprovalPolicy`).
