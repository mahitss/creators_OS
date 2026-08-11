# Decision Evidence & Contradiction Resolution

Details evidence provenance, freshness tracking, and conflict handling in Vapor OS.

## Evidence Provenance & Freshness
- Every evidence item records source type, source ID, observed timestamp, retrieved timestamp, and valid-until expiration.
- Stale evidence is automatically flagged (`stale`) and excluded from authoritative fact classifications.

## Evidence Conflicts
- Contradictory claims create an `EvidenceConflict` preserving claim A and claim B alongside source authority levels (`high`, `medium`, `low`).
- Conflict resolution uses newer evidence, authoritative source override, or human review.
