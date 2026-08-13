# Governed Calibration Proposals & Version Rollbacks

## Calibration Lifecycle & Rollbacks
Generates calibration proposals (`TransformationResilienceLearningCalibrationProposal`) requiring governed approval (`draft, review, approved, rejected, applied, rolled_back`). Every applied change creates a versioned `TransformationResilienceLearningCalibrationChange` record and supports immediate rollback (`previousVersion, rollbackReason, rollbackTimestamp, rollbackActor`).
