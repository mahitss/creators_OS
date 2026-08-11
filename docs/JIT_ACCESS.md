# Just-In-Time (JIT) & Temporary Access

Details time-bound permissions in Vapor OS.

## Temporary Grants
- Supports time-bound capability access (`TemporaryAccessGrant`) with `starts_at` and `expires_at`.
- Expired grants are automatically invalidated during policy evaluation.
