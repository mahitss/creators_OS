# Vapor OS — Tool Execution & Idempotency Architecture

## Execution States
`pending` $\rightarrow$ `executing` $\rightarrow$ `completed` | `failed` | `unknown`

## Unknown Status Resolution
If a worker crashes while an external side-effect tool is executing, the status becomes `unknown`. The recovery manager performs provider-side validation (e.g. checking local Google Calendar event records) before marking `completed` or scheduling a safe retry.
