# Model Experiments & Canary Rollouts

Model Gateway supports canary A/B traffic splits to safely evaluate new candidate models in production.

## Canary Lifecycle
1. **Experiment Creation**: Define candidate model and target traffic percentage (e.g. 5%).
2. **Safety Enforcement**: Canary requests cannot violate workspace DLP, policy engine rules, or quality thresholds.
3. **Telemetry & Evaluation**: Tracks quality, latency, cost, and error rates against baseline models using Sprint 47 Evaluation engine.
4. **Automated Canary Rollback**: Automatically halts experiment if quality regression is detected.
