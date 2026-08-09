# Vapor OS — Resource Scoping & Context Boundaries

## 1. Resource Scopes
Every resource specifies an explicit scope:
- `personal`: Owned by an individual user (e.g. personal Gmail, personal Memory).
- `workspace`: Shared across active workspace members (e.g. workspace drive documents, workspace content).
- `mission`: Attached to a specific mission (e.g. mission deliverables).
- `shared`: Explicitly shared resources.

## 2. Context Priority Order
When ContextEngine retrieves relevant sources for an agent run, narrow scopes take precedence:
$$\text{Mission Source} > \text{Shared Source} > \text{Workspace Source}$$

Personal sources are strictly excluded unless the user explicitly grants permission.
