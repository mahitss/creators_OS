# Policy Conflicts & Precedence Resolution

Details conflict detection and resolution in Vapor OS.

## Conflict Resolution
- Detects contradictory policy conditions across hierarchy levels.
- Surfaces conflicts in `PolicyConflict` records for administrative review.
- Never asks an LLM to resolve policy conflicts; uses strict deterministic precedence.
