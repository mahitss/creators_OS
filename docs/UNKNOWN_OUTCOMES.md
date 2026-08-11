# Side-Effect Crash & Unknown Outcome Resolution

If a worker crashes after sending an external side-effect request but before receiving or recording the response, the step enters status `unknown_outcome`.

## Safety Guardrails
- **No Blind Retries**: The runtime NEVER automatically retries non-idempotent external mutations when outcome is unknown.
- **Operator Evidence Inspection**: Operators inspect provider logs or external system states.
- **Explicit Resolution Endpoint**: Operators resolve step state as `resolved_success` or `resolved_failure` via `/api/v1/agents/executions/:id/unknown-outcomes/:stepId/resolve` with mandatory resolution evidence notes.
