# Skill Lifecycle & Promotion Stages

Skill status lifecycle state transitions:

1. `candidate`: Pattern detected from repeated successful executions.
2. `sandbox`: Tested against golden test cases in Simulation Lab.
3. `evaluating`: Evaluated for correctness, grounding, safety, cost, and latency.
4. `approved`: Human operator or policy sign-off granted.
5. `canary`: Deployed to a limited percentage of traffic (e.g. 5%).
6. `active`: Active version serving production traffic.
7. `paused`: Suspended due to telemetry warning.
8. `deprecated`: Superseded by newer version.
9. `rejected`: Failed approval or candidate evaluation.
10. `failed_evaluation`: Failed quality or safety benchmark threshold.
