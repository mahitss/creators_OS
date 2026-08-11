# Optimization Engine & Objective Functions

`OptimizationProblem` models multi-objective optimization across 7 objective types (`maximize_outcome`, `minimize_cost`, `minimize_risk`, `minimize_delay`, `maximize_capacity_efficiency`, `maximize_utility`, `custom`).

`OptimizationObjective` models metrics, directions, weights, priorities, and sources. Multi-objective optimization never exposes opaque scores without explaining contributing objectives.
