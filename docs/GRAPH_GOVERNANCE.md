# Graph Governance & Proposal Review

## Human-in-the-Loop AI Proposal Review
AI-derived relationships are tagged `source="ai_suggested"` and stored in `status="proposed"`. Authorized operators can review proposals at `/knowledge/graph/review` and promote them to `verified` or reject them.

## Evidence Conflict Resolution
If multiple evidence sources provide conflicting assertions, relationships are marked `status="conflicting"` and logged in `RelationshipConflict` for manual resolution.
