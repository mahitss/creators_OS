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
from app.services.context_engine import ContextEngine, ContextRequest, ContextPurpose, SourceType

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
        QuickActionItem(id="qa-gmail", label="Email Triage", href="/gmail", icon="✉️"),
        QuickActionItem(id="qa-drive", label="Document Context", href="/drive", icon="📄"),
        QuickActionItem(id="qa-memory", label="Context Vault Memory", href="/memory", icon="🧠"),
    ]

    # Use Unified Context Engine for Executive Brief Context Retrieval
    ctx_req = ContextRequest(
        workspace_id=workspace_id,
        user_id="usr_alex",
        purpose=ContextPurpose.EXECUTIVE_BRIEF,
        allowed_sources=[SourceType.MISSION, SourceType.MEMORY, SourceType.CALENDAR, SourceType.ATTENTION]
    )
    ctx_res = await ContextEngine.retrieve(db, ctx_req)

    # 1. Attention Items
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

    if not primary_rec and active_missions:
        m_curr = active_missions[0]
        primary_rec = RecommendationItem(
            id=f"rec-continue-{m_curr['id']}",
            title=f"Continue '{m_curr['title']}'",
            reason="Active mission ready for execution.",
            action_label="Open Mission",
            action_href=f"/missions/{m_curr['id']}"
        )

    # 3. Learned Memories Mapping from ContextEngine
    mem_items = [it for it in ctx_res.items if it.source_type == SourceType.MEMORY]
    learned_memories = [
        LearnedMemoryItem(
            id=m.source_id,
            title=m.title,
            content=m.content,
            type="insight",
            updated_at=m.updated_at
        )
        for m in mem_items[:3]
    ]

    # 4. Today Calendar Commitments from ContextEngine
    cal_items = [it for it in ctx_res.items if it.source_type == SourceType.CALENDAR]
    today_calendar_events = [
        CalendarCommitmentItem(
            id=c.source_id,
            title=c.title,
            start_at=c.created_at,
            end_at=c.updated_at,
            location="Virtual"
        )
        for c in cal_items[:3]
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
