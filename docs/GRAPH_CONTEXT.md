# Context Packs & Agent RAG Integration

## ContextPacks
`ContextPack` objects package authorized, bounded subgraphs for consumption by:
- AI Agent Mesh (Sprint 39)
- Decision Intelligence (Sprint 40)
- Search RAG Retrieval (Sprint 38 & 13)

## Expiration & Bounded Context
ContextPacks contain explicit `expires_at` timestamps (default 1 hour) and strictly enforce node limits (`max_nodes=50`) and depth limits (`max_depth=3`) to prevent context window bloat.
