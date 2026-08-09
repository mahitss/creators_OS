# Vapor OS — Hybrid Knowledge Retrieval & Ranking

## 1. Hybrid Retrieval Pipeline
```
Query → Scope Filter → Policy Filter → Keyword + Semantic Retrieval → Scope Priority Ranking → Deduplication → Context Budget → Agent
```

## 2. Scope Priority Order
For mission requests:
$$\text{Mission Knowledge} > \text{Attached Sources} > \text{Workspace Knowledge} > \text{Agent Knowledge} > \text{Personal Knowledge (if permitted)}$$
