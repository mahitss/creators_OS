# Decision Approvals & Human Override Audit Trail

Details decision approvals, version immutability, and human overrides in Vapor OS.

## Human Override Rules
- Approved decisions are strictly immutable (`DecisionVersion`).
- When a human user overrides an AI recommendation, a new decision version is created.
- The original AI recommendation, rationale, and full audit trail are preserved without deletion.
