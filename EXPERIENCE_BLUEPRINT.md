# Vapor OS — Experience Blueprint

**Authored by**: Chief Experience Officer, Vapor  
**Target Audience**: Every Designer, Engineer, Product Manager, and AI Architect building Vapor.

---

## First Principle

> **Every interaction must reduce stress. Never increase cognitive load.**

Vapor is not designed to be operated; it is designed to be experienced. In traditional software, every feature demands attention, configuration, and decision-making. Vapor exists to absorb stress, synthesize chaos into clarity, and return deep focus to human beings.

---

## Part 1: First Launch (Zero Friction Arrival)

### The First 30 Seconds
* **What Happens**: The user opens Vapor for the first time. There is no onboarding wizard, no multi-step slide carousel, no aggressive permission prompts, and no blank canvas paralysis.
* **What They See**: A quiet, dark, ultra-minimal atmosphere. A subtle ambient pulse indicates the system kernel is alive. In the center sits a single, calm statement:  
  *"Vapor is observing your workspace context. Point to your active project folder to begin."*
* **What They Feel**: Immediate relief. No forms to fill out, no onboarding checklists to complete, no setup fatigue.
* **What Information Is Shown**: 
  * Active repository / directory path.
  * System operational status indicator (Ambient Emerald dot).
  * One primary action affordance (`[Bind Directory]`).
* **What Information Is Hidden**: 
  * Complex settings, API key config forms, system logs, tool selectors, and advanced preference toggles.
* **Onboarding Duration**: **12 Seconds**. (Select folder $\rightarrow$ Executive initiates ambient baseline scan).

### What Must NEVER Happen
1. **NEVER** present a blank, empty chat input demanding *"What would you like to do today?"*
2. **NEVER** interrupt the user with popups, feature tour tooltips, or badge notifications.
3. **NEVER** ask the user to manually configure AI parameters, temperature sliders, or model system prompts.

---

## Part 2: First Success (The 3-Minute Magic Moment)

### The Interaction
Within 3 minutes of binding a project directory:
1. Executive silently completes a background AST & health sweep of the workspace.
2. Without a single prompt written by the user, Executive surfaces a sleek, quiet briefing card:
   > **Executive Briefing**: Detected broken import and 1 failing test in `src/auth/passkey.ts`.  
   > **Proposed Plan**: Update import specifier & verify via `npm run test:auth`.  
   > **`[Press Mod + Enter to Authorize]`**
3. The user hits `Mod + Enter`.
4. A quiet 3-second kinetic pulse streams in the background; the test suite executes to exit code `0`, and a clean green checkmark appears alongside a 2-line walkthrough diff summary.

### Why This Moment Is Unforgettable
Traditional software requires the user to discover bugs, write prompts, copy code into chats, paste output back into editors, run terminal commands, and update issue boards manually. 

In Vapor, the software anticipated the problem, prepared the solution, verified the outcome, and executed it with a single keystroke. The user realizes: *"Software has stopped waiting for me to work—it is working for me."*

---

## Part 3: Daily Experience (The 10-Minute Morning Flow)

* **Minute 0 (Silent Arrival)**: User opens laptop. Vapor launches instantaneously in the background. Zero noisy alerts. Zero red badge icons.
* **Minute 1 (The Executive Briefing)**: User opens Vapor (`Mod + Space`). Executive presents a 3-bullet synthesized morning intelligence brief:
  * What changed while you slept (automated dependency updates, green builds).
  * Top 2 high-leverage execution proposals awaiting authorization.
  * System entropy status (100% clean).
* **Minute 3 (Single-Key Approval)**: User reviews the two dry-run proposals, presses `Mod + Enter` twice. Swarm workers dispatch silently into background PTY containers.
* **Minute 5 (Deep Focus Flow)**: User transitions to creative work or high-level strategic decisions. Vapor recedes into ambient space.
* **Minute 10 (Verification & Peace of Mind)**: A subtle, quiet chime signals all background missions are verified and complete. The user has accomplished more before their first cup of coffee than they previously did by noon.

---

## Part 4: Flow & Spatial Navigation

Movement between Vapor's spatial contexts must feel weightless, immediate, and spatial—resembling physical movement through rooms rather than clicking web tabs.

* **Navigation Physics**:
  * Switching spaces uses kinetic sliding transitions ($120\text{ms}$ mass-spring curves).
  * Direct Hotkey Routing: `Mod + 1` (Home), `Mod + 2` (Studio Content), `Mod + 3` (Swarm Mission), `Mod + 4` (Memory Vault).
  * Esc Key Rule: Pressing `Esc` always moves backward towards calmness (collapsing detail views back to Executive Briefing Deck).

---

## Part 5: The Trust Architecture

1. **How Vapor Explains AI Decisions**:
   * Every Executive proposal includes an inspectable **Reasoning Chain** and explicit **Blast Radius** (exact files affected, token cost, duration).
2. **How Vapor Asks for Approval**:
   * Clear, high-contrast dry-run diffs. No destructive operation (deleting files, pushing to production, overwriting working tree) ever executes without explicit 1-click human clearance.
3. **How Vapor Admits Uncertainty**:
   * When Executive confidence falls below 85%, it explicitly states:  
     *"I have identified two potential resolution paths for this architectural issue. Path A is safer; Path B is faster. Which trajectory do you prefer?"*
4. **How Vapor Recovers from Mistakes**:
   * 1-Click Immutable Rollback (`Mod + Z`). Every Executive action creates an automatic git checkpoint. One keypress instantly restores the workspace to its pre-execution state.

---

## Part 6: Micro-Moments of Delight

* **Mission Completed**: A warm emerald pulse surrounds the mission card, accompanied by a subtle 40ms haptic tap.
* **Draft / Refactor Finished**: Side-by-side diff view automatically highlights zero syntax errors with clean, elegant typography.
* **Memory Recalled**: When Executive connects a current bug to a fix applied 3 weeks ago, it quietly notes:  
  *"Recalled solution from Project Core (Nov 14). Applied identical pattern."*
* **Approval Given**: The moment `Mod + Enter` is pressed, the proposal card smoothly morphs into an active, glowing execution telemetry line.
* **Publishing / Build Complete**: A tranquil ambient sound wave plays, leaving the user with a feeling of absolute accomplishment.

---

## Part 7: Long-Term Relationship Evolution

* **Day 1 (Immediate Relief)**: The user experiences their first background dry-run execution. They stop copy-pasting code into chat windows.
* **Day 7 (Deep Trust)**: The morning routine is locked. The user trusts Executive's self-healing test verifications.
* **Day 30 (Spatial Intuition)**: Executive's memory vault has indexed the codebase commit history. Executive anticipates architectural conventions and code style preferences perfectly.
* **Month 6 (Symbiotic Autonomy)**: Vapor has learned the entire project lifecycle. Executive manages routine maintenance, dependency bumps, test coverage, and documentation asynchronously. The user operates purely as strategic Governor.

---

## Part 8: The Ten Experience Principles

1. **Never Surprise the User Negatively**: Every side effect, diff, and command execution must be dry-run previewed before authorization.
2. **Always Explain Important Actions**: AI reasoning is never a mystery; blast radiuses and rationale must always be inspectable.
3. **Respect Human Attention**: Never compete for focus. Notifications are ambient, quiet, and batch-delivered.
4. **Reduce Work, Don't Transfer It**: Never replace manual code editing with manual prompt engineering.
5. **Reward Progress**: Make task completion feel tangible, clean, and deeply satisfying.
6. **Stay Calm**: Avoid high-contrast alert red banners, noisy badges, or frantic UI spinners.
7. **Fail Gracefully and Humbly**: When uncertain, admit it immediately. Never hallucinate confidence.
8. **Provide Instant Reversibility**: Every action must have a zero-risk 1-click rollback guarantee.
9. **Zero Configuration to Delight**: The product must deliver magic within 180 seconds of folder binding without manual setup.
10. **Honor the Executive Role**: The human is the Chief Executive making strategic decisions; Vapor is the untiring Chief of Staff executing them.
