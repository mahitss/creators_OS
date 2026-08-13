# Unified Resilience Graph & Evidentiary Relationships

## Graph Structure & Nodes
Represents relationships among existing domain entities (`transformation, portfolio, plan, risk, knowledge, evidence, decision, conflict, warning, intervention, dependency, resource, deadline, governance`).

## Evidentiary Relationship Edges
Supported edge relationship types: `depends_on, supports, blocks, affects, shared_with, constrained_by, derived_from, mitigates, causes, contributes_to, correlates_with, precedes, governed_by`. Causal relationships strictly require evidence; temporal correlation uses `correlates_with`.
