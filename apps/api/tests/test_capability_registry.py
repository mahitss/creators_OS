import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
api_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import capability_registry_service
from app.schemas.capability_registry import (
    CapabilityCreate,
    CapabilityInvokeRequest,
    CapabilityRequestCreate
)

def test_register_and_discover_capability():
    async def _test():
        req = CapabilityCreate(
            name="tool_sql_query_01",
            displayName="SQL Query Capability",
            description="Executes read-only SQL queries",
            category="analytics",
            type="tool"
        )
        cap, version = await capability_registry_service.register_capability(
            None, workspace_id="ws_test_01", req=req
        )
        assert cap["type"] == "tool"
        assert version["capability_id"] == cap["id"]

        discovered = await capability_registry_service.discover_capabilities(
            None, workspace_id="ws_test_01", query="SQL"
        )
        assert len(discovered) >= 1
        sql_cap = next(c for c in discovered if c["name"] == "tool_sql_query_01")
        assert sql_cap["display_name"] == "SQL Query Capability"
    asyncio.run(_test())

def test_invoke_capability_routing():
    async def _test():
        inv_req = CapabilityInvokeRequest(inputPayload={"doc_id": "doc_arch_01"})
        resp = await capability_registry_service.invoke_capability(
            None, workspace_id="ws_default_01", capability_id="cap_skill_doc_analysis", req=inv_req
        )
        assert resp["status"] == "completed"
        assert "AgentRuntimeV2" in resp["routed_engine"]
    asyncio.run(_test())

def test_circular_capability_dependency_rejection():
    async def _test():
        inv_req = CapabilityInvokeRequest(
            inputPayload={},
            callingCapabilityIds=["cap_skill_doc_analysis"]
        )
        with pytest.raises(ValueError, match="Circular capability dependency"):
            await capability_registry_service.invoke_capability(
                None, workspace_id="ws_default_01", capability_id="cap_skill_doc_analysis", req=inv_req
            )
    asyncio.run(_test())

def test_request_and_approve_installation():
    async def _test():
        req = CapabilityRequestCreate(
            capabilityId="cap_tool_ledger_export",
            reason="Quarterly audit requirement"
        )
        request_obj = await capability_registry_service.request_installation(
            None, workspace_id="ws_test_02", req=req, requested_by="user_auditor"
        )
        assert request_obj["status"] == "pending"

        approved_obj = await capability_registry_service.approve_request(
            None, request_id=request_obj["id"], reviewed_by="admin_sec_01"
        )
        assert approved_obj["status"] == "approved"
        assert approved_obj["reviewed_by"] == "admin_sec_01"
    asyncio.run(_test())

def test_secret_scanning_package_rejection():
    async def _test():
        with pytest.raises(ValueError, match="contains secret references"):
            await capability_registry_service.publish_package(
                None, workspace_id="ws_default_01", name="Unsafe Package", capability_ids=["cap_aws_secret_key"]
            )
    asyncio.run(_test())
