# Vapor OS — Context Engine Security & Privacy Policy

## 1. Authorization-First Paradigm
Context Engine verifies authenticated user identity, workspace membership, integration connection status, and source capabilities *before* querying underlying adapters.

## 2. Workspace Isolation
All source queries filter strictly by `workspace_id`. Zero cross-workspace data leakage is allowed.

## 3. Untrusted Data Marking
All external email bodies and document contents are marked as untrusted reference material (`<RETRIEVED_CONTEXT_DATA>`) to prevent prompt injection.
