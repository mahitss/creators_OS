# Multi-Agent Orchestration & Sub-Delegation

Details multi-agent delegation contracts and bounded debate protocols in Vapor OS.

## Delegation Controls
- **Subtask Contract**: Parent agents delegate subtasks with explicit inputs, expected outputs, deadlines, and budget limits.
- **Max Delegation Depth**: `max_delegation_depth` prevents runaway nested delegations.
- **Cycle Detection**: Detects circular delegation graphs (`Agent A -> B -> A`) and blocks execution safely.
- **Capability Scoping**: Parent agents cannot delegate capabilities they do not possess.

## Bounded Multi-Agent Debate
Supports structured multi-agent validation (proposer, reviewer, validator) with explicit round, cost, and time limits.
