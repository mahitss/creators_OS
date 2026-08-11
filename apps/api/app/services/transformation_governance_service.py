import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_profiles: Dict[str, dict] = {}
_in_memory_domains: Dict[str, dict] = {}
_in_memory_rights: Dict[str, dict] = {}
_in_memory_matrices: Dict[str, dict] = {}
_in_memory_conflicts: Dict[str, dict] = {}
_in_memory_controls: Dict[str, dict] = {}
_in_memory_frictions: Dict[str, dict] = {}
_in_memory_gaps: Dict[str, dict] = {}
_in_memory_overcontrols: Dict[str, dict] = {}
_in_memory_loads: Dict[str, dict] = {}
_in_memory_bottlenecks: Dict[str, dict] = {}
_in_memory_delegation_candidates: Dict[str, dict] = {}
_in_memory_escalation_patterns: Dict[str, dict] = {}
_in_memory_exceptions: Dict[str, dict] = {}
_in_memory_change_requests: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}
_in_memory_lessons: Dict[str, dict] = {}
_in_memory_patterns: Dict[str, dict] = {}

def _initialize_seed_governance_data():
    if _in_memory_profiles:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    expires_iso = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Profile & Domains
    prof1 = {
        "id": "gov_prof_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Enterprise Autonomous Transformation Adaptive Governance Model",
        "scope": "enterprise",
        "owner": "Executive Governance Steering Council",
        "status": "active",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_profiles[prof1["id"]] = prof1

    dom1 = {"id": "dom_01", "profile_id": prof1["id"], "domain_type": "decision"}
    dom2 = {"id": "dom_02", "profile_id": prof1["id"], "domain_type": "risk"}
    _in_memory_domains[dom1["id"]] = dom1
    _in_memory_domains[dom2["id"]] = dom2

    # Decision Rights & Matrix & Conflicts
    right1 = {
        "id": "dr_01",
        "profile_id": prof1["id"],
        "decision_type": "scale",
        "scope": "Enterprise Wave Rollout",
        "authority_level": "Transformation Steering Committee",
        "required_evidence": "Sub-100ms policy validation + verified cost reduction telemetry",
        "approval_requirement": "Two-key Executive Approval (CIO + Steering Committee Chair)",
        "escalation_requirement": "Escalate to Board if capital reallocation exceeds $5M",
        "delegation_allowed": True
    }
    _in_memory_rights[right1["id"]] = right1

    mat1 = {
        "id": "mat_01",
        "profile_id": prof1["id"],
        "decision_type": "scale",
        "authority_level": "Transformation Steering Committee",
        "approval_rule": "Two-key sign-off",
        "escalation_rule": ">$5M capital impact",
        "delegation_rule": "Permitted for sub-$200k regional pilots"
    }
    _in_memory_matrices[mat1["id"]] = mat1

    conf1 = {
        "id": "dr_conf_01",
        "profile_id": prof1["id"],
        "authority_a": "Engineering Capacity Allocation Board",
        "authority_b": "Transformation Portfolio Controller",
        "conflict_description": "Overlapping approval authority for Wave 2 FTE capacity reallocation",
        "status": "surfaced"
    }
    _in_memory_conflicts[conf1["id"]] = conf1

    # Governance Controls, Friction, Gaps, Overcontrol
    ctrl1 = {
        "id": "ctrl_01",
        "profile_id": prof1["id"],
        "control_type": "approval",
        "purpose": "Ensure zero-trust compliance before wave scale deployment",
        "scope": "All cloud infrastructure transformations",
        "trigger": "Decision case status transition to under_review",
        "owner": "Chief Information Security Officer",
        "policy_reference": "POL-2026-ZERO-TRUST-01",
        "effectiveness_method": "Automated AST Pre-signer Telemetry Verification"
    }
    _in_memory_controls[ctrl1["id"]] = ctrl1

    fric1 = {
        "id": "fric_01",
        "profile_id": prof1["id"],
        "friction_type": "approval_delay",
        "cause": "Manual CISO review queue backlog for routine low-risk policy updates",
        "affected_decisions": "Regional FinOps pilot expansions",
        "time_impact_hours": 48.0,
        "severity": "moderate"
    }
    _in_memory_frictions[fric1["id"]] = fric1

    gap1 = {
        "id": "gap_01",
        "profile_id": prof1["id"],
        "gap_type": "missing_escalation_path",
        "risk_description": "No explicit escalation SLA defined for cross-region data residency compliance ambiguity",
        "severity": "high",
        "recommendation": "Add 24-hour escalation rule to Global Compliance Board"
    }
    _in_memory_gaps[gap1["id"]] = gap1

    oc1 = {
        "id": "oc_01",
        "profile_id": prof1["id"],
        "control_id": ctrl1["id"],
        "overcontrol_reason": "Low-risk reversible regional pilot decisions require full CISO sign-off instead of delegated regional architect approval",
        "recommendation": "Delegate regional pilot approval to Regional Architecture Lead (Safety score: 0.94)"
    }
    _in_memory_overcontrols[oc1["id"]] = oc1

    # Load, Bottleneck, Delegation, Exceptions
    load1 = {
        "id": "load_01",
        "profile_id": prof1["id"],
        "decisions_count": 24,
        "approvals_count": 18,
        "reviews_count": 8,
        "escalations_count": 2,
        "exceptions_count": 1,
        "time_spent_hours": 36.5,
        "time_window": "monthly"
    }
    _in_memory_loads[load1["id"]] = load1

    btn1 = {
        "id": "btn_01",
        "profile_id": prof1["id"],
        "bottleneck_type": "approval",
        "cause": "CISO manual review queue bottleneck on routine pilot approvals",
        "severity": "moderate"
    }
    _in_memory_bottlenecks[btn1["id"]] = btn1

    del_cand1 = {
        "id": "del_cand_01",
        "profile_id": prof1["id"],
        "decision_type": "pilot",
        "rationale": "Low risk, highly reversible ($95k cost, 30-day window) with 98% policy coverage",
        "safety_score": 0.94,
        "policy_coverage": 0.98,
        "status": "recommended"
    }
    _in_memory_delegation_candidates[del_cand1["id"]] = del_cand1

    esc1 = {
        "id": "esc_01",
        "profile_id": prof1["id"],
        "pattern_description": "Repeated escalations occurring when engineering capacity allocation estimates differ by > 2.0 FTEs",
        "frequency": 5,
        "impact": "Average 72-hour decision latency addition"
    }
    _in_memory_escalation_patterns[esc1["id"]] = esc1

    exc1 = {
        "id": "exc_01",
        "profile_id": prof1["id"],
        "reason": "Temporary 30-day capacity buffer exception for Wave 2 region 2 rollout",
        "scope": "Region 2 FinOps cluster",
        "duration_days": 30,
        "approver": "Chief Information Officer",
        "risk": "low",
        "expires_at": expires_iso,
        "status": "active"
    }
    _in_memory_exceptions[exc1["id"]] = exc1

    # Change Requests, Drift, Reviews, Lessons, Patterns
    cr1 = {
        "id": "cr_01",
        "profile_id": prof1["id"],
        "change_type": "delegation",
        "description": "Delegate low-risk regional pilot approvals to Regional Architecture Leads",
        "proposed_state": "Regional Architecture Lead approval for pilot decisions < $100k",
        "simulation_results_json": {"latency_reduction_hours": 36.0, "risk_increase_pct": 0.02},
        "status": "under_review"
    }
    _in_memory_change_requests[cr1["id"]] = cr1

    drift1 = {
        "id": "gov_drift_01",
        "profile_id": prof1["id"],
        "drift_type": "approval",
        "approved_summary": "Two-key Executive Approval required for Wave 2 scale",
        "actual_summary": "Two-key approval executed on schedule with zero drift",
        "severity": "none"
    }
    _in_memory_drifts[drift1["id"]] = drift1

    rev1 = {
        "id": "gov_rev_01",
        "profile_id": prof1["id"],
        "cadence": "quarterly",
        "trigger_reason": "Governance friction detected in routine pilot approval queue",
        "status": "recommended",
        "created_at": now_iso
    }
    _in_memory_reviews[rev1["id"]] = rev1

    les1 = {
        "id": "gov_les_01",
        "profile_id": prof1["id"],
        "control_id": ctrl1["id"],
        "event": "Automated pre-signer telemetry prevented unvalidated policy deployment",
        "outcome": "Zero security incidents across 12 wave rollouts",
        "lesson": "Automated pre-signer telemetry verification is 4x more effective than manual CISO review for policy compliance",
        "confidence": "high"
    }
    _in_memory_lessons[les1["id"]] = les1

    pat1 = {
        "id": "gov_pat_01",
        "profile_id": prof1["id"],
        "pattern_description": "Delegating sub-$100k pilot decisions reduces decision latency by 68% without increasing policy violation rate",
        "sample_size": 10,
        "confidence": 0.95
    }
    _in_memory_patterns[pat1["id"]] = pat1

_initialize_seed_governance_data()


class TransformationGovernanceService:

    @staticmethod
    async def get_governance_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_governance_data()
        profiles = list(_in_memory_profiles.values())
        domains = list(_in_memory_domains.values())
        rights = list(_in_memory_rights.values())
        matrices = list(_in_memory_matrices.values())
        conflicts = list(_in_memory_conflicts.values())
        controls = list(_in_memory_controls.values())
        frictions = list(_in_memory_frictions.values())
        gaps = list(_in_memory_gaps.values())
        overcontrols = list(_in_memory_overcontrols.values())
        loads = list(_in_memory_loads.values())
        bottlenecks = list(_in_memory_bottlenecks.values())
        delegation_candidates = list(_in_memory_delegation_candidates.values())
        escalation_patterns = list(_in_memory_escalation_patterns.values())
        exceptions = list(_in_memory_exceptions.values())
        change_requests = list(_in_memory_change_requests.values())
        drifts = list(_in_memory_drifts.values())
        reviews = list(_in_memory_reviews.values())
        lessons = list(_in_memory_lessons.values())
        patterns = list(_in_memory_patterns.values())

        return {
            "activeProfilesCount": len(profiles),
            "decisionRightsCount": len(rights),
            "activeControlsCount": len(controls),
            "surfacedConflictsCount": len(conflicts),
            "detectedFrictionsCount": len(frictions),
            "delegationCandidatesCount": len(delegation_candidates),
            "activeExceptionsCount": len([e for e in exceptions if e.get("status") == "active"]),
            "governanceEfficiencyScorePct": 94.5,
            "profiles": profiles,
            "domains": domains,
            "rights": rights,
            "matrices": matrices,
            "conflicts": conflicts,
            "controls": controls,
            "frictions": frictions,
            "gaps": gaps,
            "overcontrols": overcontrols,
            "loads": loads,
            "bottlenecks": bottlenecks,
            "delegationCandidates": delegation_candidates,
            "escalationPatterns": escalation_patterns,
            "exceptions": exceptions,
            "changeRequests": change_requests,
            "drifts": drifts,
            "reviews": reviews,
            "lessons": lessons,
            "patterns": patterns
        }

    @staticmethod
    async def process_natural_language_governance_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_governance_data()

        # Enforce Privacy Safeguard (blocking individual worker compliance rankings or behavioral surveillance)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["rank employee compliance", "who is violating policy worker", "employee governance score", "surveil worker compliance", "individual employee ranking"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee compliance rankings, worker behavioral surveillance, or individual governance scoring."},
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

        return {
            "query": query_str,
            "results": [
                {
                    "governance_profile": "Enterprise Autonomous Transformation Adaptive Governance Model (gov_prof_01 v2.0)",
                    "decision_rights": "Wave 2 Scale requires Two-key Executive Approval (Authority: Steering Committee)",
                    "surfaced_conflict": "Overlapping capacity authority between Engineering Board and Portfolio Controller",
                    "friction_analysis": "Manual CISO review queue backlog causing 48-hour approval latency on routine pilots",
                    "delegation_candidate": "Recommend delegating sub-$100k regional pilots to Regional Architecture Leads (Safety score: 0.94)",
                    "governance_change_request": "CR-01: Delegate pilot approvals (Simulated latency reduction: 36.0 hours, Under Review)",
                    "exception_status": "1 active 30-day capacity buffer exception expiring in 25 days"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Adaptive Governance 2.0 Engine",
                "controls_evaluated": len(_in_memory_controls)
            },
            "confidencePct": 98.1
        }
