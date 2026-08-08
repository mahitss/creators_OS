# Vapor OS — Agent State Machine Architecture

## State Transitions
`queued` $\rightarrow$ `planning` $\rightarrow$ `running` $\rightarrow$ `waiting_for_approval` $\rightarrow$ `running` $\rightarrow$ `paused` $\rightarrow$ `running` $\rightarrow$ `completed`

## Failure & Cancellation Paths
- `running` $\rightarrow$ `failed`
- `running` $\rightarrow$ `cancelled`
- `waiting_for_approval` $\rightarrow$ `cancelled`

## Revision Control (`version`)
Every state transition increments the integer `version`. Workers verify they hold the latest version before committing database updates to prevent out-of-order writes.
