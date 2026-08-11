# Governed Control Responses

`ControlResponse` defines loop actions (`continue`, `monitor`, `reassess`, `escalate`, `simulate`, `recommend`, `pause`, `rollback`).

Consequential responses pass through `Universal Action Gateway` and `PolicyEngine`. On high uncertainty, loops safely default to `monitor` or `reassess`.
