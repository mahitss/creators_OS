# Controlled Deployment & Canary Rollbacks

`SkillDeployment` manages versioned deployments and canary traffic splits.

## Rollback Guardrails
- If canary evaluation detects quality, safety, or cost regressions, the deployment handler automatically pauses the candidate and rolls back to the previous approved active version.
- Rollbacks preserve execution history and active running execution states.
