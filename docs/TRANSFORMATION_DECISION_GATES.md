# Transformation Decision Gates & Approval Checkpoints

`TransformationDecisionGate` enforces evidence-based criteria before allowing a transformation program to transition between phases.

Gate outcomes evaluate 5 options (`proceed`, `revise`, `pause`, `stop`, `pilot_more`). Uses existing `Approval` and `PolicyEngine` infrastructure.
