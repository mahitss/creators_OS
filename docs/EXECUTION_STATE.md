# Versioned Execution State & Variables

`AgentExecutionState` maintains explicitly versioned variables, completed steps, pending steps, active steps, blocked steps, context references, and memory references.

## State Mutability & Concurrency
- State mutations are immutable per version.
- Updating variables or step lists increments the state `version` and updates `last_checkpoint_id`.
- Optimistic concurrency control rejects conflicting parallel worker mutations.
