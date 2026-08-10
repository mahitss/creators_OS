# Event Security & Webhook Payload Trust

## Threat Model & Constraints
External webhooks (Gmail, Calendar, Drive, Third-Party Integrations) are treated as untrusted inputs:
1. **Server-Side Identity Verification**: `workspace_id`, `user_id`, and permissions inside event payloads are never trusted at face value. All claims are validated against server-side session and integration records.
2. **Payload Sanitization**: Raw email bodies, full document contents, OAuth credentials, and sensitive tokens are stripped prior to event storage. Minimal metadata is persisted in `SystemEvent.metadata_dict`.
3. **Replay & Cross-Workspace Attacks**: Signature verification and deduplication hashing (`dedupe_key`) prevent replay attacks and cross-workspace injection.
4. **PolicyEngine Mandatory Gate**: Every trigger action must pass `policy_engine.evaluate_policy()` prior to starting agent runs or modifying workspace resources.
