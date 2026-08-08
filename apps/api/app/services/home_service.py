from datetime import datetime, timezone
from app.schemas.home import (
    ExecutiveBriefResponse,
    QuickActionItem,
    ActionLink,
    AttentionItem,
    ActivityItem,
)

def get_time_of_day_greeting(user_name: str) -> str:
    hour = datetime.now(timezone.utc).hour
    if 5 <= hour < 12:
        period = "Good morning"
    elif 12 <= hour < 18:
        period = "Good afternoon"
    else:
        period = "Good evening"
    
    return f"{period}, {user_name}."

async def build_executive_brief(user_name: str = "Alex") -> ExecutiveBriefResponse:
    greeting = get_time_of_day_greeting(user_name)
    
    # Available real navigation actions (no dead buttons)
    quick_actions = [
        QuickActionItem(id="qa-missions", label="Missions Orchestrator", href="/missions", icon="⚡"),
        QuickActionItem(id="qa-content", label="Studio Content Canvas", href="/content", icon="🎨"),
        QuickActionItem(id="qa-memory", label="Context Vault Memory", href="/memory", icon="🧠"),
        QuickActionItem(id="qa-settings", label="System Settings", href="/settings", icon="⚙️"),
    ]

    # Initial state when no background missions or activity logs exist
    return ExecutiveBriefResponse(
        user_name=user_name,
        greeting=greeting,
        summary_statement="Vapor is observing your workspace. All background execution daemons are active.",
        needs_attention=[],
        recent_activity=[],
        quick_actions=quick_actions,
        is_empty_state=True,
    )
