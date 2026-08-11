# Quality-Aware Cost Optimization & Canary Experiments

Recommends model switches, prompt reductions, and cache optimizations while enforcing quality evaluation guardrails.

## Safety Controls
- Recommends cheaper models ONLY when AI Evaluation scores satisfy quality thresholds.
- Supports A/B canary trials (`CostOptimizationExperiment`) with 1-click revert capability.
