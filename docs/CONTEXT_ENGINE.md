# Vapor OS — Unified Context Engine Architecture

## 1. Overview
The Unified Context Engine (`apps/api/app/services/context_engine.py`) consolidates all workspace context retrieval across Missions, Memories, Content Canvas, Google Calendar, Gmail, Google Drive, Attention items, and Execution results into a single, authorized, privacy-governed Context Engine.

## 2. Core Request Contract
`ContextEngine.retrieve(request: ContextRequest) -> ContextResult`
- `purpose`: `ContextPurpose` enum (`mission_planning`, `executive_brief`, `content_generation`, `email_summary`, `document_analysis`, etc.)
- `allowed_sources`: List of `SourceType` enums.
- `token_budget`: Maximum token budget (default 8,000 tokens).

## 3. Privacy Policy Matrix (`ContextPolicy`)
- Source selection is strictly restricted by `purpose`.
- `CONTENT_GENERATION`: `[mission, memory, content, drive]`. Gmail is strictly prohibited.
- `EMAIL_SUMMARY`: `[gmail]`. Drive and Calendar are strictly prohibited.
- `MEMORY`: Only approved memories enter context. Pending candidates and rejected memories are excluded.

## 4. Prompt Injection Defense
Retrieved context items are wrapped in `<RETRIEVED_CONTEXT_DATA>` blocks tagging all external emails and documents as untrusted reference data, preventing context injection attacks.
