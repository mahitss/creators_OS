# Intelligent Model Routing Engine

The Intelligent Model Routing Engine dynamically evaluates inbound `ModelRequirements` against candidate models.

## Routing Pipeline
1. **Capability Filter**: Selects models supporting requested capabilities.
2. **Context Window Check**: Ensures context window capacity handles prompt & context packs.
3. **PolicyEngine & DLP Check**: Excludes unauthorized providers or classification violations.
4. **Quality & Latency Ranking**: Uses Sprint 47 evaluation scores and live P95 latency snapshots to rank candidate models.
5. **Audit Logging**: Emits immutable `ModelRoutingDecision` record detailing candidates, selected model, rejected candidates, and reason codes (`capability_match`, `policy_allowed`, `preferred_provider_selected`).
