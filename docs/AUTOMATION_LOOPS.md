# Automation Loop Protection & Self-Trigger Prevention

## Infinite Loop Risk
Proactive systems can inadvertently create recursive execution loops:
`Agent Action -> System Event -> Trigger Fires -> Agent Run -> Agent Action`

## Mitigation Architecture
1. **Chain Tracking & Ancestry**: Every event propagation carries a `chain_id` and integer `chain_depth`.
2. **Maximum Chain Depth Limit**: `MAX_PROACTIVE_CHAIN_DEPTH = 5`. Any event propagation exceeding depth 5 is halted immediately and recorded as `loop_blocked` in `AutomationExecution`.
3. **Self-Trigger Protection**: If an agent action emits an event that matches a trigger owned by the same agent/mission context, cooldown and ancestry checks block automatic re-execution.
4. **Dead-Letter Visibility**: Blocked or unprocessable events are routed to `DeadLetterEvent` for operational inspection in the Agent Control Center.
