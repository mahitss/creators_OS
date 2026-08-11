# Immutable Audit Architecture

## Immutability Safeguards
`AuditEvent` entries are append-only. Application APIs prohibit `UPDATE` or `DELETE` operations on historical audit records. Adjustments require explicit audit correction entries.
