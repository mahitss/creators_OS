from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import mission_service, content_service, memory_service, attention_service

def _score_match(query_lower: str, title: str, content_desc: str) -> int:
    t_lower = title.lower()
    c_lower = content_desc.lower()

    if query_lower == t_lower:
        return 100
    elif t_lower.startswith(query_lower):
        return 75
    elif query_lower in t_lower:
        return 50
    elif query_lower in c_lower:
        return 25
    return 0

async def global_search(
    session: Optional[AsyncSession],
    workspace_id: str,
    query: str,
    limit: int = 20
) -> Tuple[List[dict], int]:
    if not query or not query.strip():
        return [], 0

    q = query.strip().lower()
    results = []

    # 1. Search Missions
    missions, _ = await mission_service.list_workspace_missions(session, workspace_id, status_filter="all")
    for m in missions:
        score = _score_match(q, m["title"], m["description"])
        if score > 0:
            results.append((
                score,
                m["created_at"],
                {
                    "type": "mission",
                    "id": m["id"],
                    "title": m["title"],
                    "description": m["description"][:160] if m["description"] else "Mission workflow orchestrator.",
                    "url": f"/missions/{m['id']}",
                    "updated_at": m["updated_at"]
                }
            ))

    # 2. Search Content Deliverables
    content_items, _ = await content_service.list_content(session, workspace_id, status_filter="all")
    for c in content_items:
        score = _score_match(q, c["title"], c["content"])
        if score > 0:
            results.append((
                score,
                c["created_at"],
                {
                    "type": "content",
                    "id": c["id"],
                    "title": c["title"],
                    "description": c["content"][:160] if c["content"] else f"{c['type'].upper()} deliverable.",
                    "url": f"/content/{c['id']}",
                    "updated_at": c["updated_at"]
                }
            ))

    # 3. Search Memory Context Vault
    memories, _ = await memory_service.list_memories(session, workspace_id, is_archived=False)
    for mem in memories:
        score = _score_match(q, mem["title"], mem["content"])
        if score > 0:
            results.append((
                score,
                mem["created_at"],
                {
                    "type": "memory",
                    "id": mem["id"],
                    "title": mem["title"],
                    "description": mem["content"][:160] if mem["content"] else f"{mem['type'].upper()} memory.",
                    "url": f"/memory/{mem['id']}",
                    "updated_at": mem["updated_at"]
                }
            ))

    # 4. Search Attention Items
    attention_items, _, _ = await attention_service.list_attention_items(session, workspace_id, status_filter="all")
    for att in attention_items:
        score = _score_match(q, att["title"], att["description"])
        if score > 0:
            results.append((
                score,
                att["created_at"],
                {
                    "type": "attention",
                    "id": att["id"],
                    "title": att["title"],
                    "description": att["description"][:160] if att["description"] else "Attention inbox item.",
                    "url": att["primary_action"]["href"],
                    "updated_at": att["updated_at"]
                }
            ))

    # Rank results by score DESC, then recency DESC
    results.sort(key=lambda x: (x[0], x[1]), reverse=True)
    items = [r[2] for r in results[:limit]]

    # Enrich search items with Semantic Graph relationship context
    for item in items:
        item["relationship_context"] = {
            "entityType": item["type"],
            "relationship": "contains",
            "source": "native",
            "explanation": f"Matched entity '{item['title']}' within workspace relationship context."
        }

    return items, len(items)
