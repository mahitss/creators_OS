# Knowledge Ingestion & Incremental Sync

## Incremental Sync Pipeline
Sources compute `contentHash` (MD5/SHA256) and track `sourceUpdatedAt`. Re-indexing is skipped when content hash matches existing version. Connectors normalize text, markdown, HTML, PDF, DOCX, CSV, JSON, Gmail emails, Drive docs, and Calendar events.
