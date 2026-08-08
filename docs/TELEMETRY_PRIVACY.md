# Vapor OS — Telemetry & Sensitive Data Privacy Policy

## 1. Zero Sensitive Data Logging Policy
To protect user privacy and workspace security, Vapor OS strictly forbids logging sensitive fields in operational or telemetry logs.

## 2. Forbidden Log Targets
The following parameters and data sources must NEVER appear in server logs, APM traces, or telemetry records:
- User Passwords & Hashed Passwords
- Session Tokens & JWT Tokens
- Cookies & Authorization Headers (`Bearer ...`)
- AI Provider API Keys
- Raw User AI Prompts
- Raw AI Generated Output Payloads
- Private Memory Vault Content
- Personal Identifiable Information (PII)

## 3. Telemetry Retention
Operational metrics (token counts, latency ms, failure categories) are retained for operational debugging and automatically purged per workspace retention rules.
