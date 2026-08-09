# Vapor OS — Team Agent Ownership & Effective Permission Intersection

## 1. Agent Ownership Model
Every `AgentRun` operates on behalf of an initiating user within a workspace:
- `initiated_by`: User ID
- `workspace_id`: Workspace ID
- `mission_id`: Associated Mission ID

## 2. Effective Permission Intersection
An agent's operational permissions are equal to the strict intersection of:
$$\text{Effective Permission} = \text{User Role} \cap \text{Workspace Policy} \cap \text{Mission Scope} \cap \text{System Policy} \cap \text{Tool Risk Matrix}$$

An agent can NEVER possess higher permissions or wider data access than its initiating user.
