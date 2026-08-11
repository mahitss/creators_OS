# Optimization Safety, Policy Gating & Side-Effect Protection

## Safety Guardrails & Side-Effect Protection
- **Side-Effect Safety**: External actions (emails, calendar events, drive modifications, external APIs) preserve intended sequential ordering and are never parallelized unsafely.
- **PolicyEngine & DLP Integrity**: Optimization proposals CANNOT weaken DLP boundaries, remove human approval gates, or grant elevated permissions.
- **Quality Guardrails**: Evaluation quality scores must remain above configured thresholds (Sprint 24 evaluation integration).
