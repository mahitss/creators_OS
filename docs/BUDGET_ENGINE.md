# Pre-Execution Budget Engine & Race Defense

## Atomic Budget Checks & Reservations
- **Pre-Flight Check**: Pre-flight verification occurs *before* expensive model/tool calls via `check_and_reserve_budget()`.
- **Soft & Hard Limits**:
  - Soft Warning at 75% and 90%.
  - Hard DENY at 100% limit.
- **Race Defense**: Budget reservations atomically deduct estimated funds before worker execution, preventing concurrent workers from double-spending remaining funds.
