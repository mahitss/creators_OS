# Knowledge Conflict Detection & Resolution

## Conflict Detection
`KnowledgeConflict` tracks contradictory assertions between evidence sources (`subject`, `claim_a`, `claim_b`, `sources`).

## Resolution Lifecycle
- `open`: Contradiction detected; surfaced in UI and AI responses.
- `investigating`: Assigned to operator for evidence review.
- `accepted_a` / `accepted_b`: Operator resolves in favor of Source A or B.
- `superseded`: Deprecated by newer authoritative release.
