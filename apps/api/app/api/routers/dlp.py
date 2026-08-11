from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.dlp import (
    DataAssetRead,
    SensitiveDataFindingRead,
    DLPPolicyCreate,
    DLPPolicyRead,
    DLPDecisionRead,
    DataLineageNodeRead,
    DataLineageEdgeRead,
    QuarantineRecordRead,
    PolicySimulationTestCreate
)
from app.services import dlp_service

router = APIRouter(prefix="/admin/data", tags=["data-security"])

@router.get("/assets")
async def list_data_assets(
    workspace_id: str = Query("ws_default_creator", alias="workspaceId"),
    session: AsyncSession = Depends(get_db)
):
    """Lists registered enterprise data assets and classification levels."""
    return [
        {
            "id": "da_gmail_01",
            "workspace_id": workspace_id,
            "organization_id": "org_default_creator",
            "source_type": "gmail",
            "source_id": "msg_quarterly_financials_104",
            "classification": "confidential",
            "owner_id": "usr_executive_01",
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        },
        {
            "id": "da_drive_02",
            "workspace_id": workspace_id,
            "organization_id": "org_default_creator",
            "source_type": "drive",
            "source_id": "doc_sec_roadmap_2026",
            "classification": "restricted",
            "owner_id": "usr_secops_01",
            "created_at": "2026-08-11T00:00:00Z",
            "updated_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/findings")
async def list_sensitive_findings(
    workspace_id: str = Query("ws_default_creator", alias="workspaceId"),
    session: AsyncSession = Depends(get_db)
):
    """Lists sensitive data pattern findings (secrets, PII, credit cards)."""
    return [
        {
            "id": "sdf_01",
            "asset_id": "da_gmail_01",
            "workspace_id": workspace_id,
            "detector": "api_key",
            "classification": "secret",
            "action": "redact",
            "resource": "msg_quarterly_financials_104",
            "status": "open",
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/policies")
async def list_dlp_policies(
    organization_id: str = Query("org_default_creator", alias="organizationId"),
    session: AsyncSession = Depends(get_db)
):
    """Lists configured DLP boundary policy rules."""
    return [
        {
            "id": "dlp_rule_01",
            "organization_id": organization_id,
            "name": "Secret Boundary & Auto-Redaction",
            "classification": "secret",
            "source_scope": "all",
            "destination_scope": "external_model",
            "allowed_action": "redact",
            "approval_required": False,
            "enabled": True,
            "version": 1,
            "created_at": "2026-08-11T00:00:00Z"
        },
        {
            "id": "dlp_rule_02",
            "organization_id": organization_id,
            "name": "Restricted Exfiltration Block",
            "classification": "restricted",
            "source_scope": "drive",
            "destination_scope": "unapproved_provider",
            "allowed_action": "block",
            "approval_required": True,
            "enabled": True,
            "version": 1,
            "created_at": "2026-08-11T00:00:00Z"
        }
    ]

@router.get("/lineage")
async def get_data_lineage(
    workspace_id: str = Query("ws_default_creator", alias="workspaceId"),
    session: AsyncSession = Depends(get_db)
):
    """Retrieves Data Lineage DAG nodes and edges."""
    return {
        "nodes": [
            {"id": "n1", "resource_id": "msg_104", "type": "gmail_source", "classification": "confidential"},
            {"id": "n2", "resource_id": "ag_creator_01", "type": "agent", "classification": "confidential"},
            {"id": "n3", "resource_id": "gpt-4o", "type": "model", "classification": "confidential"},
            {"id": "n4", "resource_id": "doc_summary", "type": "drive_destination", "classification": "confidential"}
        ],
        "edges": [
            {"id": "e1", "source_id": "n1", "destination_id": "n2", "transformation": "context_retrieval"},
            {"id": "e2", "source_id": "n2", "destination_id": "n3", "transformation": "prompt_assembly"},
            {"id": "e3", "source_id": "n3", "destination_id": "n4", "transformation": "document_generation"}
        ]
    }

@router.post("/policies/simulate")
async def simulate_dlp_policy(
    sim_in: PolicySimulationTestCreate,
    session: AsyncSession = Depends(get_db)
):
    """Simulates DLP evaluation against content sample without production state mutation."""
    findings = dlp_service.detect_sensitive_patterns(sim_in.content_sample)
    redacted_text, count = dlp_service.redact_sensitive_content(sim_in.content_sample)

    action = "ALLOW"
    if any(f["classification"] == "secret" for f in findings):
        action = "REDACTED"
    elif any(f["classification"] == "restricted" for f in findings):
        action = "BLOCKED"

    return {
        "action": action,
        "detectors": [f["detector"] for f in findings],
        "redactions_count": count,
        "simulated_output": redacted_text
    }
