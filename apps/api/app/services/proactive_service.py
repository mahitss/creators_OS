import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    SystemEvent,
    AgentTrigger,
    Signal,
    Insight,
    AutomationExecution,
    DeadLetterEvent,
    EventDeduplication
)
from app.schemas.automations import (
    SystemEventCreate,
    AgentTriggerCreate,
    AgentTriggerUpdate,
    DryRunTestResponse
)
from app.services import policy_engine, agent_event_stream
from app.services.policy_engine import PolicyContext

_in_memory_triggers: Dict[str, dict] = {}
_in_memory_events: Dict[str, dict] = {}
_in_memory_dedupe: Dict[str, str] = {}
_in_memory_insights: Dict[str, dict] = {}
_in_memory_executions: Dict[str, dict] = {}
_in_memory_dead_letters: Dict[str, dict] = {}

MAX_PROACTIVE_CHAIN_DEPTH = 5

def generate_dedupe_key(source: str, event_type: str, resource_id: str, occurred_at: Optional[datetime] = None) -> str:
    raw = f"{source}:{event_type}:{resource_id}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def evaluate_structured_condition(condition_key: str, condition_val: Any, metadata: dict) -> bool:
    """Evaluates structured, schema-based conditions without executing dynamic code."""
    if condition_key not in metadata:
        return False
    actual_val = metadata[condition_key]
    
    if isinstance(condition_val, list):
        return actual_val in condition_val
    elif isinstance(condition_val, dict):
        # Support operator comparisons: {"gt": 10}, {"contains": "important"}, etc.
        for op, target in condition_val.items():
            if op == "eq" and actual_val != target:
                return False
            elif op == "neq" and actual_val == target:
                return False
            elif op == "contains" and str(target).lower() not in str(actual_val).lower():
                return False
            elif op == "gt" and not (actual_val > target):
                return False
            elif op == "gte" and not (actual_val >= target):
                return False
            elif op == "lt" and not (actual_val < target):
                return False
            elif op == "lte" and not (actual_val <= target):
                return False
        return True
    else:
        return str(actual_val).strip().lower() == str(condition_val).strip().lower()

async def ingest_event(
    session: Optional[AsyncSession],
    event_data: SystemEventCreate,
    chain_id: Optional[str] = None,
    chain_depth: int = 0
) -> Tuple[dict, bool]:
    """Ingests a raw event, deduplicates, persists, and queues processing asynchronously (Fast ACK)."""
    now = datetime.now(timezone.utc)
    occurred_at = event_data.occurred_at or now
    dedupe_key = event_data.dedupe_key or generate_dedupe_key(
        event_data.source, event_data.event_type, event_data.resource_id, occurred_at
    )

    # 1. Deduplication check
    is_duplicate = False
    if session:
        dedupe_stmt = select(EventDeduplication).where(EventDeduplication.dedupe_key == dedupe_key)
        res = await session.execute(dedupe_stmt)
        if res.scalar_one_or_none():
            is_duplicate = True
    else:
        if dedupe_key in _in_memory_dedupe:
            is_duplicate = True

    if is_duplicate:
        # Return existing idempotently
        event_dict = {
            "id": str(uuid.uuid4()),
            "workspace_id": event_data.workspace_id,
            "source": event_data.source,
            "event_type": event_data.event_type,
            "resource_type": event_data.resource_type,
            "resource_id": event_data.resource_id,
            "actor_id": event_data.actor_id,
            "occurred_at": occurred_at.isoformat(),
            "received_at": now.isoformat(),
            "dedupe_key": dedupe_key,
            "metadata_dict": event_data.metadata_dict,
            "sensitivity": event_data.sensitivity,
            "status": "ignored",
            "created_at": now.isoformat()
        }
        return event_dict, True

    # 2. Store deduplication key
    expires_at = now + timedelta(days=7)
    if session:
        dedupe_rec = EventDeduplication(
            id=uuid.uuid4(),
            dedupe_key=dedupe_key,
            event_id=dedupe_key,
            processed_at=now,
            expires_at=expires_at
        )
        session.add(dedupe_rec)

        event_rec = SystemEvent(
            id=uuid.uuid4(),
            workspace_id=event_data.workspace_id,
            source=event_data.source,
            event_type=event_data.event_type,
            resource_type=event_data.resource_type,
            resource_id=event_data.resource_id,
            actor_id=event_data.actor_id,
            occurred_at=occurred_at,
            received_at=now,
            dedupe_key=dedupe_key,
            metadata_dict=event_data.metadata_dict,
            sensitivity=event_data.sensitivity,
            status="received",
            created_at=now
        )
        session.add(event_rec)
        await session.commit()
        await session.refresh(event_rec)
        event_dict = {
            "id": str(event_rec.id),
            "workspace_id": event_rec.workspace_id,
            "source": event_rec.source,
            "event_type": event_rec.event_type,
            "resource_type": event_rec.resource_type,
            "resource_id": event_rec.resource_id,
            "actor_id": event_rec.actor_id,
            "occurred_at": event_rec.occurred_at.isoformat(),
            "received_at": event_rec.received_at.isoformat(),
            "dedupe_key": event_rec.dedupe_key,
            "metadata_dict": event_rec.metadata_dict,
            "sensitivity": event_rec.sensitivity,
            "status": event_rec.status,
            "created_at": event_rec.created_at.isoformat()
        }
    else:
        event_id = str(uuid.uuid4())
        _in_memory_dedupe[dedupe_key] = event_id
        event_dict = {
            "id": event_id,
            "workspace_id": event_data.workspace_id,
            "source": event_data.source,
            "event_type": event_data.event_type,
            "resource_type": event_data.resource_type,
            "resource_id": event_data.resource_id,
            "actor_id": event_data.actor_id,
            "occurred_at": occurred_at.isoformat(),
            "received_at": now.isoformat(),
            "dedupe_key": dedupe_key,
            "metadata_dict": event_data.metadata_dict,
            "sensitivity": event_data.sensitivity,
            "status": "received",
            "created_at": now.isoformat()
        }
        _in_memory_events[event_id] = event_dict

    # 3. Process event through triggers & signal pipeline
    await process_system_event(session, event_dict, chain_id=chain_id, chain_depth=chain_depth)
    return event_dict, False

async def process_system_event(
    session: Optional[AsyncSession],
    event: dict,
    chain_id: Optional[str] = None,
    chain_depth: int = 0
) -> dict:
    """Processes a system event: signal extraction, insight generation, trigger matching, and policy evaluation."""
    now = datetime.now(timezone.utc)
    workspace_id = event["workspace_id"]
    event_type = event["event_type"]
    event_id = event["id"]
    metadata = event.get("metadata_dict", {})

    chain_id = chain_id or f"chain_{uuid.uuid4().hex[:8]}"

    # 1. Loop Prevention check
    if chain_depth >= MAX_PROACTIVE_CHAIN_DEPTH:
        await _record_execution(
            session=session,
            trigger_id="system_loop_protector",
            event_id=event_id,
            workspace_id=workspace_id,
            decision="denied",
            action_type="block_chain",
            status="loop_blocked",
            reason=f"Proactive event chain depth limit ({MAX_PROACTIVE_CHAIN_DEPTH}) reached.",
            chain_id=chain_id,
            chain_depth=chain_depth
        )
        return event

    # 2. Extract Signal & Insight
    await extract_signal_and_insight(session, event)

    # 3. Find active triggers for workspace & event_type
    triggers = await get_matching_triggers(session, workspace_id, event_type)

    for tr in triggers:
        tr_id = tr["id"]
        conditions = tr.get("conditions", {})
        cooldown_sec = tr.get("cooldown_seconds", 7200)
        action_type = tr.get("action_type", "create_attention")
        created_by = tr.get("created_by", "system")

        # Evaluate structured conditions
        conditions_met = True
        for cond_k, cond_v in conditions.items():
            if not evaluate_structured_condition(cond_k, cond_v, metadata):
                conditions_met = False
                break

        if not conditions_met:
            continue

        # Cooldown check
        last_trig = tr.get("last_triggered_at")
        if last_trig:
            if isinstance(last_trig, str):
                last_trig_dt = datetime.fromisoformat(last_trig)
            else:
                last_trig_dt = last_trig
            if (now - last_trig_dt).total_seconds() < cooldown_sec:
                await _record_execution(
                    session=session,
                    trigger_id=tr_id,
                    event_id=event_id,
                    workspace_id=workspace_id,
                    decision="denied",
                    action_type=action_type,
                    status="cooldown_blocked",
                    reason=f"Trigger is under active cooldown ({cooldown_sec}s).",
                    chain_id=chain_id,
                    chain_depth=chain_depth
                )
                continue

        # Policy Engine Evaluation
        p_context = PolicyContext(
            workspace_id=workspace_id,
            user_id=created_by,
            tool_name=action_type,
            risk_level="HIGH" if action_type in ["create_mission", "start_agent_run"] else "READ",
            autonomy_level="FULL_AUTONOMY",
            resource_scope=tr.get("scope", "workspace")
        )
        p_decision = await policy_engine.evaluate_policy(session, p_context)

        if p_decision.decision == "DENY":
            await _record_execution(
                session=session,
                trigger_id=tr_id,
                event_id=event_id,
                workspace_id=workspace_id,
                decision="denied",
                action_type=action_type,
                status="failed",
                reason=f"PolicyEngine denied trigger execution: {p_decision.reason}",
                chain_id=chain_id,
                chain_depth=chain_depth
            )
            continue

        # Execute Trigger Action
        ins_id = None
        agent_run_id = None
        exec_status = "completed"

        if action_type in ["create_attention", "create_insight"]:
            insight_res = await create_insight(
                session=session,
                workspace_id=workspace_id,
                scope=tr.get("scope", "workspace"),
                source_events={"event_id": event_id, "source": event["source"]},
                title=f"Automated Alert: {tr['name']}",
                summary=metadata.get("summary", f"Proactive trigger '{tr['name']}' fired for {event['event_type']}."),
                importance=metadata.get("importance", "medium"),
                source_references={"resource_id": event["resource_id"], "resource_type": event["resource_type"]}
            )
            ins_id = insight_res["id"]
        elif action_type == "request_approval":
            exec_status = "approval_required"

        # Update last_triggered_at
        await update_trigger_last_triggered(session, tr_id, now)

        await _record_execution(
            session=session,
            trigger_id=tr_id,
            event_id=event_id,
            workspace_id=workspace_id,
            decision="allowed" if p_decision.decision == "ALLOW" else "approval_required",
            action_type=action_type,
            status=exec_status,
            insight_id=ins_id,
            agent_run_id=agent_run_id,
            reason=f"Trigger successfully executed action '{action_type}'.",
            chain_id=chain_id,
            chain_depth=chain_depth + 1
        )

        # Notify via realtime stream
        await agent_event_stream.publish_agent_event(
            event_type="automation_triggered",
            agent_run_id=agent_run_id or "automation",
            mission_id=tr.get("mission_id", "proactive"),
            status=exec_status,
            extra={"trigger_id": tr_id, "trigger_name": tr["name"], "action_type": action_type}
        )

    return event

async def extract_signal_and_insight(session: Optional[AsyncSession], event: dict) -> Optional[dict]:
    """Deterministically extracts signal & generates non-fabricated high-signal insight."""
    event_type = event["event_type"]
    workspace_id = event["workspace_id"]
    metadata = event.get("metadata_dict", {})
    now = datetime.now(timezone.utc)

    # Truthful insight generation logic
    if event_type in ["calendar.event_updated", "gmail.thread_updated"]:
        if metadata.get("is_deadline_change"):
            return await create_insight(
                session=session,
                workspace_id=workspace_id,
                scope="workspace",
                source_events={"event_id": event["id"]},
                title="Schedule Updated",
                summary=metadata.get("summary", f"Schedule change detected for {event['resource_id']}."),
                importance="high",
                source_references={"resource_id": event["resource_id"], "event_type": event_type}
            )
        elif metadata.get("has_conflict"):
            return await create_insight(
                session=session,
                workspace_id=workspace_id,
                scope="workspace",
                source_events={"event_id": event["id"]},
                title="Potential Schedule Conflict Detected",
                summary=metadata.get("summary", "Potential scheduling overlap detected with an existing commitment."),
                importance="high",
                source_references={"resource_id": event["resource_id"]}
            )
    elif event_type == "mission.blocked":
        return await create_insight(
            session=session,
            workspace_id=workspace_id,
            scope="mission",
            source_events={"event_id": event["id"]},
            title="Mission Blocked",
            summary=f"Mission '{metadata.get('title', event['resource_id'])}' requires manual intervention.",
            importance="critical",
            source_references={"mission_id": event["resource_id"]}
        )
    elif event_type == "agent.failed":
        return await create_insight(
            session=session,
            workspace_id=workspace_id,
            scope="workspace",
            source_events={"event_id": event["id"]},
            title="Agent Execution Failed",
            summary=f"Agent run failed: {metadata.get('error', 'Execution error')}.",
            importance="high",
            source_references={"agent_run_id": event["resource_id"]}
        )
    return None

async def create_insight(
    session: Optional[AsyncSession],
    workspace_id: str,
    scope: str,
    source_events: dict,
    title: str,
    summary: str,
    importance: str = "medium",
    confidence: float = 1.0,
    source_references: Optional[dict] = None
) -> dict:
    now = datetime.now(timezone.utc)
    ins_id = str(uuid.uuid4())
    source_refs = source_references or {}

    if session:
        rec = Insight(
            id=uuid.UUID(ins_id),
            workspace_id=workspace_id,
            scope=scope,
            source_events=source_events,
            title=title,
            summary=summary,
            importance=importance,
            confidence=confidence,
            source_references=source_refs,
            status="new",
            created_at=now
        )
        session.add(rec)
        await session.commit()
        await session.refresh(rec)
        return {
            "id": str(rec.id),
            "workspace_id": rec.workspace_id,
            "scope": rec.scope,
            "source_events": rec.source_events,
            "title": rec.title,
            "summary": rec.summary,
            "importance": rec.importance,
            "confidence": rec.confidence,
            "source_references": rec.source_references,
            "status": rec.status,
            "created_at": rec.created_at.isoformat()
        }
    else:
        ins_dict = {
            "id": ins_id,
            "workspace_id": workspace_id,
            "scope": scope,
            "source_events": source_events,
            "title": title,
            "summary": summary,
            "importance": importance,
            "confidence": confidence,
            "source_references": source_refs,
            "status": "new",
            "created_at": now.isoformat()
        }
        _in_memory_insights[ins_id] = ins_dict
        return ins_dict

async def list_workspace_insights(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None
) -> List[dict]:
    if session:
        stmt = select(Insight).where(Insight.workspace_id == workspace_id)
        if status_filter and status_filter != "all":
            stmt = stmt.where(Insight.status == status_filter)
        stmt = stmt.order_by(Insight.created_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [
            {
                "id": str(r.id),
                "workspace_id": r.workspace_id,
                "scope": r.scope,
                "source_events": r.source_events,
                "title": r.title,
                "summary": r.summary,
                "importance": r.importance,
                "confidence": r.confidence,
                "source_references": r.source_references,
                "status": r.status,
                "created_at": r.created_at.isoformat()
            }
            for r in recs
        ]
    else:
        items = [i for i in _in_memory_insights.values() if i["workspace_id"] == workspace_id]
        if status_filter and status_filter != "all":
            items = [i for i in items if i["status"] == status_filter]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

async def update_insight_status(session: Optional[AsyncSession], insight_id: str, status: str) -> Optional[dict]:
    if session:
        try:
            u_id = uuid.UUID(insight_id)
        except ValueError:
            return None
        stmt = select(Insight).where(Insight.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        if rec:
            rec.status = status
            await session.commit()
            await session.refresh(rec)
            return {
                "id": str(rec.id),
                "workspace_id": rec.workspace_id,
                "title": rec.title,
                "status": rec.status
            }
        return None
    else:
        if insight_id in _in_memory_insights:
            _in_memory_insights[insight_id]["status"] = status
            return _in_memory_insights[insight_id]
        return None

async def create_trigger(
    session: Optional[AsyncSession],
    trigger_data: AgentTriggerCreate,
    created_by: str
) -> dict:
    now = datetime.now(timezone.utc)
    tr_id = str(uuid.uuid4())

    if session:
        rec = AgentTrigger(
            id=uuid.UUID(tr_id),
            workspace_id=trigger_data.workspace_id,
            created_by=created_by,
            name=trigger_data.name,
            description=trigger_data.description,
            event_type=trigger_data.event_type,
            conditions=trigger_data.conditions,
            action_type=trigger_data.action_type,
            agent_definition_id=trigger_data.agent_definition_id,
            mission_id=trigger_data.mission_id,
            enabled=True,
            status="active",
            scope=trigger_data.scope,
            cooldown_seconds=trigger_data.cooldown_seconds,
            created_at=now,
            updated_at=now
        )
        session.add(rec)
        await session.commit()
        await session.refresh(rec)
        return _trigger_to_dict(rec)
    else:
        tr_dict = {
            "id": tr_id,
            "workspace_id": trigger_data.workspace_id,
            "created_by": created_by,
            "name": trigger_data.name,
            "description": trigger_data.description,
            "event_type": trigger_data.event_type,
            "conditions": trigger_data.conditions,
            "action_type": trigger_data.action_type,
            "agent_definition_id": trigger_data.agent_definition_id,
            "mission_id": trigger_data.mission_id,
            "enabled": True,
            "status": "active",
            "scope": trigger_data.scope,
            "cooldown_seconds": trigger_data.cooldown_seconds,
            "last_triggered_at": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        _in_memory_triggers[tr_id] = tr_dict
        return tr_dict

async def get_matching_triggers(session: Optional[AsyncSession], workspace_id: str, event_type: str) -> List[dict]:
    if session:
        stmt = select(AgentTrigger).where(
            and_(
                AgentTrigger.workspace_id == workspace_id,
                AgentTrigger.event_type == event_type,
                AgentTrigger.enabled == True,
                AgentTrigger.status == "active"
            )
        )
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [_trigger_to_dict(r) for r in recs]
    else:
        return [
            tr for tr in _in_memory_triggers.values()
            if tr["workspace_id"] == workspace_id and tr["event_type"] == event_type and tr.get("enabled") and tr.get("status") == "active"
        ]

async def list_workspace_triggers(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    if session:
        stmt = select(AgentTrigger).where(
            and_(
                AgentTrigger.workspace_id == workspace_id,
                AgentTrigger.status != "deleted"
            )
        ).order_by(AgentTrigger.created_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [_trigger_to_dict(r) for r in recs]
    else:
        items = [tr for tr in _in_memory_triggers.values() if tr["workspace_id"] == workspace_id and tr.get("status") != "deleted"]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

async def get_trigger(session: Optional[AsyncSession], trigger_id: str) -> Optional[dict]:
    if session:
        try:
            u_id = uuid.UUID(trigger_id)
        except ValueError:
            return None
        stmt = select(AgentTrigger).where(AgentTrigger.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        return _trigger_to_dict(rec) if rec else None
    else:
        return _in_memory_triggers.get(trigger_id)

async def update_trigger(session: Optional[AsyncSession], trigger_id: str, update_data: AgentTriggerUpdate) -> Optional[dict]:
    now = datetime.now(timezone.utc)
    if session:
        try:
            u_id = uuid.UUID(trigger_id)
        except ValueError:
            return None
        stmt = select(AgentTrigger).where(AgentTrigger.id == u_id)
        res = await session.execute(stmt)
        rec = res.scalar_one_or_none()
        if not rec:
            return None
        if update_data.name is not None:
            rec.name = update_data.name
        if update_data.description is not None:
            rec.description = update_data.description
        if update_data.event_type is not None:
            rec.event_type = update_data.event_type
        if update_data.conditions is not None:
            rec.conditions = update_data.conditions
        if update_data.action_type is not None:
            rec.action_type = update_data.action_type
        if update_data.enabled is not None:
            rec.enabled = update_data.enabled
        if update_data.status is not None:
            rec.status = update_data.status
        if update_data.scope is not None:
            rec.scope = update_data.scope
        if update_data.cooldown_seconds is not None:
            rec.cooldown_seconds = update_data.cooldown_seconds
        rec.updated_at = now
        await session.commit()
        await session.refresh(rec)
        return _trigger_to_dict(rec)
    else:
        if trigger_id in _in_memory_triggers:
            tr = _in_memory_triggers[trigger_id]
            for field_name, val in update_data.model_dump(exclude_unset=True).items():
                tr[field_name] = val
            tr["updated_at"] = now.isoformat()
            return tr
        return None

async def update_trigger_last_triggered(session: Optional[AsyncSession], trigger_id: str, ts: datetime):
    if session:
        try:
            u_id = uuid.UUID(trigger_id)
            stmt = select(AgentTrigger).where(AgentTrigger.id == u_id)
            res = await session.execute(stmt)
            rec = res.scalar_one_or_none()
            if rec:
                rec.last_triggered_at = ts
                await session.commit()
        except Exception:
            pass
    else:
        if trigger_id in _in_memory_triggers:
            _in_memory_triggers[trigger_id]["last_triggered_at"] = ts.isoformat()

async def dry_run_trigger(session: Optional[AsyncSession], trigger_id: str, test_payload: dict) -> DryRunTestResponse:
    tr = await get_trigger(session, trigger_id)
    if not tr:
        return DryRunTestResponse(
            matched=False,
            trigger_id=trigger_id,
            trigger_name="Unknown",
            policy_decision="DENY",
            reason="Trigger not found",
            proposed_action="none",
            requires_approval=False,
            cooldown_active=False,
            chain_depth=0
        )

    conditions = tr.get("conditions", {})
    metadata = test_payload.get("metadata_dict", {})
    action_type = tr.get("action_type", "create_attention")

    matched = True
    for cond_k, cond_v in conditions.items():
        if not evaluate_structured_condition(cond_k, cond_v, metadata):
            matched = False
            break

    p_context = PolicyContext(
        workspace_id=tr["workspace_id"],
        user_id=tr["created_by"],
        tool_name=action_type,
        risk_level="HIGH" if action_type in ["create_mission", "start_agent_run"] else "READ",
        resource_scope=tr.get("scope", "workspace")
    )
    p_decision = await policy_engine.evaluate_policy(session, p_context)

    return DryRunTestResponse(
        matched=matched,
        trigger_id=tr["id"],
        trigger_name=tr["name"],
        policy_decision=p_decision.decision,
        reason=f"Dry run simulation completed: {p_decision.reason}",
        proposed_action=action_type,
        requires_approval=p_decision.decision == "APPROVAL_REQUIRED" or action_type in ["create_mission", "start_agent_run"],
        cooldown_active=False,
        chain_depth=1
    )

async def _record_execution(
    session: Optional[AsyncSession],
    trigger_id: str,
    event_id: str,
    workspace_id: str,
    decision: str,
    action_type: str,
    status: str,
    reason: str,
    insight_id: Optional[str] = None,
    agent_run_id: Optional[str] = None,
    chain_id: Optional[str] = None,
    chain_depth: int = 0
):
    now = datetime.now(timezone.utc)
    exec_id = str(uuid.uuid4())

    if session:
        rec = AutomationExecution(
            id=uuid.UUID(exec_id),
            trigger_id=trigger_id,
            event_id=event_id,
            workspace_id=workspace_id,
            decision=decision,
            action_type=action_type,
            status=status,
            insight_id=insight_id,
            agent_run_id=agent_run_id,
            reason=reason,
            chain_id=chain_id,
            chain_depth=chain_depth,
            created_at=now
        )
        session.add(rec)
        await session.commit()
    else:
        _in_memory_executions[exec_id] = {
            "id": exec_id,
            "trigger_id": trigger_id,
            "event_id": event_id,
            "workspace_id": workspace_id,
            "decision": decision,
            "action_type": action_type,
            "status": status,
            "insight_id": insight_id,
            "agent_run_id": agent_run_id,
            "reason": reason,
            "chain_id": chain_id,
            "chain_depth": chain_depth,
            "created_at": now.isoformat()
        }

async def list_trigger_history(session: Optional[AsyncSession], trigger_id: str) -> List[dict]:
    if session:
        stmt = select(AutomationExecution).where(AutomationExecution.trigger_id == trigger_id).order_by(AutomationExecution.created_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [
            {
                "id": str(r.id),
                "trigger_id": r.trigger_id,
                "event_id": r.event_id,
                "workspace_id": r.workspace_id,
                "decision": r.decision,
                "action_type": r.action_type,
                "status": r.status,
                "agent_run_id": r.agent_run_id,
                "insight_id": r.insight_id,
                "reason": r.reason,
                "chain_id": r.chain_id,
                "chain_depth": r.chain_depth,
                "created_at": r.created_at.isoformat()
            }
            for r in recs
        ]
    else:
        items = [ex for ex in _in_memory_executions.values() if ex["trigger_id"] == trigger_id]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

async def list_dead_letters(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    if session:
        stmt = select(DeadLetterEvent).where(DeadLetterEvent.workspace_id == workspace_id).order_by(DeadLetterEvent.created_at.desc())
        res = await session.execute(stmt)
        recs = res.scalars().all()
        return [
            {
                "id": str(r.id),
                "event_id": r.event_id,
                "workspace_id": r.workspace_id,
                "reason": r.reason,
                "error_message": r.error_message,
                "payload": r.payload,
                "created_at": r.created_at.isoformat()
            }
            for r in recs
        ]
    else:
        items = [dl for dl in _in_memory_dead_letters.values() if dl["workspace_id"] == workspace_id]
        return sorted(items, key=lambda x: x["created_at"], reverse=True)

def _trigger_to_dict(rec: AgentTrigger) -> dict:
    return {
        "id": str(rec.id),
        "workspace_id": rec.workspace_id,
        "created_by": rec.created_by,
        "name": rec.name,
        "description": rec.description,
        "event_type": rec.event_type,
        "conditions": rec.conditions,
        "action_type": rec.action_type,
        "agent_definition_id": rec.agent_definition_id,
        "mission_id": rec.mission_id,
        "enabled": rec.enabled,
        "status": rec.status,
        "scope": rec.scope,
        "cooldown_seconds": rec.cooldown_seconds,
        "last_triggered_at": rec.last_triggered_at.isoformat() if rec.last_triggered_at else None,
        "created_at": rec.created_at.isoformat(),
        "updated_at": rec.updated_at.isoformat()
    }
