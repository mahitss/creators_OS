# Post-Action Verification

`ActionOutcomeObservation` tracks actual state post-execution comparing expected vs actual metrics and variance.

Classifies outcomes as `success`, `partial_success`, `no_effect`, `negative_effect`, or `unknown`. Recommends rollback if negative effects materialize.
