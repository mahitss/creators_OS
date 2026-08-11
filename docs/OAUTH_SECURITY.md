# OAuth 2.0 Security & Scope Isolation

## OAuth Security Standard
- **Token Isolation**: Tokens are stored using AES-256 GCM encryption. Raw tokens are never logged or returned to agents/models.
- **Minimal Scope Enforcement**: Requeest only scopes required for authorized capabilities. Disconnection revokes tokens and clears local credential references.
