# Vapor OS — Mission Orchestration & Replanning

## 1. Replan Limits
When a step fails due to external dependency unavailability, the agent can propose an alternative plan fragment. The total replans per `AgentRun` are strictly capped at **3**.

## 2. Checkpointing Integration
Each `AgentCheckpoint` captures `plan_version` and `node_states` (`ready_nodes`, `running_nodes`, `completed_nodes`, `failed_nodes`) to ensure multi-step DAG missions resume safely after worker restarts.
