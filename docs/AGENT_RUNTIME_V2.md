# Enterprise Agent Runtime 2.0

Vapor OS Agent Runtime 2.0 provides durable, resumable, observable, and policy-governed cognitive execution for long-running autonomous agents.

## Architecture Pipeline

```
MISSION -> AGENT PLAN -> EXECUTION GRAPH -> RUNTIME -> CHECKPOINT -> MODEL GATEWAY -> TOOL / AGENT / KNOWLEDGE -> RESULT -> STATE UPDATE -> CHECKPOINT -> NEXT STEP
```

## Key Capabilities
1. **Durable State**: Process restarts, worker crashes, or network failures do NOT corrupt agent state or lose mission progress.
2. **Optimistic Concurrency Versioning**: State mutations increment an explicit `version` tag on every update.
3. **Pre-Action Checkpointing**: Saves immutable `ExecutionCheckpoint` BEFORE external side-effecting tools or API mutations.
4. **Crash Recovery & Unknown Outcomes**: Crashed side-effects enter `unknown_outcome` status without blind retries.
