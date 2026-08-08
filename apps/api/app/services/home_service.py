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
)
from app.services import mission_service, memory_service, execution_service

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

    # 1. Deterministic Data Collection
    active_missions, _ = await mission_service.list_workspace_missions(
        db, workspace_id, status_filter="active"
    )
    all_missions, _ = await mission_service.list_workspace_missions(
        db, workspace_id, status_filter="all"
    )
    candidates, _ = await memory_service.list_candidates(db, workspace_id)
    approved_mems, _ = await memory_service.list_memories(db, workspace_id, is_archived=False)

    needs_attention = []
    primary_rec = None

    # Check for active execution states per mission
    for m in active_missions:
        m_id = m["id"]
        exec_data = await execution_service.get_mission_steps_and_execution(db, workspace_id, m_id)
        execution = exec_data.get("execution")
        steps = exec_data.get("steps", [])

        if execution:
            e_status = execution.get("status")
            if e_status == "paused":
                needs_attention.append(
                    AttentionItem(
                        id=f"att-paused-{m_id}",
                        title=f"Execution Paused: '{m['title']}'",
                        context="Execution pipeline is currently paused.",
                        why_it_matters="Execution must be resumed to complete remaining steps.",
                        primary_action=ActionLink(label="Resume Execution", href=f"/missions/{m_id}"),
                        risk_level="HIGH"
                    )
                )
                if not primary_rec:
                    primary_rec = RecommendationItem(
                        id=f"rec-resume-{m_id}",
                        title=f"Resume '{m['title']}' Execution",
                        reason="Execution is paused with ready steps waiting.",
                        action_label="Resume",
                        action_href=f"/missions/{m_id}"
                    )
            elif e_status == "failed":
                needs_attention.append(
                    AttentionItem(
                        id=f"att-failed-{m_id}",
                        title=f"Execution Failed: '{m['title']}'",
                        context="A step in this execution pipeline encountered an error.",
                        why_it_matters="Requires review to resolve or retry.",
                        primary_action=ActionLink(label="Review Failure", href=f"/missions/{m_id}"),
                        risk_level="CRITICAL"
                    )
                )
                if not primary_rec:
                    primary_rec = RecommendationItem(
                        id=f"rec-review-{m_id}",
                        title=f"Review Failed Step in '{m['title']}'",
                        reason="Step failure requires manual attention or retry.",
                        action_label="Open Mission",
                        action_href=f"/missions/{m_id}"
                    )
            elif e_status == "running" or any(s["status"] == "ready" for s in steps):
                if not primary_rec:
                    primary_rec = RecommendationItem(
                        id=f"rec-continue-{m_id}",
                        title=f"Continue '{m['title']}'",
                        reason=f"Pipeline has {sum(1 for s in steps if s['status'] in ['completed', 'skipped'])} of {len(steps)} steps finished.",
                        action_label="Continue Execution",
                        action_href=f"/missions/{m_id}"
                    )

    # Check for pending memory candidates
    if candidates:
        needs_attention.append(
            AttentionItem(
                id="att-candidates-review",
                title=f"{len(candidates)} Memory Candidates Awaiting Review",
                context="Vapor extracted insights from completed missions that require your approval.",
                why_it_matters="Approving candidates teaches Vapor workspace preferences.",
                primary_action=ActionLink(label="Review Memory Candidates", href="/memory"),
                risk_level="MEDIUM"
            )
        )
        if not primary_rec:
            primary_rec = RecommendationItem(
                id="rec-review-candidates",
                title="Review Candidate Memories",
                reason=f"{len(candidates)} candidates are ready for approval in Memory Vault.",
                action_label="Review Memories",
                action_href="/memory"
            )

    # 2. Learned Memories Mapping
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

    # 3. Recent Activity Aggregation
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

    # 4. Deterministic Summary Statement
    if active_missions:
        m_curr = active_missions[0]
        summary_statement = f"Vapor is actively observing your workspace. '{m_curr['title']}' is your primary active mission."
    elif all_missions:
        summary_statement = f"Your workspace has {len(all_missions)} total missions on record. All background daemons are active."
    else:
        summary_statement = "Your workspace is ready. Vapor is observing for new mission triggers."

    # 5. Quiet State Evaluation
    is_quiet = len(needs_attention) == 0 and len(active_missions) == 0

    return ExecutiveBriefResponse(
        user_name=user_name,
        greeting=greeting,
        summary_statement=summary_statement,
        needs_attention=needs_attention,
        primary_recommendation=primary_rec,
        learned_memories=learned_memories,
        recent_activity=recent_activity[:5],
        quick_actions=quick_actions,
        is_quiet_state=is_quiet,
        is_empty_state=is_quiet,
    )
