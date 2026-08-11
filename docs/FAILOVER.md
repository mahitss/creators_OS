# Model & Agent Failover Architecture

Coordinates capability-compatible model failover and agent runtime state recovery.

## Model Failover Rules
- Selects alternative models via `ModelGateway`.
- Enforces DLP boundary limits (e.g., restricted classification data stays on internal models).
- Fails safely if no compliant model is available.

## Agent Failover Rules
- Replacement workers must verify capability compatibility and acquire an authoritative `StateLease`.
- Resumes execution strictly from the latest valid durable checkpoint.
