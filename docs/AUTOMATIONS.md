# Event Automations & Triggers

## Overview
Vapor OS enables users and administrators to configure structured, event-driven `AgentTrigger` records.

## Trigger Specifications
- **No Arbitrary Code Execution**: Triggers rely on schema-based JSON condition matching (e.g. `{"is_deadline_change": true}`, `{"priority": "urgent"}`). Arbitrary JavaScript or Python evaluation is prohibited.
- **Scopes**:
  - `personal`: Evaluates only authorized personal resources.
  - `workspace`: Evaluates shared workspace resources.
  - `mission`: Associated with a specific Mission context.
- **Cooldown**: Enforces configurable minimum delays (e.g. 7200 seconds) between trigger firings to prevent event storms.
- **Dry-Run Testing**: Triggers can be simulated via `POST /api/v1/automations/{id}/test` to verify matching conditions and PolicyEngine decisions without executing side effects.
