# Policy-Governed Event Routing

## Subscription & Filter Engine
The Event Router evaluates subscriptions against incoming `EventEnvelope` streams:

1. **Tenant Verification**: Filters out events where subscriber `organizationId` or `workspaceId` does not match the envelope.
2. **Event Type Matching**: Supports wildcard (`*`) and exact namespaced matching.
3. **Deterministic Property Filters**: Evaluates filter configurations against envelope headers and payload references without executing arbitrary user code.
4. **Rate Limiting & Storm Protection**: Caps publish spikes per workspace/producer to prevent event storms.
