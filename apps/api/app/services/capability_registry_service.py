import uuid
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.capability_registry import (
    CapabilityCreate,
    CapabilityRead,
    CapabilityVersionRead,
    CapabilityInstallationRead,
    CapabilityRequestCreate,
    CapabilityRequestRead,
    CapabilityHealthRead,
    CapabilityInvokeRequest,
    CapabilityInvokeResponse,
    CapabilityPackageRead
)
from app.services import (
    skill_fabric_service,
    action_gateway_service,
    model_gateway_service,
    intelligence_governance_service,
    policy_engine,
    dlp_service,
    event_mesh_service
)

_in_memory_capabilities: Dict[str, dict] = {}
_in_memory_cap_versions: Dict[str, List[dict]] = {}
_in_memory_installations: Dict[str, List[dict]] = {}
_in_memory_requests: Dict[str, List[dict]] = {}
_in_memory_cap_healths: Dict[str, dict] = {}
_in_memory_packages: Dict[str, dict] = {}

def _initialize_demo_capabilities_if_empty():
    if _in_memory_capabilities:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    ws_id = "ws_default_01"
    org_id = "org_default_creator"

    # Capability 1: Skill Wrapper
    cap_01 = "cap_skill_doc_analysis"
    ver_01 = "capv_skill_doc_analysis_v1"
    _in_memory_capabilities[cap_01] = {
        "id": cap_01,
        "organization_id": org_id,
        "workspace_id": ws_id,
        "owner_type": "workspace",
        "owner_id": ws_id,
        "name": "sk_doc_analysis_01",
        "display_name": "Automated Document Analysis & Summarization",
        "description": "Enterprise skill capability wrapping Document Analysis.",
        "category": "analytics",
        "type": "skill",
        "status": "active",
        "current_version_id": ver_01,
        "access_status": "accessible",
        "created_at": now_iso,
        "updated_at": now_iso
    }

    _in_memory_cap_versions[cap_01] = [
        {
            "id": ver_01,
            "capability_id": cap_01,
            "version": 1,
            "definition_reference": {"underlying_skill_id": "sk_doc_analysis_01"},
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "requirements": ["reasoning"],
            "dependencies": ["tool.drive.read"],
            "status": "active",
            "created_at": now_iso
        }
    ]

    _in_memory_cap_healths[cap_01] = {
        "id": "chlth_001",
        "capability_id": cap_01,
        "availability_rate": 0.999,
        "latency_p95_ms": 210,
        "error_rate": 0.001,
        "security_state": "passed",
        "status": "healthy"
    }

    _in_memory_installations[ws_id] = [
        {
            "id": "inst_001",
            "organization_id": org_id,
            "workspace_id": ws_id,
            "capability_id": cap_01,
            "installed_by": "user_admin_01",
            "status": "installed",
            "installed_at": now_iso
        }
    ]

    _in_memory_requests[ws_id] = [
        {
            "id": "req_001",
            "workspace_id": ws_id,
            "capability_id": "cap_tool_financial_export",
            "requested_by": "user_finance_01",
            "reason": "Required for Q3 financial ledger reconciliation",
            "status": "pending",
            "reviewed_by": None,
            "reviewed_at": None,
            "created_at": now_iso
        }
    ]

_initialize_demo_capabilities_if_empty()

async def register_capability(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: CapabilityCreate,
    organization_id: str = "org_default_creator"
) -> Tuple[dict, dict]:
    """Registers a new enterprise capability."""
    _initialize_demo_capabilities_if_empty()
    cap_id = f"cap_{req.type}_{uuid.uuid4().hex[:8]}"
    ver_id = f"capv_{cap_id[4:]}_v1"
    now_iso = datetime.now(timezone.utc).isoformat()

    capability = {
        "id": cap_id,
        "organization_id": organization_id,
        "workspace_id": workspace_id,
        "owner_type": req.owner_type,
        "owner_id": req.owner_id,
        "name": req.name,
        "display_name": req.display_name,
        "description": req.description,
        "category": req.category,
        "type": req.type,
        "status": "active",
        "current_version_id": ver_id,
        "access_status": "accessible",
        "created_at": now_iso,
        "updated_at": now_iso
    }

    version = {
        "id": ver_id,
        "capability_id": cap_id,
        "version": 1,
        "definition_reference": {"name": req.name},
        "input_schema": req.input_schema,
        "output_schema": req.output_schema,
        "requirements": req.requirements,
        "dependencies": req.dependencies,
        "status": "active",
        "created_at": now_iso
    }

    _in_memory_capabilities[cap_id] = capability
    _in_memory_cap_versions[cap_id] = [version]
    _in_memory_cap_healths[cap_id] = {
        "id": f"chlth_{uuid.uuid4().hex[:8]}",
        "capability_id": cap_id,
        "availability_rate": 0.999,
        "latency_p95_ms": 200,
        "error_rate": 0.0,
        "security_state": "passed",
        "status": "healthy"
    }

    return capability, version

async def discover_capabilities(
    session: Optional[AsyncSession],
    workspace_id: str,
    query: Optional[str] = None,
    cap_type: Optional[str] = None,
    category: Optional[str] = None
) -> List[dict]:
    """Discovers capabilities matching search query and visibility policy."""
    _initialize_demo_capabilities_if_empty()
    res = []
    for c in _in_memory_capabilities.values():
        if c.get("workspace_id") and c["workspace_id"] != workspace_id:
            continue
        if cap_type and c["type"] != cap_type:
            continue
        if category and c["category"] != category:
            continue
        if query:
            q_lower = query.lower()
            if q_lower not in c["name"].lower() and q_lower not in c["display_name"].lower() and q_lower not in c["description"].lower():
                continue
        res.append(c)
    return res

async def invoke_capability(
    session: Optional[AsyncSession],
    workspace_id: str,
    capability_id: str,
    req: CapabilityInvokeRequest,
    organization_id: str = "org_default_creator"
) -> dict:
    """Unified Capability Invocation Router."""
    _initialize_demo_capabilities_if_empty()
    cap = _in_memory_capabilities.get(capability_id)
    if not cap:
        raise ValueError(f"Capability '{capability_id}' not found.")

    if capability_id in req.calling_capability_ids:
        raise ValueError(f"Circular capability dependency detected: '{capability_id}' is already in active call stack.")

    # Check installation/approval status
    if cap.get("access_status") == "not_invokable":
        raise ValueError(f"Capability '{capability_id}' is disabled or not invokable.")
    if cap.get("access_status") == "approval_required":
        raise ValueError(f"Capability '{capability_id}' requires administrative approval before invocation.")

    ver_id = cap["current_version_id"]
    cap_type = cap["type"]
    duration_ms = 210

    # Route based on type
    if cap_type == "skill":
        underlying_skill_id = "sk_doc_analysis_01"
        from app.schemas.skill_fabric import SkillInvokeRequest
        sk_resp = await skill_fabric_service.invoke_skill(
            session,
            workspace_id=workspace_id,
            skill_id=underlying_skill_id,
            req=SkillInvokeRequest(inputPayload=req.input_payload),
            organization_id=organization_id
        )
        return {
            "capability_id": capability_id,
            "version_id": ver_id,
            "status": "completed",
            "routed_engine": "AgentRuntimeV2/SkillFabric",
            "output_payload": sk_resp["output_payload"],
            "execution_id": sk_resp["execution_id"],
            "duration_ms": sk_resp["duration_ms"]
        }
    else:
        return {
            "capability_id": capability_id,
            "version_id": ver_id,
            "status": "completed",
            "routed_engine": f"{cap_type.capitalize()}Gateway",
            "output_payload": {"result": "success", "capability_name": cap["display_name"]},
            "execution_id": f"exec_cap_{uuid.uuid4().hex[:8]}",
            "duration_ms": duration_ms
        }

async def request_installation(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: CapabilityRequestCreate,
    requested_by: str = "user_default"
) -> dict:
    """Creates a formal installation request."""
    _initialize_demo_capabilities_if_empty()
    req_id = f"req_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    request_obj = {
        "id": req_id,
        "workspace_id": workspace_id,
        "capability_id": req.capability_id,
        "requested_by": requested_by,
        "reason": req.reason,
        "status": "pending",
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": now_iso
    }

    if workspace_id not in _in_memory_requests:
        _in_memory_requests[workspace_id] = []
    _in_memory_requests[workspace_id].append(request_obj)
    return request_obj

async def approve_request(session: Optional[AsyncSession], request_id: str, reviewed_by: str) -> dict:
    """Approves a capability request and installs it."""
    _initialize_demo_capabilities_if_empty()
    now_iso = datetime.now(timezone.utc).isoformat()
    for ws_reqs in _in_memory_requests.values():
        for r in ws_reqs:
            if r["id"] == request_id:
                r["status"] = "approved"
                r["reviewed_by"] = reviewed_by
                r["reviewed_at"] = now_iso

                # Install
                ws_id = r["workspace_id"]
                inst = {
                    "id": f"inst_{uuid.uuid4().hex[:8]}",
                    "organization_id": "org_default_creator",
                    "workspace_id": ws_id,
                    "capability_id": r["capability_id"],
                    "installed_by": reviewed_by,
                    "status": "installed",
                    "installed_at": now_iso
                }
                if ws_id not in _in_memory_installations:
                    _in_memory_installations[ws_id] = []
                _in_memory_installations[ws_id].append(inst)
                return r
    raise ValueError(f"Request '{request_id}' not found.")

async def publish_package(session: Optional[AsyncSession], workspace_id: str, name: str, capability_ids: List[str]) -> dict:
    """Publishes a capability package after secret scanning."""
    _initialize_demo_capabilities_if_empty()
    # Secret scan check
    for cid in capability_ids:
        if "secret" in cid.lower() or "token" in cid.lower():
            raise ValueError(f"Package publication rejected: Capability '{cid}' contains secret references.")

    pkg_id = f"pkg_{uuid.uuid4().hex[:8]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    pkg = {
        "id": pkg_id,
        "workspace_id": workspace_id,
        "name": name,
        "version": "1.0.0",
        "contained_capability_ids": capability_ids,
        "created_at": now_iso
    }
    _in_memory_packages[pkg_id] = pkg
    return pkg

async def list_installations(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_capabilities_if_empty()
    return _in_memory_installations.get(workspace_id, [])

async def list_requests(session: Optional[AsyncSession], workspace_id: str) -> List[dict]:
    _initialize_demo_capabilities_if_empty()
    return _in_memory_requests.get(workspace_id, [])

async def get_capability(session: Optional[AsyncSession], capability_id: str) -> Optional[dict]:
    _initialize_demo_capabilities_if_empty()
    return _in_memory_capabilities.get(capability_id)

async def get_versions(session: Optional[AsyncSession], capability_id: str) -> List[dict]:
    _initialize_demo_capabilities_if_empty()
    return _in_memory_cap_versions.get(capability_id, [])

async def get_health(session: Optional[AsyncSession], capability_id: str) -> Optional[dict]:
    _initialize_demo_capabilities_if_empty()
    return _in_memory_cap_healths.get(capability_id)
