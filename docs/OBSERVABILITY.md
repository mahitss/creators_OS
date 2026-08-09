# Vapor OS — Observability & Telemetry Redaction

## 1. Redaction & Privacy Enforcement
`redact_sensitive_content()` sanitizes all operational telemetry prior to storage and display:
- **OAuth Credentials**: Regex replaces `ya29.*` strings with `[REDACTED_OAUTH_TOKEN]`.
- **Bearer Tokens**: Regex replaces `Bearer .*` with `Bearer [REDACTED_TOKEN]`.
- **API Keys**: Redacts `sk-.*` keys with `[REDACTED_API_KEY]`.
- **Secrets & Passwords**: Filters keys containing `token`, `secret`, `password`, `bearer`.

## 2. Admin Observability REST API Endpoints
- `GET /api/v1/admin/agents/overview`
- `GET /api/v1/admin/agents`
- `GET /api/v1/admin/agents/events`
- `GET /api/v1/admin/agents/stuck`
- `GET /api/v1/admin/agents/approvals`
- `GET /api/v1/admin/agents/failures`
- `GET /api/v1/admin/agents/providers`
- `GET /api/v1/admin/agents/metrics`
- `GET /api/v1/admin/agents/{id}`
- `POST /api/v1/admin/agents/{id}/action`
