# Memory Consolidation Engine

`MemoryConsolidationService` manages background deduplication, merging, and candidate promotion.

## Guardrails
- Merges memories ONLY when scope, source, time, and meaning are fully compatible.
- Identifies duplicate observations and consolidates evidence references.
- Flags incompatible observations as `MemoryConflict` rather than silently overwriting.
