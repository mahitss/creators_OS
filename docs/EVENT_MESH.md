# Enterprise Event Mesh Architecture

## Overview
Vapor OS Enterprise Event Mesh provides a policy-governed, high-throughput, durable event distribution fabric. It standardizes state-change notifications across Missions, Workflows, Agents, Integrations, Knowledge Fabric, and Decision Intelligence.

## Core Architectural Principles
1. **Events are DATA, Not Authority**: Events carry state notifications and resource references, NOT authorization. Consuming services MUST query authoritative Identity and PolicyEngine systems before executing side effects.
2. **Tenant & Workspace Isolation**: Every event envelope mandates `organizationId` and optional `workspaceId`. Subscriptions filter and enforce tenant isolation boundaries.
3. **Payload Minimization**: Raw secrets, OAuth tokens, passwords, private keys, and massive document blobs are strictly prohibited in payloads.
4. **Causation Tracking & Event Loop Protection**: Event chains enforce globally unique `correlationId` and `causationId` headers. Causation depth is strictly capped (`maxDepth = 10`) to prevent infinite recursive loops.
5. **Durable Processing & Dead Letter Queues**: Exhausted consumer retries are routed to the Dead Letter Queue (`EventDeadLetter`). Controlled event replay requires explicit operator authorization and current policy validation.
