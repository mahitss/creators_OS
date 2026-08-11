# Workflow AI Security & Prompt Injection Defense

## Security Controls
1. **Untrusted Content as Data**: Ingested email bodies, documents, and tool outputs are treated strictly as raw DATA. Prompt injection attempts inside content cannot alter workflow definitions or bypass security controls.
2. **Secret & Credential Protection**: OAuth tokens, API keys, database credentials, and internal secrets are strictly omitted from tool catalogs and model context windows.
3. **Privilege Escalation Rejection**: AI prompts requesting permission escalation or administrator status are detected by regex patterns and rejected with a security violation.
4. **Deterministic Risk Classification**: PolicyEngine deterministically assigns risk levels (`read-only`, `internal write`, `external side effect`, `sensitive data`, `high-risk`, `destructive`). LLM output does not determine risk or policy.
