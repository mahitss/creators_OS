# AI Model Gateway Security & Data Boundaries

Model Gateway enforces enterprise security controls before model inference.

## Security Principles
- **No Direct Credential Exposure**: Provider credentials (API keys, OAuth tokens) remain securely encapsulated inside provider adapters.
- **Pre-Inference DLP Filtering**: Data classification boundaries are evaluated prior to network egress.
- **Untrusted Model Output Handling**: All provider outputs are sanitized. Tool calls requested by models are routed through `ActionGateway` for authorization.
- **Prompt Injection Egress Protection**: Untrusted retrieved content cannot alter provider routing rules or bypass security policies.
