# Prompt Injection Defense Framework

Vapor OS enforces strict instruction boundary isolation to protect against direct and indirect prompt injection.

## Boundary Hierarchy
1. **SYSTEM POLICY** (Immutable Authority)
2. **DEVELOPER CONFIGURATION**
3. **USER REQUEST**
4. **AGENT PLAN**
5. **EXTERNAL DATA** (Untrusted Context)

## Indirect Prompt Injection Safeguards
External data sources (documents, emails, web content, calendar entries, tickets) are treated strictly as untrusted data. External content is never promoted to trusted instructions.
