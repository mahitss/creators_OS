# FinOps Architecture & Cost Attribution

## Core Principles
1. **No Fabricated Billing**: Platform metrics report `estimated platform usage cost`. Unintegrated provider invoices are never represented as exact billing charges.
2. **Versioned Pricing Model**: Every `UsageRecord` retains the active `pricing_version` at time of execution. Historical costs are never modified when pricing updates occur.
3. **Hierarchical Attribution**: Costs are attributed to workspace, mission, workflow, agent, and model levels without double-counting.
