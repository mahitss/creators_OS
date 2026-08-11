import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import agent_runtime_v2_service
from app.schemas.agent_runtime_v2 import AgentExecutionCreate, UnknownOutcomeResolveRequest

def test_create_and_execute_step_with_checkpoint():
    async def _test():
        req = AgentExecutionCreate(
            agentId="ag_test_01",
            missionId="msn_test_01",
            initialVariables={"goal": "test_goal"}
        )
        execution, state = await agent_runtime_v2_service.create_execution(
            None, workspace_id="ws_test_01", req=req, organization_id="org_test_01"
        )
        assert execution["status"] == "created"
        assert execution["version"] == 1
        assert state["last_checkpoint_id"] is not None

        # Execute model step
        step = await agent_runtime_v2_service.execute_step(
            None,
            execution_id=execution["id"],
            step_type="model_call",
            input_payload={"prompt": "Hello", "capability": "reasoning"},
            organization_id="org_test_01"
        )
        assert step["status"] == "completed"
        assert step["output_reference"] is not None

        # Execute tool step (creates pre-action checkpoint)
        step_tool = await agent_runtime_v2_service.execute_step(
            None,
            execution_id=execution["id"],
            step_type="tool_call",
            input_payload={"tool": "email.send"},
            organization_id="org_test_01"
        )
        assert step_tool["status"] == "completed"

        checkpoints = await agent_runtime_v2_service.list_checkpoints(None, execution_id=execution["id"])
        assert len(checkpoints) >= 2
    asyncio.run(_test())

def test_pause_resume_cancel_lifecycle():
    async def _test():
        req = AgentExecutionCreate(agentId="ag_test_02", initialVariables={})
        execution, _ = await agent_runtime_v2_service.create_execution(
            None, workspace_id="ws_test_01", req=req
        )

        paused = await agent_runtime_v2_service.pause_execution(None, execution["id"])
        assert paused["status"] == "paused"

        resumed = await agent_runtime_v2_service.resume_execution(None, execution["id"])
        assert resumed["status"] == "running"

        cancelled = await agent_runtime_v2_service.cancel_execution(None, execution["id"])
        assert cancelled["status"] == "cancelled"
    asyncio.run(_test())

def test_worker_crash_recovery():
    async def _test():
        req = AgentExecutionCreate(agentId="ag_test_03", initialVariables={})
        execution, _ = await agent_runtime_v2_service.create_execution(
            None, workspace_id="ws_test_01", req=req
        )

        recovered = await agent_runtime_v2_service.recover_execution(None, execution["id"])
        assert recovered["status"] == "running"
    asyncio.run(_test())

def test_unknown_outcome_detection_and_operator_resolution():
    async def _test():
        req = AgentExecutionCreate(agentId="ag_test_04", initialVariables={})
        execution, _ = await agent_runtime_v2_service.create_execution(
            None, workspace_id="ws_test_01", req=req
        )

        resolve_req = UnknownOutcomeResolveRequest(
            resolution="resolved_success",
            notes="Confirmed via API logs."
        )
        resolved = await agent_runtime_v2_service.resolve_unknown_outcome(
            None, execution_id=execution["id"], step_id="step_crashed_99", req=resolve_req, user_id="usr_op_01"
        )
        assert resolved["status"] == "resolved_success"
        assert resolved["resolution_notes"] == "Confirmed via API logs."
    asyncio.run(_test())

def test_execution_trace():
    async def _test():
        trace = await agent_runtime_v2_service.get_execution_trace(None, execution_id="exec_demo_01")
        assert trace is not None
        assert trace["execution"]["id"] == "exec_demo_01"
        assert len(trace["steps"]) >= 1
    asyncio.run(_test())
