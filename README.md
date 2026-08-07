# Vapor — The AI Chief of Staff (MVP Specification)

Vapor is an AI Chief of Staff designed to transform work into continuous background execution.

The user spends their time making executive decisions—not organizing work or engineering prompts.

---

## Founding Leadership Team Specifications

- [MVP Product Specification](./MVP_SPECIFICATION.md)

---

## Core Product Highlights

1. **Non-Reactive Executive**: Works continuously in the background, observing repository state and generating dry-run execution proposals.
2. **3 MVP Workspaces**:
   - **Executive Operations Workspace**: Proactive briefing deck & 1-click authorization (`Mod + Enter`).
   - **Studio Canvas Workspace**: Code authoring, diff inspection, and artifact rendering.
   - **Stream Console Workspace**: Multi-pane PTY shell console & live telemetry streams.
3. **Self-Healing Verification Loop**: Automatically runs build/test targets post-execution to guarantee working code before presenting diffs.
