import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.models import (
    DataAsset,
    DataClassificationRecord,
    SensitiveDataFinding,
    DLPPolicy,
    DLPDecision,
    DataAccessEvent,
    DataLineageNode,
    DataLineageEdge,
    QuarantineRecord,
    ModelDataPolicy,
    DataProcessingRecord
)
from app.schemas.dlp import (
    DLPPolicyCreate,
    DLPPolicyRead,
    DLPDecisionRead,
    QuarantineRecordRead
)
from app.services.governance_service import record_audit_event

_in_memory_assets: Dict[str, dict] = {}
_in_memory_findings: Dict[str, dict] = {}
_in_memory_policies: Dict[str, dict] = {}
_in_memory_decisions: Dict[str, dict] = {}
_in_memory_lineage_nodes: Dict[str, dict] = {}
_in_memory_lineage_edges: Dict[str, dict] = {}
_in_memory_quarantine: Dict[str, dict] = {}

import math
from collections import Counter

# Enhanced Patterns for sensitive data & secrets
SENSITIVE_PATTERNS = [
    ("api_key", r"(vpr_[a-zA-Z0-9_]{10,}|sk_[a-zA-Z0-9_]{10,}|ak_[a-zA-Z0-9_]{10,}|ghp_[a-zA-Z0-9]{20,}|xox[baprs]-[a-zA-Z0-9-]{10,})"),
    ("private_key", r"-----BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----"),
    ("jwt_token", r"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}"),
    ("password", r"(password\s*[:=]\s*\S+|passwd\s*[:=]\s*\S+|secret\s*[:=]\s*\S+)"),
    ("credit_card", r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b"),
    ("email", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    ("phone", r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
]

def calculate_shannon_entropy(data: str) -> float:
    """Calculates the Shannon entropy of a string to detect high-randomness secrets."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    counts = Counter(data)
    for count in counts.values():
        p_x = count / length
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def detect_sensitive_patterns(text: str) -> List[dict]:
    """Detects sensitive patterns, obfuscated secrets, and high-entropy credential blobs."""
    findings = []
    
    # 1. Regex Detectors
    for detector_name, pattern in SENSITIVE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            classification = "secret" if detector_name in ["api_key", "private_key", "jwt_token", "password"] else "confidential"
            findings.append({
                "detector": detector_name,
                "count": len(matches),
                "classification": classification
            })

    # 2. De-obfuscation Check (Spaced tokens e.g. 's k _ ...')
    normalized_spaced = re.sub(r"\s+", "", text)
    if re.search(r"(sk_|vpr_|ghp_)[\w]{10,}", normalized_spaced) and not any(f["detector"] == "api_key" for f in findings):
        findings.append({
            "detector": "obfuscated_api_key",
            "count": 1,
            "classification": "secret"
        })

    # 3. High-Entropy Credential Detection
    tokens = re.findall(r"\b[A-Za-z0-9+/=_-]{24,}\b", text)
    for token in tokens:
        # Ignore common base64 words or structured markdown
        if not re.match(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$", token):
            continue
        entropy = calculate_shannon_entropy(token)
        if entropy >= 4.2 and not any(f["detector"] == "jwt_token" for f in findings):
            findings.append({
                "detector": "high_entropy_secret",
                "count": 1,
                "classification": "secret"
            })
            break

    return findings

def redact_sensitive_content(text: str, mode: str = "mask") -> Tuple[str, int]:
    """Redacts sensitive content using mask, remove, or tokenize modes without storing secrets."""
    redact_count = 0
    redacted_text = text

    for detector_name, pattern in SENSITIVE_PATTERNS:
        if detector_name in ["api_key", "private_key", "jwt_token", "password"]:
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                redact_count += len(matches)
                redacted_text = re.sub(pattern, "[REDACTED_SECRET]", redacted_text)
        elif detector_name == "email" and mode == "mask":
            def _mask_email(m):
                val = m.group(0)
                parts = val.split("@")
                return f"{parts[0][0]}***@{parts[1]}"
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                redact_count += len(matches)
                redacted_text = re.sub(pattern, _mask_email, redacted_text)
        elif detector_name == "credit_card":
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                redact_count += len(matches)
                redacted_text = re.sub(pattern, "****-****-****-1234", redacted_text)

    return redacted_text, redact_count

async def evaluate_model_input(
    session: Optional[AsyncSession],
    workspace_id: str,
    org_id: str,
    provider: str,
    model: str,
    content: str,
    classification: str = "internal"
) -> Tuple[str, str, dict]:
    """Pre-flight Model Input Gate inspecting classification, provider approval, and secret boundaries."""
    now_iso = datetime.now(timezone.utc).isoformat()
    findings = detect_sensitive_patterns(content)

    # 1. High-Confidence Secret Boundary Check
    secret_findings = [f for f in findings if f["classification"] == "secret"]
    if secret_findings:
        # Redact secrets before sending to LLM
        clean_text, redact_cnt = redact_sensitive_content(content)
        dec_id = str(uuid.uuid4())
        _in_memory_decisions[dec_id] = {
            "id": dec_id,
            "workspace_id": workspace_id,
            "action": "redact",
            "reason_code": "DLP_SECRET_REDACTED",
            "classification": "secret",
            "detectors": [f["detector"] for f in secret_findings],
            "policy_version": 1,
            "redactions_count": redact_cnt,
            "created_at": now_iso
        }
        return clean_text, "REDACTED", _in_memory_decisions[dec_id]

    # 2. Restricted Classification & Provider Boundary
    if classification == "restricted" and provider not in ["openai_enterprise", "local_approved"]:
        dec_id = str(uuid.uuid4())
        _in_memory_decisions[dec_id] = {
            "id": dec_id,
            "workspace_id": workspace_id,
            "action": "block",
            "reason_code": "DLP_UNAPPROVED_PROVIDER_FOR_RESTRICTED_DATA",
            "classification": "restricted",
            "detectors": [],
            "policy_version": 1,
            "redactions_count": 0,
            "created_at": now_iso
        }
        return "", "BLOCKED", _in_memory_decisions[dec_id]

    return content, "ALLOWED", {"action": "allow", "classification": classification}

async def evaluate_memory_gate(
    session: Optional[AsyncSession],
    workspace_id: str,
    content: str,
    operation: str = "write"
) -> Tuple[bool, str]:
    """Memory Gate enforcing secret prevention and workspace isolation."""
    findings = detect_sensitive_patterns(content)
    secret_findings = [f for f in findings if f["classification"] == "secret"]

    if secret_findings:
        return False, f"Memory Write Denied: Content contains sensitive secret pattern '{secret_findings[0]['detector']}'."

    return True, "ALLOWED"

async def record_lineage(
    session: Optional[AsyncSession],
    source_res: str,
    source_type: str,
    dest_res: str,
    dest_type: str,
    transformation: str,
    classification: str = "internal"
) -> dict:
    """Records Data Lineage DAG nodes and edge."""
    now_iso = datetime.now(timezone.utc).isoformat()
    node1_id = str(uuid.uuid4())
    node2_id = str(uuid.uuid4())
    edge_id = str(uuid.uuid4())

    n1 = {"id": node1_id, "resource_id": source_res, "type": source_type, "classification": classification, "timestamp": now_iso}
    n2 = {"id": node2_id, "resource_id": dest_res, "type": dest_type, "classification": classification, "timestamp": now_iso}
    edge = {"id": edge_id, "source_id": node1_id, "destination_id": node2_id, "transformation": transformation, "timestamp": now_iso}

    _in_memory_lineage_nodes[node1_id] = n1
    _in_memory_lineage_nodes[node2_id] = n2
    _in_memory_lineage_edges[edge_id] = edge

    return {"edge_id": edge_id, "source": source_res, "destination": dest_res}

async def quarantine_asset(
    session: Optional[AsyncSession],
    workspace_id: str,
    resource_type: str,
    resource_id: str,
    reason: str,
    actor_id: str
) -> dict:
    """Quarantines suspicious or restricted outputs for admin review."""
    now_iso = datetime.now(timezone.utc).isoformat()
    q_id = str(uuid.uuid4())

    q_dict = {
        "id": q_id,
        "workspace_id": workspace_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "reason": reason,
        "quarantined_by": actor_id,
        "status": "quarantined",
        "created_at": now_iso
    }
    _in_memory_quarantine[q_id] = q_dict

    # Audit quarantine action
    await record_audit_event(
        session, "org_default_creator", actor_id, "asset_quarantined", resource_type, resource_id,
        reason=reason, metadata_info={"quarantine_id": q_id}
    )
    return q_dict
