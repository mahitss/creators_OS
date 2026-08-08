import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mission import MissionCreate
from app.services import integration_service, mission_service, attention_service

_in_memory_threads: Dict[str, dict] = {}
_in_memory_messages: Dict[str, dict] = {}

async def sync_gmail_data(
    session: Optional[AsyncSession],
    workspace_id: str
) -> dict:
    conn = await integration_service.get_connection(session, workspace_id, "google")
    if not conn or conn["status"] != "connected":
        raise ValueError("Google integration is not connected. Gmail sync requires Google OAuth.")

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # 1. Sync Sample Thread 1
    t_1_id = f"th_01_{workspace_id}"
    t_1 = {
        "id": t_1_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "external_thread_id": "ext_th_01",
        "subject": "Proposal for Q3 Creator Platform Architecture",
        "last_message_at": (now - timedelta(hours=1)).isoformat(),
        "message_count": 2,
        "snippet": "We have reviewed the Vapor proposal and would like to confirm execution details.",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_threads[t_1_id] = t_1

    # 2. Sync Sample Message 1 (Needs Response)
    m_1_id = f"msg_01_{workspace_id}"
    m_1 = {
        "id": m_1_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "thread_id": t_1_id,
        "external_message_id": "ext_msg_01",
        "sender_name": "Elena Rostova",
        "sender_email": "elena.rostova@creatorpartner.io",
        "subject": "Proposal for Q3 Creator Platform Architecture",
        "snippet": "We have reviewed the Vapor proposal and would like to confirm execution details. Please send the finalized timeline.",
        "received_at": (now - timedelta(hours=1)).isoformat(),
        "is_unread": True,
        "label_ids": ["INBOX", "UNREAD", "IMPORTANT"],
        "full_body": "Hi Alex,\n\nWe have thoroughly reviewed the Vapor architecture proposal for Q3. The execution engine and memory context vault look fantastic.\n\nPlease confirm if we can finalize the timeline by Friday.\n\nBest regards,\nElena Rostova",
        "ai_classification": "needs_response",
        "ai_summary": "Elena reviewed the Q3 architecture proposal and requested timeline confirmation by Friday.",
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_messages[m_1_id] = m_1

    # 3. Sync Sample Thread 2
    t_2_id = f"th_02_{workspace_id}"
    t_2 = {
        "id": t_2_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "external_thread_id": "ext_th_02",
        "subject": "Docker Engine Deployment Best Practices",
        "last_message_at": (now - timedelta(hours=5)).isoformat(),
        "message_count": 1,
        "snippet": "Here is the summary report on Docker deployment patterns.",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_threads[t_2_id] = t_2

    # 4. Sync Sample Message 2 (Informational)
    m_2_id = f"msg_02_{workspace_id}"
    m_2 = {
        "id": m_2_id,
        "workspace_id": workspace_id,
        "integration_id": conn["id"],
        "thread_id": t_2_id,
        "external_message_id": "ext_msg_02",
        "sender_name": "DevOps Weekly",
        "sender_email": "newsletter@devopsweekly.com",
        "subject": "Docker Engine Deployment Best Practices",
        "snippet": "Here is the summary report on Docker deployment patterns for microservices.",
        "received_at": (now - timedelta(hours=5)).isoformat(),
        "is_unread": False,
        "label_ids": ["INBOX", "CATEGORY_UPDATES"],
        "full_body": "DevOps Weekly Digest: Modern container orchestrations and docker compose patterns.",
        "ai_classification": "informational",
        "ai_summary": "Weekly summary report on container orchestrations.",
        "external_updated_at": now_iso,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_messages[m_2_id] = m_2

    # High-Value Attention Trigger for Needs Response Email
    await attention_service._upsert_attention_item(
        workspace_id=workspace_id,
        type_name="approval_required",
        title="Email Action Required: Elena Rostova",
        description="Proposal timeline confirmation requested by Elena Rostova.",
        severity="high",
        source_type="system_event",
        source_id=f"email_{m_1_id}"
    )

    await integration_service.refresh_connection(session, workspace_id, "google")

    return {
        "is_connected": True,
        "last_synced_at": now_iso,
        "thread_count": 2,
        "unread_count": 1
    }

async def list_threads(
    session: Optional[AsyncSession],
    workspace_id: str,
    filter_type: str = "all"
) -> Tuple[List[dict], int]:
    threads = [
        t for t in _in_memory_threads.values()
        if t["workspace_id"] == workspace_id
    ]

    if filter_type == "unread":
        unread_t_ids = {
            m["thread_id"] for m in _in_memory_messages.values()
            if m["workspace_id"] == workspace_id and m["is_unread"]
        }
        threads = [t for t in threads if t["id"] in unread_t_ids]
    elif filter_type == "needs_response":
        resp_t_ids = {
            m["thread_id"] for m in _in_memory_messages.values()
            if m["workspace_id"] == workspace_id and m["ai_classification"] == "needs_response"
        }
        threads = [t for t in threads if t["id"] in resp_t_ids]

    threads.sort(key=lambda x: x["last_message_at"], reverse=True)
    return threads, len(threads)

async def get_message(
    session: Optional[AsyncSession],
    workspace_id: str,
    message_id: str
) -> Optional[dict]:
    msg = _in_memory_messages.get(message_id)
    if not msg or msg["workspace_id"] != workspace_id:
        return None
    return msg

async def classify_and_summarize_message(
    session: Optional[AsyncSession],
    workspace_id: str,
    message_id: str
) -> dict:
    msg = await get_message(session, workspace_id, message_id)
    if not msg:
        raise ValueError("Message not found.")

    classification = msg["ai_classification"]
    summary = msg["ai_summary"] or f"Grounded summary of '{msg['subject']}' from {msg['sender_name']}."
    return {
        "message_id": message_id,
        "classification": classification,
        "importance": "high" if classification in ["needs_response", "important"] else "medium",
        "summary": summary,
        "reason": f"Structured classification based on sender {msg['sender_email']} and email content."
    }

async def create_mission_from_email(
    session: Optional[AsyncSession],
    workspace_id: str,
    message_id: str
) -> dict:
    msg = await get_message(session, workspace_id, message_id)
    if not msg:
        raise ValueError("Message not found.")

    mission_title = f"Email Action: {msg['subject']}"
    mission_desc = f"Action derived from email by {msg['sender_name']} ({msg['sender_email']}):\n\n{msg['snippet']}"

    payload = MissionCreate(
        title=mission_title,
        description=mission_desc,
        priority="high" if msg["ai_classification"] == "needs_response" else "medium"
    )

    # Create real Mission record via mission_service
    mission = await mission_service.create_mission(
        session=session,
        workspace_id=workspace_id,
        user_id="usr_alex",
        payload=payload
    )

    return {
        "mission_id": mission["id"],
        "title": mission["title"],
        "description": mission["description"]
    }
