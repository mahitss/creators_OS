# Mission Intelligence 2.0 & Enterprise Agent Orchestration

Vapor OS Mission Intelligence 2.0 provides a policy-governed multi-agent orchestration layer that coordinates agents,## Human-AI Collaboration Integration
Integrates with Enterprise Human-AI Collaboration 2.0 (Sprint 60) for work item decomposition (`WorkItem`), context-filtered handoffs (`WorkHandoff`), and escalation routing (`CollaborationEscalation`)., tools, workflows, knowledge sources, models, human approvals, parallel execution, dependencies, and long-running missions.

## System Architecture

```
MISSION
   ↓
OBJECTIVE ANALYSIS
   ↓
CAPABILITY DISCOVERY (Sprint 52)
   ↓
MISSION DECOMPOSITION
   ↓
AGENT / SKILL ASSIGNMENT
   ↓
DEPENDENCY GRAPH
   ↓
EXECUTION PLAN
   ↓
DURABLE RUNTIME (Sprint 49 Agent Runtime V2)
   ↓
OBSERVATION
   ↓
REPLANNING
   ↓
VALIDATION (MissionValidator)
   ↓
MISSION COMPLETION
```

> [!IMPORTANT]
> **Orchestrator Role & Security Boundaries**:
> The orchestrator decides *what* needs to happen, *who/what* should perform it, *when* it should happen, *what dependencies exist*, *when to replan*, *when to ask a human*, and *when to stop*.
> The orchestrator NEVER bypasses `PolicyEngine`, `DLP`, `ActionGateway`, `ModelGateway`, `TrustedContextBuilder`, or `AgentRuntimeV2`.

## Core Features
1. **Objective Clarity Classification**: Classifies mission objectives into `clear`, `ambiguous`, `underspecified`, or `conflicting`. Refuses to invent critical requirements when ambiguous.
2. **Capability & Skill Discovery**: Queries Sprint 52 Capability Registry and Sprint 51 Skill Fabric to select active, authorized, and healthy tools/skills for DAG step execution.
3. **Immutable Versioned Replanning**: Every event-driven replan creates a new `MissionPlanVersion` snapshot without overwriting active plans. Replan count is strictly bounded by `max_replans`.
4. **MissionValidator & Evidence Verification**: Deliverables and external actions are validated against actual artifacts or `ActionGateway` execution logs before marking steps complete. Fake progress is strictly forbidden.
5. **Decision Engine 2.0 Integration**: Complex decision nodes within mission plans delegate option evaluation, claim classification, and trade-off matrices directly to `DecisionEngineService` (Sprint 54).
