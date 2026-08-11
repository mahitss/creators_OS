# Event Security & Data Boundary Controls

## Security Principles
- **No Authority Escalation**: Events carry state context, never authority or permissions.
- **Payload Sanitization**: Automatic inspection for credentials (`bearer`, `password`, `secret`, `oauth_token`, `private_key`).
- **Restricted Event Isolation**: Security findings and restricted events require authorized subscriptions.
- **Audit Logging**: Every subscription creation, deletion, publication, dead-letter access, and replay attempt is recorded in `AuditEvent`.
