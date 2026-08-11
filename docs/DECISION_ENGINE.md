# Decision Engine 2.0 Pipeline

Details the core pipeline responsibilities of `DecisionEngineService` in Vapor OS.

## Core Pipeline Steps
1. **Build Context**: Gathers mission, knowledge, memory, and semantic graph references.
2. **Collect Evidence**: Retrieves evidence via `TrustedContextBuilder`, checks freshness, and flags stale sources.
3. **Generate & Validate Options**: Generates options via agents or skills, validating feasibility against policy.
4. **Surface Trade-offs & Risks**: Computes trade-off comparisons across weighted criteria (`cost`, `latency`, `reliability`, `security`, `quality`, `compliance`).
5. **Approval & Outcome Calibration**: Manages human approval/override and records actual outcome telemetry.
