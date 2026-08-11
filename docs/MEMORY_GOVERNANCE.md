# Memory Governance & Lifecycle Controls

Maintains memory status lifecycle state to prevent unvalidated memory contamination.

## Lifecycle States
- `candidate`: Proposed memory awaiting review or validation.
- `active`: Verified, active memory eligible for context retrieval.
- `stale`: Memory needing revalidation from authoritative source.
- `conflicting`: Memory in active conflict with another observation.
- `deprecated`: Invalidated memory marked inactive.
- `rejected`: Candidate rejected during review.
- `expired`: Memory exceeding retention TTL.
