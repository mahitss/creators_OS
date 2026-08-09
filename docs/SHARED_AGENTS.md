# Vapor OS — Shared Workspace Agent Definitions

## 1. AgentDefinition Model
`AgentDefinition` represents a reusable workspace agent template:
- `visibility`: `private` (visible only to creator), `workspace` (visible to workspace members), `mission` (attached to specific mission).
- `default_purpose`: Default task goal.
- `allowed_tools`: Default capability limits.

## 2. Shared Agent Execution
Launching a shared `AgentDefinition` instantiates a distinct `AgentRun` with explicit `initiated_by`, `workspace_id`, `mission_id`, and `delegation_id`. The `AgentDefinition` template itself never executes directly.
