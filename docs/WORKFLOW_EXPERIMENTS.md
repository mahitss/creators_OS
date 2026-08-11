# Workflow A/B Testing & Canary Experiments

## Controlled Canary Traffic Splitting
Supports A/B canary testing (`OptimizationExperiment`) where a candidate version receives a controlled percentage of traffic (e.g. 10% candidate, 90% baseline). Monitors error rates, latency, and evaluation quality before full publication. Destructive or high-risk workflows cannot be canary tested without explicit authorization.
