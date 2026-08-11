# Human-in-the-Loop Mission Approvals

Details approval workflows and escalation policies in Vapor OS.

## Approval Policy Rules
- **High-Risk Step Gating**: Steps with elevated action or financial risk require human approval.
- **Contextual Approval Request**: Approval prompts detail goal, plan, risk level, data access, estimated cost, and duration.
- **Timeout Policy**: Unanswered approval requests trigger configured escalation (`manager`, `admin`, `security_reviewer`), pause, or replan policies.
