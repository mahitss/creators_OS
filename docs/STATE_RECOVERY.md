# Durable State Recovery & Split-Brain Locks

Specifies state checkpoint integrity checks and distributed lease locking (`StateLease`).

## Checkpoint Integrity
Checkpoints record state version, execution version, and integrity hashes. Corrupted checkpoints trigger immediate mutation halts and security escalation.
