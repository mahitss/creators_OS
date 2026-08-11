import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_cases: Dict[str, dict] = {}
_in_memory_questions: Dict[str, dict] = {}
_in_memory_packs: Dict[str, dict] = {}
_in_memory_items: Dict[str, dict] = {}
_in_memory_conflicts: Dict[str, dict] = {}
_in_memory_assumptions: Dict[str, dict] = {}
_in_memory_options: Dict[str, dict] = {}
_in_memory_tradeoffs: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_packets: Dict[str, dict] = {}
_in_memory_readinesses: Dict[str, dict] = {}
_in_memory_values: Dict[str, dict] = {}
_in_memory_info_actions: Dict[str, dict] = {}
_in_memory_learnings: Dict[str, dict] = {}
_in_memory_reassessments: Dict[str, dict] = {}
_in_memory_drifts: Dict[str, dict] = {}

def _initialize_seed_decisions_data():
    if _in_memory_cases:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Decision Case
    case1 = {
        "id": "case_scale_finops_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "title": "Wave 2 Scale Authorization: Autonomous FinOps Transformation",
        "description": "Should Autonomous FinOps Scale Transformation proceed to full enterprise wave rollout?",
        "decision_type": "scale",
        "status": "ready",
        "priority": "critical",
        "owner": "Executive Transformation Steering Committee",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_cases[case1["id"]] = case1

    # Question
    q1 = {
        "id": "q_01",
        "decision_case_id": case1["id"],
        "question_text": "Should Wave 2 Autonomous FinOps proceed to full enterprise scale following sub-100ms policy validation?"
    }
    _in_memory_questions[q1["id"]] = q1

    # Evidence Pack & Items
    ep1 = {
        "id": "epack_01",
        "decision_case_id": case1["id"],
        "summary_json": {"items_count": 4, "conflicts_count": 1, "overall_freshness": "realtime"},
        "quality_score": 0.94
    }
    _in_memory_packs[ep1["id"]] = ep1

    item1 = {
        "id": "item_01",
        "evidence_pack_id": ep1["id"],
        "type": "fact",
        "source": "Zero-Trust AST Pre-signer Telemetry",
        "value_json": {"verified_latency_ms": 12.4, "build_validation_pass_rate": 0.998},
        "timestamp": now_iso,
        "freshness": "realtime",
        "confidence": 0.99,
        "provenance": "Observed AST Telemetry Pipeline"
    }
    item2 = {
        "id": "item_02",
        "evidence_pack_id": ep1["id"],
        "type": "measurement",
        "source": "Cloud Infrastructure Cost Accounting",
        "value_json": {"actual_q2_cost_reduction_pct": 31.2},
        "timestamp": now_iso,
        "freshness": "realtime",
        "confidence": 0.98,
        "provenance": "Enterprise Ledger FinOps Connector"
    }
    item3 = {
        "id": "item_03",
        "evidence_pack_id": ep1["id"],
        "type": "forecast",
        "source": "Transformation Foresight Model v2026.3.1",
        "value_json": {"projected_annual_opex_savings": "$4.2M", "confidence_range": "30-42%"},
        "timestamp": now_iso,
        "freshness": "daily",
        "confidence": 0.93,
        "provenance": "Foresight Predictive Engine"
    }
    _in_memory_items[item1["id"]] = item1
    _in_memory_items[item2["id"]] = item2
    _in_memory_items[item3["id"]] = item3

    # Evidence Conflict
    conf1 = {
        "id": "conf_01",
        "decision_case_id": case1["id"],
        "source_a": "Engineering Capacity Allocation Board",
        "source_b": "Transformation Portfolio Controller",
        "conflicting_claim": "Engineering Board estimates 6.5 FTE capacity demand vs Controller estimate of 4.0 FTE for Wave 2 scale",
        "status": "surfaced"
    }
    _in_memory_conflicts[conf1["id"]] = conf1

    # Assumption
    ass1 = {
        "id": "ass_01",
        "decision_case_id": case1["id"],
        "assumption_text": "Multi-region Zero-Trust AST pre-signer API schema stability across cloud regions",
        "source": "Cloud Architecture Governance Council",
        "confidence": 0.92,
        "status": "valid",
        "impact": "high"
    }
    _in_memory_assumptions[ass1["id"]] = ass1

    # Options
    opt1 = {
        "id": "opt_scale_full",
        "decision_case_id": case1["id"],
        "description": "Proceed to full enterprise Wave 2 scale rollout across all 4 region clusters",
        "expected_outcome": "Achieves $4.2M annual OpEx reduction within 90 days",
        "risks_json": ["Transient capacity friction during Q3 engineering migration wave"],
        "dependencies_json": ["Skill Certification Auto-signer Transformation (cand_01)"],
        "cost": "$180,000",
        "capacity": "4.5 FTEs",
        "timing": "Immediate Q3 Rollout",
        "reversibility": "partially_reversible"
    }
    opt2 = {
        "id": "opt_pilot_staggered",
        "decision_case_id": case1["id"],
        "description": "Stagger Wave 2 rollout across 2 regions initially before full 4-region scale",
        "expected_outcome": "De-risks capacity friction while delaying $1.1M of Q3 OpEx savings",
        "risks_json": ["Delayed benefits realization by 45 days"],
        "dependencies_json": ["cand_01"],
        "cost": "$95,000",
        "capacity": "2.5 FTEs",
        "timing": "Staggered Q3-Q4 Rollout",
        "reversibility": "reversible"
    }
    _in_memory_options[opt1["id"]] = opt1
    _in_memory_options[opt2["id"]] = opt2

    # Trade-off
    to1 = {
        "id": "to_01",
        "decision_case_id": case1["id"],
        "option_id": opt1["id"],
        "benefit_gained": "Unlocks full $4.2M annual OpEx savings 45 days earlier",
        "cost_incurred": "$180,000 direct implementation expenditure",
        "risk_accepted": "Minor Q3 engineering capacity stretch",
        "optionality_lost": "Immediate reallocation of 4.5 FTEs to secondary workstreams",
        "optionality_gained": "Establishes automated baseline for future zero-trust acquisitions"
    }
    _in_memory_tradeoffs[to1["id"]] = to1

    # Recommendation & Packet
    rec1 = {
        "id": "rec_01",
        "decision_case_id": case1["id"],
        "recommended_option_id": opt1["id"],
        "rationale_summary": "Proceeding to full Wave 2 scale provides highest strategic value ($4.2M OpEx reduction) with low vulnerability (0.15) and sub-100ms policy validation performance",
        "evidence_references_json": ["item_01", "item_02", "item_03"],
        "confidence": "high"
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    packet1 = {
        "id": "dpkt_01",
        "decision_case_id": case1["id"],
        "version_tag": "v1.0",
        "packet_json": {
            "question": q1["question_text"],
            "recommended_option": opt1["description"],
            "evidence_summary": "Sub-100ms AST validation + 31.2% verified Q2 cost reduction",
            "required_approvals": ["Transformation Steering Committee", "Chief Information Officer"]
        },
        "created_at": now_iso
    }
    _in_memory_packets[packet1["id"]] = packet1

    # Readiness & Value
    read1 = {
        "id": "read_01",
        "decision_case_id": case1["id"],
        "status": "ready",
        "readiness_dimensions_json": {
            "evidence": 0.95,
            "clarity": 0.98,
            "options": 0.92,
            "scenario_coverage": 0.94,
            "risk_visibility": 0.90,
            "dependency_visibility": 0.96,
            "approval_readiness": 0.95
        }
    }
    _in_memory_readinesses[read1["id"]] = read1

    val1 = {
        "id": "dval_01",
        "decision_case_id": case1["id"],
        "expected_strategic_value": "High strategic alignment with Zero-Trust & FinOps transformation goals",
        "expected_benefit": "$4.2M Annualized Cloud Infrastructure OpEx Reduction",
        "risk_reduction": "Eliminates manual policy compliance audit overhead",
        "optionality": "Preserves future multi-region automated compliance expansion options"
    }
    _in_memory_values[val1["id"]] = val1

    # Learning & Drift
    learn1 = {
        "id": "dlearn_01",
        "decision_case_id": case1["id"],
        "prediction_json": {"expected_savings_pct": 30.0},
        "actual_outcome_json": {"actual_savings_pct": 31.2},
        "lesson_text": "Pre-signer rule caching exceeded baseline speed projections by 1.2%"
    }
    _in_memory_learnings[learn1["id"]] = learn1

    drift1 = {
        "id": "ddrift_01",
        "decision_case_id": case1["id"],
        "approved_decision_summary": "Full Wave 2 scale across 4 region clusters",
        "implemented_decision_summary": "Full Wave 2 scale implemented cleanly on schedule",
        "drift_severity": "none"
    }
    _in_memory_drifts[drift1["id"]] = drift1

_initialize_seed_decisions_data()


class TransformationDecisionsService:

    @staticmethod
    async def get_decisions_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_decisions_data()
        cases = list(_in_memory_cases.values())
        questions = list(_in_memory_questions.values())
        packs = list(_in_memory_packs.values())
        items = list(_in_memory_items.values())
        conflicts = list(_in_memory_conflicts.values())
        assumptions = list(_in_memory_assumptions.values())
        options = list(_in_memory_options.values())
        tradeoffs = list(_in_memory_tradeoffs.values())
        recommendations = list(_in_memory_recommendations.values())
        packets = list(_in_memory_packets.values())
        readinesses = list(_in_memory_readinesses.values())
        values = list(_in_memory_values.values())
        info_actions = list(_in_memory_info_actions.values())
        learnings = list(_in_memory_learnings.values())
        reassessments = list(_in_memory_reassessments.values())
        drifts = list(_in_memory_drifts.values())

        return {
            "activeDecisionCasesCount": len(cases),
            "readyForReviewCount": len([c for c in cases if c.get("status") == "ready"]),
            "evidenceConflictsCount": len(conflicts),
            "decisionOptionsCount": len(options),
            "decisionPacketsCount": len(packets),
            "decisionCalibrationAccuracyPct": 97.5,
            "cases": cases,
            "questions": questions,
            "packs": packs,
            "items": items,
            "conflicts": conflicts,
            "assumptions": assumptions,
            "options": options,
            "tradeoffs": tradeoffs,
            "recommendations": recommendations,
            "packets": packets,
            "readinesses": readinesses,
            "values": values,
            "infoActions": info_actions,
            "learnings": learnings,
            "reassessments": reassessments,
            "drifts": drifts
        }

    @staticmethod
    async def process_natural_language_decision_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_decisions_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking individual employee decision scoring / employment penalty decisions)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee decision score", "rank worker for layoff", "individual employee decision", "fire worker", "evaluate employee performance score"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee decision scoring, employment termination recommendations, or individual worker surveillance."},
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
                    "decision_case": "Wave 2 Scale Authorization: Autonomous FinOps Transformation (case_scale_finops_01)",
                    "decision_question": "Should Wave 2 Autonomous FinOps proceed to full enterprise scale following sub-100ms policy validation?",
                    "evidence_summary": "Sub-100ms AST validation + 31.2% verified Q2 cost reduction (Freshness: Realtime)",
                    "evidence_conflict": "Capacity conflict: Board 6.5 FTE vs Controller 4.0 FTE (Surfaced for review)",
                    "recommended_option": "Proceed to full enterprise Wave 2 scale rollout across all 4 region clusters (Confidence: High)",
                    "tradeoff_analysis": "Unlocks $4.2M OpEx reduction 45 days earlier vs $180k implementation cost",
                    "reversibility_window": "Partially reversible within 30-day initial wave deployment window",
                    "readiness_status": "Ready for executive leadership authorization"
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Decision Intelligence 3.0 Engine",
                "cases_evaluated": len(_in_memory_cases)
            },
            "confidencePct": 98.0
        }
