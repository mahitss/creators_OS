# Vapor OS — Central Agent Policy Engine Architecture

## 1. Overview
Sprint 26 introduces the **Central Agent Policy Engine** (`apps/api/app/services/policy_engine.py`). It unifies scattered context permissions, tool permissions, risk level matrices, budget limits, autonomy modes, and workspace role limits into a single decision engine.

```
USER / MISSION → AGENT RUNTIME → POLICY ENGINE → ALLOW / DENY / APPROVAL_REQUIRED → TOOL REGISTRY → EXECUTION
```

## 2. Decision Pipeline
When `AgentRuntime` or `ContextEngine` requests evaluation, `policy_engine.evaluate_policy()` performs ordered checks:
1. **Suspended Member Check**: Denies execution if member status is `"suspended"`.
2. **Destructive Tool Shielding**: Strictly blocks tools in `DESTRUCTIVE_TOOLS` (`delete_file`, `send_gmail`, etc.).
3. **Data Scope Isolation**: Prevents personal sources (`personal_gmail`, `personal_drive`, `personal_memory`) from being accessed by workspace agents without explicit user scope.
4. **User Role Authorization**: Denies `viewer` role from triggering `WRITE` or `EXTERNAL_SIDE_EFFECT` actions.
5. **Budget & Loop Limits**: Denies execution if iteration count exceeds `max_iterations`.
6. **Autonomy Mode**: Enforces `ADVISORY_ONLY` (blocks writes) vs `HUMAN_IN_THE_LOOP` vs `FULL_AUTONOMY`.
7. **Dynamic Custom Rules**: Evaluates persistent workspace policy rules (`AgentPolicyRule`) by priority.
8. **Default Tool Risk Matrix**: Returns `ALLOW` for `READ`, `APPROVAL_REQUIRED` for `WRITE` / `EXTERNAL_SIDE_EFFECT`.

## 3. Policy Rules REST API
- `GET /api/v1/policies/rules`
- `POST /api/v1/policies/rules`
- `POST /api/v1/policies/evaluate` (dry-run evaluation)
