# Vapor OS — Agent Runtime Security & Permission Model

## 1. No Arbitrary Code Execution
The Agent Runtime strictly forbids raw shell, SQL, Python, JavaScript, or unauthorized HTTP execution.

## 2. Workspace Authorization Boundary
All tool calls and context retrievals enforce strict workspace isolation. Cross-workspace resource access returns 404/Access Denied.

## 3. Public API Restrictions
The browser can create or observe `AgentRun` records. Zero public `/tools/execute` API endpoints exist.
