# Control Loop Safety & Degradation Handling

`ControlLoopHealth` tracks signal freshness, decision validity, guardrail health, action success, and outcome quality.

If critical dependencies (Forecast/KPI/ActionGateway) fail, control loops safely degrade to `degraded` or `suspended` mode with human review. Employee profiling or worker surveillance scoring is strictly forbidden.
