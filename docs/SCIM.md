# SCIM 2.0 Provisioning & Deprovisioning

## Automated User Lifecycle
When a user is deprovisioned via SCIM (`active=false`), all active user sessions are immediately revoked, owned automations are paused, and audit history is preserved.
