import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service, predictive_operations_service

_in_memory_problems: Dict[str, dict] = {}
_in_memory_objectives: Dict[str, dict] = {}
_in_memory_variables: Dict[str, dict] = {}
_in_memory_constraints: Dict[str, dict] = {}
_in_memory_options: Dict[str, dict] = {}
_in_memory_tradeoffs: Dict[str, dict] = {}
_in_memory_robustness: Dict[str, dict] = {}
_in_memory_sensitivity: Dict[str, dict] = {}
_in_memory_recommendations: Dict[str, dict] = {}
_in_memory_action_plans: Dict[str, dict] = {}
_in_memory_performances: Dict[str, dict] = {}
_in_memory_alerts: Dict[str, dict] = {}

def _initialize_seed_prescriptive_data():
    if _in_memory_problems:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_default_creator"

    # Seed Optimization Problem
    p1 = {
        "id": "prob_opt_01",
        "organization_id": org_id,
        "workspace_id": "ws_default",
        "name": "Q3 Enterprise AI Compute & Agent Allocation Optimization",
        "description": "Optimize agent node placement and GPU compute allocation to maximize throughput while respecting strict budget and SLA constraints.",
        "objective_type": "maximize_capacity_efficiency",
        "status": "ready_for_review",
        "owner": "usr_head_of_arch",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_problems[p1["id"]] = p1

    # Seed Objective
    obj1 = {
        "id": "obj_01",
        "problem_id": p1["id"],
        "metric": "Agent Throughput (Missions/hr)",
        "direction": "maximize",
        "weight": 1.0,
        "priority": 1,
        "source": "KPI Operating System 2.0"
    }
    _in_memory_objectives[obj1["id"]] = obj1

    # Seed Decision Variable
    v1 = {
        "id": "var_01",
        "problem_id": p1["id"],
        "name": "Agent Replica Pool Size",
        "variable_type": "integer",
        "minimum": 10.0,
        "maximum": 100.0,
        "allowed_values_json": []
    }
    _in_memory_variables[v1["id"]] = v1

    # Seed Hard & Soft Constraints
    c1 = {
        "id": "cnst_01",
        "problem_id": p1["id"],
        "constraint_type": "budget",
        "is_hard": True, # Hard constraint
        "expression": "monthly_compute_cost <= $50,000",
        "source": "FinOps V2 Budget Cap",
        "owner": "usr_finops_lead",
        "freshness": "fresh"
    }
    _in_memory_constraints[c1["id"]] = c1

    # Seed Feasible Options & Pareto Frontier
    op1 = {
        "id": "opt_01",
        "problem_id": p1["id"],
        "variables_json": {"replica_pool_size": 48, "gpu_tier": "A100_SXM"},
        "constraints_satisfied": True,
        "expected_outcome": 940.0,
        "expected_cost": 42500.0,
        "expected_risk": "low",
        "confidence": 93.0
    }
    op2 = {
        "id": "opt_02",
        "problem_id": p1["id"],
        "variables_json": {"replica_pool_size": 64, "gpu_tier": "H100_SXM"},
        "constraints_satisfied": True,
        "expected_outcome": 1150.0,
        "expected_cost": 49000.0, # Close to hard budget cap
        "expected_risk": "medium",
        "confidence": 89.0
    }
    _in_memory_options[op1["id"]] = op1
    _in_memory_options[op2["id"]] = op2

    # Seed Tradeoff (Pareto Frontier)
    to1 = {
        "id": "trd_01",
        "problem_id": p1["id"],
        "option_a_id": op1["id"],
        "option_b_id": op2["id"],
        "comparison_json": {
            "throughput_delta": "+210 missions/hr (Option 2)",
            "cost_delta": "+$6,500/mo (Option 2)",
            "reversibility": "Fully reversible within 5 minutes"
        },
        "pareto_frontier_flag": True
    }
    _in_memory_tradeoffs[to1["id"]] = to1

    # Seed Robustness Analysis
    rob1 = {
        "id": "rob_01",
        "option_id": op1["id"],
        "demand_change": "+20% demand increase maintains SLA (<300ms)",
        "cost_change": "+10% pricing surge absorbed within budget",
        "capacity_change": "-15% node outage maintains 92% throughput",
        "dependency_failure_impact": "Graceful fallback to secondary cluster",
        "robustness_score": 0.94
    }
    _in_memory_robustness[rob1["id"]] = rob1

    # Seed Sensitivity Analysis
    sen1 = {
        "id": "sen_01",
        "option_id": op1["id"],
        "variable_name": "replica_pool_size",
        "impact_direction": "positive",
        "estimated_magnitude": 12.5, # +12.5 missions/hr per replica
        "confidence": 91.0
    }
    _in_memory_sensitivity[sen1["id"]] = sen1

    # Seed Prescriptive Recommendation (Advisory)
    rec1 = {
        "id": "rec_presc_01",
        "problem_id": p1["id"],
        "recommended_option_id": op1["id"],
        "alternatives_json": [op2["id"]],
        "objective_summary": "Maximize agent throughput while keeping compute cost under $50k/mo.",
        "constraints_summary": "Hard budget cap $50k satisfied; Hard security DLP policy satisfied.",
        "evidence": "Option 1 achieves 940 missions/hr at $42.5k/mo with highest robustness score (0.94).",
        "expected_impact": "+28% throughput increase with $7.5k budget buffer.",
        "risk_level": "low",
        "confidence_pct": 93.0,
        "robustness_score": 0.94,
        "status": "ready_for_review"
    }
    _in_memory_recommendations[rec1["id"]] = rec1

    # Seed Action Plan & Rollback Plan
    ap1 = {
        "id": "act_plan_01",
        "recommendation_id": rec1["id"],
        "actions_json": [
            {"step": 1, "action": "Provision 48 Agent Replicas", "system": "Universal Action Gateway"},
            {"step": 2, "action": "Update Model Gateway Routing Weights", "system": "Model Gateway"}
        ],
        "owner": "usr_head_of_arch",
        "dependencies_json": ["dep_network_mesh_v2"],
        "milestones_json": ["milestone_replica_scaling"],
        "rollback_plan": "Restore Previous Replica Weights (v1.8) via Universal Action Gateway within 60s.",
        "execution_mode": "approval_gated"
    }
    _in_memory_action_plans[ap1["id"]] = ap1

    # Seed Optimization Performance
    perf1 = {
        "id": "opt_perf_01",
        "recommendation_id": rec1["id"],
        "expected_outcome": 940.0,
        "actual_outcome": 952.0,
        "expected_cost": 42500.0,
        "actual_cost": 41800.0,
        "benefit_accuracy": 98.7,
        "cost_accuracy": 98.4,
        "forecast_error": 1.4
    }
    _in_memory_performances[perf1["id"]] = perf1

_initialize_seed_prescriptive_data()


class PrescriptiveIntelligenceService:

    @staticmethod
    async def get_optimization_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_prescriptive_data()
        problems = list(_in_memory_problems.values())
        options = list(_in_memory_options.values())
        recommendations = list(_in_memory_recommendations.values())
        action_plans = list(_in_memory_action_plans.values())
        tradeoffs = list(_in_memory_tradeoffs.values())
        robustness = list(_in_memory_robustness.values())
        sensitivity = list(_in_memory_sensitivity.values())
        performances = list(_in_memory_performances.values())

        pareto_options = sum(1 for t in tradeoffs if t.get("pareto_frontier_flag"))

        return {
            "problemsCount": len(problems),
            "optionsCount": len(options),
            "recommendationsCount": len(recommendations),
            "actionPlansCount": len(action_plans),
            "paretoOptionsCount": pareto_options,
            "problems": problems,
            "options": options,
            "recommendations": recommendations,
            "actionPlans": action_plans,
            "tradeoffs": tradeoffs,
            "robustness": robustness,
            "sensitivity": sensitivity,
            "performances": performances,
            "optimizationHealthScore": 0.96
        }

    @staticmethod
    async def create_problem(session: Optional[AsyncSession], prob_data: dict, org_id: str = "org_default_creator") -> dict:
        _initialize_seed_prescriptive_data()
        p_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        prob = {
            "id": p_id,
            "organization_id": org_id,
            "workspace_id": prob_data.get("workspaceId", "ws_default"),
            "name": prob_data["name"],
            "description": prob_data["description"],
            "objective_type": prob_data.get("objectiveType", "maximize_outcome"),
            "status": "configured",
            "owner": prob_data["owner"],
            "created_at": now_iso,
            "updated_at": now_iso
        }
        _in_memory_problems[p_id] = prob
        return prob

    @staticmethod
    async def execute_action_plan(session: Optional[AsyncSession], plan_id: str, actor_id: str = "usr_head_of_arch") -> dict:
        _initialize_seed_prescriptive_data()
        plan = _in_memory_action_plans.get(plan_id)
        if not plan:
            return {"error": "Action plan not found"}

        # Action Gateway & Policy Engine check simulation
        return {
            "actionPlanId": plan_id,
            "status": "executing",
            "authorizedBy": actor_id,
            "actionGatewayReference": f"gw_act_{uuid.uuid4().hex[:8]}",
            "rollbackPlan": plan["rollback_plan"]
        }

    @staticmethod
    async def process_natural_language_prescriptive_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_prescriptive_data()

        # Enforce DLP checks on natural language query
        findings = dlp_service.detect_sensitive_patterns(query_str)
        if any(f["classification"] == "secret" for f in findings):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked due to DLP secret boundary restriction."},
                "confidencePct": 0.0
            }

        # Privacy Anti-Surveillance Safeguard (No employee termination/salary optimization)
        lower_q = query_str.lower()
        if any(p in lower_q for p in ["fire", "terminate", "employee", "worker", "salary", "compensation", "attribute"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Denied. Employee surveillance, employment decisions or individual worker optimization is strictly prohibited by policy."},
                "confidencePct": 0.0
            }

        return {
            "query": query_str,
            "results": [
                {
                    "recommendation": "Option 1 (Replica Pool: 48, GPU Tier: A100_SXM)",
                    "expected_throughput": "940 missions/hr",
                    "expected_cost": "$42,500/mo (within $50k cap)",
                    "robustness_score": 0.94,
                    "reversibility": "Fully reversible within 60s"
                }
            ],
            "evidenceJson": {
                "referenced_problem": "prob_opt_01",
                "referenced_recommendation": "rec_presc_01",
                "data_source": "Prescriptive Intelligence 2.0 Engine"
            },
            "confidencePct": 93.0
        }
