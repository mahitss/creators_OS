import sys
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

import pytest
import asyncio
from app.services import intelligence_governance_service
from app.schemas.intelligence_governance import (
    TrustedContextRequest,
    KnowledgeVerificationRequest,
    KnowledgeFeedbackRequest
)

def test_provenance_and_authority_fetching():
    async def _test():
        prov = await intelligence_governance_service.get_provenance_by_object_id(None, "doc_arch_spec_01")
        assert prov is not None
        assert prov["source_type"] == "document"
        assert prov["author"] == "Principal Architect"
    asyncio.run(_test())

def test_trusted_context_builder_pipeline():
    async def _test():
        req = TrustedContextRequest(
            query="Project Alpha release date architecture",
            userPermissions=["read_restricted"],
            maxItems=5
        )
        res = await intelligence_governance_service.build_trusted_context(None, workspace_id="ws_default_01", req=req)
        assert res is not None
        assert isinstance(res.context_items, list)
        assert res.freshness_summary is not None
        # Conflicting active conflict is detected and surfaced
        assert len(res.conflicts) >= 1
        assert "Release Date" in res.conflicts[0].subject
    asyncio.run(_test())

def test_citation_validation_and_grounding_status():
    async def _test():
        # Valid citation matching authorized sources -> grounded
        res_valid = await intelligence_governance_service.validate_ai_response_citations(
            None,
            response_text="Project deadline is June 10 as stated in doc.",
            cited_source_ids=["src_gdrive_01"],
            authorized_source_ids=["src_gdrive_01", "src_wiki_02"]
        )
        assert res_valid.is_valid is True
        assert res_valid.status == "grounded"

        # Citation pointing to unauthorized source -> citation_error
        res_invalid = await intelligence_governance_service.validate_ai_response_citations(
            None,
            response_text="Project deadline is secret.",
            cited_source_ids=["src_unauthorized_99"],
            authorized_source_ids=["src_gdrive_01"]
        )
        assert res_invalid.is_valid is False
        assert res_invalid.status == "citation_error"
        assert "src_unauthorized_99" in res_invalid.missing_sources
    asyncio.run(_test())

def test_ai_output_provenance_and_feedback():
    async def _test():
        output_id = "out_gen_101"
        rec = await intelligence_governance_service.record_ai_output_provenance(
            None,
            output_id=output_id,
            model="gemini-1.5-pro",
            context_references=[{"sourceId": "src_gdrive_01"}],
            evaluation_status="grounded"
        )
        assert rec["output_id"] == output_id

        # Submit feedback marking output as conflicting -> updates status to unsupported
        fb_req = KnowledgeFeedbackRequest(feedbackType="conflicting", comments="Conflicting date found")
        fb = await intelligence_governance_service.submit_ai_output_feedback(None, output_id=output_id, user_id="usr_op_01", req=fb_req)
        assert fb["id"] is not None

        out_rec = intelligence_governance_service._in_memory_ai_outputs.get(output_id)
        assert out_rec["evaluation_status"] == "unsupported"
    asyncio.run(_test())

def test_human_verification_and_conflict_resolution():
    async def _test():
        # Verify knowledge object
        req_v = KnowledgeVerificationRequest(decision="verified", reason="Owner verified claim")
        v_rec = await intelligence_governance_service.verify_knowledge_object(
            None, knowledge_object_id="claim_01", user_id="usr_executive_01", req=req_v
        )
        assert v_rec["decision"] == "verified"

        # Resolve conflict
        conf, err = await intelligence_governance_service.resolve_knowledge_conflict(
            None, conflict_id="conf_01", user_id="usr_executive_01", decision="accepted_a", notes="Accepted official source"
        )
        assert err is None
        assert conf["status"] == "accepted_a"
    asyncio.run(_test())

def test_governance_overview_telemetry():
    async def _test():
        ov = await intelligence_governance_service.get_governance_overview(None)
        assert ov["total_objects"] >= 10
        assert ov["grounding_accuracy"] >= 0.90
    asyncio.run(_test())
