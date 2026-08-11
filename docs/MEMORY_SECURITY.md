# Memory Security, DLP & Secret Protection

All memory write operations pass through pre-storage DLP scanning and secret pattern filters.

## Guardrails
- **Secret Blocking**: API keys, OAuth tokens, passwords, and credentials are strictly rejected before memory persistence.
- **Sensitive Personal Attribute Policy**: Health, political, religious, or sensitive personal attributes cannot be inferred or stored.
- **Tenant Isolation**: Workspace and private scopes enforce strict authorization bounds.
