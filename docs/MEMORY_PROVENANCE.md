# Memory Provenance & Evidence Lineage

Every memory object links to an immutable `MemoryProvenance` record.

## Fields
- `memoryId`: Parent memory reference.
- `sourceType`: `conversation`, `execution`, `workflow`, `event`, `document`, `user_input`, `integration`, `agent`, `human_review`, `derived`.
- `sourceId`: Unique source entity identifier.
- `observedAt`: Ground-truth observation timestamp.
- `author`: Originating user or agent.
- `origin`: Pipeline context.
