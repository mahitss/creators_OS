# Context Compaction & Memory Snapshots

Long-running agent executions compact context windows without truncating critical mission state.

## Compaction Mechanism
- `ExecutionContextSnapshot` stores structured summaries of goals, completed work, evidence references, pending work, decisions, and constraints.
- Before replacing active context packs, the runtime verifies that ground-truth evidence references and key decisions remain represented.
