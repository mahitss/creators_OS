# Vapor OS — Agent Handoffs & Depth Bounds

## 1. Controlled Agent Handoff (`AgentHandoff`)
An active `AgentRun` can transfer task contexts to a specialized target `AgentDefinition` across pipeline stages (e.g. `Research Agent` $\rightarrow$ `Proposal Drafter` $\rightarrow$ `Scheduling Assistant`).

## 2. Recursive Spawning Protection
- **Max Handoff Depth**: $\text{depth} \le 3$. Attempts to spawn handoffs at depth $> 3$ raise `ValueError` and are blocked.
- **Max Active Mission Handoffs**: $\le 5$ active handoffs per mission.
- **No Privilege Escalation**: Target agents operate under independent, strict `PolicyEngine` evaluations.
