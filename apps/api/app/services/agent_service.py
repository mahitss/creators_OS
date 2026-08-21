"""Agent Management Service for Kinetiq Agent Runtime V1."""

import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.agent_lifecycle import (
    AgentStatus,
    validate_agent_status_transition,
    InvalidAgentStateTransitionError,
)
from app.schemas.agents import AgentCreate, AgentUpdate, AgentVersionCreate
from packages.database.models import Agent, AgentVersion
from app.services.agent_runtime_engine import (
    _in_memory_agents,
    _in_memory_agent_versions,
    _in_memory_agent_runs
)

logger = logging.getLogger("kinetiq.agent.service")


def _seed_default_workspace_agents(workspace_id: str):
    """Seeds standard authorized enterprise agents for a workspace if uninitialized."""
    if any(a.get("workspace_id") == workspace_id for a in _in_memory_agents.values()):
        return

    now_iso = datetime.now(timezone.utc).isoformat()

    seed_definitions = [
        {
            "id": "ag_revenue_analyst",
            "name": "Revenue Operations Analyst",
            "description": "Analyzes workspace pipelines, conversion rates, and revenue metrics across missions.",
            "system_instructions": "You are the Revenue Operations Analyst for Kinetiq. Inspect missions, deliverables, and financial data to formulate high-impact strategic recommendations.",
            "capabilities": ["reasoning", "retrieval", "analysis"],
            "allowed_tools": ["search_missions", "get_mission", "search_memory", "create_memory_candidate"],
            "allowed_models": ["openrouter/free", "meta-llama/llama-3.3-70b-instruct:free", "deepseek/deepseek-r1:free"],
            "max_steps": 20,
            "max_runtime_seconds": 300,
            "max_token_budget": 100000
        },
        {
            "id": "ag_security_auditor",
            "name": "Security & Architecture Auditor",
            "description": "Validates boundary integrity, tenant isolation, and security compliance.",
            "system_instructions": "You are the Enterprise Security Auditor. Scan active infrastructure, inspect memory boundaries, and detect configuration drift or permission escalation.",
            "capabilities": ["security", "analysis", "reasoning"],
            "allowed_tools": ["search_missions", "get_mission", "search_drive_files", "get_drive_file_content", "send_notification"],
            "allowed_models": ["openrouter/free", "qwen/qwen-2.5-coder-32b-instruct:free"],
            "max_steps": 25,
            "max_runtime_seconds": 300,
            "max_token_budget": 120000
        },
        {
            "id": "ag_content_strategist",
            "name": "Content Studio Orchestrator",
            "description": "Generates technical documentation, video scripts, and executive briefings.",
            "system_instructions": "You are the Executive Content Strategist. Create structured drafts, inspect existing files, and organize deliverables.",
            "capabilities": ["generation", "retrieval", "synthesis"],
            "allowed_tools": ["search_missions", "create_content", "search_drive_files", "get_drive_file_content", "create_calendar_event"],
            "allowed_models": ["openrouter/free", "mistralai/mistral-7b-instruct:free"],
            "max_steps": 20,
            "max_runtime_seconds": 300,
            "max_token_budget": 100000
        }
    ]

    for defn in seed_definitions:
        a_id = defn["id"]
        v_id = f"ver_{a_id}_v1"
        agent_data = {
            "id": a_id,
            "workspace_id": workspace_id,
            "name": defn["name"],
            "description": defn["description"],
            "status": AgentStatus.ACTIVE.value,
            "system_instructions": defn["system_instructions"],
            "capabilities": defn["capabilities"],
            "allowed_tools": defn["allowed_tools"],
            "allowed_models": defn["allowed_models"],
            "max_steps": defn["max_steps"],
            "max_runtime_seconds": defn["max_runtime_seconds"],
            "max_token_budget": defn["max_token_budget"],
            "created_by": "usr_system",
            "created_at": now_iso,
            "updated_at": now_iso,
            "current_version": 1,
            "latest_version_id": v_id
        }
        _in_memory_agents[a_id] = agent_data

        v_data = {
            "id": v_id,
            "agent_id": a_id,
            "workspace_id": workspace_id,
            "version": 1,
            "instructions": defn["system_instructions"],
            "capabilities": defn["capabilities"],
            "tool_policy": {"allowed_tools": defn["allowed_tools"]},
            "model_policy": {"allowed_models": defn["allowed_models"]},
            "limits": {
                "max_steps": defn["max_steps"],
                "max_runtime_seconds": defn["max_runtime_seconds"],
                "max_token_budget": defn["max_token_budget"]
            },
            "created_at": now_iso,
            "created_by": "usr_system"
        }
        _in_memory_agent_versions[a_id] = [v_data]


async def list_agents(
    session: Optional[AsyncSession],
    workspace_id: str,
    status_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Lists agents for workspace with optional status filter."""
    _seed_default_workspace_agents(workspace_id)

    agents = [
        a for a in _in_memory_agents.values()
        if a.get("workspace_id") == workspace_id
    ]

    if status_filter and status_filter.lower() != "all":
        st_norm = status_filter.upper()
        agents = [a for a in agents if a.get("status", "").upper() == st_norm]

    # Attach run counts
    for a in agents:
        runs = [r for r in _in_memory_agent_runs.values() if r.get("agent_id") == a["id"]]
        a["total_runs"] = len(runs)

    return sorted(agents, key=lambda x: x.get("created_at", ""), reverse=True)


async def get_agent_by_id(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_id: str
) -> Optional[Dict[str, Any]]:
    """Retrieves an agent by ID with strict workspace tenant check."""
    _seed_default_workspace_agents(workspace_id)
    agent = _in_memory_agents.get(agent_id)
    if not agent or agent.get("workspace_id") != workspace_id:
        return None

    runs = [r for r in _in_memory_agent_runs.values() if r.get("agent_id") == agent_id]
    agent["total_runs"] = len(runs)
    return agent


async def create_agent(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    payload: AgentCreate
) -> Dict[str, Any]:
    """Creates a new agent in DRAFT or ACTIVE status and creates initial immutable version v1."""
    a_id = str(uuid.uuid4())
    v_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    agent = {
        "id": a_id,
        "workspace_id": workspace_id,
        "name": payload.name,
        "description": payload.description or "",
        "status": AgentStatus.ACTIVE.value,
        "system_instructions": payload.system_instructions,
        "capabilities": payload.capabilities,
        "allowed_tools": payload.allowed_tools,
        "allowed_models": payload.allowed_models,
        "max_steps": payload.max_steps or 20,
        "max_runtime_seconds": payload.max_runtime_seconds or 300,
        "max_token_budget": payload.max_token_budget or 100000,
        "created_by": user_id,
        "created_at": now_iso,
        "updated_at": now_iso,
        "current_version": 1,
        "latest_version_id": v_id,
        "total_runs": 0
    }

    _in_memory_agents[a_id] = agent

    version_v1 = {
        "id": v_id,
        "agent_id": a_id,
        "workspace_id": workspace_id,
        "version": 1,
        "instructions": payload.system_instructions,
        "capabilities": payload.capabilities,
        "tool_policy": {"allowed_tools": payload.allowed_tools},
        "model_policy": {"allowed_models": payload.allowed_models},
        "limits": {
            "max_steps": payload.max_steps or 20,
            "max_runtime_seconds": payload.max_runtime_seconds or 300,
            "max_token_budget": payload.max_token_budget or 100000
        },
        "created_at": now_iso,
        "created_by": user_id
    }
    _in_memory_agent_versions[a_id] = [version_v1]

    # Database persistence if in postgres mode
    if session is not None:
        db_url = os.getenv("DATABASE_URL", "")
        if "postgres" in db_url or "neon.tech" in db_url:
            try:
                db_agent = Agent(
                    id=uuid.UUID(a_id),
                    workspace_id=uuid.UUID(workspace_id),
                    name=payload.name,
                    description=payload.description or "",
                    status=AgentStatus.ACTIVE.value,
                    system_instructions=payload.system_instructions,
                    capabilities=payload.capabilities,
                    allowed_tools=payload.allowed_tools,
                    allowed_models=payload.allowed_models,
                    max_steps=payload.max_steps or 20,
                    max_runtime_seconds=payload.max_runtime_seconds or 300,
                    max_token_budget=payload.max_token_budget or 100000,
                    created_by=user_id
                )
                session.add(db_agent)
            except Exception as exc:
                logger.debug(f"Could not persist Agent to DB: {exc}")

    return agent


async def update_agent(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    agent_id: str,
    payload: AgentUpdate
) -> Dict[str, Any]:
    """Updates agent metadata and creates a new immutable AgentVersion if instructions/policy change."""
    agent = await get_agent_by_id(session, workspace_id, agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found in workspace.")

    now_iso = datetime.now(timezone.utc).isoformat()
    needs_new_version = False

    if payload.name is not None:
        agent["name"] = payload.name
    if payload.description is not None:
        agent["description"] = payload.description
    if payload.status is not None:
        validate_agent_status_transition(agent["status"], payload.status, agent_id)
        agent["status"] = payload.status.upper()

    if payload.system_instructions is not None and payload.system_instructions != agent["system_instructions"]:
        agent["system_instructions"] = payload.system_instructions
        needs_new_version = True
    if payload.capabilities is not None and payload.capabilities != agent["capabilities"]:
        agent["capabilities"] = payload.capabilities
        needs_new_version = True
    if payload.allowed_tools is not None and payload.allowed_tools != agent["allowed_tools"]:
        agent["allowed_tools"] = payload.allowed_tools
        needs_new_version = True
    if payload.allowed_models is not None and payload.allowed_models != agent["allowed_models"]:
        agent["allowed_models"] = payload.allowed_models
        needs_new_version = True
    if payload.max_steps is not None and payload.max_steps != agent["max_steps"]:
        agent["max_steps"] = payload.max_steps
        needs_new_version = True
    if payload.max_runtime_seconds is not None and payload.max_runtime_seconds != agent["max_runtime_seconds"]:
        agent["max_runtime_seconds"] = payload.max_runtime_seconds
        needs_new_version = True
    if payload.max_token_budget is not None and payload.max_token_budget != agent["max_token_budget"]:
        agent["max_token_budget"] = payload.max_token_budget
        needs_new_version = True

    agent["updated_at"] = now_iso

    # If core runtime behavior changed, publish new immutable version
    if needs_new_version:
        versions = _in_memory_agent_versions.get(agent_id, [])
        new_ver_num = len(versions) + 1
        new_ver_id = str(uuid.uuid4())

        new_version = {
            "id": new_ver_id,
            "agent_id": agent_id,
            "workspace_id": workspace_id,
            "version": new_ver_num,
            "instructions": agent["system_instructions"],
            "capabilities": agent["capabilities"],
            "tool_policy": {"allowed_tools": agent["allowed_tools"]},
            "model_policy": {"allowed_models": agent["allowed_models"]},
            "limits": {
                "max_steps": agent["max_steps"],
                "max_runtime_seconds": agent["max_runtime_seconds"],
                "max_token_budget": agent["max_token_budget"]
            },
            "created_at": now_iso,
            "created_by": user_id
        }
        versions.append(new_version)
        _in_memory_agent_versions[agent_id] = versions
        agent["current_version"] = new_ver_num
        agent["latest_version_id"] = new_ver_id

    return agent


async def list_agent_versions(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_id: str
) -> List[Dict[str, Any]]:
    """Returns immutable version history for an agent."""
    agent = await get_agent_by_id(session, workspace_id, agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found in workspace.")

    versions = _in_memory_agent_versions.get(agent_id, [])
    return sorted(versions, key=lambda x: x["version"], reverse=True)


async def create_agent_version(
    session: Optional[AsyncSession],
    workspace_id: str,
    user_id: str,
    agent_id: str,
    payload: AgentVersionCreate
) -> Dict[str, Any]:
    """Explicitly publishes an immutable new AgentVersion."""
    agent = await get_agent_by_id(session, workspace_id, agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found in workspace.")

    now_iso = datetime.now(timezone.utc).isoformat()
    versions = _in_memory_agent_versions.get(agent_id, [])
    new_ver_num = len(versions) + 1
    new_ver_id = str(uuid.uuid4())

    new_version = {
        "id": new_ver_id,
        "agent_id": agent_id,
        "workspace_id": workspace_id,
        "version": new_ver_num,
        "instructions": payload.instructions,
        "capabilities": payload.capabilities,
        "tool_policy": payload.tool_policy,
        "model_policy": payload.model_policy,
        "limits": payload.limits,
        "created_at": now_iso,
        "created_by": user_id
    }
    versions.append(new_version)
    _in_memory_agent_versions[agent_id] = versions

    agent["system_instructions"] = payload.instructions
    agent["capabilities"] = payload.capabilities
    if payload.tool_policy.get("allowed_tools"):
        agent["allowed_tools"] = payload.tool_policy["allowed_tools"]
    if payload.model_policy.get("allowed_models"):
        agent["allowed_models"] = payload.model_policy["allowed_models"]
    if payload.limits.get("max_steps"):
        agent["max_steps"] = payload.limits["max_steps"]
    agent["current_version"] = new_ver_num
    agent["latest_version_id"] = new_ver_id
    agent["updated_at"] = now_iso

    return new_version


async def set_agent_status(
    session: Optional[AsyncSession],
    workspace_id: str,
    agent_id: str,
    target_status: str
) -> Dict[str, Any]:
    """Updates agent status with transition validation."""
    agent = await get_agent_by_id(session, workspace_id, agent_id)
    if not agent:
        raise ValueError(f"Agent {agent_id} not found in workspace.")

    validate_agent_status_transition(agent["status"], target_status, agent_id)
    agent["status"] = target_status.upper()
    agent["updated_at"] = datetime.now(timezone.utc).isoformat()
    return agent
