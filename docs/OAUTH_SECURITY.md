# Vapor OS — OAuth Security Architecture

## 1. CSRF State Validation
OAuth authorization requests generate a cryptographically strong UUID `state` token stored server-side.
During authorization callback processing, `state` is strictly validated and immediately popped.

## 2. Token Encryption at Rest
Access and refresh tokens are symmetrically encrypted using Fernet keys derived from `settings.SECRET_KEY`.
Tokens are NEVER stored as plaintext in PostgreSQL.

## 3. Zero Token Leakage Guarantee
Encrypted token fields (`encrypted_access_token`, `encrypted_refresh_token`) are strictly stripped from all REST API JSON response schemas, frontend clients, and server telemetry logs.

## 4. Disconnect Credentials Cleanup
When a user disconnects an integration:
1. Revocation requests are sent to provider endpoints.
2. Encrypted token strings are set to `None`.
3. Connection status becomes `disconnected`.
