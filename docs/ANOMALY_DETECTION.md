# Statistical Anomaly Detection & Baseline Engine

## Baseline Calculation & Statistical Deviations
Calculates moving average and moving median baselines for operational signals (`workflow_volume`, `agent_latency`, `model_cost`, `provider_error_rate`). Flags statistically significant deviations into `AnomalyEvent` records with deterministic severity levels (`info`, `warning`, `high`, `critical`). Normal fluctuations do not trigger critical alerts.
