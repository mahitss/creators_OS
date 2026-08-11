# Crash Recovery & Resumable Execution

When a worker node crashes or loses network connectivity, Agent Runtime V2 recovers safely without repeating completed side effects.

## Recovery Procedure
1. **Heartbeat Monitoring**: Scans active executions for missing heartbeats.
2. **Checkpoint Restoration**: Loads latest valid `ExecutionCheckpoint`.
3. **Step State Verification**: Verifies completed steps and resumes from the first pending or incomplete step.
4. **Idempotency Enforcement**: Reuses existing `idempotencyKey` for pending side-effecting calls.
