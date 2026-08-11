# Constraint Provenance & Hard vs Soft Constraints

`OptimizationConstraint` handles 9 constraint types (`budget`, `capacity`, `policy`, `deadline`, `dependency`, `security`, `resource`, `technical`, `business`).

Hard constraint violations mark options as infeasible with clear explanations. Soft constraint violations produce trade-off penalties. Constraints track source, owner, effective date, and freshness to prevent optimization on stale rules.
