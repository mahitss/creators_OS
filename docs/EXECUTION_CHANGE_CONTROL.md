# Baseline Change Control & Versioning

`ExecutionChangeRequest` manages formal change requests (`scope`, `timeline`, `budget`, `resource`, `dependency`, `quality`).

Material changes require explicit approval workflows. Approved changes generate a new `ExecutionBaseline` while locking previous historical baselines as immutable.
