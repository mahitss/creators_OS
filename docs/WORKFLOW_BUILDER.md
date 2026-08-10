# Visual Workflow Builder Interface

## Features
- **Visual Canvas**: Drag-and-drop node palette (`Trigger`, `Condition`, `Branch`, `Agent`, `Tool`, `Approval`, `Delay`, `Transform`, `Notification`, `Mission`, `End`).
- **Structured Variable Picker**: Pick variables (`{{event.subject}}`, `{{agent.result}}`, `{{mission.id}}`) without manual path typing.
- **Dry-Run Simulation**: Endpoint `POST /api/v1/workflows/{id}/test` simulates node traversal and policy decisions using synthetic payloads without executing external side-effects.
- **Capability & Risk Review**: Displays capability requirements and PolicyEngine approval requirements prior to publishing.
