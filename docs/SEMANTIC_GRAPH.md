# Enterprise Semantic Graph

## Enterprise Operating Graph 2.0 Integration
Extended in Sprint 61 with 15 Node types and 17 Relationship types (`OWNS`, `MEMBER_OF`, `ASSIGNED_TO`, `EXECUTES`, `DEPENDS_ON`, `BLOCKS`, `REQUIRES`, `PRODUCES`, `CONSUMES`, `REVIEWS`, `APPROVES`, `ESCALATES_TO`, `SUPPORTED_BY`, `USES`, `RELATED_TO`, `INFORMS`, `RESULTS_IN`). Enables organizational outcome traceability, concentration risk tracking, and production-safe scenario simulations.

## Overview
Vapor OS Enterprise Semantic Graph provides a unified relationship layer across all platform objects (`user`, `team`, `workspace`, `project`, `mission`, `task`, `workflow`, `agent`, `document`, `event`, `integration`, `decision`, `incident`, `artifact`, `policy`, `security_finding`).

## Core Architecture & Non-Negotiables
- **Not a Replacement Database**: Domain engines remain authoritative. The graph stores entities, relationships, references, and semantic metadata without duplicating application records or secret credentials.
- **Authorization-Aware Traversal**: Every graph traversal filters nodes and edges by `organizationId`, `workspaceId`, user permissions, and DLP classification.
- **AI Proposals vs. Authoritative Facts**: AI-suggested relationships are tagged `source="ai_suggested"`, include evidence references, confidence rating, start as `proposed`, and require human review for promotion to `verified`.
- **Entity Resolution**: `EntityResolver` unifies provider/external resource pointers (`provider`, `external_id`, `resource_type`) into canonical semantic nodes without duplication.
- **ContextPacks**: Bounded, expiring subgraphs delivered to AI Agent Mesh, Decision Intelligence, and Search RAG.
