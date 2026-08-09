# Vapor OS — Knowledge Architecture & Ingestion Pipeline

## 1. Overview
Sprint 29 establishes a unified, traceable **Knowledge Architecture** (`apps/api/app/services/knowledge_service.py`) that separates temporary context, source documents, derived knowledge, and user-approved persistent memory.

```
SOURCE → INGESTION → NORMALIZATION → CHUNKING → INDEXING → RETRIEVAL → RANKING → POLICY FILTER → AGENT CONTEXT → OPTIONAL MEMORY CANDIDATE → HUMAN APPROVAL → LONG-TERM MEMORY
```

## 2. Distinction of Knowledge Types
1. **Temporary Context**: Retrieved for an agent run, not persistent memory.
2. **Mission Knowledge**: Scoped exclusively to a single Mission.
3. **Workspace Knowledge**: Shared project context across workspace members.
4. **Personal Memory**: Owned by user, never leaked to team or workspace context.
5. **Agent Memory**: Attached to an `AgentDefinition` template.
6. **Source Documents**: Drive documents, emails, calendar events.
7. **Derived Knowledge**: Generated summaries, requirements, and decisions.
8. **User-Approved Memory**: Human-validated persistent facts.
