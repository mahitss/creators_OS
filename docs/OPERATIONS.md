# Vapor OS — Live Agent Operations & Stuck Agent Detection

## 1. Deterministic Stuck Agent Signals
The Control Center automatically flags stuck agents based on objective system signals:
1. `EXPIRED_LEASE`: Worker lease expired without renewal (worker crash).
2. `STALE_HEARTBEAT`: AgentRun updated_at timestamp $>60\text{s}$ old while status is `running`.
3. `STEP_TIMEOUT`: Active tool execution running $>120\text{s}$.
4. `EXPIRED_APPROVAL`: Approval request expired past TTL.
5. `REPEATED_TOOL_FAILURES`: 3+ consecutive failures on the same tool name.
6. `UNCONFIRMED_EXTERNAL_ACTION`: Tool execution state is uncertain.

## 2. Operator Audit Trail (`OperatorAuditLog`)
Every control action taken by an operational engineer is logged with `operator_id`, `action`, `target_agent_run_id`, `workspace_id`, `reason`, and `timestamp`.
