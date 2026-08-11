# Collaboration Escalation Engine

`CollaborationEscalation` handles blocked, uncertain, high-risk, or approval-requiring tasks.

## SLA & Timeout Handling
Tracks SLA due dates (`due_at`). Expired escalations trigger policy-configured actions (reminders, rerouting, or task pausing).
