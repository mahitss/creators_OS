# Vapor OS — Memory Security & Isolation Architecture

## 1. Scope Isolation Rules
- **Personal Scope (`personal`)**: Owned by user, excluded from team context, workspace agents, and other users' missions.
- **Workspace Scope (`workspace`)**: Accessible to workspace members with valid workspace permissions.
- **Mission Scope (`mission`)**: Bounded to the specific mission.

## 2. Authorization Before Retrieval
Authorization controls candidate retrieval prior to keyword or semantic search. Embeddings and vector similarity are NEVER treated as permission or authorization systems.
