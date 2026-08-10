# Visual Workflow Engine & Architecture

## Overview
Vapor OS implements a visual workflow authoring layer positioned on top of the existing, authoritative DAG Scheduler (`dag_scheduler.py`), Agent Runtime (`agent_runtime.py`), Policy Engine (`policy_engine.py`), and Approval System.

## Architectural Layers
```
VISUAL BUILDER (Frontend Authoring Interface)
       ↓
WORKFLOW DEFINITION (Pydantic Schema JSON)
       ↓
VALIDATOR & COMPILER (Kahn's Cycle Detection & Deterministic DAG Compilation)
       ↓
POLICY ENGINE REVIEW (Capability Risk Review)
       ↓
IMMUTABLE WORKFLOW VERSION (Published Versioning)
       ↓
AUTHORITATIVE DAG SCHEDULER (Existing Multi-Agent Worker Pipeline)
       ↓
AGENTS / TOOLS / APPROVALS (Existing Execution Kernel)
```

## Constraints & Security Principles
1. **Frontend is purely an authoring interface**: The browser defines nodes and edges. The backend validates, compiles, and executes through existing workers.
2. **No Second Engine**: Workflows leverage `dag_scheduler.create_dag_plan()` directly.
3. **No Arbitrary Code**: Dynamic `eval()`, arbitrary JavaScript, Python, SQL, shell, or arbitrary HTTP request nodes are strictly prohibited.
