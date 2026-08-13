# V1.0 Known Limitations & Workarounds

## Documented System Boundaries
1. **Attestation Expiration Window**: Human control attestations require periodic re-signing upon 90-day evidence expiration windows. Workaround: Continuous notification alerts 14 days prior to expiration.
2. **Telemetry Buffering Under Secondary Region Migration**: Temporary 5-minute latency buffer during active cloud region failover. Workaround: Primary region heartbeat fallback monitoring.
3. **Simulation Data Volume Limits**: Digital Twin counterfactual simulations cap scenario tree depth at 10 levels for real-time latency budgets. Workaround: High-depth simulations run asynchronously in background tasks.
