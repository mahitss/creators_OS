# Event-Driven Workflows & Agent Triggers

## Reactive Intelligence Triggers
Workflows and Agents subscribe to event topics to reactively execute automation steps:

- `knowledge.document.updated` -> Ingestion & Re-indexing Workflow
- `security.finding.created` -> Security Triage Agent Run
- `decision.recommendation.created` -> Executive Alert & Mission Trigger
- `integration.action.completed` -> Workflow Continuation Step

All triggered workflows and agents MUST pass ActionGateway and PolicyEngine authorization before taking external actions.
