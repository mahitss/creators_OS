# Vapor OS — Memory 2.0 & Candidate Approval Engine

## 1. Candidate Proposal & Human Approval Flow
Agents cannot directly write permanent memories to the memory vault.
```
AGENT → MEMORY CANDIDATE (status='candidate') → POLICY ENGINE → HUMAN APPROVAL → ACTIVE MEMORY (status='active')
```

## 2. Memory Status Lifecycle
- `candidate`: Proposed memory awaiting user review.
- `approved` / `active`: Human-validated persistent memory.
- `stale`: Source content hash changed or document was deleted.
- `superseded`: Replaced by a newer authoritative memory during conflict resolution.
- `archived`: Retained for audit but excluded from active agent retrieval.
- `rejected`: Explicitly declined by user during candidate review.
