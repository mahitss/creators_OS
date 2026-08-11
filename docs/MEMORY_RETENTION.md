# Memory Retention & Expiration Policies

`MemoryRetentionPolicy` sets time-to-live (TTL) and auto-expiration rules for workspace memories.

## Controls
- Default TTL: 90 days for unconfirmed derived memories.
- Indefinite retention requires explicit workspace administrative permission.
- Expired memories are excluded from active context retrieval.
