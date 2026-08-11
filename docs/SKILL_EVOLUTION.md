# Controlled Skill Evolution & Telemetry

Continuous evaluation tracks skill quality, reliability, latency, cost, and safety.

## Signals
- `skill.created`, `skill.candidate.created`, `skill.evaluation.completed`, `skill.approved`, `skill.activated`, `skill.rollback`, `skill.regression.detected`.
- User feedback (`useful`, `incorrect`, `outdated`, `unsafe`) triggers evaluation benchmark runs.
