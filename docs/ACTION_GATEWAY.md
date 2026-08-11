# Universal Action Gateway Architecture

## 10-Step Universal Action Flow
```
REQUEST → IDENTITY → CAPABILITY VALIDATION → RESOURCE AUTHORIZATION → DLP → RISK & APPROVAL → IDEMPOTENCY → SSRF PROTECTION → EXECUTION → VERIFICATION → AUDIT
```

## Action Risk & Idempotency
- **Risk Classification**: Actions are classified as `low`, `medium`, `high`, `critical`. High/critical actions require human approval.
- **Idempotency Keys**: Side-effecting actions enforce idempotency keys to prevent duplicate execution during retries.
