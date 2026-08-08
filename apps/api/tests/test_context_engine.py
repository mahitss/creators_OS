import asyncio
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.context_engine import (
    ContextEngine,
    ContextRequest,
    ContextPurpose,
    SourceType,
    ContextPolicy,
    estimate_tokens,
)
from app.services import (
    drive_service,
    gmail_service,
)

client = TestClient(app)

WS_ALPHA = "ws_ctx_alpha"
WS_BETA = "ws_ctx_beta"
USER_ALEX = "usr_alex"

def _connect_google_workspace(workspace_id: str):
    headers = {"X-Workspace-Id": workspace_id, "X-User-Id": USER_ALEX}
    conn_res = client.post("/api/v1/integrations/google/connect", headers=headers)
    state = conn_res.json()["state"]
    client.get(f"/api/v1/integrations/google/callback?code=mock_code&state={state}", headers=headers)

def test_context_engine_token_estimation():
    text = "Hello world! This is a test string for token estimation."
    tokens = estimate_tokens(text)
    assert tokens > 0
    assert tokens == len(text) // 4

def test_context_policy_source_matrix_enforcement():
    # Content Generation allows Mission, Memory, Content, Drive (Strictly EXCLUDES Gmail)
    permitted = ContextPolicy.get_allowed_sources(
        ContextPurpose.CONTENT_GENERATION,
        [SourceType.GMAIL, SourceType.DRIVE, SourceType.MEMORY]
    )
    assert SourceType.GMAIL not in permitted
    assert SourceType.DRIVE in permitted
    assert SourceType.MEMORY in permitted

def test_context_engine_cross_workspace_isolation_and_privacy():
    _connect_google_workspace(WS_ALPHA)

    async def run_test():
        await drive_service.sync_drive_data(None, WS_ALPHA)

        # Request context for Beta workspace
        req_beta = ContextRequest(
            workspace_id=WS_BETA,
            user_id="usr_bob",
            purpose=ContextPurpose.MISSION_PLANNING,
            allowed_sources=[SourceType.DRIVE]
        )
        res_beta = await ContextEngine.retrieve(None, req_beta)

        # Secret Drive document from Alpha MUST NOT leak to Beta
        for item in res_beta.items:
            assert item.source_type != SourceType.DRIVE or "ws_ctx_alpha" not in item.id

    asyncio.run(run_test())

def test_context_engine_prompt_injection_defense_tagging():
    _connect_google_workspace(WS_ALPHA)

    async def run_test():
        await gmail_service.sync_gmail_data(None, WS_ALPHA)

        req = ContextRequest(
            workspace_id=WS_ALPHA,
            user_id=USER_ALEX,
            purpose=ContextPurpose.EMAIL_SUMMARY,
            allowed_sources=[SourceType.GMAIL]
        )
        res = await ContextEngine.retrieve(None, req)

        assert res.formatted_prompt_context != ""
        assert "<RETRIEVED_CONTEXT_DATA" in res.formatted_prompt_context
        assert "UNTRUSTED reference material" in res.formatted_prompt_context
        assert len(res.citations) >= 1

    asyncio.run(run_test())

def test_context_engine_token_budget_trimming():
    async def run_test():
        req = ContextRequest(
            workspace_id=WS_ALPHA,
            user_id=USER_ALEX,
            purpose=ContextPurpose.EXECUTIVE_BRIEF,
            allowed_sources=[SourceType.MISSION, SourceType.MEMORY],
            token_budget=50 # Extremely small budget to force trimming
        )
        res = await ContextEngine.retrieve(None, req)

        assert res.estimated_tokens <= 100
        assert len(res.context_version) > 0

    asyncio.run(run_test())
