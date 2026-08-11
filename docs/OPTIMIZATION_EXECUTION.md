# Action Plans & Rollback Safety Controls

`OptimizationActionPlan` defines structured action steps, owners, dependencies, milestones, and explicit rollback plans.

Execution passes through `Universal Action Gateway` and `PolicyEngine` (`advisory`, `approval_gated`, `policy_authorized`). Approval does not automatically bypass authorization gateways.
