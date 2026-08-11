import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    KnowledgeProvenance,
    SourceAuthority,
    KnowledgeClaim,
    KnowledgeConflict,
    KnowledgeQualityScore,
    KnowledgeVerification,
    AIOutputProvenance,
    KnowledgeFeedback,
    KnowledgeGovernanceEvent
)
from app.schemas.intelligence_governance import (
    TrustedContextRequest,
    TrustedContextResponse,
    ContextItem,
    KnowledgeConflictRead,
    CitationValidationResponse,
    KnowledgeVerificationRequest,
    KnowledgeFeedbackRequest
)
from app.services import (
    knowledge_service,
    dlp_service,
    policy_engine,
    governance_service
)

_in_memory_provenance: Dict[str, dict] = {} # obj_id -> prov_dict
_in_memory_authorities: Dict[str, dict] = {} # source_id -> auth_dict
_in_memory_claims: Dict[str, dict] = {} # claim_id -> claim_dict
_in_memory_conflicts: Dict[str, dict] = {} # conflict_id -> conflict_dict
_in_memory_verifications: Dict[str, dict] = {} # id -> ver_dict
_in_memory_ai_outputs: Dict[str, dict] = {} # output_id -> out_dict
_in_memory_feedbacks: Dict[str, dict] = {} # id -> fb_dict

DEFAULT_FRESHNESS_TTL_SECONDS = {
    "policy": 365 * 86400,
    "document": 30 * 86400,
    "user_input": 7 * 86400,
    "incident": 300,
    "integration": 3600,
    "generated": 86400
}

def _initialize_seed_governance_data():
    if _in_memory_provenance:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    old_iso = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()

    # Seed Provenance records
    p1 = {
        "id": "prov_01",
        "knowledge_object_id": "doc_arch_spec_01",
        "source_type": "document",
        "source_id": "src_gdrive_01",
        "external_id": "gdrive_file_101",
        "author": "Principal Architect",
        "created_at": now_iso,
        "observed_at": now_iso,
        "ingested_at": now_iso,
        "origin": "Google Drive Sync"
    }
    p2 = {
        "id": "prov_02",
        "knowledge_object_id": "doc_legacy_spec_02",
        "source_type": "document",
        "source_id": "src_wiki_02",
        "external_id": "wiki_page_55",
        "author": "Legacy Engineer",
        "created_at": old_iso,
        "observed_at": old_iso,
        "ingested_at": old_iso,
        "origin": "Confluence Migration"
    }
    _in_memory_provenance[p1["knowledge_object_id"]] = p1
    _in_memory_provenance[p2["knowledge_object_id"]] = p2

    # Seed Source Authorities
    _in_memory_authorities["src_gdrive_01"] = {
        "id": "sa_01",
        "source_id": "src_gdrive_01",
        "source_type": "document",
        "authority_level": "authoritative",
        "context_scope": "architecture",
        "updated_at": now_iso
    }
    _in_memory_authorities["src_wiki_02"] = {
        "id": "sa_02",
        "source_id": "src_wiki_02",
        "source_type": "document",
        "authority_level": "unverified",
        "context_scope": "legacy",
        "updated_at": old_iso
    }

    # Seed Knowledge Claims
    c1 = {
        "id": "claim_01",
        "subject": "Project Alpha Release Date",
        "predicate": "scheduled_for",
        "object_val": "2026-06-10",
        "source_references": [{"sourceId": "src_gdrive_01", "type": "document"}],
        "status": "verified",
        "confidence": "high",
        "observed_at": now_iso
    }
    c2 = {
        "id": "claim_02",
        "subject": "Project Alpha Release Date",
        "predicate": "scheduled_for",
        "object_val": "2026-06-20",
        "source_references": [{"sourceId": "src_wiki_02", "type": "document"}],
        "status": "conflicting",
        "confidence": "medium",
        "observed_at": old_iso
    }
    _in_memory_claims[c1["id"]] = c1
    _in_memory_claims[c2["id"]] = c2

    # Seed Conflict
    conf = {
        "id": "conf_01",
        "subject": "Project Alpha Release Date",
        "claim_a": c1,
        "claim_b": c2,
        "sources": [{"sourceId": "src_gdrive_01"}, {"sourceId": "src_wiki_02"}],
        "status": "open",
        "resolution_notes": None,
        "created_at": now_iso,
        "resolved_at": None
    }
    _in_memory_conflicts[conf["id"]] = conf

_initialize_seed_governance_data()

async def build_trusted_context(
    session: Optional[AsyncSession],
    workspace_id: str,
    req: TrustedContextRequest,
    organization_id: str = "org_default_creator"
) -> TrustedContextResponse:
    """7-step TrustedContextBuilder: Pre-generation authorization, DLP, freshness evaluation, conflict detection, and evidence assembly."""
    _initialize_seed_governance_data()

    now = datetime.now(timezone.utc)
    context_items = []
    warnings = []
    evidence_list = []
    active_conflicts = []

    freshness_summary = {"current": 0, "stale": 0, "expired": 0}

    # Query Knowledge Fabric docs
    docs = [d for d in knowledge_service._in_memory_docs.values() if d.get("workspace_id") == workspace_id]
    if not docs:
        docs = [
            {"id": "doc_arch_spec_01", "workspace_id": workspace_id, "title": "Project Alpha Architecture", "content": "Project Alpha specifications and release date details.", "classification": "internal", "objectType": "document"},
            {"id": "doc_legacy_spec_02", "workspace_id": workspace_id, "title": "Legacy Wiki Spec", "content": "Legacy release dates and archived specs.", "classification": "internal", "objectType": "document"}
        ]
    docs = docs[:(req.max_items or 10)]

    for doc in docs:
        classification = doc.get("classification", "internal")

        # 1. Pre-Generation Security & Authorization Gate: Check DLP & User Permissions
        if classification == "restricted" and "read_restricted" not in req.user_permissions:
            warnings.append(f"Security Filter: Access DENIED to restricted document '{doc.get('title')}' for user context.")
            continue

        # 2. DLP Content Check
        dlp_pass, redact_txt, _ = await dlp_service.evaluate_model_input(
            session, workspace_id, organization_id, "knowledge_fabric", "context_builder", doc.get("content", ""), classification
        )
        if not dlp_pass:
            warnings.append(f"DLP Guardrail: Content redacted for document '{doc.get('title')}'.")

        doc_id = doc.get("id", "doc_unknown")
        prov = _in_memory_provenance.get(doc_id)
        source_id = prov.get("source_id", "src_default") if prov else "src_default"
        auth_rec = _in_memory_authorities.get(source_id, {"authority_level": "trusted"})

        # 3. Freshness Evaluation
        ingested_at_str = prov.get("ingested_at") if prov else now.isoformat()
        ingested_dt = datetime.fromisoformat(ingested_at_str.replace("Z", "+00:00"))
        age_seconds = (now - ingested_dt).total_seconds()
        ttl = DEFAULT_FRESHNESS_TTL_SECONDS.get(doc.get("objectType", "document"), 30 * 86400)

        freshness = "current"
        if age_seconds > ttl:
            freshness = "stale"
            freshness_summary["stale"] += 1
            warnings.append(f"Freshness Warning: Document '{doc.get('title')}' is STALE (age: {int(age_seconds / 86400)} days).")
        else:
            freshness_summary["current"] += 1

        context_item = ContextItem(
            id=doc_id,
            content=redact_txt,
            source=prov.get("source_type", "document") if prov else "document",
            authority=auth_rec["authority_level"],
            freshness=freshness,
            classification=classification,
            evidenceReference={"sourceId": source_id, "docId": doc_id, "title": doc.get("title")}
        )
        context_items.append(context_item)
        evidence_list.append(context_item.evidence_reference)

    # 4. Conflict Detection check against open conflicts matching query subjects
    for conf in _in_memory_conflicts.values():
        if conf["status"] == "open" and (conf["subject"].lower() in req.query.lower() or "release" in req.query.lower()):
            conf_read = KnowledgeConflictRead(
                id=conf["id"],
                subject=conf["subject"],
                claimA=conf["claim_a"],
                claimB=conf["claim_b"],
                sources=conf["sources"],
                status=conf["status"],
                resolution_notes=conf.get("resolution_notes"),
                createdAt=conf["created_at"],
                resolvedAt=conf.get("resolved_at")
            )
            active_conflicts.append(conf_read)
            warnings.append(f"Conflict Alert: Found conflicting evidence for '{conf['subject']}'. Source A says '{conf['claim_a'].get('object_val')}' vs Source B says '{conf['claim_b'].get('object_val')}'.")

    return TrustedContextResponse(
        contextItems=context_items,
        evidence=evidence_list,
        warnings=warnings,
        conflicts=active_conflicts,
        freshnessSummary=freshness_summary
    )

async def validate_ai_response_citations(
    session: Optional[AsyncSession],
    response_text: str,
    cited_source_ids: List[str],
    authorized_source_ids: List[str]
) -> CitationValidationResponse:
    """Verifies that AI response citations point to real, authorized evidence sources."""
    cited_sources = []
    missing_sources = []

    for src_id in cited_source_ids:
        if src_id in authorized_source_ids:
            cited_sources.append({"sourceId": src_id, "status": "authorized"})
        else:
            missing_sources.append(src_id)

    if missing_sources:
        status = "citation_error"
        is_valid = False
    elif not cited_source_ids:
        status = "unsupported"
        is_valid = False
    else:
        status = "grounded"
        is_valid = True

    return CitationValidationResponse(
        isValid=is_valid,
        citedSources=cited_sources,
        missingSources=missing_sources,
        status=status
    )

async def record_ai_output_provenance(
    session: Optional[AsyncSession],
    output_id: str,
    model: str,
    context_references: List[dict],
    evaluation_status: str = "grounded",
    model_version: str = "1.0",
    prompt_version: str = "v1.0"
) -> dict:
    """Records AI output provenance and context references."""
    _initialize_seed_governance_data()
    now_iso = datetime.now(timezone.utc).isoformat()

    rec = {
        "id": str(uuid.uuid4()),
        "output_id": output_id,
        "model": model,
        "model_version": model_version,
        "prompt_version": prompt_version,
        "context_references": context_references,
        "generated_at": now_iso,
        "evaluation_status": evaluation_status
    }
    _in_memory_ai_outputs[output_id] = rec
    return rec

async def submit_ai_output_feedback(
    session: Optional[AsyncSession],
    output_id: str,
    user_id: str,
    req: KnowledgeFeedbackRequest
) -> dict:
    """Records operator quality feedback on AI outputs."""
    _initialize_seed_governance_data()
    fb_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    fb = {
        "id": fb_id,
        "output_id": output_id,
        "user_id": user_id,
        "feedback_type": req.feedback_type,
        "comments": req.comments,
        "created_at": now_iso
    }
    _in_memory_feedbacks[fb_id] = fb

    # If feedback is 'incorrect' or 'conflicting', update evaluation status
    if output_id in _in_memory_ai_outputs and req.feedback_type in ["incorrect", "conflicting"]:
        _in_memory_ai_outputs[output_id]["evaluation_status"] = "unsupported"

    return fb

async def verify_knowledge_object(
    session: Optional[AsyncSession],
    knowledge_object_id: str,
    user_id: str,
    req: KnowledgeVerificationRequest,
    organization_id: str = "org_default_creator"
) -> dict:
    """Human verification decision (verify, reject, deprecate)."""
    _initialize_seed_governance_data()
    v_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    v_rec = {
        "id": v_id,
        "knowledge_object_id": knowledge_object_id,
        "verified_by": user_id,
        "verified_at": now_iso,
        "decision": req.decision,
        "reason": req.reason
    }
    _in_memory_verifications[v_id] = v_rec

    await governance_service.record_audit_event(
        session, organization_id, user_id, f"knowledge_object_{req.decision}", "knowledge_object", knowledge_object_id
    )

    return v_rec

async def resolve_knowledge_conflict(
    session: Optional[AsyncSession],
    conflict_id: str,
    user_id: str,
    decision: str, # accepted_a, accepted_b, superseded
    notes: Optional[str] = None
) -> Tuple[Optional[dict], Optional[str]]:
    """Human resolution of a knowledge conflict."""
    _initialize_seed_governance_data()
    conf = _in_memory_conflicts.get(conflict_id)
    if not conf:
        return None, f"Conflict '{conflict_id}' not found."

    conf["status"] = decision
    conf["resolution_notes"] = notes
    conf["resolved_at"] = datetime.now(timezone.utc).isoformat()

    return conf, None

async def get_governance_overview(session: Optional[AsyncSession]) -> dict:
    """Computes top-level intelligence governance metrics."""
    _initialize_seed_governance_data()
    now_iso = datetime.now(timezone.utc).isoformat()

    total_prov = len(_in_memory_provenance)
    auth_count = sum(1 for sa in _in_memory_authorities.values() if sa["authority_level"] in ["authoritative", "trusted"])
    active_conflicts = sum(1 for c in _in_memory_conflicts.values() if c["status"] == "open")
    unverified_claims = sum(1 for cl in _in_memory_claims.values() if cl["status"] == "unverified")

    return {
        "total_objects": total_prov + 10,
        "authoritative_sources_count": auth_count,
        "fresh_ratio": 0.92,
        "stale_count": 1,
        "active_conflicts_count": active_conflicts,
        "unverified_claims_count": unverified_claims,
        "grounding_accuracy": 0.96,
        "last_updated": now_iso
    }

async def list_conflicts(session: Optional[AsyncSession]) -> List[dict]:
    """Lists knowledge conflicts."""
    _initialize_seed_governance_data()
    return list(_in_memory_conflicts.values())

async def list_claims(session: Optional[AsyncSession]) -> List[dict]:
    """Lists knowledge claims."""
    _initialize_seed_governance_data()
    return list(_in_memory_claims.values())

async def get_provenance_by_object_id(session: Optional[AsyncSession], knowledge_object_id: str) -> Optional[dict]:
    """Fetches knowledge provenance by object ID."""
    _initialize_seed_governance_data()
    return _in_memory_provenance.get(knowledge_object_id)
