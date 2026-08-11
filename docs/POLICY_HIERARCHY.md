# Policy Hierarchy & Precedence Rules

Details hierarchy levels and precedence resolution in Vapor OS.

## Precedence Hierarchy
1. **Organization Policies** (Weight: 1000)
2. **Workspace Policies** (Weight: 800)
3. **Team Policies** (Weight: 600)
4. **Agent Policies** (Weight: 400)
5. **Mission Policies** (Weight: 200)
6. **Capability Policies** (Weight: 100)

## Deny Wins Rule
Explicit DENY at a higher hierarchy level overrides ALLOW at lower levels unless an authorized higher-level override exists.
