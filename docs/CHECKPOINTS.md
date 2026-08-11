# Pre-Action Checkpointing Engine

The Checkpoint system generates immutable state snapshots at critical execution boundaries.

## Checkpoint Trigger Reasons
- `step_completed`: Emitted after successful completion of reasoning/model/retrieval steps.
- `approval_requested`: Emitted when entering `awaiting_approval` state.
- `pause`: Emitted when operator pauses execution.
- `before_external_action`: MANDATORY checkpoint generated PRIOR to executing external side-effecting actions (emails, payments, external mutations).
- `recovery`: Emitted upon restoring execution after worker crash.
- `compaction`: Emitted when creating a compacted context snapshot.
