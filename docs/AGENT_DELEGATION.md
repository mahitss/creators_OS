# Vapor OS — Agent Delegation & Tool Whitelisting Architecture

## 1. Overview
Sprint 28 introduces controlled, explicit, time-bounded, tool-whitelisted, and revocable **Agent Delegation** (`apps/api/app/services/agent_delegation_service.py`).

```
USER → DELEGATION → SCOPED AGENT AUTHORITY → MISSION → AGENT RUN → POLICY ENGINE → TOOLS → APPROVALS → RESULT
```

## 2. Effective Authority Intersection
$$\text{Effective Agent Authority} = \text{System Policy} \cap \text{Workspace Policy} \cap \text{User Permissions} \cap \text{Delegation} \cap \text{Mission Policy} \cap \text{AgentRun Policy} \cap \text{Tool Policy}$$

## 3. Delegation Constraints
- **Privilege Escalation Protection**: A user CANNOT delegate permissions they do not possess (e.g. `viewer` role cannot delegate write permissions).
- **Tool Whitelisting**: An `AgentDelegation` can specify `allowed_tools`. Invocations of un-whitelisted tools return `DENY` from `PolicyEngine`.
- **Revocation & Expiration**: Expired or revoked delegations immediately cause `PolicyEngine` to return `DENY` for future tool executions.
- **Auditable & Non-Self-Modifying**: Agents cannot delegate themselves or alter their own delegation parameters.
