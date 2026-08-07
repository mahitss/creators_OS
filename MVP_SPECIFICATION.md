# Vapor — Official MVP Product Specification

**Authored by the Founding Leadership Team:**
* **CEO**: Vision & Product Positioning
* **CTO**: Engineering Feasibility & Systems Architecture
* **Staff Product Manager**: Scope & User Value Definition
* **Principal Product Designer**: Interaction & Spatial Experience
* **Founding Engineer**: Execution Engine & Sandbox Performance
* **AI Architect**: Executive Intelligence & Background Decision Loops

---

## 1. MVP Vision & Leadership Statement

Vapor is an **AI Chief of Staff** designed to transform raw work streams into background execution. 

Modern professionals do not suffer from a lack of tools or AI capabilities—they suffer from **execution overhead**: the exhausting cycle of organizing work, toggling between applications, writing prompts, copy-pasting stack traces, and manually verifying output.

Vapor fundamentally flips the software paradigm: **The AI works continuously in the background; the human spends their time making executive decisions.**

The MVP is engineered to be small, hyper-cohesive, fast, and reliable—delivering profound delight after just one week of use.

---

## 2. Target User Persona

* **Archetype**: Alex Chen — The "Overwhelmed Solo Builder" / Technical Founder.
* **Age**: 31
* **Profession**: Founder & Lead Product Developer (building a fast-moving software product).
* **Daily Workflow**:
  * Starts day overwhelmed by notifications across GitHub, Linear, Slack, and Email.
  * Toggles endlessly between VS Code, Terminal, Notion, Web Browser, and LLM Chat UIs.
  * Wastes 3–4 hours daily setting up tasks, writing prompts, debugging broken builds, and updating task statuses.
* **Current Tools**: VS Code, Linear, GitHub, iTerm2, Raycast, Claude / ChatGPT Web.
* **Biggest Frustrations**:
  1. *Prompt Engineering Fatigue*: Constant manual typing and re-explaining project architecture to reactive chatbots.
  2. *Context Fragmentation*: Losing focus every time a context switch is required to copy logs or check status.
  3. *Unverified AI Code*: Chatbots output code that fails when copied into the actual project.
* **Technical Skill**: High (Proficient with Git, CLI, Node/Python, APIs).
* **Core Goal**: Spend 90% of time making high-level product decisions, while an intelligent background system manages routine execution mechanics.
* **Why They Switch to Vapor**: Vapor is the only OS-level Chief of Staff that operates non-reactively in the background—transforming raw system events into dry-run execution plans ready for 1-click authorization.

---

## 3. The ONE Core Problem

> **"Execution Overhead & Context Switching Fatigue"**

Solo builders lose over 50% of their cognitive bandwidth to the administrative friction of software development—organizing tasks, reading log traces, copying code, writing prompts, and checking if builds passed.

**Vapor solves this single problem** by placing an autonomous background Executive between the system state and the user. The Executive continuously detects issues, formulates dry-run plans, and presents them for single-click authorization.

---

## 4. Essential Feature Prioritization (MVP Scope)

| Feature | Purpose | User Value | Complexity | Priority | Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Executive Background Sensor** | Monitors FS events, git commits, failing tests, and PTY logs silently. | Eliminates manual prompt engineering; system detects work automatically. | Medium | P0 | **Must Have** |
| **Proactive Proposal Engine** | Generates dry-run execution plans with blast radius and verification targets. | User shifts from manual worker to Chief Executive / Approver. | High | P0 | **Must Have** |
| **1-Click Authorization Deck** | Keyboard-first approval interface (`Mod + Enter`). | Single keystroke authorizes background worker execution. | Low | P0 | **Must Have** |
| **Sandboxed Background Swarm** | Executes approved plan DAG nodes in background PTY processes. | Work gets done in the background without blocking active window. | High | P0 | **Must Have** |
| **Self-Healing Verification Loop** | Auto-runs project build/test targets post-execution. | Prevents broken code; user only receives verified working diffs. | Medium | P0 | **Must Have** |
| **Project Context Vault** | Auto-indexes repository ASTs, docs, and commit history. | Zero re-explaining of architecture or project context. | Medium | P0 | **Must Have** |

---

## 5. MVP Workspaces Specifications

### Workspace 01: Executive Operations Workspace (The Briefing Deck)
* **Purpose**: Primary command center where Executive presents proactive proposals, pending mission dry-runs, and system health status.
* **Primary Action**: Authorize proposed execution plan (`Mod + Enter`) or reject/modify.
* **Objects**: `Proposal` (ID, Title, Blast Radius, Plan DAG, Estimated Cost/Time), `SystemHealth` (Entropy Score, Active Workers), `WalkthroughSummary`.
* **User Flow**: User opens Vapor $\rightarrow$ Reviews top proactive proposal $\rightarrow$ Inspects proposed diff preview $\rightarrow$ Hits `Mod + Enter`.
* **Success State**: Proposal transitions to "Executing in Background" with live progress status badge.
* **Empty State**: "System optimal. Executive is observing workspace." [Badge: 0 Failing Tests, All Builds Passing]
* **Error State**: "Execution plan validation failed. Blast radius exceeds policy bounds." [Button: Inspect Plan Details]

---

### Workspace 02: Studio Canvas Workspace (Creation & Verification)
* **Purpose**: Direct inspection workspace for authoring source code, reviewing side-by-side diffs, and inspecting rendered artifacts.
* **Primary Action**: Accept verified diffs into project working tree.
* **Objects**: `SourceFile`, `DiffView`, `BuildTarget` (Test suite output), `ArtifactPreview`.
* **User Flow**: User switches to Studio (`Mod + 1`) $\rightarrow$ Reviews side-by-side proposed changes $\rightarrow$ Clicks "Accept Diffs into Working Tree".
* **Success State**: Diffs committed cleanly to project filesystem.
* **Empty State**: "No modified files in working tree." [Button: Open Repository Directory]
* **Error State**: "Git merge conflict detected in `src/index.ts`." [Button: Ask Executive to Resolve]

---

### Workspace 03: Stream Console Workspace (Telemetry & Terminal)
* **Purpose**: Operational workspace displaying live background PTY worker terminals and telemetry event log streams.
* **Primary Action**: Observe live command output or open interactive terminal pane.
* **Objects**: `PTYSession`, `LogStreamBuffer`, `WorkerStatus`.
* **User Flow**: User toggles Stream Console (`Mod + ~`) $\rightarrow$ Monitors worker executing test target $\rightarrow$ Toggles back to Studio.
* **Success State**: Terminal displays exit code `0` with clean build logs.
* **Empty State**: "No background worker tasks active." [Button: Open Terminal Session]
* **Error State**: "Worker process exited with code 1." [Button: Stream Stack Trace to Executive]

---

## 6. Out of Scope List (Strictly Excluded for MVP)

To ensure realistic delivery by a small startup team, the following are **explicitly out of scope**:

1. ❌ **Multi-User Collaboration / Team Mode**: Strictly single-player solo builder focus.
2. ❌ **Plugin Ecosystem & Marketplace**: No third-party extension framework.
3. ❌ **Mobile Applications**: Desktop OS environment only (macOS / Windows).
4. ❌ **CRM / Sales / Marketing Modules**: Strictly product development & software execution scope.
5. ❌ **Custom LLM Fine-Tuning Pipelines**: Uses standard frontier LLM APIs (Gemini / Claude / OpenAI).
6. ❌ **Enterprise Administration & SSO**: No SAML, Okta, or multi-tenant RBAC portals.
7. ❌ **In-App Billing & Paywalls**: Flat local API key integration for MVP.
8. ❌ **Complex Visual Workflow Builders**: Text/DAG manifests only; no node-wire dragging UI.
9. ❌ **Chat Application Bots**: No Slack/Discord integration.

---

## 7. The First "Wow Moment"

### Scenario
Alex installs Vapor OS, points it to their active repository directory, and opens the application.

### The Interaction
1. **Zero Prompting**: Alex types nothing into a chat box. They do not write "Fix my code" or "Hello".
2. **Silent Baseline Scan**: Within **8 seconds** of binding the folder, Executive silently runs a background test sweep and detects a broken import and failing unit test in `src/auth/passkey.ts`.
3. **Proactive Briefing**: Executive pops up an unobtrusive, beautiful briefing card in the Executive Operations Deck:
   > **Executive Briefing**: Detected broken import & 1 failing test in `src/auth/passkey.ts`.
   > **Proposed Plan**:
   > 1. Update import specifier in `passkey.ts`
   > 2. Add missing type export in `types.ts`
   > 3. Verify via `npm run test:auth` *(Est: 4s, $0.02)*
   > **`[Press Mod + Enter to Authorize]`**
4. **Single Keystroke**: Alex hits `Mod + Enter`.
5. **Background Execution & Self-Healing**: Executive spawns a background worker, applies the fix, executes `npm run test:auth`, verifies exit code `0`, and displays a green checkmark with a clean 3-line diff summary.
6. **The "Wow" Realization**: Alex realizes they did not write a prompt, copy a stack trace, or leave their editor flow. Software anticipated the problem, designed the plan, executed it, tested it, and solved it with a single keypress.

---

## 8. 7-Day Success Criteria

After 7 days of using Vapor OS, Alex experiences:
* **75% Reduction in Context Switching**: Time spent toggling between chat windows, terminals, and browsers drops from ~3.5 hours/day to < 45 minutes/day.
* **3x Increase in Completed Missions**: Daily completed bug fixes, test additions, and refactors increase by 300%.
* **Near-Zero Manual Prompting**: Over 90% of all AI operations are single-click approvals of Executive proactive proposals.

---

## 9. Founding Team Launch Checklist

* [x] **Product (Staff PM)**: MVP scope locked; non-essential features relegated to Out-of-Scope.
* [x] **Design (Principal Designer)**: 3 MVP Workspaces defined with clear empty, success, and error states.
* [x] **AI Architecture (AI Architect)**: Executive background non-reactive thinking & planning loop specified.
* [x] **Engineering (Founding Engineer)**: Native PTY terminal integration and sandboxed execution loop validated.
* [x] **System (CTO)**: 8-second repository vector ingestion and self-healing test loop verified.
* [x] **Leadership (CEO)**: First "Wow Moment" and 7-day success metrics locked for public launch.
