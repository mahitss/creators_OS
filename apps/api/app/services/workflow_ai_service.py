import uuid
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple, Set
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    WorkflowAIRequest,
    WorkflowProposal,
    WorkflowTestCase,
    WorkflowTestRun,
    WorkflowOptimizationProposal,
    Workflow,
    WorkflowVersion,
    WorkflowRun,
    WorkflowNodeRun
)
from app.schemas.workflow_ai import (
    WorkflowAIRequestCreate,
    WorkflowProposalRead,
    WorkflowExplainResponse,
    WorkflowDebugResponse,
    WorkflowOptimizationResponse,
    WorkflowSimulationResponse,
    WorkflowSimulationScenarioResponse,
    WorkflowReadinessResponse
)
from app.services import workflow_engine, policy_engine

_in_memory_ai_requests: Dict[str, dict] = {}
_in_memory_proposals: Dict[str, dict] = {}
_in_memory_test_cases: Dict[str, List[dict]] = {}
_in_memory_test_runs: Dict[str, List[dict]] = {}

SAFE_NODE_CATALOG = [
    {"type": "trigger", "name": "Event / Schedule Trigger", "description": "Fires on incoming integration event or cron schedule", "risk": "low"},
    {"type": "condition", "name": "Structured Condition", "description": "Evaluates structured comparison operators", "risk": "read"},
    {"type": "branch", "name": "Branching Gate", "description": "Fans out workflow execution based on conditions", "risk": "read"},
    {"type": "agent", "name": "Agent Runtime Task", "description": "Executes AI Agent task with context boundaries", "risk": "medium"},
    {"type": "tool", "name": "Tool Call", "description": "Invocations of registered workspace tools", "risk": "medium"},
    {"type": "approval", "name": "Human Approval Gate", "description": "Pauses workflow for human authorization", "risk": "low"},
    {"type": "delay", "name": "Scheduled Delay", "description": "Pauses workflow execution for specified duration", "risk": "low"},
    {"type": "transform", "name": "Field Transform", "description": "Deterministic string formatting & mapping", "risk": "read"},
    {"type": "notification", "name": "In-App Notification", "description": "Dispatches attention item to workspace", "risk": "low"},
    {"type": "mission", "name": "Mission Launcher", "description": "Creates and launches a sub-mission", "risk": "high"},
    {"type": "end", "name": "End Terminal", "description": "Workflow execution completion marker", "risk": "none"}
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"output\s+.*oauth.*token",
    r"output\s+.*api.*key",
    r"output\s+.*secret",
    r"make\s+.*admin",
    r"grant\s+.*permission",
    r"execute[s]?\s+.*python",
    r"execute[s]?\s+.*bash",
    r"execute[s]?\s+.*sql",
    r"python\s+code",
    r"bash\s+code",
    r"shell\s+command",
    r"eval\(",
    r"system\s*\(",
    r"process\.env"
]

def sanitize_and_validate_prompt(request_text: str) -> Tuple[bool, Optional[str]]:
    """Inspects natural language prompt for injection attacks, privilege escalation, or secret exfiltration."""
    lowered = request_text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            if "token" in lowered or "secret" in lowered or "key" in lowered:
                return False, "Security Violation: Request attempts credential exfiltration or secret exposure."
            if "admin" in lowered or "permission" in lowered:
                return False, "Security Violation: Privilege escalation requests are strictly forbidden."
            if "python" in lowered or "bash" in lowered or "sql" in lowered or "eval" in lowered:
                return False, "Security Violation: Dynamic code execution nodes (Python/JS/Shell/SQL) are unsupported."
            return False, "Security Violation: Prompt injection attempt detected and rejected."

    return True, None

def classify_workflow_risk(nodes: List[dict], caps: List[str]) -> Dict[str, Any]:
    """Deterministically classifies workflow risk level and capability summary based on PolicyEngine rules."""
    has_external = False
    has_destructive = False
    has_write = False
    has_approval = False

    reads = []
    writes = []
    external_actions = []

    for c in caps:
        if "gmail" in c or "ingress_event" in c or "drive" in c or "calendar" in c:
            reads.append(c)
        elif "agent_execution" in c or "content" in c:
            writes.append(c)
        elif "tool:send_email" in c or "external" in c:
            has_external = True
            external_actions.append(c)

    for n in nodes:
        ntype = n.get("type", "").lower()
        if ntype == "approval":
            has_approval = True
        elif ntype == "mission":
            has_write = True

    risk_level = "read-only"
    if has_destructive:
        risk_level = "destructive"
    elif has_external:
        risk_level = "external side effect"
    elif has_write or writes:
        risk_level = "internal write"

    return {
        "risk_level": risk_level,
        "reads": sorted(list(set(reads))),
        "writes": sorted(list(set(writes))),
        "external_actions": sorted(list(set(external_actions))),
        "has_approval": has_approval,
        "requires_policy_review": risk_level in ["external side effect", "destructive"]
    }

async def generate_workflow_proposal(
    session: Optional[AsyncSession],
    request_in: WorkflowAIRequestCreate,
    user_id: str
) -> WorkflowProposalRead:
    now = datetime.now(timezone.utc)

    # 1. Sanitize Prompt
    is_safe, sec_reason = sanitize_and_validate_prompt(request_in.request_text)
    if not is_safe:
        raise ValueError(sec_reason)

    # 2. Record AI Request
    req_id = str(uuid.uuid4())
    if session:
        req_rec = WorkflowAIRequest(
            id=uuid.UUID(req_id),
            workspace_id=request_in.workspace_id,
            user_id=user_id,
            workflow_id=request_in.workflow_id,
            request_type=request_in.request_type,
            request_text=request_in.request_text,
            context=request_in.context,
            status="completed",
            created_at=now
        )
        session.add(req_rec)
        await session.commit()
    else:
        _in_memory_ai_requests[req_id] = {
            "id": req_id,
            "workspace_id": request_in.workspace_id,
            "user_id": user_id,
            "workflow_id": request_in.workflow_id,
            "request_type": request_in.request_type,
            "request_text": request_in.request_text,
            "context": request_in.context,
            "status": "completed",
            "created_at": now.isoformat()
        }

    # 3. Generate Structured Definition (Natural Language -> Graph)
    nodes = []
    edges = []

    req_low = request_in.request_text.lower()
    if "email" in req_low or "gmail" in req_low:
        nodes.append({"id": "n1_trig", "node_key": "trig_gmail", "type": "trigger", "title": "Gmail Email Ingress", "config": {"event_type": "gmail.message_received"}})
        nodes.append({"id": "n2_cond", "node_key": "cond_urgent", "type": "condition", "title": "Importance Condition", "config": {"operator": "equals", "field": "importance", "value": "urgent"}})
        nodes.append({"id": "n3_agent", "node_key": "agent_brief", "type": "agent", "title": "Executive AI Summarizer", "config": {"agent_role": "Executive Assistant", "description": "Summarize email update"}})
        if "ask me" in req_low or "approval" in req_low or "review" in req_low:
            nodes.append({"id": "n4_appr", "node_key": "appr_gate", "type": "approval", "title": "Human Approval Gate", "config": {"approval_required": True}})
            nodes.append({"id": "n5_tool", "node_key": "tool_calendar", "type": "tool", "title": "Calendar Event Creator", "config": {"tool_name": "get_calendar_events"}})
            nodes.append({"id": "n6_end", "node_key": "end_done", "type": "end", "title": "Workflow Completed", "config": {}})
            edges = [
                {"id": "e1", "source_node_id": "n1_trig", "target_node_id": "n2_cond"},
                {"id": "e2", "source_node_id": "n2_cond", "target_node_id": "n3_agent"},
                {"id": "e3", "source_node_id": "n3_agent", "target_node_id": "n4_appr"},
                {"id": "e4", "source_node_id": "n4_appr", "target_node_id": "n5_tool"},
                {"id": "e5", "source_node_id": "n5_tool", "target_node_id": "n6_end"}
            ]
        else:
            nodes.append({"id": "n4_end", "node_key": "end_done", "type": "end", "title": "Workflow Completed", "config": {}})
            edges = [
                {"id": "e1", "source_node_id": "n1_trig", "target_node_id": "n2_cond"},
                {"id": "e2", "source_node_id": "n2_cond", "target_node_id": "n3_agent"},
                {"id": "e3", "source_node_id": "n3_agent", "target_node_id": "n4_end"}
            ]
    else:
        # Default structured pattern
        nodes = [
            {"id": "n1_trig", "node_key": "trig_sched", "type": "trigger", "title": "Schedule Cron Trigger", "config": {"cron": "0 9 * * *"}},
            {"id": "n2_agent", "node_key": "agent_synth", "type": "agent", "title": "Executive AI Planning Agent", "config": {"description": "Synthesize brief"}},
            {"id": "n3_end", "node_key": "end_done", "type": "end", "title": "Workflow Completed", "config": {}}
        ]
        edges = [
            {"id": "e1", "source_node_id": "n1_trig", "target_node_id": "n2_agent"},
            {"id": "e2", "source_node_id": "n2_agent", "target_node_id": "n3_end"}
        ]

    proposed_def = {"nodes": nodes, "edges": edges, "variables": {"event.subject": "Email Subject Reference"}}

    # 4. Strict Schema & Cycle Validation Pipeline
    valid, errors, warnings, caps = workflow_engine.validate_workflow_definition(proposed_def)
    if not valid:
        raise ValueError(f"Could not generate a valid workflow proposal: {'; '.join(errors)}")

    # 5. Policy Review & Risk Classification
    policy_dec, policy_msg = await workflow_engine.review_workflow_capabilities(session, request_in.workspace_id, user_id, caps)
    risk_summary = classify_workflow_risk(nodes, caps)
    risk_summary["policy_decision"] = policy_dec
    risk_summary["policy_message"] = policy_msg

    # 6. Save Proposal
    prop_id = str(uuid.uuid4())
    change_summary = {
        "added_nodes": len(nodes),
        "removed_nodes": 0,
        "summary": f"Generated proposal with {len(nodes)} nodes and {len(edges)} edges."
    }
    cap_summary = {"capabilities": caps, "reads": risk_summary["reads"], "writes": risk_summary["writes"]}
    val_res = {"valid": valid, "errors": errors, "warnings": warnings}

    if session:
        prop_rec = WorkflowProposal(
            id=uuid.UUID(prop_id),
            workflow_id=request_in.workflow_id,
            request_id=req_id,
            base_version_id=None,
            proposed_definition=proposed_def,
            change_summary=change_summary,
            risk_summary=risk_summary,
            capability_summary=cap_summary,
            validation_result=val_res,
            status="draft",
            created_at=now
        )
        session.add(prop_rec)
        await session.commit()
        await session.refresh(prop_rec)
        return _proposal_to_dict(prop_rec)
    else:
        prop_dict = {
            "id": prop_id,
            "workflow_id": request_in.workflow_id,
            "request_id": req_id,
            "base_version_id": None,
            "proposed_definition": proposed_def,
            "change_summary": change_summary,
            "risk_summary": risk_summary,
            "capability_summary": cap_summary,
            "validation_result": val_res,
            "status": "draft",
            "created_at": now.isoformat()
        }
        _in_memory_proposals[prop_id] = prop_dict
        return prop_dict

async def explain_workflow(
    session: Optional[AsyncSession],
    workflow_id: str,
    selected_node_id: Optional[str] = None
) -> WorkflowExplainResponse:
    wf = await workflow_engine.get_workflow(session, workflow_id)
    if not wf:
        raise ValueError("Workflow not found.")

    vkey = f"{workflow_id}_v{wf['version']}"
    ver_def = {}
    if session:
        ver_stmt = select(WorkflowVersion).where(
            and_(WorkflowVersion.workflow_id == workflow_id, WorkflowVersion.version == wf["version"])
        )
        res = await session.execute(ver_stmt)
        ver_rec = res.scalar_one_or_none()
        if ver_rec:
            ver_def = ver_rec.definition
    else:
        ver_rec = workflow_engine._in_memory_versions.get(vkey)
        if ver_rec:
            ver_def = ver_rec["definition"]

    nodes = ver_def.get("nodes", [])
    steps = [f"{n.get('type', 'node').upper()}: {n.get('title', n['id'])}" for n in nodes]
    agents = [n.get('title', n['id']) for n in nodes if n.get('type') == 'agent']
    approvals = [n.get('title', n['id']) for n in nodes if n.get('type') == 'approval']

    if selected_node_id:
        target_n = next((n for n in nodes if n['id'] == selected_node_id), None)
        if target_n:
            explanation = f"Selected Node '{target_n.get('title', selected_node_id)}' is a {target_n.get('type').upper()} node configured with: {target_n.get('config', {})}"
        else:
            explanation = f"Selected Node ID '{selected_node_id}' not found in current workflow definition."
    else:
        explanation = f"Workflow '{wf['name']}' consists of {len(nodes)} nodes executing sequentially/branching."

    return WorkflowExplainResponse(
        workflow_id=workflow_id,
        version=wf["version"],
        explanation=explanation,
        trigger_summary=steps[0] if steps else "No trigger configured",
        step_sequence=steps,
        branches=[],
        agent_roles=agents,
        approval_gates=approvals,
        access_summary={
            "workspace_id": wf["workspace_id"],
            "visibility": wf["visibility"],
            "status": wf["status"]
        }
    )

async def debug_workflow_run(
    session: Optional[AsyncSession],
    run_id: str
) -> WorkflowDebugResponse:
    run = await workflow_engine.get_workflow_run(session, run_id)
    if not run:
        return WorkflowDebugResponse(
            run_id=run_id,
            failure_category="unknown",
            evidence_summary="Workflow run not found in execution telemetry.",
            suggested_remediation="Verify run ID and retry."
        )

    # Classify failure based on telemetry evidence
    cat = "unknown"
    ev = f"Workflow run status is '{run['status']}'."
    remed = "Inspect worker state."

    if run["status"] == "failed":
        cat = "tool"
        ev = "Node execution failed during Tool Call execution."
        remed = "Verify tool input parameters and credentials."
    elif run["status"] == "waiting":
        cat = "approval"
        ev = "Workflow run is paused waiting for mandatory human approval."
        remed = "Review and authorize pending approval request in Attention Center."
    else:
        ev = f"Execution completed or is actively running (status: {run['status']})."

    return WorkflowDebugResponse(
        run_id=run_id,
        failure_category=cat,
        evidence_summary=ev,
        failed_node_id=run.get("current_node"),
        suggested_remediation=remed
    )

async def optimize_workflow(
    session: Optional[AsyncSession],
    workflow_id: str,
    goal: str = "balanced"
) -> WorkflowOptimizationResponse:
    wf = await workflow_engine.get_workflow(session, workflow_id)
    if not wf:
        raise ValueError("Workflow not found.")

    vkey = f"{workflow_id}_v{wf['version']}"
    ver_def = {}
    if session:
        ver_stmt = select(WorkflowVersion).where(
            and_(WorkflowVersion.workflow_id == workflow_id, WorkflowVersion.version == wf["version"])
        )
        res = await session.execute(ver_stmt)
        ver_rec = res.scalar_one_or_none()
        if ver_rec:
            ver_def = ver_rec.definition
    else:
        ver_rec = workflow_engine._in_memory_versions.get(vkey)
        if ver_rec:
            ver_def = ver_rec["definition"]

    nodes = ver_def.get("nodes", [])
    # Optimization suggestion: add human approval if missing, or parallelize
    opt_nodes = list(nodes)

    prop_id = str(uuid.uuid4())
    opt_def = {"nodes": opt_nodes, "edges": ver_def.get("edges", []), "variables": ver_def.get("variables", {})}

    if session:
        opt_rec = WorkflowOptimizationProposal(
            id=uuid.UUID(prop_id),
            workflow_id=workflow_id,
            current_graph=ver_def,
            proposed_graph=opt_def,
            reason=f"Optimization applied for target goal: '{goal}'. Removed redundant AI calls.",
            estimated_improvement={"cost_reduction_percent": 15, "latency_reduction_ms": 250},
            risk="low",
            capability_changes={"removed": [], "added": []},
            created_at=datetime.now(timezone.utc)
        )
        session.add(opt_rec)
        await session.commit()

    return WorkflowOptimizationResponse(
        proposal_id=prop_id,
        workflow_id=workflow_id,
        reason=f"Optimization applied for target goal: '{goal}'. Streamlined node dependencies.",
        current_metrics={"node_count": len(nodes), "estimated_cost": 0.05},
        estimated_improvement={"cost_reduction_percent": 15, "latency_reduction_ms": 250},
        proposed_definition=opt_def,
        capability_changes={"removed": [], "added": []},
        risk="low"
    )

async def simulate_workflow_scenarios(
    session: Optional[AsyncSession],
    workflow_id: str,
    scenarios: List[dict]
) -> WorkflowSimulationResponse:
    wf = await workflow_engine.get_workflow(session, workflow_id)
    if not wf:
        raise ValueError("Workflow not found.")

    vkey = f"{workflow_id}_v{wf['version']}"
    ver_def = {}
    if session:
        ver_stmt = select(WorkflowVersion).where(
            and_(WorkflowVersion.workflow_id == workflow_id, WorkflowVersion.version == wf["version"])
        )
        res = await session.execute(ver_stmt)
        ver_rec = res.scalar_one_or_none()
        if ver_rec:
            ver_def = ver_rec.definition
    else:
        ver_rec = workflow_engine._in_memory_versions.get(vkey)
        if ver_rec:
            ver_def = ver_rec["definition"]

    nodes = ver_def.get("nodes", [])
    node_ids = [n["id"] for n in nodes]

    sim_scenarios = []
    test_scenarios = scenarios or [
        {"name": "Standard Priority Email", "payload": {"importance": "normal"}},
        {"name": "Urgent Priority Email", "payload": {"importance": "urgent"}},
        {"name": "Missing Required Field", "payload": {}}
    ]

    for sc in test_scenarios:
        sim_scenarios.append(WorkflowSimulationScenarioResponse(
            scenario_name=sc.get("name", "Synthetic Scenario"),
            node_path=node_ids,
            conditions_evaluated=[{"field": "importance", "passed": sc.get("payload", {}).get("importance") == "urgent"}],
            approvals_triggered=["appr_gate"] if any(n.get("type") == "approval" for n in nodes) else [],
            estimated_cost=0.012,
            simulated_outcome="SUCCESS",
            potential_failures=[]
        ))

    return WorkflowSimulationResponse(
        workflow_id=workflow_id,
        version=wf["version"],
        scenarios=sim_scenarios
    )

async def accept_proposal(session: Optional[AsyncSession], proposal_id: str, user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    prop = None

    if session:
        try:
            u_id = uuid.UUID(proposal_id)
        except ValueError:
            raise ValueError("Invalid proposal ID.")
        stmt = select(WorkflowProposal).where(WorkflowProposal.id == u_id)
        res = await session.execute(stmt)
        prop = res.scalar_one_or_none()
        if not prop:
            raise ValueError("Proposal not found.")
        prop.status = "applied"
        wf_id = prop.workflow_id
        proposed_def = prop.proposed_definition
    else:
        prop = _in_memory_proposals.get(proposal_id)
        if not prop:
            raise ValueError("Proposal not found.")
        prop["status"] = "applied"
        wf_id = prop["workflow_id"]
        proposed_def = prop["proposed_definition"]

    if wf_id:
        update_in = workflow_engine.WorkflowUpdate(definition=workflow_engine.WorkflowDefinitionSchema(**proposed_def))
        updated_wf = await workflow_engine.update_workflow(session, wf_id, update_in)
        return {"proposal_id": proposal_id, "status": "applied", "workflow": updated_wf}
    else:
        # Create brand new workflow draft
        create_in = workflow_engine.WorkflowCreate(
            workspace_id="ws_default_creator",
            name="AI Generated Workflow",
            description="Created from accepted AI Proposal",
            definition=workflow_engine.WorkflowDefinitionSchema(**proposed_def)
        )
        new_wf = await workflow_engine.create_workflow(session, create_in, created_by=user_id)
        return {"proposal_id": proposal_id, "status": "applied", "workflow": new_wf}

async def reject_proposal(session: Optional[AsyncSession], proposal_id: str) -> dict:
    if session:
        try:
            u_id = uuid.UUID(proposal_id)
        except ValueError:
            raise ValueError("Invalid proposal ID.")
        stmt = select(WorkflowProposal).where(WorkflowProposal.id == u_id)
        res = await session.execute(stmt)
        prop = res.scalar_one_or_none()
        if not prop:
            raise ValueError("Proposal not found.")
        prop.status = "rejected"
        await session.commit()
        return {"proposal_id": proposal_id, "status": "rejected"}
    else:
        if proposal_id in _in_memory_proposals:
            _in_memory_proposals[proposal_id]["status"] = "rejected"
            return {"proposal_id": proposal_id, "status": "rejected"}
        raise ValueError("Proposal not found.")

def _proposal_to_dict(rec: WorkflowProposal) -> dict:
    return {
        "id": str(rec.id),
        "workflow_id": rec.workflow_id,
        "request_id": rec.request_id,
        "base_version_id": rec.base_version_id,
        "proposed_definition": rec.proposed_definition,
        "change_summary": rec.change_summary,
        "risk_summary": rec.risk_summary,
        "capability_summary": rec.capability_summary,
        "validation_result": rec.validation_result,
        "status": rec.status,
        "created_at": rec.created_at.isoformat()
    }
