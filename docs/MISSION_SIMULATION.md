# Mission Simulation & Dry-Run Operations

Details plan simulation and dry-run execution in Vapor OS.

## Simulation Framework
- **Pre-Execution Simulation**: High-impact plans are simulated using Sprint 24 Simulation Lab before live execution.
- **Dry-Run Mode**: Side effects are mocked via `ActionGateway` dry-run handlers to evaluate DAG flow, cost, and latency without mutating live state.
