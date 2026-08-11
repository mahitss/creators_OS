# Identity & Access Management (IAM)

## Role Hierarchy & Privilege Escalation Defense
- System Roles: `owner` (100) > `admin` (80) > `security_admin` (70) > `billing_admin` (60) > `member` (20) > `viewer` (10).
- **Privilege Escalation Protection**: API endpoints reject attempts by lower-tier roles (e.g. `member`) to elevate themselves or others to higher roles.
- **Offboarding**: Deactivating a member revokes active sessions and pauses owned automations while preserving immutable audit logs.
