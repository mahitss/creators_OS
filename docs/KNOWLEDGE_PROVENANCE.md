# Knowledge Provenance & Source Authority

## Provenance Tracking
`KnowledgeProvenance` records `knowledge_object_id`, `source_type` (`user`, `document`, `email`, `calendar`, `integration`, `database`, `workflow`, `agent`, `system`, `external_source`, `generated`), `source_id`, `external_id`, `author`, `created_at`, `observed_at`, `ingested_at`, and `origin`.

## Source Authority
`SourceAuthority` ranks sources contextually (`authoritative`, `trusted`, `normal`, `unverified`, `generated`). Authority is context-specific—a source trusted for technical specs is not necessarily authoritative for corporate policies.
