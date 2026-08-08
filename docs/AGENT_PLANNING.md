# Vapor OS — Structured Agent Planning Architecture

## 1. Overview
Sprint 23 upgrades Vapor OS execution from linear step sequences into Directed Acyclic Graphs (`PlanNode` DAGs) capable of concurrent read execution, dependency tracking, resource locking, and human-in-the-loop approval gates.

## 2. Hard Limits & Graph Constraints
- Maximum Nodes: **50**
- Maximum Dependencies per Node: **10**
- Maximum Graph Depth: **20**
- Maximum Parallel Concurrent Operations: **5**
- Maximum Replans per AgentRun: **3**

## 3. Plan Node Types
1. `context_retrieval`: Retrieves workspace context via Sprint 19 `ContextEngine`.
2. `analysis`: Combines and evaluates upstream node outputs.
3. `tool_call`: Invokes a `ToolRegistry` tool.
4. `content_generation`: Generates draft content items (`status="draft"`).
5. `approval`: Explicit human approval gate.
6. `merge`: Combines parallel context branches safely.
7. `completion`: Verifies final deliverable criteria.
