import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple, Set
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    Workflow,
    WorkflowVersion,
    WorkflowRun,
    WorkflowNodeRun
)
from app.schemas.workflows import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowDefinitionSchema,
    WorkflowValidationResponse,
    WorkflowPublishResponse,
    WorkflowDryRunRequest,
    WorkflowDryRunResponse
)
from app.services import dag_scheduler, dag_validator, policy_engine, agent_event_stream
from app.services.policy_engine import PolicyContext

_in_memory_workflows: Dict[str, dict] = {}
_in_memory_versions: Dict[str, dict] = {}
_in_memory_runs: Dict[str, dict] = {}
_in_memory_node_runs: Dict[str, List[dict]] = {}

MAX_WORKFLOW_NODES = 100
MAX_BRANCH_FANOUT = 10

VALID_NODE_TYPES = {
    "trigger", "condition", "branch", "agent", "tool",
    "approval", "delay", "transform", "notification", "mission", "end"
}

def validate_workflow_definition(definition: dict) -> Tuple[bool, List[str], List[str], List[str]]:
    """Validates visual workflow graph structure, node types, references, and cycle prevention."""
    errors: List[str] = []
    warnings: List[str] = []
    capabilities: Set[str] = set()

    nodes = definition.get("nodes", [])
    edges = definition.get("edges", [])

    if not nodes:
        errors.append("Workflow definition must contain at least one node.")
        return False, errors, warnings, []

    if len(nodes) > MAX_WORKFLOW_NODES:
        errors.append(f"Workflow node count exceeds maximum allowed limit ({len(nodes)} > {MAX_WORKFLOW_NODES}).")
        return False, errors, warnings, []

    node_ids: Set[str] = set()
    node_map: Dict[str, dict] = {}
    has_trigger = False
    has_terminal = False

    for n in nodes:
        nid = n.get("id")
        nkey = n.get("node_key") or nid
        ntype = n.get("type", "").lower()

        if not nid:
            errors.append("All workflow nodes must possess a valid 'id'.")
            continue
        if nid in node_ids:
            errors.append(f"Duplicate node ID '{nid}' detected.")
        node_ids.add(nid)
        node_map[nid] = n

        if ntype not in VALID_NODE_TYPES:
            errors.append(f"Node '{nkey}' has invalid type '{ntype}'. Allowed types: {', '.join(sorted(VALID_NODE_TYPES))}")

        if ntype == "trigger":
            has_trigger = True
            capabilities.add("ingress_event")
        elif ntype == "agent":
            capabilities.add("agent_execution")
        elif ntype == "tool":
            tool_name = n.get("config", {}).get("tool_name", "generic_tool")
            capabilities.add(f"tool:{tool_name}")
        elif ntype == "approval":
            capabilities.add("human_approval")
        elif ntype == "mission":
            capabilities.add("mission_creation")
        elif ntype == "end":
            has_terminal = True

    if not has_trigger:
        errors.append("Workflow must contain at least one Trigger node.")

    if not has_terminal:
        warnings.append("No explicit End node detected in workflow definition.")

    # Validate Edges & Detect Cycles using Kahn's Algorithm
    adj: Dict[str, List[str]] = {nid: [] for nid in node_ids}
    in_degree: Dict[str, int] = {nid: 0 for nid in node_ids}

    for e in edges:
        src = e.get("source_node_id")
        tgt = e.get("target_node_id")

        if src not in node_ids:
            errors.append(f"Edge references non-existent source node '{src}'.")
        if tgt not in node_ids:
            errors.append(f"Edge references non-existent target node '{tgt}'.")
        if src and tgt and src in node_ids and tgt in node_ids:
            if src == tgt:
                errors.append(f"Self-referencing cycle detected on node '{src}'.")
            adj[src].append(tgt)
            in_degree[tgt] += 1

    # Check Branch Fan-Out Limit
    for src, targets in adj.items():
        if len(targets) > MAX_BRANCH_FANOUT:
            errors.append(f"Node '{src}' fan-out count ({len(targets)}) exceeds maximum branch limit ({MAX_BRANCH_FANOUT}).")

    if errors:
        return False, errors, warnings, sorted(list(capabilities))

    # Cycle Detection using Topological Sort Queue
    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    visited_count = 0

    while queue:
        curr = queue.pop(0)
        visited_count += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if visited_count < len(node_ids):
        errors.append("Graph cycle detected. Arbitrary cycles are forbidden in workflow definitions.")
        return False, errors, warnings, sorted(list(capabilities))

    return True, errors, warnings, sorted(list(capabilities))

def compile_workflow_to_dag(definition: dict, workflow_id: str, version: int) -> dict:
    """Compiles visual workflow definition into a deterministic DAG plan for dag_scheduler.py."""
    nodes = definition.get("nodes", [])
    edges = definition.get("edges", [])

    # Map dependencies per target node
    dependencies_map: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    for e in edges:
        src = e.get("source_node_id")
        tgt = e.get("target_node_id")
        if src and tgt and tgt in dependencies_map:
            dependencies_map[tgt].append(src)

    compiled_nodes = []
    for n in nodes:
        nid = n["id"]
        ntype = n.get("type", "tool").lower()
        config = n.get("config", {})
        nkey = n.get("node_key") or nid

        # Map to DAG node format
        dag_type = "tool_call"
        tool_name = config.get("tool_name")
        if ntype == "agent":
            dag_type = "analysis"
        elif ntype == "approval":
            dag_type = "approval"
        elif ntype == "transform":
            dag_type = "content_generation"
        elif ntype == "end":
            dag_type = "completion"

        compiled_nodes.append({
            "node_key": nid,
            "title": n.get("title", nkey),
            "description": config.get("description", f"Node {nkey}"),
            "type": dag_type,
            "dependencies": dependencies_map.get(nid, []),
            "tool_name": tool_name,
            "input_schema": config.get("input_schema", {}),
            "approval_required": ntype == "approval" or config.get("approval_required", False)
        })

    return {
        "compiled_id": f"dag_comp_{uuid.uuid4().hex[:8]}",
        "workflow_id": workflow_id,
        "version": version,
        "nodes": compiled_nodes,
        "compiled_at": datetime.now(timezone.utc).isoformat()
    }

async def review_workflow_capabilities(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    capabilities: List[str]
) -> Tuple[str, str]:
    """Performs capability & risk review against central PolicyEngine."""
    for cap in capabilities:
        if cap.startswith("tool:"):
            tname = cap.split("tool:", 1)[1]
            p_context = PolicyContext(
                workspace_id=workspace_id,
                user_id=user_id,
                tool_name=tname,
                risk_level="WRITE"
            )
            p_decision = await policy_engine.evaluate_policy(session, p_context)
            if p_decision.decision == "DENY":
                return "DENY", f"Capability '{cap}' denied by PolicyEngine: {p_decision.reason}"
    return "ALLOW", "All workflow capabilities verified and approved by PolicyEngine."

async def create_workflow(
    session: Optional[AsyncSession],
    wf_data: WorkflowCreate,
    created_by: str
) -> dict:
    now = datetime.now(timezone.utc)
    wf_id = str(uuid.uuid4())

    def_dict = wf_data.definition.model_dump() if wf_data.definition else {"nodes": [], "edges": [], "variables": {}}

    if session:
        rec = Workflow(
            id=uuid.UUID(wf_id),
            workspace_id=wf_data.workspace_id,
            created_by=created_by,
            name=wf_data.name,
            description=wf_data.description,
            status="draft",
            version=1,
            visibility=wf_data.visibility,
            trigger_config=wf_data.trigger_config,
            created_at=now,
            updated_at=now
        )
        session.add(rec)

        # Initial draft version
        ver_id = str(uuid.uuid4())
        ver_rec = WorkflowVersion(
            id=uuid.UUID(ver_id),
            workflow_id=wf_id,
            version=1,
            definition=def_dict,
            compiled_graph={},
            capabilities=[],
            created_by=created_by,
            status="draft",
            created_at=now
        )
        session.add(ver_rec)
        await session.commit()
        await session.refresh(rec)
        return _workflow_to_dict(rec)
    else:
        wf_dict = {
            "id": wf_id,
            "workspace_id": wf_data.workspace_id,
            "created_by": created_by,
            "name": wf_data.name,
            "description": wf_data.description,
            "status": "draft",
            "version": 1,
            "visibility": wf_data.visibility,
            "trigger_config": wf_data.trigger_config,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        _in_memory_workflows[wf_id] = wf_dict
        _in_memory_versions[f"{wf_id}_v1"] = {
            "id": str(uuid.uuid4()),
            "workflow_id": wf_id,
            "version": 1,
            "definition": def_dict,
            "compiled_graph": {},
            "capabilities": [],
            "created_by": created_by,
            "status": "draft",
            "created_at": now.isoformat(),
            "published_at": None
        }
        return wf_dict

async def get_workflow(session: Optional[AsyncSession], workflow_id: str) -> Optional[dict]:
    if session:
        try:
            u_id = uuid.UUID(workflow_id)
        except ValueError:
            return None
        stmt = select(Workflow).where(Workflow.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        return _workflow_to_dict(rec) if rec else None
    else:
        return _in_memory_workflows.get(workflow_id)

async def list_workspace_workflows(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    if session:
        stmt = select(Workflow).where(
            and_(Workflow.workspace_id == workspace_id, Workflow.status != "deleted")
        ).order_by(Workflow.updated_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [_workflow_to_dict(r) for r in recs]
    else:
        items = [w for w in _in_memory_workflows.values() if w["workspace_id"] == workspace_id and w.get("status") != "deleted"]
        return sorted(items, key=lambda x: x["updated_at"], reverse=True)

async def update_workflow(session: Optional[AsyncSession], workflow_id: str, update_data: WorkflowUpdate) -> Optional[dict]:
    now = datetime.now(timezone.utc)
    if session:
        try:
            u_id = uuid.UUID(workflow_id)
        except ValueError:
            return None
        stmt = select(Workflow).where(Workflow.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        if not rec:
            return None

        if update_data.name is not None:
            rec.name = update_data.name
        if update_data.description is not None:
            rec.description = update_data.description
        if update_data.status is not None:
            rec.status = update_data.status
        if update_data.visibility is not None:
            rec.visibility = update_data.visibility
        if update_data.trigger_config is not None:
            rec.trigger_config = update_data.trigger_config

        if update_data.definition is not None:
            # Create a draft version update
            def_dict = update_data.definition.model_dump()
            ver_stmt = select(WorkflowVersion).where(
                and_(WorkflowVersion.workflow_id == workflow_id, WorkflowVersion.version == rec.version)
            )
            ver_res = await session.execute(ver_stmt)
            ver_rec = ver_res.scalar_one_or_none()
            if ver_rec and ver_rec.status == "draft":
                ver_rec.definition = def_dict
            else:
                # Increment draft version
                rec.version += 1
                new_ver = WorkflowVersion(
                    id=uuid.uuid4(),
                    workflow_id=workflow_id,
                    version=rec.version,
                    definition=def_dict,
                    compiled_graph={},
                    capabilities=[],
                    created_by=rec.created_by,
                    status="draft",
                    created_at=now
                )
                session.add(new_ver)

        rec.updated_at = now
        await session.commit()
        await session.refresh(rec)
        return _workflow_to_dict(rec)
    else:
        if workflow_id in _in_memory_workflows:
            wf = _in_memory_workflows[workflow_id]
            for fk, fv in update_data.model_dump(exclude_unset=True).items():
                if fk != "definition":
                    wf[fk] = fv
            wf["updated_at"] = now.isoformat()

            if update_data.definition:
                vkey = f"{workflow_id}_v{wf['version']}"
                if vkey in _in_memory_versions and _in_memory_versions[vkey]["status"] == "draft":
                    _in_memory_versions[vkey]["definition"] = update_data.definition.model_dump()
                else:
                    wf["version"] += 1
                    new_vkey = f"{workflow_id}_v{wf['version']}"
                    _in_memory_versions[new_vkey] = {
                        "id": str(uuid.uuid4()),
                        "workflow_id": workflow_id,
                        "version": wf["version"],
                        "definition": update_data.definition.model_dump(),
                        "compiled_graph": {},
                        "capabilities": [],
                        "created_by": wf["created_by"],
                        "status": "draft",
                        "created_at": now.isoformat(),
                        "published_at": None
                    }
            return wf
        return None

async def publish_workflow(session: Optional[AsyncSession], workflow_id: str, user_id: str) -> WorkflowPublishResponse:
    now = datetime.now(timezone.utc)
    wf = await get_workflow(session, workflow_id)
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
        ver_rec = _in_memory_versions.get(vkey)
        if ver_rec:
            ver_def = ver_rec["definition"]

    valid, errors, warnings, caps = validate_workflow_definition(ver_def)
    if not valid:
        raise ValueError(f"Workflow validation failed: {'; '.join(errors)}")

    policy_dec, policy_msg = await review_workflow_capabilities(session, wf["workspace_id"], user_id, caps)
    if policy_dec == "DENY":
        raise ValueError(f"Policy Engine review denied publication: {policy_msg}")

    compiled = compile_workflow_to_dag(ver_def, workflow_id, wf["version"])
    ver_id_str = str(uuid.uuid4())

    if session:
        if ver_rec:
            ver_rec.compiled_graph = compiled
            ver_rec.capabilities = caps
            ver_rec.status = "published"
            ver_rec.published_at = now
            ver_id_str = str(ver_rec.id)

        # Update Workflow status
        u_id = uuid.UUID(workflow_id)
        wf_stmt = select(Workflow).where(Workflow.id == u_id)
        wf_res = await session.execute(wf_stmt)
        w_rec = wf_res.scalar_one_or_none()
        if w_rec:
            w_rec.status = "active"
            w_rec.updated_at = now
        await session.commit()
    else:
        if ver_rec:
            ver_rec["compiled_graph"] = compiled
            ver_rec["capabilities"] = caps
            ver_rec["status"] = "published"
            ver_rec["published_at"] = now.isoformat()
            ver_id_str = ver_rec["id"]
        _in_memory_workflows[workflow_id]["status"] = "active"
        _in_memory_workflows[workflow_id]["updated_at"] = now.isoformat()

    return WorkflowPublishResponse(
        workflow_id=workflow_id,
        version=wf["version"],
        workflow_version_id=ver_id_str,
        capabilities=caps,
        published_at=now
    )

async def dry_run_workflow(session: Optional[AsyncSession], workflow_id: str, test_payload: dict) -> WorkflowDryRunResponse:
    wf = await get_workflow(session, workflow_id)
    if not wf:
        return WorkflowDryRunResponse(
            simulated=False,
            workflow_id=workflow_id,
            version=0,
            evaluated_nodes=[],
            proposed_actions=[],
            capabilities_required=[],
            requires_approval=False,
            policy_decision="DENY",
            reason="Workflow not found."
        )

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
        ver_rec = _in_memory_versions.get(vkey)
        if ver_rec:
            ver_def = ver_rec["definition"]

    valid, errors, warnings, caps = validate_workflow_definition(ver_def)
    if not valid:
        return WorkflowDryRunResponse(
            simulated=False,
            workflow_id=workflow_id,
            version=wf["version"],
            evaluated_nodes=[],
            proposed_actions=[],
            capabilities_required=caps,
            requires_approval=False,
            policy_decision="DENY",
            reason=f"Simulation aborted due to validation errors: {'; '.join(errors)}"
        )

    evaluated_nodes = []
    proposed_actions = []
    requires_approval = False

    for n in ver_def.get("nodes", []):
        ntype = n.get("type", "tool").lower()
        evaluated_nodes.append({"id": n["id"], "type": ntype, "status": "simulated"})
        if ntype in ["agent", "tool", "approval", "mission"]:
            proposed_actions.append({"node_id": n["id"], "action": ntype, "config": n.get("config", {})})
        if ntype in ["approval", "mission"]:
            requires_approval = True

    policy_dec, policy_msg = await review_workflow_capabilities(session, wf["workspace_id"], wf["created_by"], caps)

    return WorkflowDryRunResponse(
        simulated=True,
        workflow_id=workflow_id,
        version=wf["version"],
        evaluated_nodes=evaluated_nodes,
        proposed_actions=proposed_actions,
        capabilities_required=caps,
        requires_approval=requires_approval,
        policy_decision=policy_dec,
        reason=f"Workflow dry-run simulation successful: {policy_msg}"
    )

async def run_workflow(session: Optional[AsyncSession], workflow_id: str, trigger_event_id: Optional[str] = None) -> dict:
    now = datetime.now(timezone.utc)
    wf = await get_workflow(session, workflow_id)
    if not wf:
        raise ValueError("Workflow not found.")

    vkey = f"{workflow_id}_v{wf['version']}"
    ver_id_str = str(uuid.uuid4())
    compiled_graph = {}
    if session:
        ver_stmt = select(WorkflowVersion).where(
            and_(WorkflowVersion.workflow_id == workflow_id, WorkflowVersion.version == wf["version"])
        )
        res = await session.execute(ver_stmt)
        ver_rec = res.scalar_one_or_none()
        if ver_rec:
            ver_id_str = str(ver_rec.id)
            compiled_graph = ver_rec.compiled_graph
    else:
        ver_rec = _in_memory_versions.get(vkey)
        if ver_rec:
            ver_id_str = ver_rec["id"]
            compiled_graph = ver_rec.get("compiled_graph", {})

    run_id = str(uuid.uuid4())

    if session:
        rec = WorkflowRun(
            id=uuid.UUID(run_id),
            workflow_id=workflow_id,
            workflow_version_id=ver_id_str,
            workspace_id=wf["workspace_id"],
            trigger_event_id=trigger_event_id,
            status="running",
            started_at=now,
            created_at=now,
            updated_at=now
        )
        session.add(rec)
        await session.commit()
        await session.refresh(rec)
        run_dict = _run_to_dict(rec)
    else:
        run_dict = {
            "id": run_id,
            "workflow_id": workflow_id,
            "workflow_version_id": ver_id_str,
            "workspace_id": wf["workspace_id"],
            "trigger_event_id": trigger_event_id,
            "status": "running",
            "started_at": now.isoformat(),
            "completed_at": None,
            "current_node": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        _in_memory_runs[run_id] = run_dict

    # Pass to existing DAG Scheduler
    if compiled_graph and compiled_graph.get("nodes"):
        try:
            await dag_scheduler.create_dag_plan(
                session=session,
                workspace_id=wf["workspace_id"],
                mission_id=f"wf_mission_{run_id[:8]}",
                goal=f"Workflow Run: {wf['name']}",
                nodes=compiled_graph["nodes"]
            )
        except Exception:
            pass

    await agent_event_stream.publish_agent_event(
        event_type="workflow_run_started",
        agent_run_id=run_id,
        mission_id=workflow_id,
        status="running"
    )

    return run_dict

async def list_workflow_runs(session: Optional[AsyncSession], workflow_id: str) -> List[dict]:
    if session:
        stmt = select(WorkflowRun).where(WorkflowRun.workflow_id == workflow_id).order_by(WorkflowRun.created_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [_run_to_dict(r) for r in recs]
    else:
        items = [r for r in _in_memory_runs.values() if r["workflow_id"] == workflow_id]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

async def get_workflow_run(session: Optional[AsyncSession], run_id: str) -> Optional[dict]:
    if session:
        try:
            u_id = uuid.UUID(run_id)
        except ValueError:
            return None
        stmt = select(WorkflowRun).where(WorkflowRun.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        return _run_to_dict(rec) if rec else None
    else:
        return _in_memory_runs.get(run_id)

def _workflow_to_dict(rec: Workflow) -> dict:
    return {
        "id": str(rec.id),
        "workspace_id": rec.workspace_id,
        "created_by": rec.created_by,
        "name": rec.name,
        "description": rec.description,
        "status": rec.status,
        "version": rec.version,
        "visibility": rec.visibility,
        "trigger_config": rec.trigger_config,
        "created_at": rec.created_at.isoformat(),
        "updated_at": rec.updated_at.isoformat()
    }

def _run_to_dict(rec: WorkflowRun) -> dict:
    return {
        "id": str(rec.id),
        "workflow_id": rec.workflow_id,
        "workflow_version_id": rec.workflow_version_id,
        "workspace_id": rec.workspace_id,
        "trigger_event_id": rec.trigger_event_id,
        "status": rec.status,
        "started_at": rec.started_at.isoformat() if rec.started_at else None,
        "completed_at": rec.completed_at.isoformat() if rec.completed_at else None,
        "current_node": rec.current_node,
        "created_at": rec.created_at.isoformat(),
        "updated_at": rec.updated_at.isoformat()
    }
