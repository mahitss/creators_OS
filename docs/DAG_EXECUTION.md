# Vapor OS — DAG Validation & Execution Engine

## 1. Validation & Cycle Detection (`apps/api/app/services/dag_validator.py`)
Plans are validated prior to execution:
- Structural limits enforcement ($\le 50$ nodes, $\le 20$ depth).
- `node_key` uniqueness & non-empty key checks.
- Cycle detection via Depth-First Search (DFS) / Kahn's algorithm.

## 2. Execution Scheduler (`apps/api/app/services/dag_scheduler.py`)
- Ready Node Resolution: A node enters `ready` state when all parent dependencies are `completed`.
- Parallel READ Execution: Independent safe `READ` nodes run concurrently (up to 5 max).
- Write Resource Locking: Mutations targeting the same logical resource (e.g. `content:{id}`) are serialized.
- Approval Nodes: Set run status to `waiting_for_approval` and trigger Attention Items.
