# V1.0 Not-To-Build Explicit Anti-Roadmap Boundary List

To prevent scope creep, roadmap drift, and architectural complexity, the following proposals are **EXPLICITLY REJECTED** for V1.0 operations:

1. **REJECTED: Autonomous AI Release Approvers** — AI subagents MUST NEVER be granted autonomous release approval, risk acceptance, or governance certification authority. Human-in-the-loop sign-off is mandatory.
2. **REJECTED: Direct Production Failure Injection** — Stress testing and failure injections MUST NEVER mutate live production databases directly. Simulations execute strictly in isolated read-only sandboxes (`CTRL_SIMULATION_ISOLATION`).
3. **REJECTED: Unnecessary Database Migrations / Schema Rewrites** — The existing 146+ SQLAlchemy async model schema (`v2.0-sprint110`) is stable and handles all 24 feature modules cleanly. Speculative schema rewrites are prohibited.
4. **REJECTED: Employee Behavioral Surveillance Tools** — Anti-surveillance guardrails strictly prohibit worker performance scoring, keystroke logging, or individual productivity tracking.
5. **REJECTED: Speculative Provider Integrations** — No additional LLM provider abstractions will be introduced unless an existing provider exhibits unmitigated production downtime.
6. **REJECTED: Speculative V2 Re-Architecture** — Redesigning stable, verified V1 services without empirical production failure evidence is prohibited.
7. **REJECTED: Unbacked Feature Scope Expansion** — Adding speculative features without explicit production incident or telemetry justification is rejected.

