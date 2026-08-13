# V1.0 Secret Management & DLP Boundaries

## Secret Handling Rules
1. **Zero Committed Secrets**: Secrets must never be committed to source control or included in build artifacts.
2. **Environment Ingestion**: Secrets are injected via environment variables (`.env`) or cloud vault infrastructure.
3. **DLP Inspection**: All incoming prompts, outgoing API responses, logs, and exports pass through `dlp_service` regex detectors to redact or block sensitive API keys (`vpr_*`, `sk_*`), private keys, passwords, and PII.
