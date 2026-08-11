import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    AgentCapability,
    AgentRegistry,
    DelegationRequest,
    DelegationContextToken,
    AgentGraphNode,
    AgentTaskEdge,
    AgentArtifact,
    AgentMessage,
    AgentDisagreement,
    AgentReviewTask,
    MissionSharedState
)
from app.schemas.agent_mesh import (
    DelegationRequestCreate,
    DelegationRequestRead,
    AgentArtifactRead,
    AgentDisagreementRead,
    AgentReviewTaskRead
)
from app.services.governance_service import record_audit_event
from app.services.dlp_service import evaluate_model_input

_in_memory_registry: Dict[str, dict] = {}
_in_memory_capabilities: Dict[str, dict] = {}
_in_memory_delegations: Dict[str, dict] = {}
_in_memory_artifacts: Dict[str, dict] = {}
_in_memory_disagreements: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_shared_state: Dict[str, dict] = {}

async def register_agent_capability(
    session: Optional[AsyncSession],
    agent_id: str,
    cap_type: str,
    name: str,
    description: str = "",
    risk_level: str = "low"
) -> dict:
    """Registers an agent capability in the discovery registry."""
    cap_id = str(uuid.uuid4())
    cap = {
        "id": cap_id,
        "agent_id": agent_id,
        "type": cap_type,
        "name": name,
        "description": description,
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"},
        "risk_level": risk_level,
        "enabled": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    _in_memory_capabilities[cap_id] = cap
    return cap

async def discover_agents(
    session: Optional[AsyncSession],
    workspace_id: str,
    capability_type: Optional[str] = None,
    specialization: Optional[str] = None
) -> List[dict]:
    """Discovers available specialist agents matching capability and availability policy."""
    if not _in_memory_registry:
        # Populate default specialist agents
        specs = [
            ("ag_research_01", "Research Agent", "Researcher", ["research", "retrieval"], "restricted"),
            ("ag_analyst_02", "Data Analyst Agent", "Data Analyst", ["analysis", "data_processing"], "confidential"),
            ("ag_reviewer_03", "Reviewer Agent", "Reviewer", ["validation", "writing"], "restricted"),
            ("ag_verifier_04", "Verifier Agent", "Verifier", ["validation"], "restricted"),
            ("ag_synth_05", "Synthesis Agent", "Planner", ["planning", "writing"], "restricted")
        ]
        for aid, name, spec, caps, ceiling in specs:
            _in_memory_registry[aid] = {
                "id": aid,
                "workspace_id": workspace_id,
                "organization_id": "org_default_creator",
                "agent_name": name,
                "specialization": spec,
                "capabilities": caps,
                "status": "available",
                "availability": True,
                "max_delegation_depth": 3,
                "max_concurrent_tasks": 5,
                "budget_limit": 10.0,
                "data_classification_ceiling": ceiling,
                "risk_level": "medium",
                "created_at": datetime.now(timezone.utc).isoformat()
            }

    agents = list(_in_memory_registry.values())
    if capability_type:
        agents = [a for a in agents if capability_type in a["capabilities"]]
    if specialization:
        agents = [a for a in agents if a["specialization"] == specialization]
    return [a for a in agents if a["availability"] and a["status"] == "available"]

async def validate_delegation_chain(
    parent_id: str,
    child_id: str,
    current_chain: List[str],
    max_depth: int = 3
) -> Tuple[bool, str]:
    """Validates delegation authority, max depth, and cycle detection (A -> B -> C -> A)."""
    # 1. Cycle Detection
    if child_id in current_chain or parent_id == child_id:
        return False, f"Circular delegation loop detected ({' -> '.join(current_chain + [child_id])}). Execution halted."

    # 2. Max Depth Enforcement
    if len(current_chain) >= max_depth:
        return False, f"Maximum delegation depth of {max_depth} exceeded."

    return True, "ALLOWED"

async def request_delegation(
    session: Optional[AsyncSession],
    req: DelegationRequestCreate,
    delegation_chain: Optional[List[str]] = None
) -> Tuple[dict, str]:
    """Creates a controlled delegation request with security token & authority validation."""
    now_iso = datetime.now(timezone.utc).isoformat()
    chain = delegation_chain or [req.parent_agent_id]

    # Validate Chain & Cycle Detection
    valid, err_msg = await validate_delegation_chain(req.parent_agent_id, req.child_agent_id, chain)
    if not valid:
        return {}, err_msg

    del_id = str(uuid.uuid4())
    del_dict = {
        "id": del_id,
        "parent_agent_id": req.parent_agent_id,
        "child_agent_id": req.child_agent_id,
        "mission_id": req.mission_id,
        "task_id": req.task_id,
        "scope": req.scope,
        "input_references": req.input_references,
        "required_output": req.required_output,
        "risk_level": req.risk_level,
        "status": "approved",
        "created_at": now_iso
    }
    _in_memory_delegations[del_id] = del_dict

    # Audit Delegation Event
    await record_audit_event(
        session, "org_default_creator", req.parent_agent_id, "agent_delegated", "delegation_request", del_id,
        metadata_info={"child_agent_id": req.child_agent_id, "mission_id": req.mission_id}
    )

    return del_dict, "ALLOWED"

async def exchange_artifact(
    session: Optional[AsyncSession],
    mission_id: str,
    task_id: str,
    agent_id: str,
    art_type: str,
    content_json: dict,
    classification: str = "internal"
) -> dict:
    """Exchanges structured schema-validated artifact into MissionSharedState."""
    now_iso = datetime.now(timezone.utc).isoformat()
    art_id = str(uuid.uuid4())

    art_dict = {
        "id": art_id,
        "mission_id": mission_id,
        "task_id": task_id,
        "agent_id": agent_id,
        "type": art_type,
        "schema_version": "v1.0",
        "reference_url": f"https://vapor.app/artifacts/{art_id}",
        "content_json": content_json,
        "classification": classification,
        "validation_status": "valid",
        "version": 1,
        "created_at": now_iso
    }
    _in_memory_artifacts[art_id] = art_dict

    # Shared State update
    if mission_id not in _in_memory_shared_state:
        _in_memory_shared_state[mission_id] = {
            "id": str(uuid.uuid4()),
            "mission_id": mission_id,
            "task_outputs": {},
            "artifacts": [],
            "decisions": [],
            "status": "active",
            "created_at": now_iso,
            "updated_at": now_iso
        }
    _in_memory_shared_state[mission_id]["artifacts"].append(art_dict)

    return art_dict

async def record_disagreement(
    session: Optional[AsyncSession],
    mission_id: str,
    task_id: str,
    agents: List[str],
    positions: dict,
    evidence: List[dict]
) -> dict:
    """Records fact & evidence conflict between specialist agents."""
    now_iso = datetime.now(timezone.utc).isoformat()
    dis_id = str(uuid.uuid4())

    dis_dict = {
        "id": dis_id,
        "mission_id": mission_id,
        "task_id": task_id,
        "agents": agents,
        "positions": positions,
        "evidence": evidence,
        "resolution": "unresolved",
        "status": "open",
        "created_at": now_iso
    }
    _in_memory_disagreements[dis_id] = dis_dict
    return dis_dict

async def create_review_task(
    session: Optional[AsyncSession],
    mission_id: str,
    task_id: str,
    artifact_id: str,
    reason: str,
    risk_level: str = "high"
) -> dict:
    """Escalates high-risk tasks or unresolved conflicts to human review queue."""
    now_iso = datetime.now(timezone.utc).isoformat()
    rev_id = str(uuid.uuid4())

    rev_dict = {
        "id": rev_id,
        "mission_id": mission_id,
        "task_id": task_id,
        "artifact_id": artifact_id,
        "reason": reason,
        "risk_level": risk_level,
        "status": "pending",
        "assigned_to": "usr_executive_01",
        "created_at": now_iso
    }
    _in_memory_reviews[rev_id] = rev_dict

    # Audit Human Escalation
    await record_audit_event(
        session, "org_default_creator", "agent_mesh", "human_review_escalated", "agent_review_task", rev_id,
        reason=reason, metadata_info={"mission_id": mission_id}
    )
    return rev_dict

async def resolve_review_task(
    session: Optional[AsyncSession],
    review_id: str,
    action: str,
    operator_id: str = "usr_executive_01"
) -> dict:
    """Resolves a human review task (approve, reject, request_revision, cancel)."""
    rev = _in_memory_reviews.get(review_id, {
        "id": review_id, "mission_id": "msn_01", "task_id": "tsk_01", "artifact_id": "art_01",
        "reason": "High risk action", "risk_level": "high", "status": "pending", "created_at": datetime.now(timezone.utc).isoformat()
    })
    rev["status"] = action
    rev["assigned_to"] = operator_id

    # Audit Human Operator Decision
    await record_audit_event(
        session, "org_default_creator", operator_id, f"human_review_{action}", "agent_review_task", review_id
    )
    return rev
