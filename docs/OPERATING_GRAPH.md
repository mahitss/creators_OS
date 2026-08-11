# Enterprise Operating Graph 2.0 Architecture

Vapor OS Enterprise Operating Graph 2.0 provides a living graph connecting enterprise entities across 15 Node types and 17 Relationship types.

## Graph Topology
```
ORGANIZATION -> WORKSPACES -> TEAMS -> PEOPLE -> AGENTS -> CAPABILITIES -> MISSIONS -> WORK -> DECISIONS -> KNOWLEDGE -> OUTCOMES
```

## Node Types (15)
- `Organization`, `Workspace`, `Team`, `Human`, `Agent`, `Capability`, `Skill`, `Mission`, `WorkItem`, `Decision`, `KnowledgeObject`, `Workflow`, `Integration`, `Resource`, `Outcome`.

## Relationship Types (17)
- `OWNS`, `MEMBER_OF`, `ASSIGNED_TO`, `EXECUTES`, `DEPENDS_ON`, `BLOCKS`, `REQUIRES`, `PRODUCES`, `CONSUMES`, `REVIEWS`, `APPROVES`, `ESCALATES_TO`, `SUPPORTED_BY`, `USES`, `RELATED_TO`, `INFORMS`, `RESULTS_IN`.

## Strategic Planning 2.0 Integration
Integrates in Sprint 62 with Enterprise Strategic Planning 2.0 (`StrategicPlan`, `StrategicObjective`, `StrategicInitiative`, `StrategicAssumption`). Connects strategic objectives to Operating Graph `Outcome` and `Mission` entities for executive outcome traceability.
Graph ownership describes operational responsibility. It does NOT track employee social graphs, rank workers, or perform hidden productivity scoring. Authorization remains strictly governed by Identity and PolicyEngine.
