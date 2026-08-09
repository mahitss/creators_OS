# Vapor OS — Workspace Security & Team Isolation

## 1. Non-Negotiable Workspace Isolation
Workspace isolation is strictly enforced across every entity: `Mission`, `AgentRun`, `Content`, `Memory`, `Integration`, `AttentionItem`, `ToolExecution`. Cross-workspace access returns 403 Forbidden / DENY.

## 2. Personal vs. Workspace Data Boundary
- **Personal Scope** (`personal_gmail`, `personal_drive`, `personal_calendar`, `personal_memory`) belongs exclusively to an individual user.
- Personal sources are NEVER automatically promoted to workspace context or searched by workspace-wide agents.

## 3. Last Owner Protection
- A workspace must always maintain at least one active owner.
- The Policy & Workspace engine blocks any attempt to demote, suspend, or remove the last remaining owner.
