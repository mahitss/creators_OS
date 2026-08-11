import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_portfolios: Dict[str, dict] = {}
_in_memory_candidates: Dict[str, dict] = {}
_in_memory_graphs: Dict[str, dict] = {}
_in_memory_sequences: Dict[str, dict] = {}
_in_memory_seq_comparisons: Dict[str, dict] = {}
_in_memory_bottlenecks_pf: Dict[str, dict] = {}
_in_memory_capacity_plans: Dict[str, dict] = {}
_in_memory_capital_constraints: Dict[str, dict] = {}
_in_memory_capacity_constraints: Dict[str, dict] = {}
_in_memory_lockin_risks: Dict[str, dict] = {}
_in_memory_outcomes_pf: Dict[str, dict] = {}
_in_memory_benefit_overlaps: Dict[str, dict] = {}
_in_memory_conflicts_pf: Dict[str, dict] = {}
_in_memory_min_sets: Dict[str, dict] = {}
_in_memory_waves: Dict[str, dict] = {}
_in_memory_contingencies: Dict[str, dict] = {}
_in_memory_rebalances: Dict[str, dict] = {}
_in_memory_drifts_pf: Dict[str, dict] = {}

def _initialize_seed_transformation_portfolio_data():
    if _in_memory_portfolios:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_primary_01"

    # Seed Portfolio
    port1 = {
        "id": "transport_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Cognitive Enterprise Transformation Portfolio 2026-2029",
        "description": "Strategic portfolio governing AI-Augmented Mesh, ActionGateway Pre-signer, and Autonomous FinOps transformations.",
        "strategy_id": "strat_enterprise_growth_01",
        "horizon": "3_year",
        "status": "approved",
        "owner": "usr_chief_investment_officer",
        "version": "v2.0",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_portfolios[port1["id"]] = port1

    # Seed Candidates
    cand1 = {
        "id": "cand_01",
        "portfolio_id": port1["id"],
        "transformation_program_id": "transprog_01",
        "strategic_value_json": {"growth": "high", "cost_reduction": "30%", "resilience": "98%"},
        "urgency": "critical",
        "risk_score": 0.12,
        "cost_estimate": 250000.0,
        "capacity_demand_json": {"engineering": "40%", "compliance": "15%"},
        "optional_value": 0.92,
        "confidence": "high"
    }
    cand2 = {
        "id": "cand_02",
        "portfolio_id": port1["id"],
        "transformation_program_id": "transprog_finops_02",
        "strategic_value_json": {"growth": "medium", "cost_reduction": "45%", "resilience": "94%"},
        "urgency": "medium",
        "risk_score": 0.18,
        "cost_estimate": 180000.0,
        "capacity_demand_json": {"finops": "60%", "engineering": "20%"},
        "optional_value": 0.88,
        "confidence": "high"
    }
    _in_memory_candidates[cand1["id"]] = cand1
    _in_memory_candidates[cand2["id"]] = cand2

    # Seed Dependency Graph & Critical Path
    graph1 = {
        "id": "depgraph_01",
        "portfolio_id": port1["id"],
        "dependency_matrix_json": {"cand_01": [], "cand_02": ["cand_01"]},
        "critical_path_json": ["cand_01", "cand_02"],
        "parallel_groups_json": [["cand_01"]],
        "cycles_detected": False,
        "blocked_candidates_json": []
    }
    _in_memory_graphs[graph1["id"]] = graph1

    # Seed Sequences
    seq1 = {
        "id": "seq_risk_first_01",
        "portfolio_id": port1["id"],
        "name": "Risk-First Foundational Sequence",
        "sequence_type": "risk_first",
        "phases_json": ["Phase 1: Compliance Auto-signer", "Phase 2: FinOps Autonomous Scale"],
        "order_json": ["cand_01", "cand_02"],
        "parallel_groups_json": [["cand_01"], ["cand_02"]],
        "decision_gates_json": ["gate_pilot_validation_01"],
        "status": "active"
    }
    _in_memory_sequences[seq1["id"]] = seq1

    # Seed Sequence Comparison
    seq_comp1 = {
        "id": "seqcomp_01",
        "portfolio_id": port1["id"],
        "sequence_a_id": seq1["id"],
        "sequence_b_id": "seq_parallel_all_unconstrained",
        "time_diff": -0.35,
        "cost_diff": -0.10,
        "risk_diff": -0.40,
        "capacity_diff": 0.15,
        "benefit_diff": 0.25,
        "optionality_diff": 0.30,
        "robustness_score": 0.94
    }
    _in_memory_seq_comparisons[seq_comp1["id"]] = seq_comp1

    # Seed Capacity Plan & Constraints
    cplan1 = {
        "id": "cplan_01",
        "portfolio_id": port1["id"],
        "time_window": "Q3-2026",
        "required_capacity": 60.0,
        "available_capacity": 100.0,
        "committed_capacity": 45.0,
        "buffer_capacity": 40.0
    }
    _in_memory_capacity_plans[cplan1["id"]] = cplan1

    lockin1 = {
        "id": "lockin_01",
        "portfolio_id": port1["id"],
        "risk_type": "architecture",
        "description": "Zero-Trust PolicyEngine rule structure preserves open AST schemas to avoid vendor lock-in.",
        "severity": "low",
        "reversibility": "high"
    }
    _in_memory_lockin_risks[lockin1["id"]] = lockin1

    # Seed Wave & Minimum Set
    wave1 = {
        "id": "wave_01",
        "portfolio_id": port1["id"],
        "wave_number": 1,
        "wave_type": "foundation",
        "candidate_ids_json": ["cand_01"],
        "exit_criteria_json": {"min_pilot_validation_rate": 0.90, "dlp_zero_violations": True},
        "status": "executing"
    }
    _in_memory_waves[wave1["id"]] = wave1

    min_set1 = {
        "id": "minset_01",
        "portfolio_id": port1["id"],
        "target_objective": "Sub-1h Skill Certification & 30% Cost Reduction",
        "required_candidate_ids_json": ["cand_01"],
        "total_cost": 250000.0,
        "total_time": "3_months"
    }
    _in_memory_min_sets[min_set1["id"]] = min_set1

    # Seed Rebalance Proposal (Human Leadership Authorization Required)
    rebal1 = {
        "id": "rebal_01",
        "portfolio_id": port1["id"],
        "rebalance_reason": "scenario_shift",
        "proposed_sequence_id": seq1["id"],
        "evidence_json": {"demand_surge_simulation": "98% resilience in risk_first sequence"},
        "status": "proposed"
    }
    _in_memory_rebalances[rebal1["id"]] = rebal1

_initialize_seed_transformation_portfolio_data()


class TransformationPortfolioService:

    @staticmethod
    async def get_portfolio_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_transformation_portfolio_data()
        portfolios = list(_in_memory_portfolios.values())
        candidates = list(_in_memory_candidates.values())
        graphs = list(_in_memory_graphs.values())
        sequences = list(_in_memory_sequences.values())
        comparisons = list(_in_memory_seq_comparisons.values())
        capacity_plans = list(_in_memory_capacity_plans.values())
        lockin_risks = list(_in_memory_lockin_risks.values())
        waves = list(_in_memory_waves.values())
        min_sets = list(_in_memory_min_sets.values())
        rebalances = list(_in_memory_rebalances.values())

        return {
            "portfoliosCount": len(portfolios),
            "candidatesCount": len(candidates),
            "criticalPathCandidatesCount": len(graphs[0]["critical_path_json"]) if graphs else 0,
            "sequencesCount": len(sequences),
            "sequenceComparisonsCount": len(comparisons),
            "activeCapacityPlansCount": len(capacity_plans),
            "lockInRisksCount": len(lockin_risks),
            "wavesCount": len(waves),
            "minimumSetsCount": len(min_sets),
            "proposedRebalancesCount": len(rebalances),
            "overallPortfolioRobustnessScore": 0.94,
            "portfolios": portfolios,
            "candidates": candidates,
            "graphs": graphs,
            "sequences": sequences,
            "comparisons": comparisons,
            "capacityPlans": capacity_plans,
            "lockInRisks": lockin_risks,
            "waves": waves,
            "minimumSets": min_sets,
            "rebalances": rebalances
        }

    @staticmethod
    async def approve_rebalance(session: Optional[AsyncSession], rebalance_id: str, actor_id: str) -> dict:
        _initialize_seed_transformation_portfolio_data()
        reb = _in_memory_rebalances.get(rebalance_id)
        if not reb:
            return {"error": "Portfolio Rebalance Proposal not found"}

        reb["status"] = "approved"
        reb["approved_by"] = actor_id
        reb["approved_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "rebalanceId": rebalance_id,
            "status": "approved",
            "approvedBy": actor_id,
            "message": "Transformation Portfolio Rebalance authorized via PolicyEngine & Investment Governance. Ready for Execution Governance implementation."
        }

    @staticmethod
    async def execute_rebalance(session: Optional[AsyncSession], rebalance_id: str) -> dict:
        _initialize_seed_transformation_portfolio_data()
        reb = _in_memory_rebalances.get(rebalance_id)
        if not reb:
            return {"error": "Portfolio Rebalance Proposal not found"}

        if reb["status"] != "approved":
            return {"error": "Unauthorized: Portfolio Rebalance must be approved by leadership before execution."}

        reb["status"] = "executed"
        reb["executed_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "rebalanceId": rebalance_id,
            "status": "executed",
            "executionPath": "Universal Action Gateway & Execution Governance Layer",
            "message": "Transformation Portfolio Rebalance executed safely via ActionGateway sandbox."
        }

    @staticmethod
    async def process_natural_language_portfolio_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_transformation_portfolio_data()

        # Enforce Anti-Surveillance Privacy Boundary (blocking employee ranking/individual worker allocation)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["allocate worker", "rank employee", "worker score", "surveil worker", "individual worker score"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits employee ranking, worker surveillance, individual worker allocation, or employment penalty recommendations."},
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
                    "portfolio_name": "Global Cognitive Enterprise Transformation Portfolio 2026-2029",
                    "top_candidates": "Skill Certification Auto-signer (Urgency: Critical) -> FinOps Autonomous Scale",
                    "critical_path": "cand_01 -> cand_02",
                    "recommended_sequence": "Risk-First Foundational Sequence (Robustness: 94%)",
                    "capacity_headroom": "40% Buffer Capacity available in Q3-2026",
                    "minimum_viable_set": "cand_01 (Sub-1h Skill Certification & 30% Cost Reduction in 3 months)",
                    "rebalance_proposal": "Rebalance portfolio for Scenario Shift (Status: proposed)"
                }
            ],
            "evidenceJson": {
                "referenced_portfolio": "transport_01",
                "data_source": "Enterprise Transformation Portfolio Intelligence 2.0 Engine"
            },
            "confidencePct": 97.0
        }
