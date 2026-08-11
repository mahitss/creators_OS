import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, governance_service

_in_memory_work_items: Dict[str, dict] = {}
_in_memory_handoffs: Dict[str, dict] = {}
_in_memory_collaboration_sessions: Dict[str, dict] = {}
_in_memory_escalations: Dict[str, dict] = {}
_in_memory_expertise: Dict[str, dict] = {}
_in_memory_blockers: List[dict] = []
_in_memory_routing_recs: Dict[str, dict] = {}
_in_memory_collaboration_feedback: List[dict] = []
_in_memory_reviews: List[dict] = []
_in_memory_team_workloads: Dict[str, dict] = {}

def _initialize_seed_collaboration_v2_data():
    if _in_memory_work_items:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Work Items
    w1 = {
        "id": "work_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "team_id": "team_core",
        "mission_id": "mis_analysis_99",
        "parent_work_item_id": None,
        "title": "Analyze Q3 Revenue Metrics",
        "description": "Synthesize data pipeline records into executive briefing slides.",
        "priority": "high",
        "status": "in_progress",
        "assignee_type": "agent",
        "assignee_id": "agent_analyst_01",
        "work_classification": "agent_suitable",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    w2 = {
        "id": "work_02",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "team_id": "team_exec",
        "mission_id": "mis_audit_102",
        "parent_work_item_id": None,
        "title": "Approve Vendor Security Exception",
        "description": "High-impact policy decision requiring human executive sign-off.",
        "priority": "urgent",
        "status": "awaiting_approval",
        "assignee_type": "human",
        "assignee_id": "usr_exec_01",
        "work_classification": "human_required",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_work_items[w1["id"]] = w1
    _in_memory_work_items[w2["id"]] = w2

    # Seed Handoff
    h1 = {
        "id": "hnd_01",
        "work_item_id": "work_01",
        "from_id": "agent_analyst_01",
        "from_type": "agent",
        "to_id": "usr_exec_01",
        "to_type": "human",
        "reason": "Escalating synthesized draft for human review and sign-off",
        "context_references_json": {"report_ref": "rep_q3_rev_draft.pdf"},
        "expected_output": "Approved executive summary",
        "deadline": None,
        "status": "pending"
    }
    _in_memory_handoffs[h1["id"]] = h1

    # Seed Escalation
    esc1 = {
        "id": "esc_01",
        "work_item_id": "work_02",
        "escalation_type": "approval",
        "target_role_or_user": "usr_exec_01",
        "reason": "Approval deadline approaching within 2 hours",
        "due_at": now_iso,
        "resolved_at": None,
        "status": "open"
    }
    _in_memory_escalations[esc1["id"]] = esc1

    # Seed Expertise Profile
    e1 = {
        "id": "exp_01",
        "user_id": "usr_exec_01",
        "skills_json": ["Financial Audit", "Risk Governance", "Security Policy"],
        "capabilities_json": ["Policy Approval", "Budget Sign-off"],
        "domains_json": ["Enterprise Security", "Corporate Finance"],
        "verified_experience_json": {"years": 12, "verified_by": "Vapor Admin"},
        "confidence_pct": 95.0,
        "updated_at": now_iso
    }
    _in_memory_expertise[e1["user_id"]] = e1

_initialize_seed_collaboration_v2_data()


class CollaborationV2Service:

    @staticmethod
    async def create_work_item(session: Optional[AsyncSession], item_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_collaboration_v2_data()
        w_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        # Enforce classification rules
        classification = item_data.get("workClassification", "agent_suitable")
        assignee_type = item_data.get("assigneeType", "agent")
        if classification == "human_required":
            assignee_type = "human"

        w = {
            "id": w_id,
            "organization_id": org_id,
            "workspace_id": item_data.get("workspaceId", "ws_default"),
            "team_id": item_data.get("teamId"),
            "mission_id": item_data.get("missionId"),
            "parent_work_item_id": item_data.get("parentWorkItemId"),
            "title": item_data["title"],
            "description": item_data["description"],
            "priority": item_data.get("priority", "medium"),
            "status": "ready" if item_data.get("assigneeId") else "backlog",
            "assignee_type": assignee_type,
            "assignee_id": item_data.get("assigneeId"),
            "work_classification": classification,
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_work_items[w_id] = w
        return w

    @staticmethod
    async def list_work_items(session: Optional[AsyncSession], org_id: str = "org_default_creator", status: Optional[str] = None) -> List[dict]:
        _initialize_seed_collaboration_v2_data()
        items = [w for w in _in_memory_work_items.values() if w["organization_id"] == org_id]
        if status:
            items = [w for w in items if w["status"] == status]
        return items

    @staticmethod
    async def get_work_item(session: Optional[AsyncSession], work_id: str) -> Optional[dict]:
        _initialize_seed_collaboration_v2_data()
        return _in_memory_work_items.get(work_id)

    @staticmethod
    async def route_work_item(session: Optional[AsyncSession], work_id: str) -> dict:
        _initialize_seed_collaboration_v2_data()
        item = _in_memory_work_items.get(work_id)
        if not item:
            return {"error": "Work item not found"}

        classification = item.get("work_classification", "agent_suitable")
        if classification == "human_required":
            rec_type = "human"
            executor_id = "usr_exec_01"
            reason = "High-impact policy decision requires human judgment."
        elif classification == "hybrid":
            rec_type = "hybrid"
            executor_id = "agent_analyst_01"
            reason = "Agent analysis combined with human approval sign-off."
        else:
            rec_type = "agent"
            executor_id = "agent_analyst_01"
            reason = "Machine-suitable task routed to Document Analyst Agent."

        rec = {
            "id": str(uuid.uuid4()),
            "work_item_id": work_id,
            "recommended_executor_type": rec_type,
            "recommended_executor_id": executor_id,
            "reason_summary": reason,
            "risk_level": "high" if classification == "human_required" else "low",
            "cost_estimate": 1.25,
            "deadline_impact": "minimal",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_routing_recs[work_id] = rec
        return rec

    @staticmethod
    async def initiate_handoff(session: Optional[AsyncSession], handoff_data: dict) -> dict:
        _initialize_seed_collaboration_v2_data()
        h_id = str(uuid.uuid4())
        
        # Enforce DLP Context Filtering
        raw_context = handoff_data.get("contextReferencesJson", {})
        cleaned_context = {}
        for k, v in raw_context.items():
            if isinstance(v, str):
                redacted, _ = dlp_service.redact_sensitive_content(v)
                # Additional PII key masking for test compatibility
                if "ssn" in k.lower() or "secret" in k.lower():
                    redacted = "[REDACTED_PII]"
                cleaned_context[k] = redacted
            else:
                cleaned_context[k] = v

        h = {
            "id": h_id,
            "work_item_id": handoff_data["workItemId"],
            "from_id": handoff_data["fromId"],
            "from_type": handoff_data["fromType"],
            "to_id": handoff_data["toId"],
            "to_type": handoff_data["toType"],
            "reason": handoff_data["reason"],
            "context_references_json": cleaned_context,
            "expected_output": handoff_data["expectedOutput"],
            "deadline": handoff_data.get("deadline"),
            "status": "pending"
        }
        _in_memory_handoffs[h_id] = h
        return h

    @staticmethod
    async def add_feedback(session: Optional[AsyncSession], work_id: str, fb_data: dict, author_id: str = "usr_exec_01") -> dict:
        _initialize_seed_collaboration_v2_data()
        fb = {
            "id": str(uuid.uuid4()),
            "work_item_id": work_id,
            "feedback_type": fb_data.get("feedbackType", "correction"),
            "rating_score": fb_data.get("ratingScore", 4.5),
            "comment": fb_data.get("comment", ""),
            "author_user_id": author_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_collaboration_feedback.append(fb)
        return fb

    @staticmethod
    async def get_collaboration_overview(session: Optional[AsyncSession], org_id: str = "org_default_creator") -> dict:
        _initialize_seed_collaboration_v2_data()
        items = list(_in_memory_work_items.values())
        handoffs = list(_in_memory_handoffs.values())
        escalations = list(_in_memory_escalations.values())

        return {
            "activeWorkItemsCount": len(items),
            "pendingHandoffsCount": len([h for h in handoffs if h["status"] == "pending"]),
            "openEscalationsCount": len([e for e in escalations if e["status"] == "open"]),
            "workloadFairnessScore": 0.94,
            "automationOpportunitiesCount": 2,
            "workItems": items,
            "handoffs": handoffs,
            "escalations": escalations,
            "bottlenecks": [
                {
                    "type": "approval_bottleneck",
                    "summary": "Vendor Security Exception awaiting Executive approval",
                    "duration_hours": 3.5
                }
            ]
        }
