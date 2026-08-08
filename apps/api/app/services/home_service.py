from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.home import (
    ExecutiveBriefResponse,
    QuickActionItem,
    ActionLink,
    AttentionItem,
    ActivityItem,
)
from app.services import mission_service

def get_time_of_day_greeting(user_name: str) -> str:
    hour = datetime.now(timezone.utc).hour
    if 5 <= hour < 12:
        period = "Good morning"
    elif 12 <= hour < 18:
        period = "Good afternoon"
    else:
        period = "Good evening"
    
    return f"{period}, {user_name}."

async def build_executive_brief(
    db: Optional[AsyncSession] = None,
    user_name: str = "Alex",
    workspace_id: str = "ws_default_01"
) -> ExecutiveBriefResponse:
    greeting = get_time_of_day_greeting(user_name)
    
    quick_actions = [
        QuickActionItem(id="qa-missions", label="Missions Orchestrator", href="/missions", icon="⚡"),
        QuickActionItem(id="qa-content", label="Studio Content Canvas", href="/content", icon="🎨"),
        QuickActionItem(id="qa-memory", label="Context Vault Memory", href="/memory", icon="🧠"),
        QuickActionItem(id="qa-settings", label="System Settings", href="/settings", icon="⚙️"),
    ]

    # Query real active missions from mission service
    active_missions, _ = await mission_service.list_workspace_missions(
        db, workspace_id, status_filter="active"
    )

    needs_attention = []
    recent_activity = []

    for m in active_missions:
        needs_attention.append(
            AttentionItem(
                id=m["id"],
                title=m["title"],
                context=m["description"] or "Active workspace mission requiring decision or execution.",
                why_it_matters=f"Priority set to {m['priority'].upper()}.",
                primary_action=ActionLink(label="Open Mission", href=f"/missions/{m['id']}"),
                risk_level="HIGH" if m["priority"] in ["high", "urgent"] else "LOW"
            )
        )

    is_empty = len(active_missions) == 0

    return ExecutiveBriefResponse(
        user_name=user_name,
        greeting=greeting,
        summary_statement="Vapor is observing your workspace. All background execution daemons are active.",
        needs_attention=needs_attention,
        recent_activity=recent_activity,
        quick_actions=quick_actions,
        is_empty_state=is_empty,
    )
