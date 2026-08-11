# Webhook Security, Verification & Replay Protection

## Cryptographic Webhook Security
- **HMAC Verification**: Webhooks require cryptographic HMAC-SHA256 signature verification.
- **Replay Protection**: Provider event IDs are tracked to guarantee idempotent processing.
- **DLP Payload Scan**: Webhook payloads are scanned for data classification and DLP compliance before event subscription routing.
