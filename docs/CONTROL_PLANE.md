# Enterprise Control Plane Architecture

## Overview
Vapor OS Enterprise Control Plane aggregates operational telemetry across all platform subsystems (Reliability, Event Mesh, Integration Fabric, Workflows, Agents, Decision Intelligence, DLP, FinOps) into a unified operational view.

## Core Architecture
- **Aggregation Without Duplicate State**: The Control Plane does NOT own business state, run a second event bus, or maintain duplicate databases. It queries authoritative domain services in real time.
- **Control Action Gateway**: Enforces a strict 7-step pipeline: `IDENTITY -> AUTHORIZATION -> RISK -> APPROVAL -> EXECUTION -> VERIFICATION -> AUDIT`.
- **Two-Person Approval Gate**: High-risk and critical control actions require explicit 2-person approval. Requester self-approval is strictly rejected.
- **Post-Action State Verification**: After dispatching control commands, state verification confirms resource state mutation. If state remains unchanged, status transitions to `verification_failed`.
- **Self-Lockout Safeguards**: Protects core authentication (`auth_kernel`), SSO (`identity_sso`), SCIM, and PolicyEngine security controls from accidental or unauthorized disabling.
