import uuid
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import dlp_service

_in_memory_twins: Dict[str, dict] = {}
_in_memory_baselines: Dict[str, dict] = {}
_in_memory_snapshots: Dict[str, dict] = {}
_in_memory_states: Dict[str, dict] = {}
_in_memory_change_sets: Dict[str, dict] = {}
_in_memory_runs: Dict[str, dict] = {}
_in_memory_models: Dict[str, dict] = {}
_in_memory_inputs: Dict[str, dict] = {}
_in_memory_outputs: Dict[str, dict] = {}
_in_memory_multi_scenario_runs: Dict[str, dict] = {}
_in_memory_comparisons: Dict[str, dict] = {}
_in_memory_tradeoffs: Dict[str, dict] = {}
_in_memory_sensitivity_analyses: Dict[str, dict] = {}
_in_memory_reviews: Dict[str, dict] = {}

def _initialize_seed_simulation_data():
    if _in_memory_twins:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    org_id = "org_global_enterprise_01"
    ws_id = "ws_transformation_01"

    # Twin & Baseline
    twin1 = {
        "id": "twin_01",
        "organization_id": org_id,
        "workspace_id": ws_id,
        "name": "Global Enterprise Transformation Digital Twin",
        "description": "Multi-layer virtual representation connecting strategy, operating model, portfolios, dependencies, capacity, and benefits.",
        "scope": "enterprise",
        "version": "v2.0",
        "baseline_snapshot_id": "snap_01",
        "status": "active",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    _in_memory_twins[twin1["id"]] = twin1

    base1 = {
        "id": "base_01",
        "twin_id": twin1["id"],
        "strategy_state_json": {"active_initiatives": 12, "target_growth_pct": 18.5},
        "operating_model_json": {"domain_teams": 6, "decentralized_decision_rights": True},
        "portfolio_json": {"active_waves": 4, "total_budget_millions": 24.5},
        "governance_json": {"active_controls": 8, "friction_level": "moderate"},
        "capacity_json": {"fte_available": 140, "capacity_utilization_pct": 86.5},
        "dependencies_json": {"cross_wave_dependencies": 18},
        "risks_json": {"critical_risks": 2},
        "benefits_json": {"realized_benefits_millions": 4.2},
        "kpis_json": {"on_time_delivery_pct": 92.4}
    }
    _in_memory_baselines[base1["id"]] = base1

    snap1 = {
        "id": "snap_01",
        "twin_id": twin1["id"],
        "timestamp": now_iso,
        "source_versions_json": {"operating_graph": "v2.0", "semantic_graph": "v2.0", "foresight": "v2.0"},
        "included_systems_json": ["Operating Graph 2.0", "Transformation Control Tower", "Benefits Realization 2.0"],
        "data_freshness_minutes": 2.5
    }
    _in_memory_snapshots[snap1["id"]] = snap1

    # States & Change Sets
    st_curr = {
        "id": "st_curr_01",
        "twin_id": twin1["id"],
        "state_type": "current",
        "state_data_json": {"wave_2_status": "in_progress", "completion_pct": 65.0}
    }
    st_prop = {
        "id": "st_prop_01",
        "twin_id": twin1["id"],
        "state_type": "proposed",
        "state_data_json": {"wave_2_delay_months": 3, "capacity_reallocated_fte": 15.0}
    }
    _in_memory_states[st_curr["id"]] = st_curr
    _in_memory_states[st_prop["id"]] = st_prop

    cs1 = {
        "id": "cs_01",
        "twin_id": twin1["id"],
        "changes_json": [
            {"change_type": "pause_wave", "wave_id": "wave_02", "duration_months": 3},
            {"change_type": "reallocate_capacity", "from": "wave_02", "to": "wave_01", "fte_count": 15}
        ],
        "status": "validated"
    }
    _in_memory_change_sets[cs1["id"]] = cs1

    # Simulation Run, Model, Input, Output
    run1 = {
        "id": "sim_run_01",
        "twin_id": twin1["id"],
        "baseline_state_id": st_curr["id"],
        "proposed_state_id": st_prop["id"],
        "scenario": "baseline",
        "model_version": "v2.0",
        "status": "completed",
        "started_at": now_iso,
        "completed_at": now_iso,
        "hash_fingerprint": "sim_fingerprint_hash_8492049182",
        "created_at": now_iso
    }
    _in_memory_runs[run1["id"]] = run1

    mod1 = {
        "id": "model_01",
        "model_type": "combined",
        "version": "v2.0",
        "assumptions_json": {"capacity_elasticity": 0.85, "dependency_propagation_decay": 0.12},
        "parameters_json": {"monte_carlo_iterations": 10000},
        "evaluation_status": "validated",
        "limitations": "Model assumes linear capacity scaling up to +25% FTE reallocation."
    }
    _in_memory_models[mod1["id"]] = mod1

    inp1 = {
        "id": "inp_01",
        "run_id": run1["id"],
        "entity": "Wave 2 Schedule",
        "value": "Delay by 3 months",
        "source": "ChangeSet cs_01",
        "confidence": 0.98,
        "assumption": "Wave 2 team redirected to accelerate Wave 1 critical path"
    }
    _in_memory_inputs[inp1["id"]] = inp1

    out1 = {
        "id": "out_01",
        "run_id": run1["id"],
        "metric": "Wave 1 Completion Timing",
        "low_value": -21.0,
        "expected_value": -14.0,
        "high_value": -7.0,
        "confidence": 0.94,
        "time_horizon": "Q4 2026",
        "scenario": "baseline"
    }
    out2 = {
        "id": "out_02",
        "run_id": run1["id"],
        "metric": "Cost Impact ($)",
        "low_value": 80000.0,
        "expected_value": 150000.0,
        "high_value": 220000.0,
        "confidence": 0.92,
        "time_horizon": "Q4 2026",
        "scenario": "baseline"
    }
    _in_memory_outputs[out1["id"]] = out1
    _in_memory_outputs[out2["id"]] = out2

    # Multi-Scenario, Comparison, Tradeoff, Sensitivity, Review
    msr1 = {
        "id": "msr_01",
        "twin_id": twin1["id"],
        "change_set_id": cs1["id"],
        "scenarios_json": [
            {"name": "baseline", "expected_delivery_days_saved": 14},
            {"name": "optimistic", "expected_delivery_days_saved": 21},
            {"name": "stress", "expected_delivery_days_saved": 5}
        ],
        "robustness_score": 0.92,
        "status": "completed",
        "created_at": now_iso
    }
    _in_memory_multi_scenario_runs[msr1["id"]] = msr1

    comp1 = {
        "id": "comp_01",
        "run_id": run1["id"],
        "current_summary": "Wave 1 at risk of 14-day delay due to FTE capacity bottleneck.",
        "proposed_summary": "Wave 1 accelerated by 14 days by redirecting 15 FTEs from Wave 2.",
        "alternative_summary": "Outsource Wave 1 bottleneck tasks (higher cost, lower control).",
        "comparison_dimensions_json": {
            "strategic_alignment": {"current": 0.85, "proposed": 0.96, "alternative": 0.78},
            "risk": {"current": "high", "proposed": "low", "alternative": "moderate"}
        }
    }
    _in_memory_comparisons[comp1["id"]] = comp1

    to1 = {
        "id": "to_01",
        "run_id": run1["id"],
        "benefit_gained": "Wave 1 finishes 14 days earlier, unlocking $1.2M Q4 benefits",
        "risk_gained": "Wave 2 start delayed by 90 days",
        "cost_impact": 150000.0,
        "delay_days": 14.0,
        "optionality_score": 0.88
    }
    _in_memory_tradeoffs[to1["id"]] = to1

    sens1 = {
        "id": "sens_01",
        "run_id": run1["id"],
        "variable_name": "Reallocated FTE Ramp Velocity",
        "low_value": 0.5,
        "expected_value": 0.85,
        "high_value": 1.0,
        "impact_score": 0.85,
        "created_at": now_iso
    }
    _in_memory_sensitivity_analyses[sens1["id"]] = sens1

    rev1 = {
        "id": "sim_rev_01",
        "run_id": run1["id"],
        "decision_impact": "Informs Steering Committee Decision Case DC-2026-WAVE1-ACCEL",
        "limitations": "Model assumes linear capacity scaling up to +25% FTE reallocation.",
        "status": "approved",
        "created_at": now_iso
    }
    _in_memory_reviews[rev1["id"]] = rev1

_initialize_seed_simulation_data()


class TransformationSimulationService:

    @staticmethod
    async def get_simulation_overview(session: Optional[AsyncSession]) -> dict:
        _initialize_seed_simulation_data()
        twins = list(_in_memory_twins.values())
        baselines = list(_in_memory_baselines.values())
        snapshots = list(_in_memory_snapshots.values())
        states = list(_in_memory_states.values())
        change_sets = list(_in_memory_change_sets.values())
        runs = list(_in_memory_runs.values())
        models = list(_in_memory_models.values())
        inputs = list(_in_memory_inputs.values())
        outputs = list(_in_memory_outputs.values())
        multi_scenario_runs = list(_in_memory_multi_scenario_runs.values())
        comparisons = list(_in_memory_comparisons.values())
        tradeoffs = list(_in_memory_tradeoffs.values())
        sensitivity_analyses = list(_in_memory_sensitivity_analyses.values())
        reviews = list(_in_memory_reviews.values())

        return {
            "activeTwinsCount": len(twins),
            "totalSnapshotsCount": len(snapshots),
            "completedRunsCount": len([r for r in runs if r.get("status") == "completed"]),
            "modelsValidatedCount": len(models),
            "multiScenarioRobustnessScore": 0.92,
            "simulationAccuracyCalibrationPct": 95.8,
            "twins": twins,
            "baselines": baselines,
            "snapshots": snapshots,
            "states": states,
            "changeSets": change_sets,
            "runs": runs,
            "models": models,
            "inputs": inputs,
            "outputs": outputs,
            "multiScenarioRuns": multi_scenario_runs,
            "comparisons": comparisons,
            "tradeoffs": tradeoffs,
            "sensitivityAnalyses": sensitivity_analyses,
            "reviews": reviews
        }

    @staticmethod
    async def process_natural_language_what_if_query(session: Optional[AsyncSession], query_str: str) -> dict:
        _initialize_seed_simulation_data()

        # Enforce Privacy Safeguard (blocking individual employee digital twins or behavioral forecasts)
        lower_q = query_str.lower()
        if any(term in lower_q for term in ["employee digital twin", "individual worker simulation", "simulate employee behavior", "predict worker performance"]):
            return {
                "query": query_str,
                "results": [],
                "evidenceJson": {"error": "Query blocked. Vapor strictly prohibits individual employee digital twins, worker behavioral simulations, or personal performance forecasting."},
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
                    "digital_twin": "Global Enterprise Transformation Digital Twin (twin_01 v2.0)",
                    "simulated_change_set": "Pause Wave 2 for 3 months & reallocate 15 FTEs to Wave 1",
                    "output_ranges": {
                        "wave_1_completion_acceleration_days": {"low": 7, "expected": 14, "high": 21},
                        "cost_impact_dollars": {"low": 80000, "expected": 150000, "high": 220000}
                    },
                    "multi_scenario_robustness": 0.92,
                    "tradeoff_analysis": "Unlocks $1.2M Q4 benefits 14 days earlier at $150k cost impact with 0.88 optionality score",
                    "simulation_fingerprint_hash": "sim_fingerprint_hash_8492049182",
                    "model_limitations": "Model assumes linear capacity scaling up to +25% FTE reallocation."
                }
            ],
            "evidenceJson": {
                "data_source": "Enterprise Transformation Governance Digital Twin 2.0 Engine",
                "snapshot_freshness_minutes": 2.5
            },
            "confidencePct": 94.0
        }
