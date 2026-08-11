# Vapor OS — Central Agent Policy Engine Architecture

## 1. Overview
Sprint 26 introduces the **Central Agent Policy Engine** (`apps/api/app/services/policy_engine.py`). It unifies scattered context permissions, tool permissions, risk level matrices, budget limits, autonomy modes, workspace role limits, and **Sprint 28 Delegation Constraints** into a single decision engine.

```
USER / MISSION → AGENT RUNTIME → POLICY ENGINE → ALLOW / DENY / APPROVAL_REQUIRED → TOOL REGISTRY → EXECUTION
```

## 2. Decision Pipeline
When `AgentRuntime` or `ContextEngine` requests evaluation, `policy_engine.evaluate_policy()` performs ordered checks:
1. **Suspended Member Check**: Denies execution if member status is `"suspended"`.
2. **Delegation Evaluation**: Validates active delegation status, expiration date, delegator active status, and `allowed_tools` whitelist.
3. **Destructive Tool Shielding**: Strictly blocks tools in `DESTRUCTIVE_TOOLS` (`delete_file`, `send_gmail`, etc.).
4. **Data Scope Isolation**: Prevents personal sources (`personal_gmail`, `personal_drive`, `personal_calendar`, `personal_memory`) from being accessed by workspace agents without explicit user scope.
5. **User Role Authorization**: Denies `viewer` role from triggering `WRITE` or `EXTERNAL_SIDE_EFFECT` actions.
6. **Budget & Loop Limits**: Denies execution if iteration count exceeds `max_iterations`.
7. **Autonomy Mode**: Enforces `ADVISORY_ONLY` (blocks writes) vs `HUMAN_IN_THE_LOOP` vs `FULL_AUTONOMY`.
8. **Dynamic Custom Rules**: Evaluates persistent workspace policy rules (`AgentPolicyRule`) by priority.
9. **Default Tool Risk Matrix**: Returns `ALLOW` for `READ`, `APPROVAL_REQUIRED` for `WRITE` / `EXTERNAL_SIDE_EFFECT`.

## 3. Policy Rules REST API
- `GET /api/v1/policies/rules`
- `POST /api/v1/policies/rules`
- `POST /api/v1/policies/evaluate` (dry-run evaluation)

## 4. Policy Intelligence 2.0 Upgrade (Sprint 55)
`PolicyEngine` now wraps `PolicyIntelligenceService` (Sprint 55), incorporating 7-dimension risk assessment (`data`, `financial`, `security`, `privacy`, `operational`, `compliance`, `reputational`), deterministic precedence hierarchy (`Organization > Workspace > Team > Agent > Mission > Capability`), explicit DENY wins enforcement, control chains, break-glass grants, fail-closed safeguards, and full auditability.
