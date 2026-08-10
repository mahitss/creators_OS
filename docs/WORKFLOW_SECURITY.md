# Workflow Security & Policy Enforcement

## Threat Model & Safeguards
1. **PolicyEngine Review Gate**: Every node capability (e.g. `tool:create_content`, `agent_execution`) is evaluated against `policy_engine.evaluate_policy()`. Workflows cannot grant permissions beyond allowed policy.
2. **Cycle Prevention**: Visual graphs are validated using a topological sort cycle detection algorithm prior to compilation; cycles are rejected.
3. **No Dynamic Code Injection**: Structured condition operators (`equals`, `contains`, `greater_than`) and deterministic field transforms replace arbitrary code execution.
4. **Approval-Gated Tools**: Risky side-effects (creating content, sending emails, revoking integrations) remain gated by the existing Approval system.
