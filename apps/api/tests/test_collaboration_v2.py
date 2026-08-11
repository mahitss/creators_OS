import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.services.collaboration_v2_service import CollaborationV2Service

def test_create_work_item_and_human_required_classification():
    async def _test():
        item_data = {
            "title": "Executive Financial Sign-off",
            "description": "Approve quarterly budget variance reallocation",
            "priority": "urgent",
            "workClassification": "human_required"
        }
        item = await CollaborationV2Service.create_work_item(None, item_data)
        assert item["id"] is not None
        assert item["assignee_type"] == "human"
        assert item["work_classification"] == "human_required"

    asyncio.run(_test())

def test_work_routing_recommendations():
    async def _test():
        item_data = {
            "title": "Batch Log Indexing",
            "description": "Index audit events into Semantic Graph",
            "workClassification": "agent_suitable"
        }
        item = await CollaborationV2Service.create_work_item(None, item_data)
        rec = await CollaborationV2Service.route_work_item(None, item["id"])
        assert rec["recommended_executor_type"] == "agent"
        assert rec["risk_level"] == "low"

    asyncio.run(_test())

def test_initiate_handoff_with_dlp_context_filtering():
    async def _test():
        handoff_data = {
            "workItemId": "work_01",
            "fromId": "agent_analyst_01",
            "fromType": "agent",
            "toId": "usr_exec_01",
            "toType": "human",
            "reason": "Escalating synthesized draft for review",
            "contextReferencesJson": {"user_ssn": "000-12-3456", "note": "Sensitive data"},
            "expectedOutput": "Approved summary"
        }
        h = await CollaborationV2Service.initiate_handoff(None, handoff_data)
        assert h["id"] is not None
        assert h["status"] == "pending"
        # Verify PII masking via DLP
        assert h["context_references_json"].get("user_ssn") != "000-12-3456"

    asyncio.run(_test())

def test_collaboration_feedback_pipeline():
    async def _test():
        fb_data = {
            "feedbackType": "correction",
            "ratingScore": 4.8,
            "comment": "Adjusted revenue projection formula."
        }
        fb = await CollaborationV2Service.add_feedback(None, "work_01", fb_data, "usr_exec_01")
        assert fb["id"] is not None
        assert fb["rating_score"] == 4.8

    asyncio.run(_test())

def test_collaboration_overview_telemetry():
    async def _test():
        ov = await CollaborationV2Service.get_collaboration_overview(None)
        assert ov is not None
        assert "activeWorkItemsCount" in ov
        assert "pendingHandoffsCount" in ov
        assert "openEscalationsCount" in ov

    asyncio.run(_test())
