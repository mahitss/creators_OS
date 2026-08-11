# Model FinOps & Cost Controls

Integrates with Sprint 33 FinOps & Observability to enforce budget limits and record token usage.

## Features
- **Token & Cost Tracking**: Records input tokens, output tokens, and estimated cost per request in `ModelUsage`.
- **Workspace Budget Limits**: Checks workspace budget thresholds (`ModelBudget`) before routing.
- **Budget Exceeded Handling**: Blocks requests or routes to explicitly approved lower-cost models according to workspace policy.
- **Model Cost Dashboard**: Visualized at `/ai/models` and `/finops`.
