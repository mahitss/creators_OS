# Event Schema Registry & Versioning

## Schema Registry
The Event Schema Registry (`EventSchemaRegistry`) maintains active contracts and versions for all published events across Vapor OS.

## EventEnvelope Structure
- `eventId`: Globally unique identifier (`evt_...`).
- `eventType`: Namespaced string (`mission.created`, `workflow.completed`, `agent.task.completed`, `integration.action.completed`, `knowledge.document.updated`, `security.finding.created`, `decision.recommendation.created`).
- `eventVersion`: Semantic version string (`1.0.0`).
- `organizationId` & `workspaceId`: Multi-tenant isolation markers.
- `source`: Subsystem name emitting the event.
- `subject`: Primary entity reference.
- `timestamp`: ISO 8601 UTC timestamp.
- `correlationId` & `causationId`: Distributed tracing identifiers.
- `producer`: Service or agent generator name.
- `payloadReference`: Lightweight JSON data payload.
- `classification`: Security boundary (`internal`, `confidential`, `restricted`).
