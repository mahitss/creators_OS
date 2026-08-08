from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.home import (
    ExecutiveBriefResponse,
    QuickActionItem,
    ActionLink,
    AttentionItem,
    ActivityItem,
    RecommendationItem,
    LearnedMemoryItem,
    CalendarCommitmentItem,
)
from app.services import mission_service, memory_service, attention_service, calendar_service

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
        QuickActionItem(id="qa-attention", label="Attention Center", href="/attention", icon="🔔"),
        QuickActionItem(id="qa-missions", label="Missions Orchestrator", href="/missions", icon="⚡"),
        QuickActionItem(id="qa-content", label="Studio Content Canvas", href="/content", icon="🎨"),
        QuickActionItem(id="qa-memory", label="Context Vault Memory", href="/memory", icon="🧠"),
    ]

    # 1. Single Source of Truth: Reconcile Attention Engine
    open_attentions, _, _ = await attention_service.list_attention_items(db, workspace_id, status_filter="open")

    needs_attention = []
    primary_rec = None

    for att in open_attentions:
        needs_attention.append(
            AttentionItem(
                id=att["id"],
                title=att["title"],
                context=att["description"],
                why_it_matters="Action required to unblock mission workspace.",
                primary_action=ActionLink(
                    label=att["primary_action"]["label"],
                    href=att["primary_action"]["href"]
                ),
                risk_level=att["severity"].upper()
            )
        )
        if not primary_rec:
            primary_rec = RecommendationItem(
                id=f"rec-{att['id']}",
                title=att["title"],
                reason=att["description"],
                action_label=att["primary_action"]["label"],
                action_href=att["primary_action"]["href"]
            )

    # 2. Workspace Probes for Additional Recommendations
    active_missions, _ = await mission_service.list_workspace_missions(db, workspace_id, status_filter="active")
    all_missions, _ = await mission_service.list_workspace_missions(db, workspace_id, status_filter="all")
    approved_mems, _ = await memory_service.list_memories(db, workspace_id, is_archived=False)

    if not primary_rec and active_missions:
        m_curr = active_missions[0]
        primary_rec = RecommendationItem(
            id=f"rec-continue-{m_curr['id']}",
            title=f"Continue '{m_curr['title']}'",
            reason="Active mission ready for execution.",
            action_label="Open Mission",
            action_href=f"/missions/{m_curr['id']}"
        )

    # 3. Learned Memories Mapping
    learned_memories = [
        LearnedMemoryItem(
            id=m["id"],
            title=m["title"],
            content=m["content"],
            type=m["type"],
            updated_at=m["updated_at"]
        )
        for m in approved_mems[:3]
    ]

    # 4. Today Calendar Commitments
    cal_events, _ = await calendar_service.list_events(db, workspace_id, timeframe="next_7_days")
    today_calendar_events = [
        CalendarCommitmentItem(
            id=ev["id"],
            title=ev["title"],
            start_at=ev["start_at"],
            end_at=ev["end_at"],
            location=ev.get("location")
        )
        for ev in cal_events[:3]
    ]

    # 5. Recent Activity Aggregation
    recent_activity = []
    for m in all_missions[:3]:
        for act in m.get("activities", [])[:2]:
            recent_activity.append(
                ActivityItem(
                    id=act["id"],
                    title=f"{act['action']}: {m['title']}",
                    category="Mission",
                    timestamp=act["created_at"],
                    status="completed"
                )
            )

    # 6. Summary Statement
    if needs_attention:
        summary_statement = f"Vapor requires your decision on {len(needs_attention)} open attention items."
    elif active_missions:
        m_curr = active_missions[0]
        summary_statement = f"Vapor is observing your workspace. '{m_curr['title']}' is active."
    else:
        summary_statement = "Your workspace is clear. Vapor is observing for new mission triggers."

    is_quiet = len(needs_attention) == 0 and len(active_missions) == 0

    return ExecutiveBriefResponse(
        user_name=user_name,
        greeting=greeting,
        summary_statement=summary_statement,
        needs_attention=needs_attention,
        primary_recommendation=primary_rec,
        learned_memories=learned_memories,
        today_calendar_events=today_calendar_events,
        recent_activity=recent_activity[:5],
        quick_actions=quick_actions,
        is_quiet_state=is_quiet,
        is_empty_state=is_quiet,
    )
