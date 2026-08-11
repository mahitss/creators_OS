# Entity Resolution & Deduplication

## EntityResolver Pipeline
Maps external provider identifiers (e.g. Google Drive document, GitHub commit, Gmail message) to a single canonical `SemanticEntity` node using `(provider, external_id, resource_type)` lookup.

## Anti-Duplication Strategy
Prevents duplicate entity nodes for the same underlying real-world resource across multiple integrations or ingestion events.
