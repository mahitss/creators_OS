# Bounded Self-Healing & Security Safeguards

## Strictly Forbidden Autonomous Actions
The self-healing engine is strictly prohibited from autonomously modifying:
- Security policies, permissions, roles, or workspace access.
- Secret credentials, API keys, or OAuth tokens.
- Production source code, database schemas, or billing records.
- Executing arbitrary SQL or privilege escalations.

## Safe Remediation Operations
Workers, queues, failed jobs, provider fallback routing, stuck workflows, expired leases, index partitions, and transient integration failures.
