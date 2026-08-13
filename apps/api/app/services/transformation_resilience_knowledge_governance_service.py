import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_assurance_domains: Dict[str, dict] = {}
_in_memory_knowledge_healths: Dict[str, dict] = {}
_in_memory_evidence_assurances: Dict[str, dict] = {}
_in_memory_claims: Dict[str, dict] = {}
_in_memory_claim_supports: Dict[str, dict] = {}
_in_memory_claim_conflicts: Dict[str, dict] = {}
_in_memory_context_drifts: Dict[str, dict] = {}
_in_memory_reuse_assurances: Dict[str, dict] = {}
_in_memory_influences: Dict[str, dict] = {}
_in_memory_knowledge_risks: Dict[str, dict] = {}
_in_memory_assurance_reviews: Dict[str, dict] = {}
_in_memory_review_packets: Dict[str, dict] = {}
_in_memory_revalidations: Dict[str, dict] = {}
_in_memory_lineages: Dict[str, dict] = {}
_in_memory_evidence_gaps: Dict[str, dict] = {}
_in_memory_governance_states: Dict[str, dict] = {}

_EMITTED_GOVERNANCE_EVENTS: List[dict] = []

EMITTED_GOVERNANCE_EVENT_TYPES = [
    "transformation.resilience.knowledge.assurance.domain.created",
    "transformation.resilience.knowledge.health.updated",
    "transformation.resilience.knowledge.evidence.assured",
    "transformation.resilience.knowledge.claim.created",
    "transformation.resilience.knowledge.claim.supported",
    "transformation.resilience.knowledge.claim.conflict.detected",
    "transformation.resilience.knowledge.context.drift.detected",
    "transformation.resilience.knowledge.reuse.assured",
    "transformation.resilience.knowledge.influence.updated",
    "transformation.resilience.knowledge.risk.detected",
    "transformation.resilience.knowledge.review.requested",
    "transformation.resilience.knowledge.review.packet.created",
    "transformation.resilience.knowledge.revalidated",
    "transformation.resilience.knowledge.narrowed",
    "transformation.resilience.knowledge.retirement.requested",
    "transformation.resilience.knowledge.lineage.updated",
    "transformation.resilience.knowledge.evidence_gap.detected",
    "transformation.resilience.knowledge.governance_state.changed"
]

def _initialize_seed_resilience_governance_data():
    if _in_memory_assurance_domains:
        return
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Assurance Domain
    adom1 = {
        "id": "adom_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Continuous Knowledge Assurance & Evidence Quality 2.0",
        "scope": "enterprise",
        "owner": "Principal Enterprise Knowledge Governance Architect",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_assurance_domains[adom1["id"]] = adom1

    kobj_id = "kobj_less_01"

    # Health Dimensions
    h1 = {
        "id": "kh_01",
        "knowledge_object_id": kobj_id,
        "freshness_score": 0.96,
        "provenance_score": 0.98,
        "validation_strength": 0.95,
        "applicability_score": 0.94,
        "reuse_score": 0.92,
        "consistency_score": 0.90,
        "context_stability": 0.96,
        "evidence_coverage": 0.95,
        "overall_status": "trusted",
        "updated_at": now_iso
    }
    _in_memory_knowledge_healths[h1["id"]] = h1

    # Evidence Assurance with Source Independence
    eass1 = {
        "id": "eass_01",
        "knowledge_object_id": kobj_id,
        "source": "Multi-Region Token Cache Telemetry Mesh",
        "freshness": 0.96,
        "quality": 0.95,
        "reliability": 0.98,
        "independence_type": "independent",
        "coverage": 0.94,
        "conflicts_count": 0
    }
    _in_memory_evidence_assurances[eass1["id"]] = eass1

    # Claims & Supports & Conflicts
    c1 = {
        "id": "claim_01",
        "knowledge_object_id": kobj_id,
        "statement": "Secondary Cloud SLA buffer must be +15ms to absorb vendor maintenance jitter.",
        "claim_type": "validated",
        "confidence": 0.95,
        "status": "active",
        "created_at": now_iso
    }
    _in_memory_claims[c1["id"]] = c1

    cs1 = {
        "id": "csupp_01",
        "claim_id": c1["id"],
        "evidence_id": "eass_01",
        "support_strength": 0.94,
        "source_independence": "independent"
    }
    _in_memory_claim_supports[cs1["id"]] = cs1

    cconf1 = {
        "id": "cconf_01",
        "claim_a_id": c1["id"],
        "claim_b_id": "claim_eventual_consistency",
        "evidence_json": {"source_a": "OAuth telemetry", "source_b": "SSO background sync"},
        "context_description": "Claim A applies to real-time auth; Claim B applies to background sync.",
        "severity": "medium",
        "created_at": now_iso
    }
    _in_memory_claim_conflicts[cconf1["id"]] = cconf1

    # Context Drift
    cdrift1 = {
        "id": "cdrift_01",
        "knowledge_object_id": kobj_id,
        "dimension": "vendor_infrastructure_topology",
        "drift_description": "Secondary cloud region network provider announced fiber route upgrade in Q3.",
        "status": "changing",
        "created_at": now_iso
    }
    _in_memory_context_drifts[cdrift1["id"]] = cdrift1

    # Reuse Assurance
    rass1 = {
        "id": "rass_01",
        "knowledge_object_id": kobj_id,
        "reuse_count": 5,
        "successful_reuse_count": 5,
        "failed_reuse_count": 0,
        "inconclusive_reuse_count": 0,
        "context_similarity_score": 0.95
    }
    _in_memory_reuse_assurances[rass1["id"]] = rass1

    # Knowledge Influence & Risk
    inf1 = {
        "id": "inf_01",
        "knowledge_object_id": kobj_id,
        "target_type": "decision",
        "target_id": "dec_res_01",
        "influence_level": "high",
        "created_at": now_iso
    }
    _in_memory_influences[inf1["id"]] = inf1

    risk1 = {
        "id": "krisk_01",
        "knowledge_object_id": kobj_id,
        "risk_type": "high_influence_low_quality",
        "severity": "low",
        "affected_decisions_json": ["dec_res_01", "dec_wave_04_hr"],
        "confidence": 0.92
    }
    _in_memory_knowledge_risks[risk1["id"]] = risk1

    # Review & Review Packet
    rev1 = {
        "id": "arev_01",
        "knowledge_object_id": kobj_id,
        "trigger": "context_drift_detected",
        "priority": "high",
        "recommended_action": "revalidate",
        "status": "pending",
        "created_at": now_iso
    }
    _in_memory_assurance_reviews[rev1["id"]] = rev1

    pack1 = {
        "id": "apack_01",
        "review_id": rev1["id"],
        "knowledge_object_id": kobj_id,
        "claims_json": [c1],
        "evidence_json": eass1,
        "conflicts_json": [cconf1],
        "context_drift_json": cdrift1,
        "reuse_history_json": [rass1],
        "influence_json": inf1,
        "risk_json": risk1,
        "recommended_action": "revalidate",
        "created_at": now_iso
    }
    _in_memory_review_packets[pack1["id"]] = pack1

    # Revalidation
    reval1 = {
        "id": "reval_01",
        "knowledge_object_id": kobj_id,
        "review_question": "Does the +15ms SLA buffer apply to new 10Gbps interconnects?",
        "new_evidence_json": {"interconnect_speed": "10Gbps", "measured_jitter": "3ms"},
        "new_context": "Applicable specifically to multi-region OAuth token cache gateways.",
        "result": "narrowed",
        "reviewer": "Principal Knowledge Governance Architect",
        "created_at": now_iso
    }
    _in_memory_revalidations[reval1["id"]] = reval1

    # Lineage
    lin1 = {
        "id": "lin_01",
        "knowledge_object_id": kobj_id,
        "source_decision_id": "dec_res_01",
        "outcome_id": "obs_out_01",
        "lesson_id": "less_01",
        "pattern_id": "spat_01",
        "claim_ids_json": [c1["id"]],
        "evidence_ids_json": [eass1["id"]],
        "reuse_ids_json": ["reuse_01"],
        "review_ids_json": [rev1["id"]]
    }
    _in_memory_lineages[lin1["id"]] = lin1

    # Evidence Gap & Governance State
    gap1 = {
        "id": "egap_01",
        "domain_id": adom1["id"],
        "gap_title": "Lack of Independent Corroboration for Secondary Cloud Provider SLA Jitter",
        "gap_type": "non_independent",
        "priority": "high",
        "recommended_activity": "Collect telemetry from independent third-party monitoring vendor."
    }
    _in_memory_evidence_gaps[gap1["id"]] = gap1

    govstate1 = {
        "id": "govstate_01",
        "knowledge_object_id": kobj_id,
        "state": "trusted",
        "authorized_by": "Enterprise Knowledge Governance Board",
        "rationale": "High evidence coverage and 100% successful reuse rate across 5 decisions.",
        "updated_at": now_iso
    }
    _in_memory_governance_states[govstate1["id"]] = govstate1

_initialize_seed_resilience_governance_data()


class TransformationResilienceKnowledgeGovernanceService:

    @staticmethod
    def emit_event(event_type: str, payload: dict) -> dict:
        evt = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        _EMITTED_GOVERNANCE_EVENTS.append(evt)
        return evt

    @staticmethod
    def enforce_agent_governance(agent_id: str, action: str) -> dict:
        # Agents may monitor knowledge quality, detect conflicts, prepare review packets, identify evidence gaps, recommend revalidation, and summarize lineage
        # Agents may NOT approve knowledge state changes, invalidate institutional knowledge, change governance, or modify historical evidence
        forbidden_actions = [
            "approve_knowledge_state_change", "invalidate_institutional_knowledge",
            "change_governance", "modify_historical_evidence"
        ]
        if action in forbidden_actions:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' is strictly blocked from executing governance decision action '{action}'. State authorization and institutional knowledge invalidation require human governance authority."
            }
        return {"allowed": True, "reason": "Action permitted for knowledge governance agent."}

    @staticmethod
    async def get_knowledge_governance_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_resilience_governance_data()
        domains = list(_in_memory_assurance_domains.values())
        healths = list(_in_memory_knowledge_healths.values())
        evidence = list(_in_memory_evidence_assurances.values())
        claims = list(_in_memory_claims.values())
        supports = list(_in_memory_claim_supports.values())
        conflicts = list(_in_memory_claim_conflicts.values())
        drifts = list(_in_memory_context_drifts.values())
        reuses = list(_in_memory_reuse_assurances.values())
        influences = list(_in_memory_influences.values())
        risks = list(_in_memory_knowledge_risks.values())
        reviews = list(_in_memory_assurance_reviews.values())
        packets = list(_in_memory_review_packets.values())
        revalidations = list(_in_memory_revalidations.values())
        lineages = list(_in_memory_lineages.values())
        gaps = list(_in_memory_evidence_gaps.values())
        states = list(_in_memory_governance_states.values())

        trusted_cnt = sum(1 for s in states if s.get("state") == "trusted")
        review_req_cnt = sum(1 for s in states if s.get("state") == "review_required")
        contested_cnt = sum(1 for s in states if s.get("state") == "contested")

        return {
            "domainsCount": len(domains),
            "healthsCount": len(healths),
            "trustedCount": trusted_cnt,
            "reviewRequiredCount": review_req_cnt,
            "contestedCount": contested_cnt,
            "claimsCount": len(claims),
            "conflictsCount": len(conflicts),
            "contextDriftsCount": len(drifts),
            "reviewsCount": len(reviews),
            "revalidationsCount": len(revalidations),
            "gapsCount": len(gaps),
            "domains": domains,
            "healths": healths,
            "evidence": evidence,
            "claims": claims,
            "supports": supports,
            "conflicts": conflicts,
            "drifts": drifts,
            "reuses": reuses,
            "influences": influences,
            "risks": risks,
            "reviews": reviews,
            "packets": packets,
            "revalidations": revalidations,
            "lineages": lineages,
            "gaps": gaps,
            "states": states
        }

    @staticmethod
    async def revalidate_knowledge(session: Optional[AsyncSession], review_id: str, data: dict) -> dict:
        _initialize_seed_resilience_governance_data()
        rev = _in_memory_assurance_reviews.get(review_id)
        if not rev:
            return {"error": "Review not found."}

        k_id = rev.get("knowledge_object_id", "kobj_less_01")
        reval_id = f"reval_{uuid.uuid4().hex[:8]}"
        result = data.get("result", "confirmed")

        reval = {
            "id": reval_id,
            "knowledge_object_id": k_id,
            "review_question": data.get("review_question", "Knowledge revalidation review question"),
            "new_evidence_json": data.get("new_evidence_json", {}),
            "new_context": data.get("new_context", "Narrowed applicability context"),
            "result": result,
            "reviewer": data.get("reviewer", "Principal Knowledge Governance Architect"),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        _in_memory_revalidations[reval_id] = reval
        rev["status"] = "completed"

        # Emit revalidated or narrowed event
        if result == "narrowed":
            TransformationResilienceKnowledgeGovernanceService.emit_event(
                "transformation.resilience.knowledge.narrowed",
                {"knowledge_object_id": k_id, "revalidation_id": reval_id, "narrowed_context": reval["new_context"]}
            )
        else:
            TransformationResilienceKnowledgeGovernanceService.emit_event(
                "transformation.resilience.knowledge.revalidated", reval
            )
        return reval

    @staticmethod
    async def process_natural_language_governance_query(session: Optional[AsyncSession], query_str: str, caller_org_id: str = "org_global_enterprise_01") -> dict:
        _initialize_seed_resilience_governance_data()

        # Enforce Anti-Surveillance / Privacy safeguards (blocking employee knowledge scores, individual behavioral profiles, or employee decision-quality rankings)
        lower_q = query_str.lower()
        forbidden_privacy_terms = [
            "employee knowledge score", "employee knowledge ranking", "individual behavioral profile",
            "employee decision-quality ranking", "surveillance", "rank personnel", "rank employee"
        ]
        if any(term in lower_q for term in forbidden_privacy_terms):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee knowledge scores, individual behavioral profiles, or employee decision-quality rankings."},
                "confidencePct": 0.0
            }

        # Enforce DLP checks
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Enforce Multi-Tenant Isolation
        if caller_org_id != "org_global_enterprise_01":
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "DENY. Organization tenant isolation breach detected."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "trustworthiness": "Knowledge Object 'kobj_less_01' is TRUSTED (Freshness: 96%, Provenance: 98%, Coverage: 95%).",
                    "evidence_assurance": "Independent evidence from Multi-Region Token Cache Telemetry Mesh (Zero same-origin duplication bias).",
                    "claims_support": "Claim A supported by telemetry (Support Strength: 94%, Source Independence: Independent).",
                    "context_drift": "Vendor topology changing in Q3; review recommended for high-concurrency expansion.",
                    "contested_warning": "Warning: Claim B is CONTESTED due to workload mismatch between real-time OAuth and non-critical SSO.",
                    "knowledge_influence": "Influences Decision 'dec_res_01' and Wave 4 HR Cloud implementation.",
                    "evidence_gaps": "Lack of Independent Corroboration for Secondary Cloud Provider SLA Jitter (Priority: High)."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Resilience Knowledge Assurance & Evidence Quality 2.0 Engine",
                "freshness_pct": 100.0
            },
            "confidencePct": 99.5
        }
